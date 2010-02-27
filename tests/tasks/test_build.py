from pu.tasks.build import CopyModulesToBuild, CompileByteCode
from pu.task_queue import Queue

def test_copy_build(source, tmpdir):
    source.ensure('testpkg/__init__.py')
    source.join('kij.yml').write('name: test\npackages: testpkg\n')
    task = CopyModulesToBuild(
                    source=source,
                    build_lib=tmpdir.join('build/lib'),
                    )
    task()
    assert tmpdir.join('build/lib/testpkg/__init__.py').check()


def test_build_and_compile(source, tmpdir):

    queue = Queue()

    source.ensure('testpkg/__init__.py')
    build_lib=tmpdir.join('build/lib')

    copy = CopyModulesToBuild(
        source=source,
        build_lib=build_lib,
        )
    queue.add(copy)

    compile = CompileByteCode(build_lib=build_lib)
    queue.add(compile)
    queue.add(copy, parent=compile)

    queue.run_all()
    target =  build_lib.join('testpkg/__init__.pyc')
    assert build_lib.join('testpkg/__init__.py').check()
    assert target.check()
    import imp
    magic = imp.get_magic()
    target_magic = target.read()[:4]
    assert target_magic == magic

