from helpers.files import JSON, listNames
from helpers.builders import Folder
import copy

class Config:
    def __init__(self):
        self.file = JSON(r'config/config.json')
        'Global configuration file.'

        self.CONFIG = self.file.read()
        'Global configuration dict.'

        self.folders = copy.deepcopy(self.CONFIG['app']['folders'])
        'Dict that contains global styles and configurations of windows and screens.'

        self.loadNormalFolder('configs')
        self.loadNormalFolder('icons')
        self.loadNormalFolder('styles')
        self.loadLocales()
        'Load everything.'
    
    def tree(self, *args):
        'Function to go into folders.'
        cursor = self.folders

        for path in args:
            cursor = cursor[path]
   
        return cursor

    def loadLocales(self) -> None:
        languages = Folder(self.folders['locales']['path']).listFolders()

        bases: dict = self.folders['locales']['base']
        path: str = self.folders['locales']['path']

        for language in languages:
            self.folders['locales']['languages'][language] = {}
            
            for key, value in bases.items():
                items = listNames(
                    Folder(
                        f'{path}{language}{value}'
                    ).listFiles()
                )

                self.folders['locales']['languages'][language][key] = items

    def loadNormalFolder(self, name: str) -> None:
        bases: dict = self.folders[name]['base']
        path: str = self.folders[name]['path']

        for key, value in bases.items():
            self.folders[name]['files'][key] = {}

            items = listNames(
                Folder(
                    f'{path}{value}'
                ).listFiles()
            )

            self.folders[name]['files'][key] = items

CONFIG = Config()
'Application Inherent Configuration.'