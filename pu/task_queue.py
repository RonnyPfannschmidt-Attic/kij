from pu.tasks.util import task_failed
from pu.tasks.util import task_succeeded



class Queue(object):
    def __init__(self):
        self._key_to_identity = {}
        self.depends = {}
        self.completed = set()
        self.runnable = set()
        self.taken = set()
        self.running = set()

    def find_and_add_new_runnable(self):
        found = set()

        for k, v in  self.depends.items():
            if k in self.completed:
                continue
            if k in self.running:
                continue
            if hasattr(k, '__iter__'):
                new_item = next(k, None)
                if new_item is not None:
                    new_item = self.add(new_item, parent=k)
                    found.add(new_item)
            if not v - self.completed:
                self.runnable.add(k)
        return bool(found)

    def report_failure(self, task):
        #XXX: evil
        task_failed.send(task)
        self.completed.add(task)
        self.running.remove(task)

    def report_sucess(self, task):
        task_succeeded.send(task)
        self.completed.add(task)
        self.running.remove(task)

    def next(self):
        if not self.runnable:
            #XXX: expensive
            f = self.find_and_add_new_runnable()
            while f and not self.runnable:
                f = self.find_and_add_new_runnable()

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
        """add a `task`
        if `parent` is given this task is a new dependency for parent
        """
        if parent:
            assert parent in self.depends

        if task not in self.depends:
            self.depends[task] = set()
            self._key_to_identity[task] = task
        else:
            task = self._key_to_identity[task]
        if parent:
            self.depends[parent].add(task)
            task_succeeded.connect(parent._requirement_succeeded, sender=task)
            task_failed.connect(parent._requirement_failed, sender=task)
        return task

    def run_all_possible(self):
        """runs all tasks it can complete

        leaves the queue in a state where
        all completable tasks are completed
        """
        for item in self:
            print 'trying to run', item
            try:
                item()
                self.report_sucess(item)
            except RuntimeError:
                #reraise if report_failure tells us to do so
                if self.report_failure(item):
                    raise

    def run_all(self):
        """try to run all tasks

        if some tasks are unaccessible
        :raises: RuntimeError
        """
        self.run_all_possible()
        if len(self.completed) < len(self.depends):
            print 'completed: \n ', '\n  '.join(str(x)
                                                for x in sorted(self.completed))
            print 'depends', '\n  '.join(str(x)
                                         for x in sorted(self.depends))
            raise RuntimeError('not all tasks are executable')
