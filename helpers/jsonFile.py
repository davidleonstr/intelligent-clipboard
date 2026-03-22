import json
import os
from typing import Any, Dict, List

class JSONFile:
    """
    Class to manage JSON files easily.
    Allows reading, writing, editing, and manipulating JSON files.
    """
    
    def __init__(self, filepath: str):
        """
        Initialize the JSON manager.
        
        Args:
            filepath: Path to the JSON file
        """
        self.filepath = filepath
        self.data = None
    
    def read(self) -> Dict[str, Any]:
        """
        Read the JSON file and return its content.
        
        Returns:
            Dictionary with the JSON content
        
        Raises:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file is not a valid JSON
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{self.filepath}' does not exist")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON: {e}", e.doc, e.pos)
    
    def write(self, data: Dict[str, Any], indent: int = 4) -> None:
        """
        Write data to the JSON file.
        
        Args:
            data: Data to write to the file
            indent: Indentation spaces (default: 4)
        """
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        self.data = data
    
    def create(self, data: Dict[str, Any] = None, indent: int = 4) -> None:
        """
        Create a new JSON file.
        
        Args:
            data: Initial data (default: empty dictionary)
            indent: Indentation spaces (default: 4)
        """
        if data is None:
            data = {}
        self.write(data, indent)
    
    def update(self, key: str, value: Any) -> None:
        """
        Update or add a value in the JSON.
        
        Args:
            key: Key to update/add
            value: Value to assign
        """
        if self.data is None:
            self.read()
        self.data[key] = value
        self.write(self.data)
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from the JSON.
        
        Args:
            key: Key to delete
        
        Returns:
            True if deleted, False if the key did not exist
        """
        if self.data is None:
            self.read()
        if key in self.data:
            del self.data[key]
            self.write(self.data)
            return True
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the JSON.
        
        Args:
            key: Key to search for
            default: Default value if the key does not exist
        
        Returns:
            Value associated with the key or default
        """
        if self.data is None:
            self.read()
        return self.data.get(key, default)
    
    def exists(self) -> bool:
        """
        Check if the JSON file exists.
        
        Returns:
            True if it exists, False otherwise
        """
        return os.path.exists(self.filepath)
    
    def keys(self) -> List[str]:
        """
        Return all keys from the JSON.
        
        Returns:
            List of keys
        """
        if self.data is None:
            self.read()
        return list(self.data.keys())
    
    def values(self) -> List[Any]:
        """
        Return all values from the JSON.
        
        Returns:
            List of values
        """
        if self.data is None:
            self.read()
        return list(self.data.values())
    
    def items(self) -> List[tuple]:
        """
        Return key-value pairs from the JSON.
        
        Returns:
            List of tuples (key, value)
        """
        if self.data is None:
            self.read()
        return list(self.data.items())
    
    def merge(self, new_data: Dict[str, Any]) -> None:
        """
        Merge new data with existing data.
        
        Args:
            new_data: Dictionary with new data
        """
        if self.data is None:
            self.read()
        self.data.update(new_data)
        self.write(self.data)
    
    def clear(self) -> None:
        """
        Clear all content from the JSON (leaves an empty dictionary).
        """
        self.data = {}
        self.write(self.data)
    
    def reload(self) -> Dict[str, Any]:
        """
        Reload the JSON file from disk.
        
        Returns:
            Updated data from the file
        """
        return self.read()