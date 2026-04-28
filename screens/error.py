import QFlow
from QFlow.modules import session

from qtpy.QtWidgets import (
    QVBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtWebEngineWidgets import QWebEngineView

from helpers.builders import Object

from pym import Render

from config import CONFIG
from app import RELATIVES

SCREENCONFIG = Object(
    CONFIG.language(
        name='error', language=RELATIVES.LANGUAGE, objType='screens'
    )
).obj

@QFlow.screen(
    name='error',
    parentType=QFlow.App
)
@session()
class ErrorScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)

        html = Render(
            context={
                'SCREENCONFIG': SCREENCONFIG
            }
        ).get(
            open(
                'screens/html/error-screen.html',
                encoding='utf-8'
            ).read()
        )

        self.browser = QWebEngineView()
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))
        self.browser.setHtml(html)

        self.screenLayout.addWidget(self.browser)

        self.setLayout(self.screenLayout)