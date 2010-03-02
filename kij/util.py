from blinker import Namespace
namespace = Namespace()


def signal(name):
    return namespace.signal(name)

task_succeeded = signal('task_succeeded')
task_failed = signal('task_failed')
