# Author: TAKAHASHI Taro <takahashi.taro@takedasystem.com>
# Copyright (c) 2022- TAKAHASHI Taro
# Licence: MIT

from setuptools import setup, find_packages

DESCRIPTION = 'gat gaze data form record.'
NAME = 'get_eyedata'
AUTHOR = 'ikrfun'
AUTHOR_EMAIL = 't.nobuto130625@gmail.com'
URL = 'https://github.com/ikrfun/get_eyedata'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '1.2.0'
PYTHON_REQUIRES = '>=3.10'
INSTALL_REQUIRES = [
    'matplotlib>=3.7.1',
    'moviepy>=1.0.3',
    'numpy>=1.24.3',
    'opencv_contrib_python>=4.6.0.66',
    'opencv_python>=4.7.0.72',
    'opencv_python_headless>=4.7.0.72',
    'pandas>=2.0.2',
    'setuptools>=67.8.0',
    'tqdm>=4.65.0',
    'utils>=1.0.1'
]

KEYWORDS = 'gaze game'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)