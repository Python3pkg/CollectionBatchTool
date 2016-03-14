from setuptools import setup, find_packages
from os.path import join, dirname
import sys


if sys.version_info.major < 3:
    print("Sorry, currently only Python 3 is supported!")
    sys.exit(1)


setup(
    name = 'CollectionBatchTool',
    version=__import__('collectionbatchtool').__version__,
    description = 'batch import and export of Specify data',
    long_description = open(
        join(dirname(__file__), 'README.rst'), encoding='utf-8').read(),
    packages = find_packages(),
    py_modules = ['collectionbatchtool', 'specifymodels'],
    install_requires = ['pandas>=0.16', 'peewee>=2.6', 'pymysql'],
    author = 'Markus Englund',
    author_email = 'jan.markus.englund@gmail.com',
    url = 'https://github.com/jmenglund/CollectionBatchTool',
    license = 'MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords = ['Specify', 'Collection management']
)
