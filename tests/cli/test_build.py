
import sys
VERSION_INFO = tuple(sys.version_info[:2])

from kij.commands.build import build_command
from kij.task_queue import Queue

def test_build_command(config, site, fullsource):
    queue = Queue()
    build_command(config, queue)
    queue.run_all()
    build = fullsource.join('build')
    assert build.check()
    assert build.join('lib').check()
    assert build.join('scripts-%s.%s' % VERSION_INFO).check()

