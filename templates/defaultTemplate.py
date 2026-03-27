from QFlow import Template
from QFlow.modules import config
from QFlow.components import TitleBar

from qtpy.QtWidgets import (
    QVBoxLayout, QStackedWidget, QSizeGrip, QApplication, QSystemTrayIcon, QMenu
)
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QIcon, QAction

from helpers.builders import Object
from helpers.files import JSON

from config import CONFIG

SCREENCONFIG = Object(
    JSON(CONFIG.folders['configs']['screens']['template']).read()
).obj

@config(SCREENCONFIG)
class DefaultTemplate(Template):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.titleBar = TitleBar(
            parent=parent, 
            title=self.parent().title, 
            onWindowMinimize=self.windowsMinimize,
        )

        self.titleBar.btnMaximize.setDisabled(True)

        self.screens = QStackedWidget()
        self.screens.setObjectName('screens')

        self.sizegrip = QSizeGrip(self)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.screens)
        self.mainLayout.addWidget(self.sizegrip, 0, Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(self.mainLayout)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(self.Config.icons.appIcon)) # Icon

        trayMenu = QMenu()

        showAction = QAction(self.Config.texts.menu.actions.open, self)
        quitAction = QAction(self.Config.texts.menu.actions.close, self)

        showAction.triggered.connect(self.showWindow)
        quitAction.triggered.connect(QApplication.quit)

        trayMenu.addAction(showAction)
        trayMenu.addAction(quitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.activated.connect(self.onTrayClick)
        self.trayIcon.show()
    
    def windowsMinimize(self):
        QTimer.singleShot(0, self.parent().hide)

        self.trayIcon.showMessage(
            self.Config.texts.menu.messages.title,
            self.Config.texts.menu.messages.information,
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )

    def showWindow(self):
        self.parent().show()
        self.parent().setWindowState(Qt.WindowState.WindowNoState)
        self.parent().activateWindow()
        self.parent().showNormal()

    def onTrayClick(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showWindow()