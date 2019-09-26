import sys
import os


class ConnectionError(Exception):
    pass


class Version(Exception):
    def __init__(self, text, version):
        super().__init__(text)
        self.version = str(version)

    @ValueError
    def checkversion(self, version):
        try:
            if '3' in sys.version[0]:
                sys.stdout.write(
                    '\x1b[1;32m' + '[+] Running Python version: ' + sys.version + '\x1b[0m' + '\n')
        except:
            sys.stderr.write(
                '\x1b[1;31m' + 'Run application with latest version of python' + '\x1b[0m')
