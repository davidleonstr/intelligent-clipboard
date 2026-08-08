from pathlib import Path
import base64
import json as pyjson
from typing import Dict

from QFlow.builders import JSON

from app.helpers.obfuscation import Cipher
from app.tree import FOLDERS, UNFROZEN

class Settings:
    def __init__(self):
        self.AUTH = JSON(FOLDERS.f[UNFROZEN, 'app', 'settings', 'auth.json'])
        self.GUI = JSON(FOLDERS.f[UNFROZEN, 'app', 'settings', 'gui.json'])
        self.IC = JSON(FOLDERS.f[UNFROZEN, 'app', 'settings', 'ic.json'])
        self.HOTKEYS = JSON(FOLDERS.f[UNFROZEN, 'app', 'settings', 'hotkeys.json'])

        self.SEEDCIPHER = self.AUTH.get('seed-chiper')
        self.LANGUAGE = self.GUI.get('language')
        self.KEYPATTERN = self.IC.get('ic-key-pattern')
        self.ICKEY = self.IC.get('ic-key')
        self.OPENAIWRAPPER = self.IC.get('ic-openai-wrapper')

        self.CIPHER: Cipher = Cipher(self.SEEDCIPHER)

        self.promptsFolder = Path(
            FOLDERS.f[UNFROZEN, 'app', 'settings', 'prompts']
        )

        self.hotkeysPath = Path(
            FOLDERS.f[UNFROZEN, 'app', 'settings', 'hotkeys.json']
        )

    def decryptKey(self, key: str) -> str:
        return self.CIPHER.decrypt(base64.b64decode(key))

    def encryptKey(self, key: str) -> str:
        return base64.b64encode(self.CIPHER.encrypt(key)).decode('utf-8')
    
    def updateKey(self, key: str) -> None:
        self.IC.update(
            'ic-key', 
            self.encryptKey(key) if key else None
        )
        
        self.ICKEY = self.IC.get('ic-key')

    def getHotkeys(self) -> Dict[str, str]:
        hotkeys = {}

        for hotkey, prompt in self.HOTKEYS.items():
            hotkeys[hotkey] = open(
                Path(
                    FOLDERS.f[UNFROZEN, 'app', 'settings', 'prompts', 'main.md']
                ).parent / prompt, 
                encoding='utf-8'
            ).read()

        return hotkeys

    @staticmethod
    def getLanguages() -> list:
        localesPath = Path(FOLDERS.f['app', 'locales'])
        return [p.name for p in localesPath.iterdir() if p.is_dir()]

    def updateLanguage(self, language: str) -> None:
        self.GUI.update('language', language)
        self.LANGUAGE = language

    def getPromptContent(self, hotkey: str) -> str:
        promptFilename = self.HOTKEYS.get(hotkey)

        try:
            return (self.promptsFolder / promptFilename).read_text(encoding='utf-8')
        except Exception:
            return ''

    def addHotkey(self, hotkey: str, promptFilename: str, promptContent: str) -> None:
        (self.promptsFolder / promptFilename).write_text(promptContent, encoding='utf-8')

        self.HOTKEYS.update(hotkey, promptFilename)
        self.reloadHotkeys()

    def updateHotkeyPrompt(self, hotkey: str, promptContent: str) -> None:
        promptFilename = self.HOTKEYS.get(hotkey)
        (self.promptsFolder / promptFilename).write_text(promptContent, encoding='utf-8')

    def renameHotkey(self, oldHotkey: str, newHotkey: str) -> None:
        promptFilename = self.HOTKEYS.get(oldHotkey)

        self.deleteHotkey(oldHotkey, removePromptFile=False)

        self.HOTKEYS.update(newHotkey, promptFilename)
        self.reloadHotkeys()

    def deleteHotkey(self, hotkey: str, removePromptFile: bool = True) -> None:
        data = pyjson.loads(self.hotkeysPath.read_text(encoding='utf-8'))
        promptFilename = data.pop(hotkey, None)

        self.hotkeysPath.write_text(pyjson.dumps(data, indent=4), encoding='utf-8')

        if removePromptFile and promptFilename:
            promptPath = self.promptsFolder / promptFilename
            if promptPath.exists():
                promptPath.unlink()

        self.reloadHotkeys()

    def reloadHotkeys(self) -> None:
        self.HOTKEYS = JSON(FOLDERS.f[UNFROZEN, 'app', 'settings', 'hotkeys.json'])

    def updateOpenAIWrapper(self, wrapper: str) -> None:
        self.IC.update('ic-openai-wrapper', wrapper)
        self.OPENAIWRAPPER = self.IC.get('ic-openai-wrapper')

    def updateKeyPattern(self, pattern: str) -> None:
        self.IC.update('ic-key-pattern', pattern)
        self.KEYPATTERN = self.IC.get('ic-key-pattern')

    def updateSeedCipher(self, seed: str) -> None:
        self.AUTH.update('seed-chiper', seed)
        self.SEEDCIPHER = self.AUTH.get('seed-chiper')
        self.CIPHER = Cipher(self.SEEDCIPHER)

SETTINGS = Settings()