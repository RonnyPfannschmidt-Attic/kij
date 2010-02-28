"""
    pu.files.dist
    ~~~~~~~~~~~~~

    Read and write pu distribution files.

    :license: MIT/PSF (see LICENSE.txt file)
    :copyright: pu Authors (see AUTHORS.txt file)

    This is the primary configuration file for any Python distribution. It
    aims to capture all the data required for distribution. The dist file is
    presented as a Yaml file, with a number of keys, each corresponding to a
    configuration directive for the distribution.

    A very simple example can be seen::

    name:    Blogatron
    version: 1.0
    author:  Ali Afshar
    packages:
        - blogatron

    Although the specification will grow, certain fields are recognised, some
    are required, and some optional. Other when present need to be of a
    certain type. The recognised attributes are desribed:

    name
        The distribution name, usually the name of the project. *required*

    version
        The version of the distribution, should be a string of the numerical
        version number.

    summary
        A short one-line summary of the distribution.

    packages
        A list of package descriptions to add to the distribution


    Being Yaml, there is a certain degree of type expressivity over ini-based
    systems. Addiitonally, the Yaml loading layer can be easily swapped out
    for anything else.
"""

import yaml


from py.path import local


DIST_FILE_KEYS = set((
    'packages', 'summary',
))


class DistFileError(ValueError):
    """Error with Dist File"""


class DistFile(object):

    def __init__(self, path):
        self.path = local(path)
        self._load()

    def _load(self):
        # XXX Handle exceptions
        try:
            conf = yaml.load(self.path.open())
        except Exception, e:
            raise DistFileError('Error loading file %s %s' % (self.path, e))
        self.name = conf.get('name')
        if self.name is None:
            raise DistFileError('Missing "name" key %s' % self.path)
        # now the optional keys
        for k in DIST_FILE_KEYS:
            setattr(self, k, conf.get(k))
        # now some validation
        if self.packages and not isinstance(self.packages, list):
            raise DistFileError('packages must be a list')
        self._model = conf

    def __str__(self):
        return "<DistFile: %s>" % self.path
