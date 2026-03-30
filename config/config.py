from helpers.files import JSON
from helpers.builders import Folder
import os

class Config:
    def __init__(self):
        self.ConfigFile= JSON(r'config/config.json')
        'Global configuration file.'

        self.CONFIG = self.ConfigFile.read()
        'Global configuration dict.'
        
        self.folders = {
            'styles': Config.loadFolderFiles(
                Folder(self.CONFIG['app']['folders']['styles']).listFiles()
            ),
            'configs': {
                'windows': Config.loadFolderFiles(
                    Folder(self.CONFIG['app']['folders']['configs']['windows']).listFiles()
                ),
                'screens': Config.loadFolderFiles(
                    Folder(self.CONFIG['app']['folders']['configs']['screens']).listFiles()
                )
            },
            'icons': Config.loadFolderFiles(
                Folder(self.CONFIG['app']['folders']['icons']).listFiles()
            )
        }
        'Dict that contains global styles and configurations of windows and screens.'
    
    def loadFolderFiles(items: list) -> dict:
        files = {}

        for item in items:
            item: str
            name, _ = os.path.splitext(os.path.basename(item))

            files[name] = item

        return files

CONFIG = Config()
'Application Inherent Configuration.'