'''

    :license: MIT/PSF
    :copyright: 2010 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>
'''

class Queue(object):
    def __init__(self):
        self._added = set()
        self.items = []

    def next(self):
        if self.items:
            return self.items.pop()
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def add_task(self, task, *k, **kw):
        key = task, k, tuple(sorted(kw.items()))
        if key in self._added:
            return
        self._added.add(key)
        task = task(*k, **kw)
        self.items.append(task)
        return task

    def run_all(self):
        for item in self:
            item.run()
