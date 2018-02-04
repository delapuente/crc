"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    python_requires='>=3.5',
    name='crc',
    version='0.1.0a1',
    description='Translate Quantum circuit files to Qiskit',
    long_description=long_description,
    #url='https://github.com/delapuente/crc',
    author='Salvador de la Puente González',
    author_email='salva@unoyunodiez.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='quantic computing circuit development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['astor', 'tatsu'],
    extras_require={
        'dev': ['pylint']
    }
)
