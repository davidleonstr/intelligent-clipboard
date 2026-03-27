import os
import sys

# Set GUI Framwork
os.environ['QT_API'] = 'pyqt6'

import QFlow
from QFlow.modules import style
from config import CONFIG
from helpers import JSONFile
from app import RELATIVES

# Get APP Config
APPCONFIG = JSONFile(CONFIG.folders['configs']['windows']['main']).read()

import sys
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QIcon
import os

# Import screens
from screens import SetupScreen, HomeScreen, ErrorScreen, HelpScreen, LoadingScreen

# Import default template
from templates import DefaultTemplate

import base64

from helpers import hasInternet

# Web bridge
from helpers import Bridge

@QFlow.app(
    title=APPCONFIG.get('title'), 
    geometry=APPCONFIG.get('geometry'), 
    icon=lambda:QIcon(APPCONFIG.get('icon-path')),
    customTemplate=DefaultTemplate,
    frameless=True
)
@style(style=CONFIG.folders.get('styles')[APPCONFIG['style']], path=True)
class App(QFlow.App):
    def __init__(self):
        # Create SetupScreen
        self.setupScreen = SetupScreen(parent=self)
        self.homeScreen = HomeScreen(parent=self)
        self.errorScreen = ErrorScreen(parent=self)
        self.helpScreen = HelpScreen(parent=self)
        self.loadingScreen = LoadingScreen(parent=self)
        
        # Add screens
        self.addScreen(self.setupScreen)
        self.addScreen(self.homeScreen)
        self.addScreen(self.errorScreen)
        self.addScreen(self.helpScreen)
        self.addScreen(self.loadingScreen)

        # If not have internet
        if not hasInternet():
            # Error screen
            self.setScreen(self.errorScreen.name)

            # Stop here
            return 

        # Initial screen
        initialScreen = self.setupScreen.name

        # Default key
        self.key = RELATIVES.RelativesFile.get('ic-key', False)

        # Default args
        args = {}

        # If key exists
        if self.key:
            args = {
                # Decrypt key
                'key': RELATIVES.CIPHER.decrypt(
                    base64.b64decode(
                        self.key
                    )
                )
            }

            # Initial screen
            initialScreen = self.homeScreen.name

        # Set load channel
        self.bridge = Bridge()
        self.bridge.add(
            'finished', # Function name in JS to use in execute
            lambda: self.setScreen(initialScreen, args=args) # lambda to set next screen
        )

        # Set loading screen
        self.setScreen(self.loadingScreen.name, args={
            'bridge': self.bridge # Add the bridge
        })
    
    # Update key
    def updateKey(self, key: str):
        # Set null in JSON if not key
        if not key:
            # Encrypt key
            RELATIVES.RelativesFile.update('ic-key', None) 

            return # Return function
            
        # Encrypt key
        RELATIVES.RelativesFile.update(
            'ic-key', 
            base64.b64encode(
                RELATIVES.CIPHER.encrypt(key)
            ).decode('utf-8')
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.run(QApp=app)
