from kij.tasks.install import LinkPTH, UnlinkPTH
from kij.storage.pth import PthFile


def test_enable(site, source):
    task = LinkPTH(site=site, source=source)
    assert not site.join(task.pth_name).check()
    task.run()
    assert site.join(task.pth_name).check()


def test_disable(site, source):
    test_enable(site, source)

    task = UnlinkPTH(site=site, source=source)

    pth = PthFile(site.join(task.pth_name))
    assert source in pth.entries

    task.run()

    pth = PthFile(site.join(task.pth_name))
    assert source not in pth.entries
