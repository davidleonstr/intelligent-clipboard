import os
import shutil
from typing import List, Optional
from pathlib import Path
import fnmatch

class Folder:
    """
    Class to manage folders easily.
    Allows creating, deleting, copying, moving, and listing folder contents.
    """
    
    def __init__(self, folderpath: str):
        """
        Initialize the folder manager.
        
        Args:
            folderpath: Path to the folder
        """
        self.folderpath = folderpath
        self.path = Path(folderpath)
    
    def create(self, exist_ok: bool = True) -> None:
        """
        Create the folder.
        
        Args:
            exist_ok: If True, don't raise error if folder already exists
        
        Raises:
            FileExistsError: If folder exists and exist_ok is False
        """
        try:
            os.makedirs(self.folderpath, exist_ok=exist_ok)
        except FileExistsError:
            raise FileExistsError(f"Folder '{self.folderpath}' already exists")
    
    def delete(self, confirm: bool = False) -> bool:
        """
        Delete the folder and all its contents.
        
        Args:
            confirm: Safety flag to confirm deletion
        
        Returns:
            True if deleted, False if folder doesn't exist
        
        Raises:
            ValueError: If confirm is False (safety measure)
        """
        if not confirm:
            raise ValueError("Must set confirm=True to delete folder")
        
        if self.exists():
            shutil.rmtree(self.folderpath)
            return True
        return False
    
    def exists(self) -> bool:
        """
        Check if the folder exists.
        
        Returns:
            True if exists, False otherwise
        """
        return os.path.exists(self.folderpath) and os.path.isdir(self.folderpath)
    
    def is_empty(self) -> bool:
        """
        Check if the folder is empty.
        
        Returns:
            True if empty, False otherwise
        
        Raises:
            FileNotFoundError: If folder doesn't exist
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        return len(os.listdir(self.folderpath)) == 0
    
    def list_contents(self, pattern: Optional[str] = None, recursive: bool = False) -> List[str]:
        """
        List contents of the folder.
        
        Args:
            pattern: Optional pattern to filter files (e.g., "*.txt")
            recursive: If True, list contents recursively
        
        Returns:
            List of file/folder names
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        if recursive:
            contents = []
            for root, dirs, files in os.walk(self.folderpath):
                for item in dirs + files:
                    full_path = os.path.join(root, item)
                    rel_path = os.path.relpath(full_path, self.folderpath)
                    if pattern is None or fnmatch.fnmatch(item, pattern):
                        contents.append(rel_path)
            return contents
        else:
            contents = os.listdir(self.folderpath)
            if pattern:
                contents = [item for item in contents if fnmatch.fnmatch(item, pattern)]
            return contents
    
    def list_files(self, pattern: Optional[str] = None, recursive: bool = False) -> List[str]:
        """
        List only files in the folder.
        
        Args:
            pattern: Optional pattern to filter files (e.g., "*.txt")
            recursive: If True, list files recursively
        
        Returns:
            List of absolute file paths
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        files = []
        if recursive:
            for root, _, filenames in os.walk(self.folderpath):
                for filename in filenames:
                    if pattern is None or fnmatch.fnmatch(filename, pattern):
                        full_path = os.path.join(root, filename)
                        files.append(os.path.abspath(full_path))
        else:
            for item in os.listdir(self.folderpath):
                item_path = os.path.join(self.folderpath, item)
                if os.path.isfile(item_path):
                    if pattern is None or fnmatch.fnmatch(item, pattern):
                        files.append(os.path.abspath(item_path))
        
        return files
    
    def list_folders(self, recursive: bool = False) -> List[str]:
        """
        List only subfolders in the folder.
        
        Args:
            recursive: If True, list folders recursively
        
        Returns:
            List of folder names
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        folders = []
        if recursive:
            for root, dirnames, _ in os.walk(self.folderpath):
                for dirname in dirnames:
                    full_path = os.path.join(root, dirname)
                    rel_path = os.path.relpath(full_path, self.folderpath)
                    folders.append(rel_path)
        else:
            for item in os.listdir(self.folderpath):
                item_path = os.path.join(self.folderpath, item)
                if os.path.isdir(item_path):
                    folders.append(item)
        return folders
    
    def copy_to(self, destination: str) -> None:
        """
        Copy the folder to a new location.
        
        Args:
            destination: Destination path
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        shutil.copytree(self.folderpath, destination)
    
    def move_to(self, destination: str) -> None:
        """
        Move the folder to a new location.
        
        Args:
            destination: Destination path
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        shutil.move(self.folderpath, destination)
        self.folderpath = destination
        self.path = Path(destination)
    
    def rename(self, new_name: str) -> None:
        """
        Rename the folder.
        
        Args:
            new_name: New folder name
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        parent = os.path.dirname(self.folderpath)
        new_path = os.path.join(parent, new_name)
        os.rename(self.folderpath, new_path)
        self.folderpath = new_path
        self.path = Path(new_path)
    
    def get_size(self) -> int:
        """
        Get total size of the folder in bytes.
        
        Returns:
            Size in bytes
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.folderpath):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size
    
    def get_size_formatted(self) -> str:
        """
        Get total size of the folder in human-readable format.
        
        Returns:
            Size as formatted string (e.g., "1.5 MB")
        """
        size = self.get_size()
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def count_items(self, recursive: bool = False) -> dict:
        """
        Count files and folders.
        
        Args:
            recursive: If True, count recursively
        
        Returns:
            Dictionary with 'files' and 'folders' counts
        """
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        file_count = 0
        folder_count = 0
        
        if recursive:
            for root, dirs, files in os.walk(self.folderpath):
                file_count += len(files)
                folder_count += len(dirs)
        else:
            for item in os.listdir(self.folderpath):
                item_path = os.path.join(self.folderpath, item)
                if os.path.isfile(item_path):
                    file_count += 1
                elif os.path.isdir(item_path):
                    folder_count += 1
        
        return {'files': file_count, 'folders': folder_count}
    
    def create_subfolder(self, subfolder_name: str) -> 'Folder':
        """
        Create a subfolder inside this folder.
        
        Args:
            subfolder_name: Name of the subfolder
        
        Returns:
            Folder instance for the new subfolder
        """
        subfolder_path = os.path.join(self.folderpath, subfolder_name)
        subfolder = Folder(subfolder_path)
        subfolder.create()
        return subfolder
    
    def clear(self, confirm: bool = False) -> None:
        """
        Delete all contents of the folder but keep the folder itself.
        
        Args:
            confirm: Safety flag to confirm clearing
        
        Raises:
            ValueError: If confirm is False (safety measure)
        """
        if not confirm:
            raise ValueError("Must set confirm=True to clear folder")
        
        if not self.exists():
            raise FileNotFoundError(f"Folder '{self.folderpath}' does not exist")
        
        for item in os.listdir(self.folderpath):
            item_path = os.path.join(self.folderpath, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)