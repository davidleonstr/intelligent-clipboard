import os

def listNames(items: list) -> dict:
    'That function makes a dictionary with file names as key and file path as value.'
    files = {}

    for item in items:
        item: str
        name, _ = os.path.splitext(os.path.basename(item))

        files[name] = item

    return files