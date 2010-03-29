

class Config(object):
    def __init__(self, vars):
        self.__dict__.update(vars)


# python stuff
dirs = {
    'site': 'site',
    'source': 'source',
    'build_lib': 'build/lib',
    'build_scripts': 'builds/scripts',
}

for name in dirs:
    globals()['pytest_funcarg__' + name] = lambda request, name=name: getattr(request.getfuncargvalue('config'), name)


def pytest_funcarg__config(request):
    tmpdir = request.getfuncargvalue('tmpdir')

    paths = {}
    for name, subdir in dirs.items():
        paths[name] = tmpdir.ensure(subdir, dir=1)

    contents = getattr(request.function, 'has_source', None)
    if contents is not None:
        for name, content in contents.args[0].iteritems():
            file = paths['source'].ensure(name)
            file.write(content)

    return Config(paths)
