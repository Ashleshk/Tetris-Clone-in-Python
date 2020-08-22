import platform
import sys

# try to guess the python executable's name
if platform.platform() == 'Windows':
    python = 'py'
else:
    python = 'python3'


