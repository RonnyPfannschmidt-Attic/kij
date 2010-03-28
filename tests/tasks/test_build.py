from kij.tasks.build import CopyPackagesToBuild, CompileByteCode, \
        CopyScripts, Build
from kij.task_queue import Queue


def test_copy_build(source,config):
    source.ensure('testpkg/__init__.py')
    source.join('kij.yml').write('name: test\npackages: [testpkg]\n')
    task = CopyPackagesToBuild(config)
    queue = Queue()
    queue.add(task)
    queue.run_all()
    assert config.build_lib.join('testpkg/__init__.py').check()


def test_build_and_compile(source, tmpdir, config, build_lib):

    queue = Queue()

    source.ensure('testpkg/__init__.py')
    source.join('kij.yml').write('name: test\npackages: [testpkg]\n')

    compile = CompileByteCode(config)
    queue.add(compile)

    queue.run_all()
    target = build_lib.join('testpkg/__init__.pyc')
    assert build_lib.join('testpkg/__init__.py').check()
    assert target.check()

    import imp
    magic = imp.get_magic()
    target_magic = target.read()[:4]
    assert target_magic == magic


def test_copy_scripts(config, source, build_scripts):
    source.join('kij.yml').write('name: test\nscripts: [foo, bin/bar]')
    source.ensure('foo')
    source.ensure('bin/bar')
    task = CopyScripts(config)
    queue = Queue()
    queue.add(task)
    queue.run_all()
    assert len(build_scripts.listdir()) == 2


def test_build_(source, tmpdir):
    source.join('kij.yml').write(
            'name: test\n'
            'scripts: [foo, bin/bar]\n'
            'packages: [testpkg]\n'
            )
    source.ensure('foo')
    source.ensure('bin/bar')
    source.ensure('testpkg/__init__.py')

    task = Build(
        source=source,
        build_scripts=tmpdir.join('scripts'),
        build_lib=tmpdir.join('lib'),
        )

    queue = Queue()
    queue.add(task)

    queue.run_all()
    assert len(tmpdir.join('scripts').listdir()) == 2
    assert tmpdir.join('lib/testpkg/__init__.py').check()
    assert tmpdir.join('lib/testpkg/__init__.pyc').check()



