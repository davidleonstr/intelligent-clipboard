from QFlow import Template
from QFlow.modules import config

from QFlow.components import TitleBar
from qtpy.QtWidgets import QVBoxLayout, QStackedWidget, QSizeGrip, QApplication, QSystemTrayIcon, QMenu
from qtpy.QtCore import Qt, QTimer

from qtpy.QtGui import QIcon, QAction

from config import CONFIG
from helpers import JSONFile, ObjectBuilder

SCREENCONFIG = ObjectBuilder(
    JSONFile(CONFIG.folders['configs']['screens']['template']).read()
).obj

# Default window template
@config(SCREENCONFIG)
class DefaultTemplate(Template):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        # Window bar
        self.titleBar = TitleBar(
            parent=parent, 
            title=self.parent().title, 
            onWindowMinimize=self.windowsMinimize,
        )

        # I don't want that option
        self.titleBar.btnMaximize.setDisabled(True) 

        # Main Layout
        self.mainLayout = QVBoxLayout()

        # Remove margins
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Screens pointer
        self.screens = QStackedWidget()
        self.screens.setObjectName('screens')

        self.mainLayout.setSpacing(0)

        # Add widgets
        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addWidget(self.screens)

        # Widget to resize window
        self.sizegrip = QSizeGrip(self)
        self.mainLayout.addWidget(self.sizegrip, 0, Qt.AlignRight | Qt.AlignBottom)

        # Set layout
        self.setLayout(self.mainLayout)

        # Set tray
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon(self.Config.icons.appIcon)) # Icon

        # Create tray menu
        trayMenu = QMenu()

        # Add actions
        showAction = QAction(self.Config.texts.open, self)
        quitAction = QAction(self.Config.texts.close, self)

        # Set actions
        showAction.triggered.connect(self.showWindow)
        quitAction.triggered.connect(QApplication.quit)

        # Add actions
        trayMenu.addAction(showAction)
        trayMenu.addAction(quitAction)

        # Set context menu to the icon
        self.trayIcon.setContextMenu(trayMenu)

        # When shows options
        self.trayIcon.activated.connect(self.onTrayClick)

        # Show tray icon
        self.trayIcon.show()
    
    # When the window is minimized
    def windowsMinimize(self):
        # Change order
        QTimer.singleShot(0, self.parent().hide)

        self.trayIcon.showMessage(
            self.Config.texts.minimized,
            self.Config.texts.whenItIsMinimized,
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )

    # When the windows is showed
    def showWindow(self):
        # RANDOM BULLSHIT GO !!!
        self.parent().show()
        self.parent().setWindowState(Qt.WindowState.WindowNoState)
        self.parent().activateWindow()
        self.parent().showNormal()

    # I don't know. I found this in stackoverflow
    def onTrayClick(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showWindow()