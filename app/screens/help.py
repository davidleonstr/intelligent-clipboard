from functools import partial
import i18n

import QFlow
from QFlow.hooks import Navigator

from app.tree import FOLDERS
from app.settings import SETTINGS

from pym import Render

from qtpy.QtWidgets import (
    QVBoxLayout, QPushButton, QHBoxLayout
)
from qtpy.QtGui import QColor

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
except:
    from qtpy.QtWebEngineWidgets import QWebEngineView

@QFlow.screen(
    name='help',
    parentType=QFlow.App
)
class HelpScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.navigator = Navigator(self)

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)
        self.screenLayout.setSpacing(20)

        self.backgroundColor = QFlow.globals.config.get('background-color')
        
        self.bottom = QHBoxLayout()

        self.html = Render(
            context={
                'i18n': i18n,
                'HOTKEYS': SETTINGS.HOTKEYS.keys()
            }
        ).get(
            open(
                FOLDERS.f['app', 'screens', 'html', 'help-screen.html'],
                encoding='utf-8'
            ).read()
        )

        self.browser = QWebEngineView()

        self.browser.setStyleSheet(f'background-color: {self.backgroundColor};')
        self.browser.page().setBackgroundColor(QColor(self.backgroundColor))

        self.browser.setHtml(self.html)

        self.backButton = QPushButton(i18n.t('screens.help.buttons.goBack'))
        self.backButton.setObjectName('normalButton')
        self.backButton.clicked.connect(partial(self.navigator.navigate, screen=-1))

        self.bottom.addWidget(self.backButton)
        self.bottom.addStretch(1)

        self.screenLayout.addWidget(self.browser)
        self.screenLayout.addLayout(self.bottom)

        self.setLayout(self.screenLayout)