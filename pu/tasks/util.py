"""
    pu.tasks.util
    ~~~~~~~~~~~~~

    utility base classes and functions
"""

import Queue


class TaskBase(object):
    """
    utility base class for implementing Tasks

    """
    keys = ()
    requirements = ()
    queue = None

    def __init__(self, **kw):
        for key in self.keys:
            setattr(self, key, kw[key])

        self._kw = kw

    # hashing and equality
    def _key(self):
        return tuple((key, getattr(self, key)) for key in self.keys)

    def __hash__(self):
        return hash(self._key())

    def __repr__(self):
        return '<%s %s>' % (
                type(self).__name__,
                ' '.join('%s=%r' % k 
                    for k in self._key()))

    def __eq__(self, other):
        return (isinstance(other, TaskBase)
                and self._key() == other._key())

    # reporting dispatch
    def _dispatch(self, base, item):
        name = getattr(item, 'category', item.__class__.__name__.lower())
        method = 'on_%s_%s' % (name, base)
        default_method = 'on_'+name
        if hasattr(self, method):
            return getattr(self, method)(item)
        elif hasattr(self, default_method):
            return getattr(self, default_method)(item)

    def report_failure(self, dependency):
        return self._dispatch('failure', dependency)

    def report_success(self, dependency):
        return self._dispatch('success', dependency)



    def next(self):
        if self.queue is None:
            self.queue = Queue.Queue()
            evil_kw = zip(self.keys, self.__keytuple())
            for req in self.requirements:
                self.queue.put(req(**evil_kw))
        try:
            return self.queue.get_nowait()
        except Queue.Empty:
            raise StopIteration



