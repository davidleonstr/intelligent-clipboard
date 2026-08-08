from functools import partial
import i18n

import QFlow
from QFlow.components import Notify
from QFlow.builders import Icon, JSON, Object
from QFlow.extensions import QWebEngineViewBridge
from QFlow.injectors import style, config

from app.tree import FOLDERS
from app.settings import SETTINGS
from app.screens import (
    SetupScreen, 
    HomeScreen, 
    ErrorScreen, 
    HelpScreen, 
    LoadingScreen, 
    SettingsScreen,
    HotkeysScreen
)
from app.helpers.checkers import hasInternet
from app.templates import DefaultTemplate

from qtpy.QtGui import QIcon

CONFIG = Object(
    JSON(FOLDERS.f['app', 'configs', 'windows', 'app.json']).read()
).obj

ICON = partial(QIcon, FOLDERS.f['app', 'resources', 'icons', CONFIG.icon])

@QFlow.app(
    title=i18n.t('windows.app.title'), 
    geometry=CONFIG.geometry, 
    icon=ICON,
    frameless=True,
    template=DefaultTemplate,
)
@style(
    style=FOLDERS.f['app', 'styles', 'windows', CONFIG.style.sheet], 
    path=True
)
@config(CONFIG)
class App(QFlow.App):
    def __init__(self):
        self.setupScreen = SetupScreen(parent=self)
        self.homeScreen = HomeScreen(parent=self)
        self.errorScreen = ErrorScreen(parent=self)
        self.helpScreen = HelpScreen(parent=self)
        self.loadingScreen = LoadingScreen(parent=self)
        self.settingsScreen = SettingsScreen(parent=self)
        self.hotkeysScreen = HotkeysScreen(parent=self)
        
        self.addScreen(self.setupScreen)
        self.addScreen(self.homeScreen)
        self.addScreen(self.errorScreen)
        self.addScreen(self.helpScreen)
        self.addScreen(self.loadingScreen)
        self.addScreen(self.settingsScreen)
        self.addScreen(self.hotkeysScreen)

        self.backgroundColor = self.Config.style.backgroundColor

        if not hasInternet():
            self.setScreen(self.errorScreen.name)
            return 

        self.bridge = QWebEngineViewBridge()
        self.bridge.add(
            'finish',
            self.finish
        )

        self.initialScreen = self.setupScreen.name

        self.screenArgs = {}

        self.key = SETTINGS.ICKEY

        if self.key:
            self.screenArgs = {
                'key': SETTINGS.decryptKey(self.key)
            }

            self.initialScreen = self.homeScreen.name

        self.setScreen(self.loadingScreen.name, args={
            'bridge': self.bridge
        })
    
    def finish(self) -> None:
        self.setScreen(self.initialScreen, args=self.screenArgs)

    def showNotify(self, message: str, type: str) -> Notify:
        customTypes = {
            'success': Icon(
                FOLDERS.f['app', 'resources', 'icons', 'notifications', 'success-icon.svg'], 
                25, 25
            ),
            'info': Icon(
                FOLDERS.f['app', 'resources', 'icons', 'notifications', 'info-icon.svg'], 
                25, 25
            ),
            'error': Icon(
                FOLDERS.f['app', 'resources', 'icons', 'notifications', 'error-icon.svg'], 
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
