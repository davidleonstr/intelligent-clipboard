import os
import shutil
from typing import List, Optional
from pathlib import Path
import fnmatch

class Folder:
    '''
    Class to manage folders easily.
    Allows creating, deleting, copying, moving, and listing folder contents.
    '''
    
    def __init__(self, folderpath: str):
        '''
        Initialize the folder manager.
        
        Args:
            folderpath: Path to the folder
        '''
        self.folderpath = folderpath
        self.path = Path(folderpath)
    
    def create(self, existOk: bool = True) -> None:
        '''
        Create the folder.
        
        Args:
            existOk: If True, don't raise error if folder already exists
        
        Raises:
            FileExistsError: If folder exists and existOk is False
        '''
        try:
            os.makedirs(self.folderpath, existOk=existOk)
        except FileExistsError:
            raise FileExistsError(f"Folder '{self.folderpath}' already exists")
    
    def delete(self, confirm: bool = False) -> bool:
        '''
        Delete the folder and all its contents.
        
        Args:
            confirm: Safety flag to confirm deletion
        
        Returns:
            True if deleted, False if folder doesn't exist
        
        Raises:
            ValueError: If confirm is False (safety measure)
        '''
        if not confirm:
            raise ValueError("Must set confirm=True to delete folder")
        
        if self.exists():
            shutil.rmtree(self.folderpath)
            return True
        return False
    
    def exists(self) -> bool:
        '''
        Check if the folder exists.
        
        Returns:
            True if exists, False otherwise
        '''
        return os.path.exists(self.folderpath) and os.path.isdir(self.folderpath)
    
    def isEmpty(self) -> bool:
        '''
        Check if the folder is empty.
        
        Returns:
            True if empty, False otherwise
        
        Raises:
            FileNotFoundError: If folder doesn't exist
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        return len(os.listdir(self.folderpath)) == 0
    
    def listContents(self, pattern: Optional[str] = None, recursive: bool = False) -> List[str]:
        '''
        List contents of the folder.
        
        Args:
            pattern: Optional pattern to filter files (e.g., "*.txt")
            recursive: If True, list contents recursively
        
        Returns:
            List of file/folder names
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        if recursive:
            contents = []
            for root, dirs, files in os.walk(self.folderpath):
                for item in dirs + files:
                    fullPath = os.path.join(root, item)
                    relPath = os.path.relpath(fullPath, self.folderpath)
                    if pattern is None or fnmatch.fnmatch(item, pattern):
                        contents.append(relPath)
            return contents
        else:
            contents = os.listdir(self.folderpath)
            if pattern:
                contents = [item for item in contents if fnmatch.fnmatch(item, pattern)]
            return contents
    
    def listFiles(self, pattern: Optional[str] = None, recursive: bool = False) -> List[str]:
        '''
        List only files in the folder.
        
        Args:
            pattern: Optional pattern to filter files (e.g., "*.txt")
            recursive: If True, list files recursively
        
        Returns:
            List of absolute file paths
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        files = []
        if recursive:
            for root, _, filenames in os.walk(self.folderpath):
                for filename in filenames:
                    if pattern is None or fnmatch.fnmatch(filename, pattern):
                        fullPath = os.path.join(root, filename)
                        files.append(os.path.abspath(fullPath))
        else:
            for item in os.listdir(self.folderpath):
                itemPath = os.path.join(self.folderpath, item)
                if os.path.isfile(itemPath):
                    if pattern is None or fnmatch.fnmatch(item, pattern):
                        files.append(os.path.abspath(itemPath))
        
        return files
    
    def listFolders(self, recursive: bool = False) -> List[str]:
        '''
        List only subfolders in the folder.
        
        Args:
            recursive: If True, list folders recursively
        
        Returns:
            List of folder names
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        folders = []
        if recursive:
            for root, dirnames, _ in os.walk(self.folderpath):
                for dirname in dirnames:
                    fullPath = os.path.join(root, dirname)
                    relPath = os.path.relpath(fullPath, self.folderpath)
                    folders.append(relPath)
        else:
            for item in os.listdir(self.folderpath):
                itemPath = os.path.join(self.folderpath, item)
                if os.path.isdir(itemPath):
                    folders.append(item)
        return folders
    
    def copyTo(self, destination: str) -> None:
        '''
        Copy the folder to a new location.
        
        Args:
            destination: Destination path
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        shutil.copytree(self.folderpath, destination)
    
    def moveTo(self, destination: str) -> None:
        '''
        Move the folder to a new location.
        
        Args:
            destination: Destination path
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        shutil.move(self.folderpath, destination)
        self.folderpath = destination
        self.path = Path(destination)
    
    def rename(self, newName: str) -> None:
        '''
        Rename the folder.
        
        Args:
            newName: New folder name
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        parent = os.path.dirname(self.folderpath)
        newPath = os.path.join(parent, newName)
        os.rename(self.folderpath, newPath)
        self.folderpath = newPath
        self.path = Path(newPath)
    
    def getSize(self) -> int:
        '''
        Get total size of the folder in bytes.
        
        Returns:
            Size in bytes
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        totalSize = 0
        for dirpath, dirnames, filenames in os.walk(self.folderpath):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    totalSize += os.path.getsize(filepath)
        return totalSize
    
    def getSizeFormatted(self) -> str:
        '''
        Get total size of the folder in human-readable format.
        
        Returns:
            Size as formatted string (e.g., "1.5 MB")
        '''
        size = self.getSize()
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def countItems(self, recursive: bool = False) -> dict:
        '''
        Count files and folders.
        
        Args:
            recursive: If True, count recursively
        
        Returns:
            Dictionary with 'files' and 'folders' counts
        '''
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        fileCount = 0
        folderCount = 0
        
        if recursive:
            for root, dirs, files in os.walk(self.folderpath):
                fileCount += len(files)
                folderCount += len(dirs)
        else:
            for item in os.listdir(self.folderpath):
                itemPath = os.path.join(self.folderpath, item)
                if os.path.isfile(itemPath):
                    fileCount += 1
                elif os.path.isdir(itemPath):
                    folderCount += 1
        
        return {'files': fileCount, 'folders': folderCount}
    
    def createSubfolder(self, subfolderName: str) -> 'Folder':
        '''
        Create a subfolder inside this folder.
        
        Args:
            subfolderName: Name of the subfolder
        
        Returns:
            Folder instance for the new subfolder
        '''
        subfolderPath = os.path.join(self.folderpath, subfolderName)
        subfolder = Folder(subfolderPath)
        subfolder.create()
        return subfolder
    
    def clear(self, confirm: bool = False) -> None:
        '''
        Delete all contents of the folder but keep the folder itself.
        
        Args:
            confirm: Safety flag to confirm clearing
        
        Raises:
            ValueError: If confirm is False (safety measure)
        '''
        if not confirm:
            raise ValueError("Must set confirm=True to clear folder")
        
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        for item in os.listdir(self.folderpath):
            itemPath = os.path.join(self.folderpath, item)
            if os.path.isfile(itemPath):
                os.remove(itemPath)
            elif os.path.isdir(itemPath):
                shutil.rmtree(itemPath)