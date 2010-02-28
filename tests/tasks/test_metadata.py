import py
from pu.tasks.metadata import FindPackages, find_packages as gen_find_packages
from pu.tasks.metadata import ReadYamlMetadata

def find_packages(source, pkg):
    return list(gen_find_packages(source, pkg))

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

    task = FindPackages(source=source, match='pkg')
    task()
    assert task.result == ['pkg']

    task.match = 'missing'
    py.test.raises(IOError, task)

    task.match = 'pkg.*'
    task()
    assert task.result == ['pkg']


def test_read_yaml_task(source):
    source.join('kij.yaml').write('name: test\npackages: [foo, bar]')
    task = ReadYamlMetadata(source=source)
    task()
    assert task.result.name == 'test'
    assert task.result.packages == ['foo', 'bar']
