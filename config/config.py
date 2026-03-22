from helpers import JSONFile, Folder
import os

class Config:
    def __init__(self):
        self.ConfigFile= JSONFile(r'config/config.json')

        self.CONFIG = self.ConfigFile.read()
        
        self.folders = {
            'styles': Config._loadFolderFiles(
                Folder(self.CONFIG['app']['folders']['styles']).list_files()
            ),
            'configs': {
                'windows': Config._loadFolderFiles(
                    Folder(self.CONFIG['app']['folders']['configs']['windows']).list_files()
                ),
                'screens': Config._loadFolderFiles(
                    Folder(self.CONFIG['app']['folders']['configs']['screens']).list_files()
                )
            }
        }
    
    # Resolve paths using names
    def _loadFolderFiles(items: list) -> dict:
        files = {}

        # Insert name instead name + suffix
        for item in items:
            item: str
            name, _ = os.path.splitext(os.path.basename(item))

            files[name] = item

        return files

# Global config
CONFIG = Config()
'Application Inherent Configuration.'