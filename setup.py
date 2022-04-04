#!/usr/bin/env python3
import importlib
import pathlib

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent


def get_version():
    """
    Read version
    :return: str
    """
    return importlib.import_module("pytitle").__version__


def get_description():
    """
    Read full description from 'README.md'
    :return: description
    :rtype: str
    """
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="pytitle",
    version=get_version(),
    packages=find_packages(
        exclude=(
            "tests",
            "tests.*",
            "examples.*",
            "docs",
        )
    ),
    url="https://github.com/sina-e/pytitle",
    license="MIT",
    author="Sina Ebrahimi",
    python_requires=">=3.8",
    author_email="ebrahimisina78@gmail.com",
    description="Subtitle manipulation library for python.",
    long_description=get_description(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Typing :: Typed",
    ],
    keywords=[
        "subtitle",
        "subtitles",
        "subtitle-manipulation",
        "subtitle-manipulation-library",
        "subtitle-manipulation-python",
        "srt-subtitles",
        "vtt-subtitles",
        "ssa-subtitles",
        "ass-subtitles",
        "srt",
        "vtt",
        "ass",
        "ssa",
        "subtitle-edit",
        "subtitle-editor",
    ],
    install_requires=["pydantic>=1.9.0"],
    extras_require={},
    project_urls={
        "Documentation": "https://pytitle.readthedocs.io",
        "Source": "https://github.com/sina-e/pytitle",
    },
    include_package_data=False,
)
