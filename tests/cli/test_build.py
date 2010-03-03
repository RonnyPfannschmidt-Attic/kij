
import sys
VERSION_INFO = tuple(sys.version_info[:2])

from kij.commands.build import BuildCommand
from kij.commands import kij_script
from kij.task_queue import Queue

def test_build_command(script, fullsource):
    script.main(['kij', 'build'])
    build = fullsource.join('build')
    assert build.check()
    assert build.join('lib').check()
    assert build.join('scripts-%s.%s' % VERSION_INFO).check()

