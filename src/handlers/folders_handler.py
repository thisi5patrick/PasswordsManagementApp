from os import makedirs
from os.path import dirname, join


class FoldersHandler:
    def __init__(self):
        ...

    @staticmethod
    def createFolders():
        scriptdir = dirname(__file__)
        makedirs(join(scriptdir, '..', 'data'), exist_ok=True)
        makedirs(join(scriptdir, '..', 'data/users'), exist_ok=True)
        makedirs(join(scriptdir, '..', 'data/passwords'), exist_ok=True)
