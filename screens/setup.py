import QFlow
from QFlow.modules import config, session
from QFlow.components import Notify
import re

from config import CONFIG
from helpers import JSONFile, ObjectBuilder

SCREENCONFIG = ObjectBuilder(
    JSONFile(CONFIG.folders['configs']['screens']['setup']).read()
).obj

from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout, QWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

from app import RELATIVES

# Initial Form
@config(SCREENCONFIG)
class KeyForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        centerLayout = QHBoxLayout()

        formLayout = QFormLayout()
        formLayout.setFormAlignment(Qt.AlignCenter)
        formLayout.setLabelAlignment(Qt.AlignLeft)

        self.title = QLabel(
            self.Config.texts.title
        )
        self.title.setObjectName('subtitle')
        self.title.setAlignment(Qt.AlignCenter)

        self.logo = QLabel()

        pixmap = QPixmap(self.Config.icons.appIcon)

        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)

        self.inputKey = QLineEdit()
        self.inputKey.setPlaceholderText(self.Config.texts.inputKeyPlaceholder)
        self.inputKey.setFixedWidth(250)
        self.inputKey.setEchoMode(QLineEdit.Password)

        self.btnConfirm = QPushButton(self.Config.texts.confirm)
        self.btnConfirm.setObjectName('confirmButton')

        # Execute checking
        self.btnConfirm.clicked.connect(
            lambda: self.parent().checkKey(
                key=self.inputKey.text().strip(),
                button=self.btnConfirm
            )
        )

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignCenter)

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignCenter)

        container.addWidget(self.logo)

        self.appName = QLabel(self.Config.texts.appName)
        self.appName.setObjectName('title')
        self.appName.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container.addWidget(self.appName)
        container.addSpacing(10)

        container.addWidget(self.title)
        container.addSpacing(10)

        formLayout.addRow(self.Config.texts.keyIndicator, self.inputKey)

        container.addLayout(formLayout)
        container.addSpacing(10)

        container.addWidget(self.btnConfirm)

        centerLayout.addStretch()
        centerLayout.addLayout(container)
        centerLayout.addStretch()

        mainLayout.addStretch()
        mainLayout.addLayout(centerLayout)
        mainLayout.addStretch()

        self.setLayout(mainLayout)

@QFlow.screen(
    name='setup',
    parentType=QFlow.App,
    autoreloadUI=True
)
@config(SCREENCONFIG)
@session()
class SetupScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        self.params = QFlow.hooks.Params(self).get()

        # If key
        self.key = self.params.get('key', False)

        # Create screen layout
        self.screenlayout = QVBoxLayout()

        # Create form
        self.keyForm = KeyForm(parent=self)

        # Add form
        self.screenlayout.addWidget(self.keyForm)

        # Set layour
        self.setLayout(self.screenlayout)
    
    def checkKey(self, key: str, button: QPushButton):
        # Check if it is a valid key
        pattern = RELATIVES.RelativesFile.get('api-key-pattern')
        
        if not re.match(pattern, key):
            # Show error
            Notify(self.Config.texts.invalidKey, type='error', parent=self.parent()).show()

            # Return if error
            return
        
        # Disable
        button.setDisabled(True)
        
        # Key Setted
        Notify(self.Config.texts.keySetted, type='success', parent=self.parent()).show()
        # Show redirecting
        Notify(self.Config.texts.redirecting, type='info', parent=self.parent()).show()

        # Update key using app method
        self.parent().updateKey(key)

        # Move to the other screen
        QTimer.singleShot(
            2500, 
            lambda: self.parent().setScreen(
                'home', 
                args={
                    'key': key
                }
            )
        )