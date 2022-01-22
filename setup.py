import os
import re
import setuptools

MYPATH = os.path.abspath(os.path.dirname(__file__))
VERSION = os.path.join(MYPATH, 'smartapp/version.py')

def readme():
    mypath = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(mypath, 'README.md')) as f:
        readme = f.read()
    return readme

def version(ver=None):
    __version__ = ver
    with open(VERSION, 'r+') as f:
        if not ver:
            for line in f.readlines():
                exec(line)
            return __version__
        else:
            f.truncate()
            f.writelines( ['__version__ = "{}"'.format(ver)])
            return ver

def build_version():
    ver = os.getenv('BUILD_VERSION').split('-')
    if len(ver) == 1:
        return ver.pop()
    return '-'.join(['+'.join([ver[0], ver[1]]), ver[2]])

def reset_version():
    with open(VERSION, 'w') as f:
        f.writelines(['__version__ = "see setup.py / Makefile"\n'])

try:
    setuptools.setup(
        name='smartapp-sdk',
        version=version(build_version()),
        description='SmartApp Base',
        long_description=readme(),
        packages=setuptools.find_packages(where='.', exclude=('tests')),
        python_requires='==3.*',
        install_requires=[
        'fastapi==0.*',
        'itsdangerous==1.*',
        'httpx==0.*',
        'python-dateutil==2.*',
        'aiohttp==3.*',
        'redis==4.*',
        ]
    )
finally:
    reset_version()
