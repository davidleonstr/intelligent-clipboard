import keyboard
import threading
import asyncio
from functools import partial
import i18n

import QFlow
from QFlow.components import ToggleSwitch
from QFlow.builders import Icon
from QFlow.typing import privatemethod
from QFlow.hooks import Navigator

from app.tree import FOLDERS
from app.controllers import AIController
from app.services import Combinations
from app.settings import SETTINGS

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QApplication
)
from qtpy.QtCore import QTimer

@QFlow.screen(
    name='home',
    parentType=QFlow.App
)
class HomeScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.isRunning = False

        self.navigator = Navigator(self)

    def effect(self):
        self.params = QFlow.hooks.Params(self).get()

        if self.params.get('key'):
            self.key = self.params.pop('key')

            if hasattr(self, 'screenLayout'):
                self.loadScreenData()
                return
                
            QTimer.singleShot(0, self.loadScreenData)

    def UI(self):        
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)

        self.nav = QHBoxLayout()

        self.logo = QLabel()
        self.logoPixmap = Icon(FOLDERS.f['app', 'resources', 'icons', 'app-icon.svg'], 42, 42)
        self.logo.setPixmap(self.logoPixmap)

        self.titleLabel = QLabel(i18n.t('screens.home.labels.title'))
        self.titleLabel.setObjectName('title')

        self.selectModelLabel = QLabel(i18n.t('screens.home.labels.selectModel'))
        self.toggleServiceLabel = QLabel(i18n.t('screens.home.labels.enableService'))

        self.content = QVBoxLayout()
        self.content.setSpacing(20)
        self.content.setContentsMargins(0, 20, 0, 20)

        self.bottom = QHBoxLayout()
        self.bottom.setSpacing(20)

        self.helpButton = QPushButton(i18n.t('screens.home.buttons.help'))
        self.helpButton.setObjectName('normalButton')
        self.helpButton.clicked.connect(partial(self.navigator.navigate, screen='help'))

        self.deleteKeyButton = QPushButton(i18n.t('screens.home.buttons.deleteKey'))
        self.deleteKeyButton.setObjectName('resetButton')
        self.deleteKeyButton.clicked.connect(self.deleteKey)

        self.settingsButton = QPushButton(i18n.t('screens.home.buttons.settings'))
        self.settingsButton.setObjectName('normalButton')
        self.settingsButton.clicked.connect(partial(self.navigator.navigate, screen='settings'))

        self.modelsCombo = QComboBox()
        self.modelsCombo.setPlaceholderText(i18n.t('screens.home.combos.selectModel'))

        self.selectModelLayout = QVBoxLayout()
        self.toggleServiceLayout = QVBoxLayout()

        self.toggleServiceSwitch = ToggleSwitch(
            parent=self, 
            checked=False,
            height=30,
            width=55
        )

        self.nav.addWidget(self.logo)
        self.nav.addSpacing(10)
        self.nav.addWidget(self.titleLabel)
        self.nav.addStretch()

        self.toggleServiceLayout.addWidget(self.toggleServiceLabel)
        self.toggleServiceLayout.addWidget(self.toggleServiceSwitch)
        self.toggleServiceLayout.addStretch(1)

        self.selectModelLayout.addWidget(self.selectModelLabel)
        self.selectModelLayout.addWidget(self.modelsCombo)
        self.selectModelLayout.addStretch(1)

        self.content.addLayout(self.selectModelLayout)
        self.content.addLayout(self.toggleServiceLayout)

        self.bottom.addWidget(self.deleteKeyButton)
        self.bottom.addWidget(self.helpButton)
        self.bottom.addWidget(self.settingsButton)

        self.bottom.addStretch(1) 

        self.screenLayout.addLayout(self.nav)
        self.screenLayout.addLayout(self.content)
        self.screenLayout.addStretch(1) 
        self.screenLayout.addLayout(self.bottom)

        self.setLayout(self.screenLayout)

        self.showNotify = QFlow.globals.app.showNotify
        
        self.showNotify(
            message=i18n.t('screens.home.notifications.welcome'),
            type='info'
        )

        self.setListeners()

    @privatemethod
    def setListeners(self):
        def handleHotkey(prompt: str):
            if self.isRunning:
                return

            if not self.toggleServiceSwitch.isChecked():
                return

            self.isRunning = True

            def task():
                try:
                    model = self.modelsCombo.currentText()
                    asyncio.run(
                        Combinations.interpret(
                            apiKey=self.key, 
                            modelName=model, 
                            prompt=prompt
                        )
                    )
                finally:
                    self.isRunning = False

            threading.Thread(target=task, daemon=True).start()

        COMBINATIONS = SETTINGS.getHotkeys()

        for key in SETTINGS.HOTKEYS.keys():
            keyboard.add_hotkey(
                hotkey=key, 
                callback=partial(handleHotkey, COMBINATIONS[key])
            )
    
    def deleteKey(self):
        SETTINGS.updateKey(None)
        
        self.navigator.navigate(screen='setup')

        self.showNotify(
            message=i18n.t('screens.home.notifications.keyDeleted'),
            type='success'
        )

    def copyKey(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.key)

        self.showNotify(
            message=i18n.t('screens.home.notifications.keyCopied'),
            type='success'
        )

    def handleLoadError(self):
        self.showNotify(
            message=i18n.t('screens.home.notifications.noModels'),
            type='error'
        )

        self.toggleServiceSwitch.setDisabled(True)
        self.setModelsList([])
    
    def handleLoadSuccess(self):
        self.toggleServiceSwitch.setDisabled(False)
        self.setModelsList(self.models)

    def loadScreenData(self) -> list:
        self.models = AIController(self.key).getModels()

        if not self.models:
            self.handleLoadError()
            return
        
        self.handleLoadSuccess()
    
    def setModelsList(self, models: list) -> None:
        self.modelsCombo.clear()
        self.modelsCombo.addItems(models)
        self.modelsCombo.setCurrentIndex(0)