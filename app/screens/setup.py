import re
from functools import partial
import i18n

import QFlow
from QFlow.builders import Icon
from QFlow.components import Notify
from QFlow.hooks import Navigator

from app.settings import SETTINGS
from app.tree import FOLDERS

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from qtpy.QtCore import Qt, QTimer

@QFlow.screen(
    name='setup',
    parentType=QFlow.App
)
class SetupScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.navigator = Navigator(self)

    def UI(self):
        self.mainLayout = QVBoxLayout()
        self.centerLayout = QHBoxLayout()
        self.keyLayout = QHBoxLayout()

        self.keyLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titleLabel = QLabel(
            i18n.t('screens.setup.labels.title')
        )
        self.titleLabel.setObjectName('subtitle')
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo = QLabel()
        self.logoPixmap = Icon(
            FOLDERS.f['app', 'resources', 'icons', 'app-icon.svg'],
            120, 120
        )
        self.logo.setPixmap(self.logoPixmap)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.appNameLabel = QLabel(i18n.t('screens.setup.labels.appName'))
        self.appNameLabel.setObjectName('title')
        self.appNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.confirmButton = QPushButton(i18n.t('screens.setup.buttons.confirmKey'))
        self.confirmButton.setObjectName('resetButton')
        self.confirmButton.clicked.connect(self.sendKey)

        self.inputKey = QLineEdit()
        self.inputKey.returnPressed.connect(self.confirmButton.click)
        self.inputKey.setPlaceholderText(i18n.t('screens.setup.inputs.inputKey'))
        self.inputKey.setFixedWidth(250)
        self.inputKey.setEchoMode(QLineEdit.EchoMode.Password)

        self.aiLogo = QLabel()
        self.aiPixmap = Icon(
            FOLDERS.f['app', 'resources', 'icons', 'labels', 'ai-icon.svg'],
            31, 31
        )
        self.aiLogo.setPixmap(self.aiPixmap)
        self.aiLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.content = QVBoxLayout()
        self.content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.keyLayout.addWidget(self.aiLogo)
        self.keyLayout.addWidget(self.inputKey)

        self.content.addWidget(self.logo)
        self.content.addSpacing(12)
        self.content.addWidget(self.appNameLabel)
        self.content.addSpacing(12)
        self.content.addWidget(self.titleLabel)
        self.content.addSpacing(12)
        self.content.addLayout(self.keyLayout)
        self.content.addSpacing(12)
        self.content.addWidget(self.confirmButton)

        self.content.addWidget(self.confirmButton)

        self.centerLayout.addStretch()
        self.centerLayout.addLayout(self.content)
        self.centerLayout.addStretch()

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.centerLayout)
        self.mainLayout.addStretch()

        self.mainLayout.setContentsMargins(30, 20, 30, 10)
        self.setLayout(self.mainLayout)

        self.showNotify = QFlow.globals.app.showNotify

    def sendKey(self) -> None:
        self.processKey(
            key=self.inputKey.text().strip(),
            button=self.confirmButton,
            input=self.inputKey
        )

    def validateKey(self, key: str) -> bool:
        pattern = SETTINGS.KEYPATTERN
        return bool(re.match(pattern, key))

    def processKey(self, key: str, button: QPushButton, input: QLineEdit):
        if not self.validateKey(key):
            self.handleInvalidKey()
            return

        self.handleValidKey(key, button, input)

    def handleInvalidKey(self):
        self.showNotify(
            message=i18n.t('screens.setup.notifications.invalidKey'),
            type='error'
        )

    def handleValidKey(self, key: str, button: QPushButton, input: QLineEdit):
        button.setDisabled(True)

        self.showNotify(i18n.t('screens.setup.notifications.validKey'), 'success')

        SETTINGS.updateKey(key)

        self.showNotify(i18n.t('screens.setup.notifications.keySaved'), 'success')

        redirectNotify: Notify = self.showNotify(
            message=i18n.t('screens.setup.notifications.redirecting'),
            type='info'
        )

        QTimer.singleShot(
            redirectNotify.duration,
            partial(self.redirect, key, button, input)
        )

    def redirect(self, key: str, button: QPushButton, input: QLineEdit):
        button.setDisabled(False)
        input.clear()

        self.navigator.navigate(
            screen='home',
            params={
                'key': key
            }
        )