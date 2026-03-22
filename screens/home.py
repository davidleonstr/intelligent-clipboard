import QFlow
from QFlow.modules import config, session
from QFlow.components import Notify, ToggleSwitch

from config import CONFIG
from helpers import JSONFile, ObjectBuilder

SCREENCONFIG = ObjectBuilder(
    JSONFile(CONFIG.folders['configs']['screens']['home']).read()
).obj

from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from app.controllers import GeminiController
from app import Combinations, RELATIVES

import keyboard
import threading
import asyncio

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

    def UI(self):
        # Parameters from another screen or windows
        params = QFlow.hooks.Params(self).get()

        # API Key
        self.key = params.get('key')

        Notify(
            self.Config.texts.welcomeMessage,
            type='info',
            parent=self.parent()
        ).show()
        
        self.screenlayout = QVBoxLayout()
        self.screenlayout.setContentsMargins(0, 0, 0, 0)
        self.screenlayout.setSpacing(0)

        self.nav = QHBoxLayout()
        self.nav.setContentsMargins(30, 10, 10, 10)

        self.logo = QLabel()
        pixmap = QPixmap(self.Config.icons.appIcon)
        pixmap = pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)

        self.title = QLabel(self.Config.texts.homeTitle)
        self.title.setObjectName('title')

        self.nav.addWidget(self.logo)
        self.nav.addSpacing(8)
        self.nav.addWidget(self.title)
        self.nav.addStretch()

        self.content = QVBoxLayout()
        self.content.setContentsMargins(30, 10, 10, 10)

        self.bottom = QHBoxLayout()
        self.bottom.setContentsMargins(30, 10, 10, 10)

        self.keyLayout = QHBoxLayout()

        self.keyLabel = QLabel(
            self.Config.texts.keyLabel +
            'X' * len(self.key) +
            '.'
        )

        self.copyKeyBtn = QPushButton(self.Config.texts.copyKey)
        self.copyKeyBtn.clicked.connect(self.copyKey)

        self.keyLayout.addWidget(self.keyLabel)
        self.keyLayout.addSpacing(5)
        self.keyLayout.addWidget(self.copyKeyBtn)
        self.keyLayout.addStretch(1)

        self.toggleServiceLayout = QHBoxLayout()

        self.toggleServicelbl = QLabel(self.Config.texts.enableListener)

        self.toggleServiceSwitch = ToggleSwitch(self, checked=False)

        self.toggleServiceLayout.addWidget(self.toggleServicelbl)
        self.toggleServiceLayout.addSpacing(5)
        self.toggleServiceLayout.addWidget(self.toggleServiceSwitch)
        self.toggleServiceLayout.addStretch(1)

        self.selectModelLayout = QHBoxLayout()

        self.selectModelLbl = QLabel(self.Config.texts.selectModel)

        self.modelsCombo = QComboBox()

        self.selectModelLayout.addWidget(self.selectModelLbl)
        self.selectModelLayout.addSpacing(5)
        self.selectModelLayout.addWidget(self.modelsCombo)
        self.selectModelLayout.addStretch(1)

        self.content.addLayout(self.keyLayout)
        self.content.addLayout(self.selectModelLayout)
        self.content.addLayout(self.toggleServiceLayout)

        self.content.setSpacing(15)

        self.deleteKeyButton = QPushButton(self.Config.texts.deleteKey)
        self.deleteKeyButton.setObjectName('resetButton')

        self.deleteKeyButton.clicked.connect(self.deleteKey)

        self.bottom.addWidget(self.deleteKeyButton)

        self.bottom.addStretch(1) 
        
        self.helpButton = QPushButton(self.Config.texts.help)

        self.bottom.addWidget(self.helpButton)

        self.screenlayout.addLayout(self.nav)
        self.screenlayout.addLayout(self.content)

        self.screenlayout.addStretch(1) 

        self.screenlayout.addLayout(self.bottom)

        self.setLayout(self.screenlayout)

        # Load models
        self.loadModels()

        # Set listeners
        self.setListeners()

    # Home exclusive listener
    def setListeners(self):
        def handleHotkey():
            # To avoid multiple executions
            if self.isRunning:
                return

            if not self.toggleServiceSwitch.isChecked():
                return

            # To avoid multiple executions
            self.isRunning = True

            def task():
                try:
                    model = self.modelsCombo.currentText()
                    asyncio.run(Combinations.onCtrlI(self.key, model))
                finally:
                    # To avoid multiple executions
                    self.isRunning = False

            threading.Thread(target=task, daemon=True).start()

        keyboard.add_hotkey(RELATIVES.RelativesFile.get('key-combination'), handleHotkey)

    def copyKey(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.key)

        Notify(
            self.Config.texts.keyCopied,
            type='success',
            parent=self.parent()
        ).show()
    
    def deleteKey(self):
        self.parent().updateKey('') # Set IC key in blank        
        self.parent().setScreen('setup') # Move to setup

        Notify(
            self.Config.texts.keyDeleted,
            type='success',
            parent=self.parent()
        ).show()
    
    def loadModels(self) -> list:
        # Get models
        models = GeminiController(self.key).getAvailableModels()

        # Add models to options
        self.modelsCombo.addItems(models)

        # Select the first model
        self.modelsCombo.setCurrentIndex(0)