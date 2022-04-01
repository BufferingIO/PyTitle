Subtitle manipulation library for Python
========================================

|PyPI| |PyPI - Downloads| |PyPI - Python Version| |PyPI - License| |Read
the Docs| |GitHub issues|

PyTitle is a subtitle manipulation library for python, it’s built on top
of Pydantic.

**note that development of this project is just started and it’s not
anywhere near complete or ready for production code. use it at your own
risk**

what this library can do?

well, it’s able to do a lot of things, and more in the future, but for now:

-  search for a text or pattern in a subtitle.
-  shift all the timestaps, or just one timestap to forward or backward.
-  split the subtitle from an index or timestamp.
-  fix common problems in a subtitle, such as:

   -  re-index .srt subtitles.
   -  remove or fix italic, bold and other formatting tags.
   -  add coloring or other formattings to a subtitle.
   -  fix enconding problems.
   -  fix arabic charachters, question marks and other formattings for
      persian subtitles.
   -  fix overlays in timestamps.


supported formats:
~~~~~~~~~~~~~~~~~~

-  ☒ srt
-  ☐ ass
-  ☐ vtt

.. |PyPI| image:: https://img.shields.io/pypi/v/pytitle
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/pytitle
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/pytitle
.. |PyPI - License| image:: https://img.shields.io/pypi/l/pytitle
.. |Read the Docs| image:: https://img.shields.io/readthedocs/pytitle
.. |GitHub issues| image:: https://img.shields.io/github/issues/sina-e/pytitle


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installing
   quick_start
   pytitle



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
