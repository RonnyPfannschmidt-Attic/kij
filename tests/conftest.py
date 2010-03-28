
from sanescript.config import Config

from kij.commands import kij_script


# python stuff
dirs = {
    'site': 'site',
    'source': 'source',
    'build_lib': 'build/lib',
    'build_scripts': 'builds/scripts',
}

for name in dirs:
    globals()['pytest_funcarg__' + name] = lambda request, name=name: getattr(request.getfuncargvalue('config'), name)


def pytest_funcarg__fullsource(request):
    source = request.getfuncargvalue('config').source
    source.join('kij.yml').write(
            'name: test\n'
            'scripts: [foo, bin/bar]\n'
            'packages: [testpkg]\n'
            )
    source.ensure('foo')
    source.ensure('bin/bar')
    source.ensure('testpkg/__init__.py')
    return source

def pytest_funcarg__config(request):
    tmpdir = request.getfuncargvalue('tmpdir')

    paths = {}
    for name, subdir in dirs.items():
        paths[name] = tmpdir.ensure(subdir, dir=1)

    config = Config()
    config.grab_from_dict(paths)
    return config

def pytest_funcarg__script(request):
    config = request.getfuncargvalue('config')
    kij_script._config.grab_from_ns(config)
    return kij_script

