from pu.tasks.util import TaskBase

class CopyModulesToBuild(TaskBase):
    keys = 'source', 'build_lib'

    def __call__(self):
        self.build_lib.ensure(dir=1)
        for module in self.source.visit('*.py'):
            #XXX: grab from packages finder
            target = self.build_lib.join(module.relto(self.source))
            target.dirpath().ensure(dir=1)
            target.write(module.read())


class CompileByteCode(TaskBase):
    """
    compiles all python files below the target directory
    uses the optimizer settings of the current interpreter

    .. warning::

        ignores `sys.dont_write_bytecode`
    """
    keys = 'build_lib',

    def __call__(self):
        from py_compile import compile
        for x in self.build_lib.visit('*.py'):
            compile(str(x))



