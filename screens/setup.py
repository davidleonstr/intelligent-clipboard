import re

import QFlow
from QFlow.helpers import Icon
from QFlow.modules import config, session

from app import RELATIVES
from config import CONFIG

from helpers.builders import Object
from helpers.files import JSON

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget
)
from qtpy.QtCore import Qt, QTimer

SCREENCONFIG = Object(
    JSON(
        CONFIG.folders['locales']['languages'][RELATIVES.LANGUAGE]['screens']['setup']
    ).read()
).obj

@config(SCREENCONFIG)
class KeyForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout()
        self.centerLayout = QHBoxLayout()
        self.keyLayout = QHBoxLayout()

        self.keyLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel(
            self.Config.texts.labels.title
        )
        self.title.setObjectName('subtitle')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo = QLabel()
        self.logoPixmap = Icon(CONFIG.folders['icons']['files']['normals']['app-icon'], 120, 120)
        self.logo.setPixmap(self.logoPixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.appName = QLabel(self.Config.texts.labels.appName)
        self.appName.setObjectName('title')
        self.appName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.inputKey = QLineEdit()
        self.inputKey.setPlaceholderText(self.Config.texts.inputs.inputKey)
        self.inputKey.setFixedWidth(250)
        self.inputKey.setEchoMode(QLineEdit.EchoMode.Password)

        self.aiLogo = QLabel()
        self.aiPixmap = Icon(CONFIG.folders['icons']['files']['labels']['ai-icon'], 31, 31)
        self.aiLogo.setPixmap(self.aiPixmap)
        self.aiLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btnConfirm = QPushButton(self.Config.texts.buttons.confirmKey)
        self.btnConfirm.setObjectName('resetButton')
        self.btnConfirm.clicked.connect(self.sendKey)

        self.content = QVBoxLayout()
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content = QVBoxLayout()
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.keyLayout.addWidget(self.aiLogo)
        self.keyLayout.addWidget(self.inputKey)

        self.content.addWidget(self.logo)
        self.content.addWidget(self.appName) 
        self.content.addSpacing(15)
        self.content.addWidget(self.title)
        self.content.addSpacing(5)
        self.content.addLayout(self.keyLayout)
        self.content.addSpacing(9)

        self.content.addWidget(self.btnConfirm)

        self.centerLayout.addStretch()
        self.centerLayout.addLayout(self.content)
        self.centerLayout.addStretch()

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.centerLayout)
        self.mainLayout.addStretch()

        self.setLayout(self.mainLayout)
    
    def sendKey(self) -> None:
        parent: SetupScreen = self.parent()
        parent.processKey(
            key=self.inputKey.text().strip(),
            button=self.btnConfirm,
            input=self.inputKey
        )

@QFlow.screen(
    name='setup',
    parentType=QFlow.App
)
@config(SCREENCONFIG)
@session()
class SetupScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)
        self.keyForm = KeyForm(parent=self)
        self.screenLayout.addWidget(self.keyForm)
        self.setLayout(self.screenLayout)

        self.updateKey = self.Session.getItem('updateKey')
        self.showNotify = self.Session.getItem('showNotify')

    def validateKey(self, key: str) -> bool:
        pattern = RELATIVES.RelativesFile.get('auth')['ic-key-pattern']
        return bool(re.match(pattern, key))
    
    def processKey(self, key: str, button: QPushButton, input: QLineEdit):
        if not self.validateKey(key):
            self.handleInvalidKey()
            return

        self.handleValidKey(key, button, input)

    def handleInvalidKey(self):
        self.showNotify(
            self.Config.texts.notifications.invalidKey,
            'error'
        )

    def handleValidKey(self, key: str, button: QPushButton, input: QLineEdit):
        self.updateKey(key)

        button.setDisabled(True)

        self.showNotify(self.Config.texts.notifications.validKey, 'success')
        self.showNotify(self.Config.texts.notifications.keySetted, 'success')

        redirectNotify = self.showNotify(
            self.Config.texts.notifications.redirecting,
            'info'
        )

        QTimer.singleShot(
            redirectNotify.duration,
            lambda: self.redirect(key, button, input)
        )

    def redirect(self, key: str, button: QPushButton, input: QLineEdit):
        button.setDisabled(False)
        input.clear()

        self.parent().setScreen(
            name='home',
            args={
                'key': key
            }
        )