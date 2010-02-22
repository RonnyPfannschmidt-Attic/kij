import py
from pu.tasks.metadata import FindPackages, find_packages

def test_find_packages(source):
    pkg = source.join('pkg')
    assert find_packages(source, pkg) == []

    source.ensure('pkg/__init__.py')
    assert find_packages(source, pkg) == ['pkg']

    source.ensure('pkg/sub/__init__.py')
    assert find_packages(source, pkg) == ['pkg', 'pkg.sub']


def test_find_packages_task(source):
    pkg = source.join('pkg')
    source.ensure('pkg/__init__.py')

    task = FindPackages(source, 'pkg')
    task.run()
    assert task.result == ['pkg']

    task.match = 'missing'
    py.test.raises(IOError, task.run)

    task.match = 'pkg.*'
    task.run()
    assert task.result == ['pkg']



