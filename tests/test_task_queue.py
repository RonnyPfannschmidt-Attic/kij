import py
from pu.task_queue import Queue
from pu.tasks.install import LinkPTH
from pu.tasks.util import TaskBase

class SimpleTask(TaskBase):
    ndeps = None
    keys = 'number',
    called = False

    def __repr__(self):
        return '<ST %d>' % self.number

    def next(self):
        if self.ndeps is None:
            self.ndeps = self.number
        if self.ndeps:
            self.ndeps -= 1
            return SimpleTask(number=self.ndeps)
        raise StopIteration

    def __eq__(self, other):
        return type(self) == type(other) and self.number == other.number

    def __call__(self):
        assert not self.called
        self.called = True
        print self.number


class WeirdTask(TaskBase):
    keys = 'number',
    called = False
    requirements = SimpleTask,
    def __call__(self):
        self.called = True

def test_create():
    Queue()


def test_simple():
    queue = Queue()
    # will create SimpleTask(0) as dependency
    queue.add(SimpleTask(number=1))
    first_task = next(queue)
    assert first_task.number == 0

    py.test.raises(StopIteration, next, queue)

    assert isinstance(first_task, SimpleTask)

    queue.report_sucess(first_task)
    next_task = next(queue)
    assert next_task.number == 1
    queue.report_sucess(next_task)
    py.test.raises(StopIteration, next, queue)


def test_adding_the_same_twice_has_no_effect():
    queue = Queue()
    queue.add(SimpleTask(number=0))
    queue.add(SimpleTask(number=0))
    assert len(queue) == 1


def test_run_all(source, site):
    #XXX: run-all sucks
    queue = Queue()
    task = LinkPTH(site=site, source=source)
    queue.add(task)
    queue.run_all()
    assert site.join(task.pth_name).check()


def test_dependencies():
    queue = Queue()
    queue.add(SimpleTask(number=3))
    queue.run_all()
    assert len(queue.completed) == 4


def test_dependency_cycle_wont_complete_all():
    queue = Queue()
    base = SimpleTask(number=1)

    queue.add(base)
    a_runnable = next(queue)
    queue.add(base, a_runnable)
    queue.run_all_possible()
    assert set(queue.depends) > queue.completed

    py.test.raises(RuntimeError, queue.run_all)


def test_dependencies():
    queue = Queue()
    task = queue.add(WeirdTask(number=1))
    queue.run_all()
    print queue.completed
    assert task.called
