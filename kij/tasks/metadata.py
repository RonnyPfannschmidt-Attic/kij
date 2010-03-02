from .util import TaskBase
from kij.files.dist import DistFile


def find_packages(base, start):
    if start.join('__init__.py').check(file=1):
        package = start.relto(base).replace('/', '.')
        yield package
        for path in start.listdir(lambda p: p.check(dir=1)):
            for result in find_packages(base, path):
                yield result


class FindSubPackages(TaskBase):
    keys = 'source', 'match',
    result = None

    def __call__(self):
        deep = self.match[-2:] == '.*'
        elements = self.match.split('.')
        if deep:
            elements.pop()

        self.result = list(find_packages(self.source,
                                         self.source.join(*elements)))
        print 'found', self.result
        if not self.result:
            raise IOError('package %s not found below %s' % (
                           self.match, self.source))


class ReadYamlMetadata(TaskBase):
    keys = 'source',
    result = None
    requirements = ()
    def __call__(self):
        self.result = DistFile(self.source.join('kij.yml'))


class FindPackages(TaskBase):
    keys = 'source',
    requirements = ReadYamlMetadata,

    def on_readyamlmetadata_success(self, item):
        self.result = []
        print 'got yaml for', self
        print item.result.packages
        for package in item.result.packages:
            task = FindSubPackages(
                match=package,
                source=self.source)
            self.queue.append(task)

    def on_findsubpackages_success(self, item):
        print item
        self.result.extend(item.result)

    def __call__(self):
        assert self.result
