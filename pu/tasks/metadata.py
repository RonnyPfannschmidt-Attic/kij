from .util import TaskBase


def find_packages(base, start):
    if start.join('__init__.py').check(file=1):
        package = start.relto(base).replace('/', '.')
        yield package
        for path in start.listdir(lambda p: p.check(dir=1)):
            for result in find_packages(base, path):
                yield result


class FindPackages(TaskBase):
    keys = 'source', 'match',
    result = None

    def __call__(self):
        deep = self.match[-2:] == '.*'
        elements = self.match.split('.')
        if deep:
            elements.pop()

        self.result = list(find_packages(self.source,
                                         self.source.join(*elements)))
        if not self.result:
            raise IOError('package %s not found below %s' % (
                           self.match, self.source))


class ReadYamlMetadata(TaskBase):
    keys = 'source',
    result = None

    def __call__(self):
        from pu.files.dist import DistFile
        self.result = DistFile(self.source.join('kij.yaml'))


