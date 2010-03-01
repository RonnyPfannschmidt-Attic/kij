import py
from pu.tasks.metadata import FindSubPackages, find_packages as gen_find_packages
from pu.tasks.metadata import ReadYamlMetadata, FindPackages
from pu.task_queue import Queue

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

    task = FindSubPackages(source=source, match='pkg')
    task()
    assert task.result == ['pkg']

    task.match = 'missing'
    py.test.raises(IOError, task)

    task.match = 'pkg.*'
    task()
    assert task.result == ['pkg']


def test_read_yaml_task(source):
    source.join('kij.yml').write('name: test\npackages: [foo, bar]')
    task = ReadYamlMetadata(source=source)
    task()
    assert task.result.name == 'test'
    assert task.result.packages == ['foo', 'bar']


def test_find_packages_task(source):
    source.join('kij.yml').write('name: test\npackages: [foo, bar]')
    source.join('foo/__init__.py').ensure()
    source.join('bar/__init__.py').ensure()

    queue = Queue()
    task = FindPackages(source=source)
    queue.add(task)
    queue.run_all_possible()
    for k, v in queue.depends.items():
        print k, 'depends on', v
    assert task.result == ['foo', 'bar']

