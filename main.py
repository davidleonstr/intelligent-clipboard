import os

os.environ['QT_API'] = 'pyqt6'

import sys
import base64

import QFlow
from QFlow.extensions import QWebEngineViewBridge
from QFlow.modules import style

from config import CONFIG
from app import RELATIVES

from helpers.files import JSON
from helpers.checkers import hasInternet

from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QIcon

from screens import SetupScreen, HomeScreen, ErrorScreen, HelpScreen, LoadingScreen
from templates import DefaultTemplate

APPCONFIG = JSON(CONFIG.folders['configs']['windows']['main']).read()

@QFlow.app(
    title=APPCONFIG.get('title'), 
    geometry=APPCONFIG.get('geometry'), 
    icon=lambda: QIcon(APPCONFIG.get('icon-path')),
    customTemplate=DefaultTemplate,
    frameless=True
)
@style(
    style=CONFIG.folders.get('styles')[APPCONFIG['style']], 
    path=True
)
class App(QFlow.App):
    def __init__(self):
        self.setupScreen = SetupScreen(parent=self)
        self.homeScreen = HomeScreen(parent=self)
        self.errorScreen = ErrorScreen(parent=self)
        self.helpScreen = HelpScreen(parent=self)
        self.loadingScreen = LoadingScreen(parent=self)
        
        self.addScreen(self.setupScreen)
        self.addScreen(self.homeScreen)
        self.addScreen(self.errorScreen)
        self.addScreen(self.helpScreen)
        self.addScreen(self.loadingScreen)

        if not hasInternet():
            self.setScreen(self.errorScreen.name)
            return 

        initialScreen = self.setupScreen.name

        self.key = RELATIVES.RelativesFile.get('ic-key', False)

        args = {}

        if self.key:
            args = {
                'key': self.decryptKey(self.key)
            }

            initialScreen = self.homeScreen.name

        self.bridge = QWebEngineViewBridge()
        self.bridge.add(
            'finished',
            lambda: self.setScreen(initialScreen, args=args)
        )

        self.setScreen(self.loadingScreen.name, args={
            'bridge': self.bridge
        })
    
    def updateKey(self, key: str):
        if not key:
            RELATIVES.RelativesFile.update('ic-key', None) 
            return
            
        RELATIVES.RelativesFile.update(
            'ic-key', 
            self.encryptKey(key)
        )
    
    def encryptKey(self, key: str) -> str:
        return base64.b64encode(
            RELATIVES.CIPHER.encrypt(key)
        ).decode('utf-8')

    def decryptKey(self, key: str) -> str:
        return RELATIVES.CIPHER.decrypt(
        base64.b64decode(
            key
            )
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.run(QApp=app)