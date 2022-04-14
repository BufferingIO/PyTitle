# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
-  Add encoding detection for `SrtSubtitle.open()` (fixes #1)
## [0.1.6] - 2022-4-12
### Added
- docstring for `__init__.py` file, add short project description
- add `Timing.shift` and `SrtSubtitle.shift` for shifting the timing of lines forward or backward
- add `SrtSubtitle.shift_forward` and `SrtSubtitle.shift_backward` as a shorthand for `SrtSubtitle.shift`
- add exception classes to raise them instead of generic exceptions
### Changed
- fixed some typos in docstrings
- removed custom `__eq__` and `__ne__` from the Timestamp and let pydantic handle that
- changed the value limits for Timestamp attributes, `Timestamp.hours` can be any integer >= 0 now
- fixed how `__add__` and `__sub__` were calculating and fixed overflows to add or subtract the times correctly

## [0.1.5] - 2022-04-04
### Added
- test for Timestamp.get_value
- This CHANGELOG file to track changelogs

### changed
- update setup.py keywords and classifiers for pypi


[Unreleased]: https://github.com/sina-e/PyTitle/compare/v0.1.6...HEAD
[0.1.6]: https://github.com/sina-e/PyTitle/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/sina-e/PyTitle/compare/v0.1.4...v0.1.5