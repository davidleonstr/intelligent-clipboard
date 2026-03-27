import os

import QFlow
from QFlow.modules import session

from qtpy.QtWidgets import (
    QVBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView

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
        self.screenlayout = QVBoxLayout()

        self.browser = QWebEngineView()
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))
        self.browser.setUrl(
            QUrl.fromLocalFile(
                os.path.abspath('screens/html/loading-screen.html')
            )
        )

        self.screenlayout.addWidget(self.browser)

        self.setLayout(self.screenlayout)