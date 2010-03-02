import py
from kij.files.pth import PthFile


def pytest_funcarg__pthfile(request):
    return request.getfuncargvalue('tmpdir').join('test.pth')


def pytest_funcarg__pth(request):
    return PthFile(request.getfuncargvalue('pthfile'))


def pytest_funcarg__item(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('test-1.3.zip')


def test_instanciate(tmpdir):
    PthFile(tmpdir.join('test.pthfail'))


def test_create_pth(tmpdir):
    file = tmpdir.join('test.pth')
    pth = PthFile(file)
    assert not pth.entries


def test_append(pth, tmpdir, item):

    pth.append(item)
    assert pth.entries == [item]

    # dont get double entries
    pth.append(item)
    assert pth.entries == [item]


def test_remove(pth, tmpdir, item):

    pth.append(item)
    assert pth.entries == [item]

    # dont get double entries
    pth.remove(item)
    assert pth.entries == []


def test_save_relative(pth, pthfile, tmpdir, item):
    pth.append(item)
    pth.save()
    assert pthfile.read() == './test-1.3.zip\n'


def test_save_absolute(pth, pthfile):
    pth.append(py.path.local('/usr/local/lib'))
    pth.save()
    assert pthfile.read() == '/usr/local/lib\n'


def test_parse_relative(pthfile, item):
    pthfile.write('./test-1.3.zip')
    pth = PthFile(pthfile)
    assert pth.entries == [item]


def test_parse_absolute(pthfile):
    pthfile.write('/usr/local/bin/test')
    pth = PthFile(pthfile)
    assert pth.entries == ['/usr/local/bin/test']
