from pu.tasks.util import TaskBase
from pu.tasks.metadata import FindPackages

import logging
log = logging.getLogger('kij.build')

class CopySinglePackageToBuild(TaskBase):
    keys = 'source', 'build_lib', 'package'

    def __call__(self):
        elem = self.package.split('.')
        source_pkg = self.source.join(*elem)
        build_pkg = self.build_lib.join(*elem).ensure(dir=1)
        for src in source_pkg.listdir('*.py'):
            src.copy(build_pkg.join(src.basename))


class CopyPackagesToBuild(TaskBase):
    keys = 'source', 'build_lib'
    requirements = FindPackages,

    def on_findpackages_success(self, task):
        print 'found packages', task.result
        for pkg in task.result:
            task = CopySinglePackageToBuild(
                    source=self.source,
                    build_lib=self.build_lib,
                    package=pkg,
                    )
            self.queue.append(task)

    def __call__(self):
        pass


class CompileByteCode(TaskBase):
    """
    compiles all python files below the target directory
    uses the optimizer settings of the current interpreter

    .. warning::

        ignores `sys.dont_write_bytecode`
    """
    keys = 'build_lib',
    requirements = CopyPackagesToBuild,

    def __call__(self):
        from py_compile import compile
        for x in self.build_lib.visit('*.py'):
            compile(str(x))
