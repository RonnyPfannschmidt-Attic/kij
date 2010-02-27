import py
from pu.tasks.util import TaskBase

class Omg(TaskBase):
    keys = ()

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
    assert o.report_success(o) is None
    assert u1.report_failure(o) is o
    assert u1.report_success(u2) == 'a'
    assert u1.report_success(o) is None



