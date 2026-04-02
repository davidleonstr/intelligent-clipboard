import re

import QFlow
from QFlow.helpers import Icon
from QFlow.modules import config, session

from app import RELATIVES
from config import CONFIG

from helpers.builders import Object
from helpers.files import JSON

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QWidget
)
from qtpy.QtCore import Qt, QTimer

SCREENCONFIG = Object(
    JSON(CONFIG.folders['configs']['screens']['setup']).read()
).obj

@config(SCREENCONFIG)
class KeyForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        centerLayout = QHBoxLayout()

        formLayout = QFormLayout()
        formLayout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title = QLabel(
            self.Config.texts.labels.title
        )
        self.title.setObjectName('subtitle')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo = QLabel()
        logoPixmap = Icon(self.Config.icons.appIcon, 120, 120)
        self.logo.setPixmap(logoPixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.appName = QLabel(self.Config.texts.labels.appName)
        self.appName.setObjectName('title')
        self.appName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.inputKey = QLineEdit()
        self.inputKey.setPlaceholderText(self.Config.texts.inputs.inputKey)
        self.inputKey.setFixedWidth(250)
        self.inputKey.setEchoMode(QLineEdit.EchoMode.Password)

        self.aiLogo = QLabel()
        aiPixmap = Icon(self.Config.icons.aiIcon, 31, 31)
        self.aiLogo.setPixmap(aiPixmap)
        self.aiLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btnConfirm = QPushButton(self.Config.texts.buttons.confirmKey)
        self.btnConfirm.setObjectName('resetButton')
        self.btnConfirm.clicked.connect(self.sendKey)

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container.addWidget(self.logo)
        container.addWidget(self.appName) 
        container.addWidget(self.title)

        formLayout.addRow(self.aiLogo, self.inputKey)

        container.addLayout(formLayout)
        container.addSpacing(20)
        container.addWidget(self.btnConfirm)

        centerLayout.addStretch()
        centerLayout.addLayout(container)
        centerLayout.addStretch()

        mainLayout.addStretch()
        mainLayout.addLayout(centerLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)
    
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