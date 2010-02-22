from pu.task_queue import Queue
from pu.tasks.install import LinkPTH

class SimpleTask(object):
    def __init__(self, number):
        self.number = number

    def run(self):
        print self.number


def test_create():
    Queue()


def test_simple():
    queue = Queue()
    queue.add_task(SimpleTask, 1)
    first_task = next(queue)
    assert first_task.number == 1
    assert isinstance(first_task, SimpleTask)

def test_adding_the_same_twice_has_no_effect():
    queue = Queue()
    queue.add_task(SimpleTask, 1)
    queue.add_task(SimpleTask, 1)
    assert len(queue.items) == 1


def test_run_all(source, site):
    queue = Queue()
    task = queue.add_task(LinkPTH, site=site, source=source)
    queue.run_all()
    assert site.join(task.pth_name).check()




