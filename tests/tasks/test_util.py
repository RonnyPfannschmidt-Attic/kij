import py
from pu.tasks.util import TaskBase, task_succeeded, task_failed
from pu.task_queue import Queue


class Omg(TaskBase):
    keys = ()

    def __call__(self):
        pass


class NeedOmg(Omg):
    keys = ()
    requirements = Omg,


class U(TaskBase):
    keys = 'name', 'age'

    def on_omg_failure(self, item):
        return item

    def on_u_success(self, item):
        return item.name


def test_base():
    py.test.raises(KeyError, U, )

    u1 = U(name='a', age=1)
    u2 = U(name='a', age=1)
    assert u1 == u2
    assert hash(u1) == hash(u2)

    o = Omg()
    with task_succeeded.temporarily_connected_to(
            o._requirement_succeeded,
            sender=o):
        result = task_succeeded.send(o)
        assert result[0][1] is None

    with task_failed.temporarily_connected_to(
            u1._requirement_failed,
            sender=o):
        assert task_failed.send(o)[0][1] is o

    with task_succeeded.temporarily_connected_to(
            u1._requirement_succeeded,
            sender=u2):
        assert task_succeeded.send(u2)[0][1] == 'a'

    with task_succeeded.temporarily_connected_to(
            u1._requirement_succeeded,
            sender=o):
        assert task_succeeded.send(o)[0][1] is None


def test_requirement():
    queue = Queue()
    task = NeedOmg()
    depends = next(task)
    py.test.raises(StopIteration, next, task)
    queue.add(task)
    queue.run_all()
