import QFlow
from QFlow.modules import session, config

from config import CONFIG
from helpers import JSONFile, ObjectBuilder

SCREENCONFIG = ObjectBuilder(
    JSONFile(CONFIG.folders['configs']['screens']['help']).read()
).obj

from qtpy.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView
import os

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
        # Create screen layout
        self.screenlayout = QVBoxLayout()

        # Init brower
        self.browser = QWebEngineView()

        # To avoid white flash
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))

        # Set screen
        path = os.path.abspath('screens/html/help-screen.html')
        self.browser.setUrl(QUrl.fromLocalFile(path))
        
        # Add browser
        self.screenlayout.addWidget(self.browser)

        self.bottom = QHBoxLayout()
        
        # Create back button
        self.backButton = QPushButton(self.Config.texts.goBack)
        # Set default object name for button style
        self.backButton.setObjectName('normalButton')
        # Add action
        self.backButton.clicked.connect(
            lambda: self.parent().goBack()
        )

        self.bottom.addStretch(1)
        self.bottom.addWidget(self.backButton)

        # Add back button
        self.screenlayout.addLayout(self.bottom)

        # Set layour
        self.setLayout(self.screenlayout)