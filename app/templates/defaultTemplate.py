import i18n

from QFlow import Template
from QFlow.components import TitleBar

from app.tree import FOLDERS

from qtpy.QtWidgets import (
    QVBoxLayout, QStackedWidget, QSizeGrip, QApplication, QSystemTrayIcon, QMenu
)
from qtpy.QtCore import Qt, QTimer
from qtpy.QtGui import QIcon

try:
    from PyQt6.QtGui import QAction
except:
    from qtpy.QtGui import QAction

class DefaultTemplate(Template):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.titleBar = TitleBar(
            parent=parent, 
            title=self.parent().title, 
            onWindowMinimize=self.windowsMinimize,
        )

        self.titleBar.title.setContentsMargins(5, 0, 0, 0)
        self.titleBar.btnMaximize.setDisabled(True)

        self.screens = QStackedWidget()
        self.screens.setObjectName('screens')

        self.sizegrip = QSizeGrip(self)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.screens)
        self.mainLayout.addWidget(
            self.sizegrip, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )

        self.setLayout(self.mainLayout)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(FOLDERS.f['app', 'resources', 'icons', 'app-icon.svg']))

        trayMenu = QMenu()

        showAction = QAction(i18n.t('screens.template.menu.actions.open'), self)
        quitAction = QAction(i18n.t('screens.template.menu.actions.close'), self)

        showAction.triggered.connect(self.showWindow)
        quitAction.triggered.connect(QApplication.quit)

        trayMenu.addAction(showAction)
        trayMenu.addAction(quitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.activated.connect(self.onTrayClick)
        self.trayIcon.show()
    
    def windowsMinimize(self):
        parent = self.parent()

        QTimer.singleShot(0, parent.hide)

        self.trayIcon.showMessage(
            i18n.t('screens.template.menu.messages.title'),
            i18n.t('screens.template.menu.messages.information'),
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )

    def showWindow(self):
        parent = self.parent()
        
        parent.show()
        parent.setWindowState(Qt.WindowState.WindowNoState)
        parent.activateWindow()
        parent.showNormal()

    def onTrayClick(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showWindow()