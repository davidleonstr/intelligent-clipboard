from qtpy.QtCore import QObject, Slot
from typing import Callable

class Bridge(QObject):
    'Bridge between QWebEngineView and Python.'
    def __init__(self):
        super().__init__()

        self.functions = {}
        'List of functions.'

    def add(self, name: str, callable: Callable):
        'Add a function to the brigde.'
        self.functions[name] = callable
    
    def delete(self, name: str):
        'Delete a function to the brigde.'
        del self.functions[name]

    @Slot(str)
    def execute(self, name: str):
        'Execute a function. (JS Available).'
        self.functions[name]()