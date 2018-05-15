#!/usr/bin/env python
import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'README.rst')

# When running tests using tox, README.md is not found
try:
    with open(README) as file:
        long_description = file.read()
except Exception:
    long_description = ''

setup(
    name='async-mailchimp3',
    version='0.1.0',
    description='A python asynchronous client for v3 of MailChimp API',
    long_description=long_description,
    url='https://github.com/MyMusicTaste/async-python-mailchimp',
    author='MinJeong Kim',
    author_email='mj111@mymusictaste.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mailchimp api v3 asynchronous client wrapper',
    packages=find_packages(),
    install_requires=['aiohttp>=3.0.0'],
    # test_suite='tests',
)
