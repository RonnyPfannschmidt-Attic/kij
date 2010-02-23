from pu.task_queue import Queue
from pu.tasks.install import LinkPTH

class SimpleTask(object):
    def __init__(self, number):
        self.number = number

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return type(self) == type(other) and self.number == other.number

    def __call__(self):
        print self.number


def test_create():
    Queue()


def test_simple():
    queue = Queue()
    queue.add(SimpleTask(1))
    first_task = next(queue)
    assert first_task.number == 1
    assert isinstance(first_task, SimpleTask)

def test_adding_the_same_twice_has_no_effect():
    queue = Queue()
    queue.add(SimpleTask(1))
    queue.add(SimpleTask(1))
    assert len(queue) == 1


def test_run_all(source, site):
    #XXX: run-all sucks
    queue = Queue()
    task = LinkPTH(site=site, source=source)
    queue.add(task)
    queue.run_all()
    assert site.join(task.pth_name).check()



