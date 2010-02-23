from pu.files.pth import PthFile
class LinkTask(object):
    pth_name = 'pu-links.pth'

    def __init__(self, site, source):
        self.site = site
        self.source = source
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


