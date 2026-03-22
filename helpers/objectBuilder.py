from types import SimpleNamespace

class ObjectBuilder:
    """Class to create an object using a dictionary."""
    def __init__(self, data: dict):
        self.obj = self._to_namespace(data)

    def _to_namespace(self, data):
        if isinstance(data, dict):
            return SimpleNamespace(**{k: self._to_namespace(v) for k, v in data.items()})
        elif isinstance(data, list):
            return [self._to_namespace(item) for item in data]
        else:
            return data