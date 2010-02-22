

def find_packages(base, start):
    result = []
    if start.join('__init__.py').check(file=1):
        result.append(start.relto(base).replace('/','.'))
        for path in start.listdir(lambda p:p.check(dir=1)):
            result.extend(find_packages(base, path))
    return result







class FindPackages(object):
    def __init__(self, source, match):
        self.source = source
        self.match = match
        self.result = None

    def run(self):
        deep = self.match[-2:] == '.*'
        elements = self.match.split('.')
        if deep:
            elements.pop()

        self.result = find_packages(self.source, self.source.join(*elements))
        if not self.result:
            raise IOError('package %s not found below %s' % (
                           self.match, self.source))

