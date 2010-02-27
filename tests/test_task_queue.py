import py
from pu.task_queue import Queue
from pu.tasks.install import LinkPTH

class SimpleTask(object):
    def __init__(self, number):
        self.number = number
        self.ndeps = number
        self.called = False

    def __hash__(self):
        return hash(self.number)

    def __repr__(self):
        return '<ST %d>' % self.number

    def __iter__(self):
        return self

    def next(self):
        if self.ndeps:
            self.ndeps -= 1
            return SimpleTask(self.ndeps)
        raise StopIteration

    def __eq__(self, other):
        return type(self) == type(other) and self.number == other.number

    def __call__(self):
        assert not self.called
        self.called = True
        print self.number


def test_create():
    Queue()


def test_simple():
    queue = Queue()
    queue.add(SimpleTask(1)) # will create SimpleTask(0) as dependency
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
    queue.add(SimpleTask(0))
    queue.add(SimpleTask(0))
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
    queue.add(SimpleTask(3))
    queue.run_all()
    assert len(queue.completed) == 4



def test_dependency_cycle_wont_complete_all():
    queue = Queue()
    base = SimpleTask(1)

    queue.add(base)
    a_runnable = next(queue)
    queue.add(base, a_runnable)
    queue.run_all_possible()
    assert set(queue.depends) > queue.completed

    py.test.raises(RuntimeError, queue.run_all)

