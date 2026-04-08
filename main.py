import os

os.environ['QT_API'] = 'pyqt6'

import sys
import base64

import QFlow
from QFlow.components import Notify
from QFlow.helpers import Icon
from QFlow.extensions import QWebEngineViewBridge
from QFlow.modules import style, session

from config import CONFIG
from app import RELATIVES

from helpers.files import JSON
from helpers.checkers import hasInternet

from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QIcon

from screens import SetupScreen, HomeScreen, ErrorScreen, HelpScreen, LoadingScreen
from templates import DefaultTemplate

APPCONFIG = JSON(CONFIG.folders['configs']['files']['windows']['main']).read()

WINDOWCONFIG = JSON(
    CONFIG.folders['locales']['languages'][RELATIVES.LANGUAGE]['windows']['main']
).read()

@QFlow.app(
    title=WINDOWCONFIG['texts']['title'], 
    geometry=APPCONFIG['geometry'], 
    icon=lambda:QIcon(APPCONFIG['icon-path']),
    customTemplate=DefaultTemplate,
    frameless=True
)
@style(
    style=CONFIG.folders['styles']['files']['normals'][APPCONFIG['style']], 
    path=True
)
@session()
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
        args = {}

        self.key = RELATIVES.RelativesFile.get(
            'ic-key', 
            False
        )

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

        self.Session.setItem('updateKey', self.updateKey)
        self.Session.setItem('showNotify', self.showNotify)
    
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

    def showNotify(self, message: str, type: str):
        customTypes = {
            'success': Icon(CONFIG.folders['icons']['files']\
                ['notifications']['success-icon'], 25, 25),
            'info': Icon(CONFIG.folders['icons']['files']\
                ['notifications']['info-icon'], 25, 25),
            'error': Icon(CONFIG.folders['icons']['files']\
                ['notifications']['error-icon'], 25, 25)
        }

        notify = Notify(
            message,
            type=type,
            parent=self,
            toggleProgressBar=False,
            autoShow=False,
            customIcon=customTypes.get(type, None)
        )
        notify.containerLayout.setContentsMargins(20, 15, 20, 15)
        notify.show()
        return notify

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.run(QApp=app)