"""
    pu.tasks.util
    ~~~~~~~~~~~~~

    utility base classes and functions
"""

import Queue
from blinker import Namespace

ns = Namespace()
task_failed = ns.signal('task_failed')
task_succeeded = ns.signal('task_succeeded')
task_finished = ns.signal('task_finished')

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

    def __eq__(self, other):
        return (isinstance(other, TaskBase)
                and self._key() == other._key())

    def __repr__(self):
        return '<%s %s>' % (
                type(self).__name__,
                ' '.join('%s=%r' % k 
                    for k in self._key()))

    # reporting dispatch
    def _dispatch(self, base, item):
        task_succeeded.disconnect(
                self._requirement_succeeded,
                sender=item)
        task_succeeded.disconnect(
                self._requirement_failed,
                sender=item)

        name = getattr(item, 'category', item.__class__.__name__.lower())
        method = 'on_%s_%s' % (name, base)
        default_method = 'on_'+name
        if hasattr(self, method):
            return getattr(self, method)(item)
        elif hasattr(self, default_method):
            return getattr(self, default_method)(item)

    def _requirement_succeeded(self, requirement):
        return self._dispatch('success', requirement)

    def _requirement_failed(self, requirement):
        return self._dispatch('failure', requirement)

    def next(self):
        if self.queue is None:
            self.queue = Queue.Queue()
            if self.requirements:
                self.requirements = Queue()
                task = req(**self._kw)
                task_succeeded.connect(self._requirement_succeeded, sender=task)
                task_failed.connect(self._requirement_failed, sender=task)
                self.queue.put_nowait(task)
        try:
            return self.queue.get_nowait()
        except Queue.Empty:
            raise StopIteration



