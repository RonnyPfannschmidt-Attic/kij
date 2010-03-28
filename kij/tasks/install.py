from kij.storage.pth import PthFile
from . import TaskBase

class LinkTask(TaskBase):
    pth_name = 'pu-links.pth'
    keys = 'site', 'source'

    def __call__(self):
        self.run()


class LinkPTH(LinkTask):

    def run(self):
        pth = PthFile(self.site.join(self.pth_name))
        pth.append(self.source)
        pth.save()


class UnlinkPTH(LinkTask):

    def run(self):
        pth = PthFile(self.site.join(self.pth_name))
        pth.remove(self.source)
        pth.save()
