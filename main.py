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
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import os

# Import HomeScreen
from screens import SetupScreen, HomeScreen

# Import default template
from templates import DefaultTemplate

import base64

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
        
        # Add screens
        self.addScreen(self.setupScreen)
        self.addScreen(self.homeScreen)

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

        # Set screen
        self.setScreen(initialScreen, args=args)
    
    # Update key
    def updateKey(self, key: str):
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
