'''
    kid.files.pth
    ~~~~~~~~~~~~~

    deals with reading, editing and writing pth files

    :license: GNU GPL3
    :copyright: 2010 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>
'''
from py.path import local

class PthFile(object):
    def __init__(self, path):
        self.path = local(path)
        self.entries = []
        if not self.path.check():
            return
        with self.path.open() as f:
            for entry in f:
                entry = entry.strip()
                if entry[0] == '.':
                    self.append(self.path.dirpath().join(entry))
                else:
                    self.append(local(entry))

    def append(self, path):
        if path not in self.entries:
            self.entries.append(path)

    def remove(self, path):
        self.entries.remove(path)

    def save(self):
        with self.path.open('w') as f:
            for path in self.entries:
                rel = path.relto(self.path.dirpath())
                if rel:
                    f.write('./%s\n'%rel)
                else:
                    f.write('%s\n'%path)


