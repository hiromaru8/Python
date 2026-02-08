import json
from pathlib import Path


class Config:
    def __init__(self, path):
        self._data = self._load(path)

    @staticmethod
    def _load(path):
        with open(Path(path), encoding="utf-8") as f:
            return json.load(f)

    def get(self, key, default=None):
        return self._data.get(key, default)
