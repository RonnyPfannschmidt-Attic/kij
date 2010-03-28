
"""
    kij.commands
    ~~~~~~~~~~~~

    Command line interface to kij
"""


import os

import py

from sanescript import Script, Command, Option

from build import BuildCommand


class KijScript(Script):

    options = [
        Option(
            'source',
            help='The source code directory',
            default=py.path.local(os.getcwd()),
            processor=py.path.local
        ),
    ]


class KijCommand(Command):
    """The base Kij command
    """

kij_script = KijScript()
kij_script.add_command(BuildCommand)

