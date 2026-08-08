from functools import partial
import i18n

import QFlow
from QFlow.builders import Icon
from QFlow.hooks import Navigator

from app.tree import FOLDERS
from app.settings import SETTINGS

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QTextEdit, QScrollArea, QWidget, QFrame
)

@QFlow.screen(
    name='hotkeys',
    parentType=QFlow.App
)
class HotkeysScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.navigator = Navigator(self)
        self.editingHotkey = None

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)

        self.nav = QHBoxLayout()

        self.logo = QLabel()
        self.logoPixmap = Icon(FOLDERS.f['app', 'resources', 'icons', 'app-icon.svg'], 42, 42)
        self.logo.setPixmap(self.logoPixmap)

        self.titleLabel = QLabel(i18n.t('screens.hotkeys.labels.title'))
        self.titleLabel.setObjectName('title')

        self.nav.addWidget(self.logo)
        self.nav.addSpacing(10)
        self.nav.addWidget(self.titleLabel)
        self.nav.addStretch()

        self.content = QHBoxLayout()
        self.content.setSpacing(20)
        self.content.setContentsMargins(0, 20, 0, 20)

        self.listContainer = QVBoxLayout()
        self.listContainer.setSpacing(10)

        self.listScrollArea = QScrollArea()
        self.listScrollArea.setWidgetResizable(True)

        self.listWidget = QWidget()
        self.listLayout = QVBoxLayout(self.listWidget)
        self.listLayout.setSpacing(10)
        self.listLayout.addStretch(1)

        self.listScrollArea.setWidget(self.listWidget)

        self.addButton = QPushButton(i18n.t('screens.hotkeys.buttons.add'))
        self.addButton.setObjectName('normalButton')
        self.addButton.clicked.connect(self.startAdd)

        self.listContainer.addWidget(self.listScrollArea)
        self.listContainer.addWidget(self.addButton)

        self.formLayout = QVBoxLayout()
        self.formLayout.setSpacing(10)

        self.comboNameLabel = QLabel(i18n.t('screens.hotkeys.labels.hotkeyComboName'))
        self.comboNameInput = QLineEdit()
        self.comboNameInput.setPlaceholderText(i18n.t('screens.hotkeys.inputs.hotkeyComboName'))

        self.comboLabel = QLabel(i18n.t('screens.hotkeys.labels.hotkeyCombo'))
        self.comboInput = QLineEdit()
        self.comboInput.setPlaceholderText(i18n.t('screens.hotkeys.inputs.hotkeyCombo'))

        self.promptLabel = QLabel(i18n.t('screens.hotkeys.labels.promptContent'))
        self.promptInput = QTextEdit()
        self.promptInput.setPlaceholderText(i18n.t('screens.hotkeys.inputs.promptContent'))

        self.formButtons = QHBoxLayout()
        self.formButtons.setSpacing(10)

        self.saveButton = QPushButton(i18n.t('screens.hotkeys.buttons.save'))
        self.saveButton.setObjectName('resetButton')
        self.saveButton.clicked.connect(self.saveHotkey)

        self.cancelButton = QPushButton(i18n.t('screens.hotkeys.buttons.cancel'))
        self.cancelButton.setObjectName('normalButton')
        self.cancelButton.clicked.connect(self.clearForm)

        self.formButtons.addWidget(self.saveButton)
        self.formButtons.addWidget(self.cancelButton)
        self.formButtons.addStretch(1)

        self.formLayout.addWidget(self.comboNameLabel)
        self.formLayout.addWidget(self.comboNameInput)
        self.formLayout.addWidget(self.comboLabel)
        self.formLayout.addWidget(self.comboInput)
        self.formLayout.addWidget(self.promptLabel)
        self.formLayout.addWidget(self.promptInput)
        self.formLayout.addLayout(self.formButtons)

        self.content.addLayout(self.listContainer, 1)
        self.content.addLayout(self.formLayout, 1)

        self.bottom = QHBoxLayout()
        self.bottom.setSpacing(20)

        self.backButton = QPushButton(i18n.t('screens.hotkeys.buttons.goBack'))
        self.backButton.setObjectName('normalButton')
        self.backButton.clicked.connect(partial(self.navigator.navigate, screen=-1))

        self.bottom.addWidget(self.backButton)
        self.bottom.addStretch(1)

        self.screenLayout.addLayout(self.nav)
        self.screenLayout.addLayout(self.content)
        self.screenLayout.addLayout(self.bottom)

        self.setLayout(self.screenLayout)

        self.showNotify = QFlow.globals.app.showNotify

        self.reloadHotkeysList()

    def reloadHotkeysList(self):
        while self.listLayout.count() > 1:
            item = self.listLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        hotkeys = list(SETTINGS.HOTKEYS.keys())

        if not hotkeys:
            emptyLabel = QLabel(i18n.t('screens.hotkeys.labels.noHotkeys'))
            self.listLayout.insertWidget(0, emptyLabel)
            return

        for index, hotkey in enumerate(hotkeys):
            row = QFrame()
            rowLayout = QHBoxLayout(row)
            rowLayout.setContentsMargins(0, 0, 0, 0)

            rowLabel = QLabel(hotkey)

            editButton = QPushButton(i18n.t('screens.hotkeys.buttons.edit'))
            editButton.setObjectName('normalButton')
            editButton.clicked.connect(partial(self.startEdit, hotkey))

            deleteButton = QPushButton(i18n.t('screens.hotkeys.buttons.delete'))
            deleteButton.setObjectName('resetButton')
            deleteButton.clicked.connect(partial(self.removeHotkey, hotkey))

            rowLayout.addWidget(rowLabel)
            rowLayout.addStretch(1)
            rowLayout.addWidget(editButton)
            rowLayout.addWidget(deleteButton)

            self.listLayout.insertWidget(index, row)

    def startAdd(self):
        self.editingHotkey = None
        self.comboNameInput.clear()
        self.comboInput.clear()
        self.promptInput.clear()

    def startEdit(self, hotkey: str):
        fileName: str = SETTINGS.HOTKEYS.get(hotkey)
        self.editingHotkey = hotkey
        self.comboNameInput.setText(fileName.replace('.md', str()))
        self.comboInput.setText(hotkey)
        self.promptInput.setText(SETTINGS.getPromptContent(hotkey))

    def clearForm(self):
        self.editingHotkey = None
        self.comboInput.clear()
        self.comboNameInput.clear()
        self.promptInput.clear()

    def saveHotkey(self):
        newHotkey = self.comboInput.text().strip().lower()
        newHotkeyName = self.comboNameInput.text().strip().lower()
        promptContent = self.promptInput.toPlainText()

        if not newHotkey:
            self.showNotify(i18n.t('screens.hotkeys.notifications.invalidHotkey'), 'error')
            return

        if not promptContent.strip():
            self.showNotify(i18n.t('screens.hotkeys.notifications.emptyPrompt'), 'error')
            return

        existingHotkeys = list(SETTINGS.HOTKEYS.keys())

        if self.editingHotkey is None:
            if newHotkey in existingHotkeys:
                self.showNotify(i18n.t('screens.hotkeys.notifications.invalidHotkey'), 'error')
                return

            promptFilename = f'{newHotkeyName}.md'
            SETTINGS.addHotkey(newHotkey, promptFilename, promptContent)

            self.showNotify(i18n.t('screens.hotkeys.notifications.hotkeyAdded'), 'success')
        else:
            if newHotkey != self.editingHotkey:
                if newHotkey in existingHotkeys:
                    self.showNotify(i18n.t('screens.hotkeys.notifications.invalidHotkey'), 'error')
                    return

                SETTINGS.renameHotkey(self.editingHotkey, newHotkey)

            SETTINGS.updateHotkeyPrompt(newHotkey, promptContent)

            self.showNotify(i18n.t('screens.hotkeys.notifications.hotkeyUpdated'), 'success')

        self.clearForm()
        self.reloadHotkeysList()

    def removeHotkey(self, hotkey: str):
        SETTINGS.deleteHotkey(hotkey)

        if self.editingHotkey == hotkey:
            self.clearForm()

        self.showNotify(i18n.t('screens.hotkeys.notifications.hotkeyDeleted'), 'success')

        self.reloadHotkeysList()