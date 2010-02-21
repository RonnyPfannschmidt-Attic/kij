from pu.tasks.install import LinkPTH, UnlinkPTH
from pu.files.pth import PthFile

def pytest_funcarg__site(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('site', dir=True)

def pytest_funcarg__source(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.ensure('source', dir=True)


def test_enable(site, source):
    task = LinkPTH(site, source)
    assert not site.join(task.pth_name).check()
    task.run()
    assert site.join(task.pth_name).check()

def test_disable(site, source):
    test_enable(site, source)

    task = UnlinkPTH(site, source)

    pth = PthFile(site.join(task.pth_name))
    assert source in pth.entries

    task.run()

    pth = PthFile(site.join(task.pth_name))
    assert source not in pth.entries

