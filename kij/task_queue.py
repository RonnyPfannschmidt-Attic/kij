from kij.util import signal
task_failed = signal('task_failed')
task_succeeded = signal('task_succeeded')
task_finished = signal('task_finished')


class Queue(object):
    def __init__(self):
        self._key_to_identity = {}
        self.depends = {}
        self.completed = set()
        self.runnable = set()
        self.failed = set()
        self.running = set()

    def _run_canidates(self):
        for k, v in self.depends.iteritems():
            if k in self.completed:
                continue
            if k in self.running:
                continue
            if v - self.completed:
                continue
            yield k, v


    def find_and_add_new_runnable(self):
        for k, v in  self._run_canidates():
            try:
                new_item = next(k)
                new_item = self.add(new_item, parent=k)
                return True
            except (TypeError, StopIteration):
                self.runnable.add(k)
                return False


    def report_failure(self, task):
        self.failed.add(task)
        task_failed.send(task)
        self.completed.add(task)
        self.running.remove(task)

    def report_success(self, task):
        task_succeeded.send(task)
        self.completed.add(task)
        self.running.remove(task)

    def next(self):
        #XXX: expensive
        if not self.runnable:
            retry = True
            while retry:
                retry = self.find_and_add_new_runnable()


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

            # directly resignal on already completed signals
            if task in self.completed:
                print 'completed, but reasked', task
                if task in self.failed:
                    task_failed.send(task)
                else:
                    task_succeeded.send(task)
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
                self.report_success(item)
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

            def sanestr(x):
                for a in 'match package'.split():
                    if hasattr(x, a):
                        return '%s %s=%s' % (
                                x.__class__.__name__,
                                a,
                                getattr(x, a))

                return x.__class__.__name__

            def depspec(x):
                if not self.depends[x]:
                    return sanestr(x)
                return '%s -> %s' % (
                        sanestr(x),
                        ', '.join(sanestr(v)
                                  for v in sorted(self.depends[x])),
                        )

            print 'completed: \n ', '\n  '.join(sanestr(x)
                                                for x in sorted(self.completed))
            print 'depends', '\n  '.join(depspec(x) 
                                         for x in sorted(self.depends))
            raise RuntimeError('not all tasks are executable')
