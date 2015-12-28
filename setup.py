import sys
from setuptools import setup, find_packages
from aerospace.version import version

py_version = sys.version_info[:2]
if not py_version == (2, 7):
    raise RuntimeError('Requires Python version 2.7 but '
                       ' ({}.{} detected).'.format(*py_version))

setup(
    name='aerospace',
    version=version,
    packages=find_packages(),
    install_requires=[
        'matplotlib>=1.4.2',
        'numpy>=1.9.1',
        'odespy>=0.3.0'
    ],
    url='https://github.com/zokalo/aerospace',
    license='GPL v3.0',
    author='Don D.S.',
    author_email='dondmitriys@gmail.com',
    description=
    'Package of static and dynamic math-models for aerospace computations'
)
