"""
    pu.tasks.util
    ~~~~~~~~~~~~~

    utility base classes and functions
"""

from collections import deque



class TaskBase(object):
    """
    utility base class for implementing Tasks

    """
    keys = ()
    requirements = ()
    queue = None

    def __init__(self, config=None, **kw):

        for key in self.keys:
            if key in kw:
                setattr(self, key, kw[key])
            elif hasattr(config, key):
                setattr(self, key, getattr(config, key))
            else:
                raise KeyError('%r required to set up %s' % (
                    key,
                    type(self).__name__)
                    )

        self._kw = kw
        self._config = config

    # hashing and equality
    def _key(self):
        return tuple((key, getattr(self, key, LookupError)) for key in self.keys)

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return (type(self) == type(other)
                and self._key() == other._key())

    def __repr__(self):
        return '<%s %s>' % (
                type(self).__name__,
                ' '.join('%s=%r' % k
                    for k in self._key()))

    # reporting dispatch
    def _dispatch(self, base, item):
        name = getattr(item, 'category', item.__class__.__name__.lower())
        method = 'on_%s_%s' % (name, base)
        default_method = 'on_' + name
        if hasattr(self, method):
            return getattr(self, method)(item)
        elif hasattr(self, default_method):
            return getattr(self, default_method)(item)

    def _requirement_succeeded(self, requirement):
        self._enqueue_next_requirement()
        return self._dispatch('success', requirement)

    def _requirement_failed(self, requirement):
        #XXX: how to deal with failure
        return self._dispatch('failure', requirement)

    def _enqueue_next_requirement(self):
        if self.requirements:
            print 'equeue next for', self
            req = self.requirements.popleft()
            task = req(self._config, **self._kw)
            print 'made', task
            self.queue.append(task)

    def __iter__(self):
        return self

    def next(self):
        if self.queue is None:
            self.queue = deque()
            #XXX: we need to re-suffle the connections inside of queue
            #     that is absolutely required since
            #     the returned requirement might already be in the queue
            #     but with different identity
            if self.requirements:
                print self, 'needs', self.requirements
                self.requirements = deque(self.requirements)
                self._enqueue_next_requirement()
        if self.queue:
            return self.queue.popleft()
        else:
            raise StopIteration
