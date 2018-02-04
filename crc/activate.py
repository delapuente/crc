import os
import sys
from importlib.machinery import SourcelessFileLoader

from . import transpiler

class CacheProxy:
  """When Python is loading a module, it uses, the import system protocol:
  
    https://docs.python.org/3/reference/import.html

  The import system can be summarized in finding modules and loading modules.
  Finding a module consists into looking for it in several locations. Loading
  is actually executing the module. Finding a module returns a module spec
  object which includes the proper loader.

  One of the default finders is a local system finder. When asked for a module,
  it resolves the root folder of the module and delegates to a FileFinder
  object. This object tries the name of the module with different suffixes (file
  extensions) and selects the proper loader.

  Unfortunately, there is no API for supporting new loaders per extension.
  
  However, these FileFinder objects are cached in sys.path_importer_cache.
  
  The hack consists into wrapping the cache so any access intent gets
  intercepted and we can monkeypatch the list of loaders per extension to
  include the CRCLoader for the *.crc extension."""

  def __init__(self, cache):
    self._cache = cache
    self._cachecls = type(cache)

  def __setitem__(self, key, finder):
    """Enforces the new paths to support *.crc compilation"""
    _ensureCrc(finder)
    return self._cachecls.__setitem__(self._cache, key, finder)

  def __getitem__(self, key):
    """Enforces the old paths to support *.crc compilation"""
    finder = self._cachecls.__getitem__(self._cache, key)
    return _ensureCrc(finder)

  def __getattr__(self, key):
    return object.__getattribute__(self._cache, key)

class CRCLoader(SourcelessFileLoader):
  """The CRCLoader loads the contents of a .crc file and compile it to the
  proper backend."""
  
  def get_code(self, fullname):
    with open(self.path) as f:
      ast = transpiler.translate(f.read())
      return compile(ast, self.path, 'exec')

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