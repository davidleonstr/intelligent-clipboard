from helpers import JSONFile, SeedCipher

class Relatives:
    def __init__(self):
        self.RelativesFile= JSONFile(r'app/relatives.json')
        'Application inherent configuration.'

        self.prompt = open(self.RelativesFile.get('files')['prompt-file'], encoding='utf-8').read()
        'AI Prompt.'

        self.SCIPHER = self.RelativesFile.get('auth')['s-chiper']
        'Seed IC Key Cipher.'

        self.CIPHER: SeedCipher = SeedCipher(self.SCIPHER)
        'IC Key Cipher.'

RELATIVES = Relatives()
'Application Relative Configuration.'