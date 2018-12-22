# Automatically created by: scrapyd-deploy
from setuptools import setup, find_packages

setup(
    name             = 'japanese-address',
    version          = '0.1.2',
    description      = 'Japanese address parser',
    long_description = open('README.md').read(),
    license      = 'BSD',
    author       = 'Martin Olveyra',
    author_email = 'molveyra@gmail.com',
    url = 'https://github.com/kalessin/japanese-address',
    packages         = find_packages(),
    package_data={
        'japanese_address': ['data/*'],
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires = [
        'parsel',
    ]
)
