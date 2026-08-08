import i18n

import QFlow
from QFlow.hooks import Params

from app.tree import FOLDERS

from pym import Render

from qtpy.QtWidgets import (
    QVBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtWebChannel import QWebChannel

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except:
    from qtpy.QtWebEngineWidgets import QWebEngineView

@QFlow.screen(
    name='loading',
    parentType=QFlow.App
)
class LoadingScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        self.params = Params(self).get()

        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)

        self.backgroundColor = QFlow.globals.config.get('background-color')

        self.loadingScreenChannel = QWebChannel()
        self.loadingScreenChannel.registerObject('bridge', self.params.get('bridge'))

        self.html = Render(
            context={
                'i18n': i18n
            }
        ).get(
            open(
                FOLDERS.f['app', 'screens', 'html', 'loading-screen.html'],
                encoding='utf-8'
            ).read()
        )

        self.browser = QWebEngineView()

        self.browser.setStyleSheet(f'background-color: {self.backgroundColor};')
        self.browser.page().setBackgroundColor(QColor(self.backgroundColor))

        self.browser.page().setWebChannel(self.loadingScreenChannel)
        
        self.browser.setHtml(self.html)

        self.screenLayout.addWidget(self.browser)

        self.setLayout(self.screenLayout)