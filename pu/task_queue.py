"""

    :license: MIT/PSF
    :copyright: 2010 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>
"""

class Queue(object):
    def __init__(self):
        self.depends = {}
        self.completed = set()
        self.runnable = set()
        self.taken = set()
        self.running = set()

    def find_and_add_new_runnable(self):
        found = set()

        for k, v in self.depends.items():
            if k in self.completed:
                continue
            if k in self.running:
                continue
            if hasattr(k, '__iter__'):
                new_item = next(k, None)
                if new_item is not None:
                    self.add(new_item, parent=k)
                    found.add(new_item)
            if not v-self.completed:
                self.runnable.add(k)
        return bool(found)



    def report_failure(self, t):
        self.completed.add(t) #XXX: evil
        self.running.remove(t)

    def report_sucess(self, t):
        self.completed.add(t)
        self.running.remove(t)

    def next(self):
        if not self.runnable:
            f = self.find_and_add_new_runnable() #XXX: expensive
            while f and not self.runnable:
                f = self.find_and_add_new_runnable() #XXX: expensive
            
            print 'dep', set(self.depends)
            print 'don', self.completed
            print 'run', self.runnable
        
        if not self.runnable:
            raise StopIteration

        result = self.runnable.pop()
        self.running.add(result)
        return result

    def __iter__(self):
        return self
    def __len__(self):
        return len(self.depends) - len(self.completed)

    def add(self, task, parent=None):
        if task not in self.depends:
            self.depends[task] = set()
        if parent:
            self.depends[parent].add(task)


    def run_all(self):
        for item in self:
            try:
                item()
                self.report_sucess(item)
                print 'all:', self.depends.keys()
                print 'completed', self.completed
            except RuntimeError:
                #reraise if report_failure tells us to do so
                if self.report_failure(item):
                    raise


