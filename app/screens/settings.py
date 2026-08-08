from functools import partial
import i18n

import QFlow
from QFlow.builders import Icon
from QFlow.hooks import Navigator

from app.tree import FOLDERS
from app.settings import SETTINGS

from qtpy.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QLineEdit
)

from qtpy.QtWidgets import QFrame

from qtpy.QtCore import Qt

@QFlow.screen(
    name='settings',
    parentType=QFlow.App
)
class SettingsScreen(QFlow.Screen):
    def __init__(self, parent):
        self.args['parent'] = parent
        super().__init__(**self.args)

        self.navigator = Navigator(self)

    def UI(self):
        self.screenLayout = QVBoxLayout()
        self.screenLayout.setContentsMargins(30, 20, 30, 10)

        self.nav = QHBoxLayout()

        self.logo = QLabel()
        self.logoPixmap = Icon(FOLDERS.f['app', 'resources', 'icons', 'app-icon.svg'], 42, 42)
        self.logo.setPixmap(self.logoPixmap)

        self.titleLabel = QLabel(i18n.t('screens.settings.labels.title'))
        self.titleLabel.setObjectName('title')

        self.nav.addWidget(self.logo)
        self.nav.addSpacing(10)
        self.nav.addWidget(self.titleLabel)
        self.nav.addStretch()

        self.content = QVBoxLayout()
        self.content.setSpacing(20)
        self.content.setContentsMargins(0, 20, 0, 20)

        self.languageLabel = QLabel(i18n.t('screens.settings.labels.selectLanguage'))
        self.languageCombo = QComboBox()

        for code in SETTINGS.getLanguages():
            self.languageCombo.addItem(code, code)

        currentIndex = self.languageCombo.findData(SETTINGS.LANGUAGE)
        if currentIndex != -1:
            self.languageCombo.setCurrentIndex(currentIndex)

        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.addWidget(self.languageLabel)
        self.settingsLayout.addWidget(self.languageCombo)

        self.hrLineL = QFrame()
        self.hrLineL.setFrameShape(QFrame.Shape.HLine)
        self.hrLineL.setFrameShadow(QFrame.Shadow.Sunken)

        self.separationLabel = QLabel(i18n.t('screens.settings.labels.advancedSettings'))
        self.separationLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hrLineR = QFrame()
        self.hrLineR.setFrameShape(QFrame.Shape.HLine)
        self.hrLineR.setFrameShadow(QFrame.Shadow.Sunken)

        self.lineLayout = QHBoxLayout()
        self.lineLayout.addWidget(self.hrLineL)
        self.lineLayout.addWidget(self.separationLabel)
        self.lineLayout.addWidget(self.hrLineR)

        self.settingsLayout.addLayout(self.lineLayout)

        self.advancedLayout = QVBoxLayout()
        self.advancedLayout.setSpacing(20)

        self.openaiWrapperLabel = QLabel(i18n.t('screens.settings.labels.openaiWrapper'))
        self.openaiWrapperInput = QLineEdit()
        self.openaiWrapperInput.setPlaceholderText(i18n.t('screens.settings.inputs.openaiWrapper'))
        self.openaiWrapperInput.setText(SETTINGS.OPENAIWRAPPER or str())

        self.keyPatternLabel = QLabel(i18n.t('screens.settings.labels.keyPattern'))
        self.keyPatternInput = QLineEdit()
        self.keyPatternInput.setPlaceholderText(i18n.t('screens.settings.inputs.keyPattern'))
        self.keyPatternInput.setText(SETTINGS.KEYPATTERN or str())

        self.seedCipherLabel = QLabel(i18n.t('screens.settings.labels.seedCipher'))
        self.seedCipherInput = QLineEdit()
        self.seedCipherInput.setPlaceholderText(i18n.t('screens.settings.inputs.seedCipher'))
        self.seedCipherInput.setText(SETTINGS.SEEDCIPHER or str())
        self.seedCipherInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.openaiWrapperLayout = QVBoxLayout()
        self.openaiWrapperLayout.addWidget(self.openaiWrapperLabel)
        self.openaiWrapperLayout.addWidget(self.openaiWrapperInput)

        self.keyPatternLayout = QVBoxLayout()
        self.keyPatternLayout.addWidget(self.keyPatternLabel)
        self.keyPatternLayout.addWidget(self.keyPatternInput)

        self.seedCipherLayout = QVBoxLayout()
        self.seedCipherLayout.addWidget(self.seedCipherLabel)
        self.seedCipherLayout.addWidget(self.seedCipherInput)

        self.openAdvancedSectionButton = QPushButton(
            i18n.t('screens.settings.buttons.openAdvancedSettings')
        )
        self.openAdvancedSectionButton.setObjectName('normalButton')
        self.openAdvancedSectionButton.clicked.connect(self.showAdvancedSection)

        self.openAdvancedSectionLayout = QHBoxLayout()
        self.openAdvancedSectionLayout.addStretch(1)
        self.openAdvancedSectionLayout.addWidget(self.openAdvancedSectionButton)
        self.openAdvancedSectionLayout.addStretch(1) 

        self.advancedLayout.addLayout(self.openaiWrapperLayout)
        self.advancedLayout.addLayout(self.keyPatternLayout)
        self.advancedLayout.addLayout(self.seedCipherLayout)

        self.settingsLayout.addLayout(self.advancedLayout)

        self.settingsLayout.addLayout(self.openAdvancedSectionLayout)
        
        self.settingsLayout.addStretch(1)

        self.content.addLayout(self.settingsLayout)

        self.bottom = QHBoxLayout()
        self.bottom.setSpacing(20)

        self.saveButton = QPushButton(i18n.t('screens.settings.buttons.save'))
        self.saveButton.setObjectName('resetButton')
        self.saveButton.clicked.connect(self.saveSettings)

        self.hotkeysButton = QPushButton(i18n.t('screens.settings.buttons.manageHotkeys'))
        self.hotkeysButton.setObjectName('normalButton')
        self.hotkeysButton.clicked.connect(partial(self.navigator.navigate, screen='hotkeys'))

        self.backButton = QPushButton(i18n.t('screens.settings.buttons.goBack'))
        self.backButton.setObjectName('normalButton')
        self.backButton.clicked.connect(partial(self.navigator.navigate, screen=-1))

        self.bottom.addWidget(self.saveButton)
        self.bottom.addWidget(self.hotkeysButton)
        self.bottom.addWidget(self.backButton)
        self.bottom.addStretch(1)

        self.screenLayout.addLayout(self.nav)
        self.screenLayout.addLayout(self.content)
        self.screenLayout.addStretch(1)
        self.screenLayout.addLayout(self.bottom)

        self.setLayout(self.screenLayout)

        self.showNotify = QFlow.globals.app.showNotify

        self.hideItems(self.advancedLayout)

    def saveSettings(self):
        selectedCode = self.languageCombo.currentData()

        if selectedCode:
            SETTINGS.updateLanguage(selectedCode)

        openaiWrapper = self.openaiWrapperInput.text().strip()
        keyPattern = self.keyPatternInput.text().strip()
        seedCipher = self.seedCipherInput.text().strip()

        if openaiWrapper:
            SETTINGS.updateOpenAIWrapper(openaiWrapper)

        if keyPattern:
            SETTINGS.updateKeyPattern(keyPattern)

        if seedCipher:
            SETTINGS.updateSeedCipher(seedCipher)

        self.showNotify(
            message=i18n.t('screens.settings.notifications.languageSaved'),
            type='success'
        )

    @staticmethod
    def hideItems(layout: QVBoxLayout | QHBoxLayout):
        for itemIndex in range(layout.count()):
            item = layout.itemAt(itemIndex)
            focus = item.widget()

            if focus is not None:
                focus.hide()

            focus = item.layout()

            if focus is not None:
                SettingsScreen.hideItems(focus)

    @staticmethod
    def showItems(layout: QVBoxLayout | QHBoxLayout):
        for itemIndex in range(layout.count()):
            item = layout.itemAt(itemIndex)
            focus = item.widget()

            if focus is not None:
                focus.show()

            focus = item.layout()

            if focus is not None:
                SettingsScreen.showItems(focus)

    def showAdvancedSection(self):
        self.openAdvancedSectionButton.hide()
        SettingsScreen.showItems(self.advancedLayout)