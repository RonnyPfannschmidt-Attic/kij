from sanescript.config import Config

def pytest_funcarg__site(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('site', dir=True)

def pytest_funcarg__source(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('source', dir=True)

def pytest_funcarg__config(request):
    source = request.getfuncargvalue('source');
    site = request.getfuncargvalue('site')
    config = Config()
    config.grab_from_dict(dict(
            site=site,
            source=source,
            ))
    return config
