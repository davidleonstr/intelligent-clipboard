import keyboard
import threading
import asyncio

import QFlow
from QFlow.modules import config, session
from QFlow.components import Notify, ToggleSwitch

from config import CONFIG
from helpers.builders import Object
from helpers.files import JSON

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QApplication
)
from qtpy.QtCore import QTimer

from app.controllers import ServiceController
from app import Combinations, RELATIVES

SCREENCONFIG = Object(
    JSON(CONFIG.folders['configs']['screens']['home']).read()
).obj

@QFlow.screen(
    name='home',
    parentType=QFlow.App
)
@config(SCREENCONFIG)
@session()
class HomeScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.isRunning = False

    def effect(self):
        self.params = QFlow.hooks.Params(self).get()

        if self.params.get('key', False):
            self.key = self.params.get('key')
            self.params.pop('key')

            def load():
                self.loadScreenData()

            if hasattr(self, 'screenLayout'):
                load()
                return
                
            QTimer.singleShot(0, load)

    def UI(self):
        self.showNotify(
            self.Config.texts.notifications.welcome,
            'info'
        )
        
        self.screenlayout = QVBoxLayout()
        self.screenlayout.setContentsMargins(0, 0, 0, 0)
        self.screenlayout.setSpacing(0)

        self.nav = QHBoxLayout()
        self.nav.setContentsMargins(30, 10, 10, 10)

        self.logo = QLabel()
        logoPixmap = QFlow.helpers.Icon(self.Config.icons.appIcon, 42, 42)
        self.logo.setPixmap(logoPixmap)

        self.title = QLabel(self.Config.texts.labels.title)
        self.title.setObjectName('title')

        self.selectModelLbl = QLabel(self.Config.texts.labels.selectModel)
        self.keyLabel = QLabel()
        self.toggleServicelbl = QLabel(self.Config.texts.labels.enableService)

        self.content = QVBoxLayout()
        self.content.setContentsMargins(30, 10, 10, 10)
        self.content.setSpacing(15)

        self.bottom = QHBoxLayout()
        self.bottom.setContentsMargins(30, 10, 10, 10)

        self.helpButton = QPushButton(self.Config.texts.buttons.help)
        self.helpButton.setObjectName('normalButton')
        self.helpButton.clicked.connect(self.goToHelp)

        self.deleteKeyButton = QPushButton(self.Config.texts.buttons.deleteKey)
        self.deleteKeyButton.setObjectName('resetButton')
        self.deleteKeyButton.clicked.connect(self.deleteKey)

        self.modelsCombo = QComboBox()

        self.keyLayout = QHBoxLayout()
        self.selectModelLayout = QHBoxLayout()
        self.toggleServiceLayout = QHBoxLayout()

        self.copyKeyBtn = QPushButton(self.Config.texts.buttons.copyKey)
        self.copyKeyBtn.setObjectName('normalButton')
        self.copyKeyBtn.clicked.connect(self.copyKey)

        self.toggleServiceSwitch = ToggleSwitch(self, checked=False)

        self.nav.addWidget(self.logo)
        self.nav.addSpacing(8)
        self.nav.addWidget(self.title)
        self.nav.addStretch()

        self.keyLayout.addWidget(self.keyLabel)
        self.keyLayout.addSpacing(5)
        self.keyLayout.addWidget(self.copyKeyBtn)
        self.keyLayout.addStretch(1)

        self.toggleServiceLayout.addWidget(self.toggleServicelbl)
        self.toggleServiceLayout.addSpacing(5)
        self.toggleServiceLayout.addWidget(self.toggleServiceSwitch)
        self.toggleServiceLayout.addStretch(1)

        self.selectModelLayout.addWidget(self.selectModelLbl)
        self.selectModelLayout.addSpacing(5)
        self.selectModelLayout.addWidget(self.modelsCombo)
        self.selectModelLayout.addStretch(1)

        self.content.addLayout(self.keyLayout)
        self.content.addLayout(self.selectModelLayout)
        self.content.addLayout(self.toggleServiceLayout)

        self.bottom.addWidget(self.deleteKeyButton)
        self.bottom.addStretch(1) 
        self.bottom.addWidget(self.helpButton)

        self.screenlayout.addLayout(self.nav)
        self.screenlayout.addLayout(self.content)
        self.screenlayout.addStretch(1) 
        self.screenlayout.addLayout(self.bottom)

        self.setLayout(self.screenlayout)

        self.setListeners()

    def setListeners(self):
        def handleHotkey():
            if self.isRunning:
                return

            if not self.toggleServiceSwitch.isChecked():
                return

            self.isRunning = True

            def task():
                try:
                    model = self.modelsCombo.currentText()
                    asyncio.run(Combinations.interpret(self.key, model))
                finally:
                    self.isRunning = False

            threading.Thread(target=task, daemon=True).start()

        keyboard.add_hotkey(RELATIVES.RelativesFile.get('keyboard')['key-combination'], handleHotkey)

    def copyKey(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.key)

        self.showNotify(
            self.Config.texts.notifications.keyCopied,
            'success'
        )
    
    def deleteKey(self):
        updateKey = self.Session.getItem('updateKey')
        updateKey(None)
        
        self.goToSetup()

        self.showNotify(
            self.Config.texts.notifications.keyDeleted,
            'success'
        )
    
    def loadScreenData(self) -> list:
        models = ServiceController(self.key).getAvailableModels()

        self.toggleServiceSwitch.setDisabled(False)

        if not models:
            self.showNotify(
                self.Config.texts.notifications.noModels,
                'error'
            )

            self.toggleServiceSwitch.setDisabled(True)

        self.setKeyLabel(self.key)
        self.setModelsList(models)

    def formatKey(self, key: str) -> str:
        return (
            self.Config.texts.labels.key 
            +
            ''.join(
                self.Config.texts.labels.symbolToHideText if c != '-' else '-' for c in key
            ) 
            +
            '.'
        )

    def setKeyLabel(self, key: str):
        formatedKey = self.formatKey(key)
        self.keyLabel.setText(formatedKey)
    
    def setModelsList(self, models: list) -> None:
        self.modelsCombo.clear()
        self.modelsCombo.addItems(models)
        self.modelsCombo.setCurrentIndex(0)
    
    def showNotify(self, message: str, type: str):
        notify = Notify(
            message,
            type=type,
            parent=self.parent(),
            toggleProgressBar=False,
            autoShow=False
        )
        notify.containerLayout.setContentsMargins(20, 15, 20, 15)
        notify.show()
        return notify
    
    def goToHelp(self):
        self.parent().setScreen('help')
    
    def goToSetup(self):
        self.parent().setScreen('setup')