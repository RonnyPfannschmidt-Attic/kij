"""

    :license: MIT/PSF
    :copyright: 2010 by Ali Afshar <aafshar@gmail.com>
"""

import sys

from sanescript import Command, Option

from kij.task_queue import Queue
from kij.tasks.build import Build


VERSION_INFO = tuple(sys.version_info[:2])


def build_command(config, queue):
    build = config.source.ensure('build', dir=True)
    build_lib = build.ensure('lib', dir=True)
    build_scripts = build.ensure('scripts-%s.%s' % VERSION_INFO, dir=True)
    queue.add(Build(
                   source=config.source,
                   build_lib=build_lib,
                   build_scripts=build_scripts,
                   ))


class BuildCommand(Command):

    name = 'build'

    def __call__(self, config):
        queue = Queue()
        build = config.source_directory.ensure('build', dir=True)
        build_lib = build.ensure('lib', dir=True)
        build_scripts = build.ensure('scripts-%s.%s' % VERSION_INFO, dir=True)
        task = Build(
            source=config.source_directory,
            build_lib=build_lib,
            build_scripts=build_scripts,
        )
        queue.add(task)
        queue.run_all()

