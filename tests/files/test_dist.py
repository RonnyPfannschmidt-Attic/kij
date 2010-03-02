import py
from kij.files.dist import DistFile, DistFileError


def pytest_funcarg__distfile(request):
    return request.getfuncargvalue('tmpdir').join('test-kij.yml')


def pytest_funcarg__distfilegen(request):
    distfile = request.getfuncargvalue('distfile')

    def _create_file(s, distfile=distfile):
        f = distfile.open('w')
        f.write(s)
        f.close()
        return DistFile(distfile)
    return _create_file


d = """
name: Kij
summary: Python packaging utilities
packages:
    - anyvc.*
"""


def test_name(distfilegen):
    df = distfilegen(d)
    assert df.name == 'Kij'

e = """
packages:
    - anyvc.*
"""


def test_missing_name(distfilegen):
    py.test.raises(DistFileError, distfilegen, e)


def test_summary(distfilegen):
    df = distfilegen(d)
    assert df.summary == 'Python packaging utilities'


def test_packages(distfilegen):
    df = distfilegen(d)
    assert df.packages[0] == 'anyvc.*'
    assert len(df.packages) == 1


f = """
name: banana
"""


def test_missing_packages_ok(distfilegen):
    df = distfilegen(f)
    assert df.packages is None


g = """
name: banana
packages: manana
"""


def test_bad_packages(distfilegen):
    py.test.raises(DistFileError, distfilegen, g)
