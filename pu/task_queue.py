"""

    :license: MIT/PSF
    :copyright: 2010 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>
"""

class Queue(object):
    def __init__(self):
        self.depends = {}
        self.completed = set()
        self.runnable = set()

    def find_and_add_new_runnable(self):
        found = set()
        for k, v in self.depends.items():
            if hasattr(k, '__iter__'):
                new_items = list(k)
                for item in new_items:
                    self.add(new, parent, l)
            if not v-self.completed:
                self.runnable.add(k)

    def report_failure(self, t):
        self.completed.add(t)

    def report_sucess(self, t):
        self.completed.add(t)

    def next(self):
        if not self.runnable:
            self.find_and_add_new_runnable() #XXX: expensive
            if not set(self.depends)-self.completed:
                raise StopIteration


        return self.runnable.pop()


    def __iter__(self):
        return self
    def __len__(self):
        return len(self.depends) - len(self.completed)

    def add(self, task, requires=None):
        if task not in self.depends:
            self.depends[task] = set()
        if requires:
            self.depends[task].add(requires)


    def run_all(self):
        for item in self:
            try:
                item()
                self.report_sucess(item)
            except:
                #reraise if report_failure tells us to do so
                if self.report_failure(item):
                    raise


