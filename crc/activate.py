import os
import sys
from importlib.machinery import SourcelessFileLoader

import transpiler

class CRCLoader(SourcelessFileLoader):
  
  def get_code(self, fullname):
    with open(self.path) as f:
      ast = transpiler.translate(f.read())
      return compile(ast, self.path, 'exec')


class CacheProxy:

  def __init__(self, cache):
    self._cache = cache
    self._cachecls = type(cache)

  def __setitem__(self, key, value):
    """Enforces the new paths support *.crc compilation"""
    value._loaders.append(('.crc', CRCLoader))
    return self._cachecls.__setitem__(self._cache, key, value)

  def __getitem__(self, key):
    return self._cachecls.__getitem__(self._cache, key)

  def __getattr__(self, key):
    return object.__getattribute__(self._cache, key)

def _install():
  sys.path_importer_cache = CacheProxy(sys.path_importer_cache)

_install()