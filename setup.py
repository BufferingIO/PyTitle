#!/usr/bin/env python3
import pathlib
import re
import sys

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """
    Read version
    :return: str
    """
    return "0.1.0"
    # txt = (WORK_DIR / 'aiogram' / '__init__.py').read_text('utf-8')
    # try:
    #     return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    # except IndexError:
    #     raise RuntimeError('Unable to determine version.')


def get_description():
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    return ""
    # with open('README.rst', 'r', encoding='utf-8') as f:
    #     return f.read()


setup(
    name='pytitle',
    version=get_version(),
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    url='https://github.com/sina-e/pytitle',
    license='MIT',
    author='Sina Ebrahimi',
    python_requires='>=3.7',
    author_email='ebrahimisina78@gmail.com',
    description='Subtitle manipulation library for python.',
    long_description=get_description(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'pydantic>=1.9.0'
    ],
    extras_require={
    },
    project_urls={
        'Documentation': 'https://pytitle.readthedocs.io',
        'Source': 'https://github.com/sina-e/pytitle',
    },
    include_package_data=False,
)