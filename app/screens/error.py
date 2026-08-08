import i18n

import QFlow
from QFlow.injectors import session

from pym import Render

from qtpy.QtWidgets import (
    QVBoxLayout
)
from qtpy.QtGui import QColor

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except:
    from qtpy.QtWebEngineWidgets import QWebEngineView

from app.tree import FOLDERS

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

        self.backgroundColor = QFlow.globals.config.get('background-color')

        self.html = Render(
            context={
                'i18n': i18n
            }
        ).get(
            open(
                FOLDERS.f['app', 'screens', 'html', 'error-screen.html'],
                encoding='utf-8'
            ).read()
        )

        self.browser = QWebEngineView()

        self.browser.setStyleSheet(f'background-color: {self.backgroundColor};')
        self.browser.page().setBackgroundColor(QColor(self.backgroundColor))

        self.browser.setHtml(self.html)

        self.screenLayout.addWidget(self.browser)

        self.setLayout(self.screenLayout)