from pu.commands.install import link_command
from pu.task_queue import Queue

def test_link_command(config, site):
    queue = Queue()
    link_command(config, queue)
    queue.run_all()
    assert len(site.listdir()) == 1
