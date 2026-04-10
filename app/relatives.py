from helpers.files import JSON
from helpers.obfuscation import Cipher

class Relatives:
    def __init__(self):
        self.RelativesFile= JSON(r'app/relatives.json')
        'Application inherent configuration.'

        self.prompt = open(self.RelativesFile.get('files')['prompt-file'], encoding='utf-8').read()
        'AI Prompt.'

        self.SEEDCIPHER = self.RelativesFile.get('auth')['s-chiper']
        'Seed IC Key Cipher.'

        self.LANGUAGE = self.RelativesFile.get('gui')['language']
        'Application language.'

        self.CIPHER: Cipher = Cipher(self.SEEDCIPHER)
        'IC Key Cipher.'

RELATIVES = Relatives()
'Application Relative Configuration.'