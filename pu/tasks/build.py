

class CopyModulesToBuild(object):
    def __init__(self, source, build_lib):
        self.source = source
        self.build_lib = build_lib


    def __call__(self):
        self.build_lib.ensure(dir=1)
        for module in self.source.visit('*.py'):
            #XXX: grab from packages finder
            target = self.build_lib.join(module.relto(self.source))
            target.dirpath().ensure(dir=1)
            target.write(module.read())




class CompileByteCode(object):
    def __init__(self, build_lib):
        self.build_lib = build_lib

    def __call__(self):
        for x in self.build_lib.visit('*.py'):
            x.new(ext='.pyc').ensure() #XXX: actually compile
