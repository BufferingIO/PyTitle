from typing import List, Optional, Union

from pytitle.logger import get_logger

from . import regex
from .types import Line, PathType, Timestamp, Timing

logger = get_logger(__name__)


class SrtSubtitle:
    """Subtitle object for .srt formatted subtitles"""

    def __init__(
        self,
        path: Optional[PathType] = None,
        lines: Optional[List[Line]] = None,
        encoding: str = "utf-8",
    ) -> None:
        self.path = path
        self.encoding = encoding
        self.lines: Optional[List[Line]] = lines

    @classmethod
    def open(
        cls,
        path: PathType,
        encoding: str = "utf-8",
    ) -> "SrtSubtitle":
        """Open subtitle file from a path

        :param path: the path to the subtitle file
        :type path: str
        :param encoding: the encoding of the subtitle file
        :type encoding: str
        :return: the subtitle object
        :rtype: SrtSubtitle
        """
        with open(path, "r", encoding=encoding) as file:
            filestring = file.read()
            lines = cls.parse(filestring)
            return cls(path=path, lines=lines, encoding=encoding)

    @classmethod
    def parse(cls, filestring: str) -> List[Line]:
        """Parse the string formatted as a .srt file

        :param filestring: the string of the subtitle file
        :type filestring: str
        :return: a list of Line objects
        :rtype: List[Line]
        """
        lines = list()
        for index, match in enumerate(
            regex.LINE.finditer(filestring),
            start=1,
        ):
            logger.debug(f"Parsing [index={index}]:")
            start, end, text = match.groups()
            timing = Timing.from_string(start, end)
            logger.debug(f"\ttimestamp: {timing}")
            text = text.strip()
            logger.debug(f"\ttext: {repr(text)}")
            line = Line(
                index=index,
                timing=timing,
                text=text,
            )
            lines.append(line)
        return lines

    def save(
        self,
        path: Optional[PathType] = None,
        encoding: str = None,
    ) -> None:
        """Save subtitle to a path

        :param path: the path to save the subtitle to
        :type path: str
        :param encoding: the encoding of the subtitle file
        :type encoding: str
        :return: None
        :rtype: None
        """
        path = path or self.path
        if path is None:
            raise ValueError("No path specified")

        with open(path, "w+", encoding=encoding or self.encoding) as file:
            file.write(self.output)

    def shift(
        self,
        incrby: Union[int, Timestamp],
        index: Optional[Union[int, List[int], List[Line]]] = None,
        backward: bool = False,
    ) -> None:
        """
        Shift the timing of a one or multiple lines of subtitle, backward or forward

        :param incrby: the number of seconds or a Timestamp object to shift by
        :type incrby: Union[int, Timestamp]
        :param index: the index of a line, list of indexs or list of
            Line objects to shift
        :type index: Optional[Union[int, List[int], List[Line]]]
        :param backward: if True, shift backward, otherwise forward
        :type backward: bool
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def shift_forward(
        self,
        seconds: int,
        index: int = None,
    ) -> None:
        """
        Shift the timing of a line by index or all
            lines of subtitle forward by seconds

        :param seconds: the number of seconds to shift
        :type seconds: int
        :param index: the index of the line to shift, all lines if None
        :type index: int
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def shift_backward(
        self,
        seconds: int,
        index: int = None,
    ) -> None:
        """
        Shift the timing of a line by index or all
            lines of subtitle backward by seconds

        :param seconds: the number of seconds to shift
        :type seconds: int
        :param index: the index of the line to shift, all lines if None
        :type index: int
        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def search(self, keyword: str, filters: str = None) -> Line:
        """
        Serach a keyword in text lines, duration in timings and line index
        """
        raise NotImplementedError

    def reindex(self) -> None:
        """Reindexes the subtitle lines by timing"""
        raise NotImplementedError

    def remove_italic(self):
        """Remove italic tags from subtitle"""
        raise NotImplementedError

    def fix_italic(self):
        """Fix italic tags from subtitle"""
        raise NotImplementedError

    def fix_arabic(self):
        """Fix arabic/persian characters in subtitle"""
        raise NotImplementedError

    def fix_question_mark(self):
        """Fix question marks for arabic/persian subtitles"""
        raise NotImplementedError

    def find_overlaps(self) -> List[Line]:
        """Find overlapping lines in subtitle"""
        raise NotImplementedError

    def __str__(self) -> str:
        lines = len(self.lines) if self.lines is not None else 0
        return (
            f"Subtitle(path='{self.path!r}'"
            f"lines={lines} "
            f"encoding='{self.encoding!r}'"
        )

    @property
    def output(self) -> str:
        if self.lines is None:
            raise ValueError("No lines to output")
        return "\n".join(line.output for line in self.lines)
