from helpers.files import JSON
from helpers.obfuscation import Cipher

import base64

class Relatives:
    def __init__(self):
        self.file= JSON(r'app/relatives.json')
        'Application inherent configuration.'

        self.PROMPT = open(self.file.get('files')['prompt-file'], encoding='utf-8').read()
        'AI Prompt.'

        self.SEEDCIPHER = self.file.get('auth')['s-chiper']
        'Seed IC Key Cipher.'

        self.KEYPATTERN = self.file.get('auth')['ic-key-pattern']
        'IC Key validation pattern.'

        self.KEYCOMBINATION = self.file.get('keyboard')['key-combination']
        'Keyboard hotkey to use AI.'

        self.LANGUAGE = self.file.get('gui')['language']
        'Application language.'

        self.CIPHER: Cipher = Cipher(self.SEEDCIPHER)
        'IC Key Cipher.'

        self.ICKEY = self.file.get('ic-key', None)
        'IC Key.'

        self.OPENAIWRAPPER = self.file.get('ic-openai-wrapper')
        'API ENDPOINT.'

    def updateKey(self, key: str):
        if not key:
            self.file.update('ic-key', None) 
            return

        encKey = self.encryptKey(key)

        self.file.update(
            'ic-key', 
            encKey
        )

        self.ICKEY = encKey
    
    def encryptKey(self, key: str) -> str:
        return base64.b64encode(
            self.CIPHER.encrypt(key)
        ).decode('utf-8')

    def decryptKey(self, key: str) -> str:
        return self.CIPHER.decrypt(
        base64.b64decode(
            key
            )
        )

RELATIVES = Relatives()
'Application Relative Configuration.'