"""
    pu.tasks.util
    ~~~~~~~~~~~~~

    utility base classes and functions
"""

class CreateHelper(object):
    def __init__(self, **kw):
        for key in self.keys:
            setattr(self, key, kw.pop(key))

        self._debug_extra_kw = kw


class HashHelper(object):

    def __keytuple(self):
        return tuple(getattr(self, key) for key in self.keys)

    def __hash__(self):
        return hash(self.__keytuple())

    def __repr__(self):
        return '<%s %s>' % (
                type(self).__name__,
                ' '.join('%s=%r' % k 
                    for k in zip(self.keys, self.__keytuple())))
    def __eq__(self, other):
        return (isinstance(other, HashHelper)  # probably evil
                and self.keys == other.keys
                and self.__keytuple() == other.__keytuple())

class ReportHelper(object):
    def __dispatch(self, base, item):
        name = getattr(item, 'category', item.__class__.__name__.lower())
        method = 'on_%s_%s' % (name, base)
        default_method = 'on_'+name
        if hasattr(self, method):
            return getattr(self, method)(item)
        elif hasattr(self, default_method):
            return getattr(self, default_method)(item)

    def report_failure(self, dependency):
        return self.__dispatch('failure', dependency)

    def report_success(self, dependency):
        return self.__dispatch('success', dependency)

class TaskBase(CreateHelper, HashHelper, ReportHelper):
    pass
