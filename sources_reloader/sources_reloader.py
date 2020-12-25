import hashlib
import importlib
import io
from types import ModuleType


class SourcesReloader:

    def __init__(self):
        self._sources = {}

    @classmethod
    def _calculate_hash(cls, file_path):
        sha_hash = hashlib.sha256()
        with io.open(file_path, 'rb') as source_code:
            for chunk in iter(lambda: source_code.read(4096), b''):
                sha_hash.update(chunk)

        return sha_hash.hexdigest()

    def _update_hashes(self, module):
        hexdigest = self._calculate_hash(module.__file__)
        if self._sources[module.__file__] != hexdigest:
            self._sources[module.__file__] = hexdigest
            setattr(self, module.__name__, importlib.reload(module))

    def __setattr__(self, key, value):
        if isinstance(value, ModuleType):
            self._sources[value.__file__] = self._calculate_hash(value.__file__)

        super().__setattr__(key, value)

    def __getattribute__(self, attr):
        value = super().__getattribute__(attr)
        if not isinstance(value, ModuleType):
            return value

        self._update_hashes(value)

        return super().__getattribute__(attr)
