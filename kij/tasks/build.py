from kij.tasks.util import TaskBase
from kij.tasks.metadata import FindPackages, ReadYamlMetadata

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


class CopyScripts(TaskBase):
    #XXX: fix shebangs
    keys = 'source', 'build_scripts'
    scripts = None
    requirements = ReadYamlMetadata,

    def on_readyamlmetadata_success(self, item):
        self.scripts = item.result.scripts or ()

    def __call__(self):
        self.build_scripts.ensure(dir=True)
        for script in self.scripts:
            script = self.source.join(script)
            print script
            #XXX: better error
            assert script.check(file=1), 'script %s missing'%script
            script.copy(target=self.build_scripts.join(script.basename))


class Build(TaskBase):
    keys = 'source', 'build_scripts', 'build_lib'
    requirements = CopyScripts, CompileByteCode, CopyScripts

    def __call__(self):
        pass
