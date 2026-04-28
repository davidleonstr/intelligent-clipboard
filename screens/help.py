import QFlow
from QFlow.modules import session, config

from helpers.builders import Object

from qtpy.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtWebEngineWidgets import QWebEngineView

from pym import Render

from config import CONFIG
from app import RELATIVES

SCREENCONFIG = Object(
    CONFIG.language(
        name='help', language=RELATIVES.LANGUAGE, objType='screens'
    )
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

        html = Render(
            context={
                'SCREENCONFIG': SCREENCONFIG
            }
        ).get(
            open(
                'screens/html/help-screen.html',
                encoding='utf-8'
            ).read()
        )

        self.browser = QWebEngineView()
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))
        self.browser.setHtml(html)
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
        hotkey = RELATIVES.KEYCOMBINATION

        self.browser.page().runJavaScript(
            f'writeHotkeyCombination(`{hotkey}`);'
        )