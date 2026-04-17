import os

os.environ['QT_API'] = 'pyqt6'

import sys

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

from helpers.builders import Object

APPCONFIG = Object(
    JSON(
        CONFIG.tree(
            'configs',
            'files',
            'windows',
            'main'
        )
    ).read()
).obj

WINDOWCONFIG = Object(
    JSON(
        CONFIG.tree(
            'locales', 
            'languages', 
            RELATIVES.LANGUAGE,
            'windows',
            'main'
        )
    ).read()
).obj

@QFlow.app(
    title=WINDOWCONFIG.texts.title, 
    geometry=APPCONFIG.geometry, 
    icon=lambda:QIcon(APPCONFIG.icon),
    customTemplate=DefaultTemplate,
    frameless=True
)
@style(
    style=CONFIG.tree(
        'styles',
        'files',
        'normals',
        APPCONFIG.style
    ), 
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

        self.key = RELATIVES.ICKEY

        if self.key:
            args = {
                'key': RELATIVES.decryptKey(self.key)
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

        self.Session.setItem('showNotify', self.showNotify)

    def showNotify(self, message: str, type: str):
        customTypes = {
            'success': Icon(
                CONFIG.tree('icons', 'files', 'notifications', 'success-icon'), 
                25, 25
            ),
            'info': Icon(
                CONFIG.tree('icons', 'files', 'notifications', 'info-icon'), 
                25, 25
            ),
            'error': Icon(
                CONFIG.tree('icons', 'files', 'notifications', 'error-icon'), 
                25, 25
            )
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