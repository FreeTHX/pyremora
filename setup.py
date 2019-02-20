"""A setuptools based setup module.

See:
https://github.com/FreeTHX/pyremora
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open
import remora

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyremora',
    version=remora.__version__,
    description='A Python library to use the Remora API (Fil Pilote)',
    long_description_content_type='text/markdown',
    url='https://github.com/FreeTHX/pyremora',
    author='FreeTHX',
    author_email='freethx.dev@gmail.com',
    license='Apache License 2.0',
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Home Automation',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='remora fil pilote',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  
    install_requires=['requests'],
)
