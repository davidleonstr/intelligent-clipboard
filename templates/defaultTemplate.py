from QFlow import Template
from QFlow.components import TitleBar
from qtpy.QtWidgets import QVBoxLayout, QStackedWidget, QSizeGrip
from qtpy.QtCore import Qt

# Default window template
class DefaultTemplate(Template):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        # Window bar
        self.titleBar = TitleBar(parent=parent, title=self.parent().title)

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