"""

    :license: MIT/PSF
    :copyright: 2010 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>
"""
from pu.tasks.install import LinkPTH

def link_command(config, queue):
    #XXX: handle fscked paths?
    #XXX: scripts
    queue.add(LinkPTH(
                   source=config.source,
                   site=config.site,
                   ))


