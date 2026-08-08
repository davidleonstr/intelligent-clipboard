import os

os.environ['QT_API'] = 'pyqt6'

import sys

import i18n

import QFlow

from qtpy.QtWidgets import QApplication, QMessageBox
from qtpy.QtGui import QGuiApplication
from qtpy.QtCore import Qt
from qtpy.QtGui import QPalette, QColor

from app.windows import App

if __name__ == '__main__':
    APP = QApplication(sys.argv)

    WINDOW = App()

    QFlow.globals.app = WINDOW
    
    QFlow.globals.config = {
        'background-color': WINDOW.backgroundColor
    }

    if QGuiApplication.styleHints().colorScheme() != Qt.ColorScheme.Dark:
        MESSAGEBOX = QMessageBox()
        
        MESSAGEBOX.setWindowIcon(WINDOW.icon())
        MESSAGEBOX.setWindowTitle(i18n.t('common.main.alerts.whiteMode.title'))
        MESSAGEBOX.setIcon(QMessageBox.Critical)
        MESSAGEBOX.setText(i18n.t('common.main.alerts.whiteMode.message'))

        MESSAGEBOX.exec()

        exit(1)

    PALETTE = APP.palette()
    PALETTE.setColor(QPalette.Window, QColor(WINDOW.backgroundColor))

    APP.setPalette(PALETTE)

    WINDOW.run(QApp=APP)