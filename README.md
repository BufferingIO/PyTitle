# Subtitle manipulation library for Python

[![PyPI](https://img.shields.io/pypi/v/pytitle)](https://pypi.org/project/pytitle/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pytitle)](https://pypi.org/project/pytitle/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytitle)](https://pypi.org/project/pytitle/)
[![Codecov coverage](https://img.shields.io/codecov/c/github/sina-e/PyTitle)](https://app.codecov.io/gh/sina-e/PyTitle/)
[![PyPI - License](https://img.shields.io/pypi/l/pytitle)](https://pypi.org/search/?c=License+%3A%3A+OSI+Approved+%3A%3A+MIT+License)
[![Read the Docs](https://img.shields.io/readthedocs/pytitle)](https://pytitle.readthedocs.io)
[![GitHub issues](https://img.shields.io/github/issues/sina-e/pytitle)](https://github.com/sina-e/PyTitle/issues)

PyTitle is a subtitle manipulation library for python, it's built on top of Pydantic.

**note that development of this project is just started and it's not anywhere near complete or ready for production code. use it at your own risk**

what this library can do?

well, it's able to do a lot of things, and more in the future, but for now:

- search for a text or pattern in a subtitle.
- shift all the timestaps, or just one timestap to forward or backward.
- split the subtitle from an index or timestamp.
- fix common problems in a subtitle, such as:
    - re-index .srt subtitles.
    - remove or fix italic, bold and other formatting tags.
    - add coloring or other formattings to a subtitle.
    - fix enconding problems.
    - fix arabic charachters, question marks and other formattings for persian subtitles.
    - fix overlays in timestamps.

## Installing PyTitle

`pip install pytitle`

## Quick start

For now, the only supported subtitle format is `.srt`. other formats will be added to the library soon.

Open a .srt Subtitle:

```python
from pytitle.srt import SrtSubtitle

subtitle = SrtSubtitle.open("~/path/to/subtitle.srt")
```

shift all the timestamps for the opened subtitle 2 seconds forward:

```python
subtitle.shift_forward(seconds=2)
```

or you can shift only one line, for example the 10th line(.srt indexes start at 1):

```python
subtitle.shift_forward(seconds=2, index=10)
```

and when you done editing, save the file:

```python
subtitle.save()
```

the above method will override the existing file, if you want to save the file in a different place or seperately:

```python
subtitle.save(path="~/path/to/edited_subtitle.srt")
```

**Read the full documentation and tutorial [here](https://pytitle.readthedocs.io).**


### supported formats:

- [x] srt
- [ ] ass
- [ ] vtt
