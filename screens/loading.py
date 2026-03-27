import QFlow
from QFlow.modules import session
from QFlow.hooks import Params

from qtpy.QtWidgets import (
    QVBoxLayout
)
from qtpy.QtGui import QColor
from qtpy.QtCore import QUrl
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWebChannel import QWebChannel
import os

@QFlow.screen(
    name='loding',
    parentType=QFlow.App
)
@session()
class LoadingScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

    def UI(self):
        # Window params
        self.params = Params(self).get()

        # Create screen layout
        self.screenlayout = QVBoxLayout()

        # Init brower
        self.browser = QWebEngineView()

        # To avoid white flash
        self.browser.setStyleSheet('background-color: #1e1e1e;')
        self.browser.page().setBackgroundColor(QColor('#1e1e1e'))

        # Set web channel
        self.loadingScreenChannel = QWebChannel()
        self.loadingScreenChannel.registerObject('bridge', self.params.get('bridge'))
        self.browser.page().setWebChannel(self.loadingScreenChannel)

        # Set screen
        path = os.path.abspath('screens/html/loading-screen.html')
        self.browser.setUrl(QUrl.fromLocalFile(path))

        # Add browser
        self.screenlayout.addWidget(self.browser)

        # Set layour
        self.setLayout(self.screenlayout)