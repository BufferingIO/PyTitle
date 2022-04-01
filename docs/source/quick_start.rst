Quick start
===========

For now, the only supported subtitle format is ``.srt``. other formats
will be added to the library soon.

Open a .srt Subtitle:

.. code:: python

   from pytitle.srt import SrtSubtitle

   subtitle = SrtSubtitle.open("~/path/to/subtitle.srt")

shift all the timestamps for the opened subtitle 2 seconds forward:

.. code:: python

   subtitle.shift_forward(seconds=2)

or you can shift only one line, for example the 10th line(.srt indexes
start at 1):

.. code:: python

   subtitle.shift_forward(seconds=2, index=10)

and when you done editing, save the file:

.. code:: python

   subtitle.save()

the above method will override the existing file, if you want to save
the file in a different place or seperately:

.. code:: python

   subtitle.save(path="~/path/to/edited_subtitle.srt")
