import os

import QFlow
from QFlow.modules import session, config

from helpers.builders import Object
from helpers.files import JSON

from qtpy.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView

from config import CONFIG

from app import RELATIVES

SCREENCONFIG = Object(
    JSON(CONFIG.folders['configs']['screens']['help']).read()
).obj

@QFlow.screen(
    name='help',
    parentType=QFlow.App
)
@config(SCREENCONFIG)
@session()
class HelpScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)
        self.screenLayout.setSpacing(20)
        
        self.bottom = QHBoxLayout()

        self.browser = QWebEngineView()
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))
        self.browser.setUrl(
            QUrl.fromLocalFile(
                os.path.abspath('screens/html/help-screen.html')
            )
        )
        self.browser.page().loadFinished.connect(self.onPageLoaded)

        self.backButton = QPushButton(self.Config.texts.buttons.goBack)
        self.backButton.setObjectName('normalButton')
        self.backButton.clicked.connect(self.parent().goBack)

        self.bottom.addWidget(self.backButton)
        self.bottom.addStretch(1)

        self.screenLayout.addWidget(self.browser)
        self.screenLayout.addLayout(self.bottom)

        self.setLayout(self.screenLayout)

    def onPageLoaded(self):
        hotkey = RELATIVES.RelativesFile.get('keyboard')['key-combination']

        self.browser.page().runJavaScript(
            f'writeHotkeyCombination(`{hotkey}`);'
        )