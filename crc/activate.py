from importlib.machinery import SourcelessFileLoader, SourceFileLoader
# noinspection PyUnresolvedReferences
import abm.activate
from abm.loaders import AbmLoader
from . import transpiler


class CRCLoader(AbmLoader, SourceFileLoader):
    """The CRCLoader loads the contents of a .crc file and compile it to the
    proper backend.
    """

    extensions = ('.crc', )

    def source_to_code(self, data, path, *, _optimize=-1):
        source = data.decode('utf-8')
        ast = transpiler.translate(source)
        return super().source_to_code(ast, path, _optimize=_optimize)


CRCLoader.register()
