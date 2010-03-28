
import sys
VERSION_INFO = tuple(sys.version_info[:2])

from kij.commands.build import BuildCommand
from kij.commands import kij_script
from kij.task_queue import Queue

def test_build_command(script, fullsource, build_lib, build_scripts):
    script.main(['kij', 'build'])
    assert build_lib.check()
    assert build_scripts.check()

