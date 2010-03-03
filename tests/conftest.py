
from sanescript.config import Config

from kij.commands import kij_script

def pytest_funcarg__site(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('site', dir=True)


def pytest_funcarg__source(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('source', dir=True)

def pytest_funcarg__fullsource(request):
    source = request.getfuncargvalue('source')
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
    source = request.getfuncargvalue('source')
    site = request.getfuncargvalue('site')
    config = Config()
    config.grab_from_dict(dict(
            site=site,
            source=source,
            source_directory=source,
            ))
    return config

def pytest_funcarg__script(request):
    config = request.getfuncargvalue('config')
    kij_script._config.grab_from_ns(config)
    return kij_script

