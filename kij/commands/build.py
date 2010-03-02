"""

    :license: MIT/PSF
    :copyright: 2010 by Ali Afshar <aafshar@gmail.com>
"""

import sys

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
