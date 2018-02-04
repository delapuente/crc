import os
import sys
from importlib.machinery import SourcelessFileLoader

from . import transpiler

class CRCLoader(SourcelessFileLoader):
  
  def get_code(self, fullname):
    with open(self.path) as f:
      ast = transpiler.translate(f.read())
      return compile(ast, self.path, 'exec')

class CacheProxy:

  def __init__(self, cache):
    self._cache = cache
    self._cachecls = type(cache)

  def __setitem__(self, key, finder):
    """Enforces the new paths support *.crc compilation"""
    _ensureCrc(finder)
    return self._cachecls.__setitem__(self._cache, key, finder)

  def __getitem__(self, key):
    finder = self._cachecls.__getitem__(self._cache, key)
    return _ensureCrc(finder)

  def __getattr__(self, key):
    return object.__getattribute__(self._cache, key)

def _ensureCrc(fileFinder):
  if (fileFinder and not _isCrcEnabled(fileFinder)):
    fileFinder._loaders.append(('.crc', CRCLoader))

  return fileFinder

def _isCrcEnabled(fileFinder):
  if fileFinder:
    for ext, _ in fileFinder._loaders:
      if ext == '.crc':
        return True

  return False

def _install():
  sys.path_importer_cache = CacheProxy(sys.path_importer_cache)

_install()