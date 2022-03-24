from typing import List

from pytitle.logger import get_logger

from .types import Line, Timing
from . import regex

logger = get_logger(__name__)


class SrtSubtitle:
    def __init__(
        self,
        path: str = None,
        lines: List[Line] = None,
        encoding: str = "utf-8",
    ) -> None:
        self.path = path
        self.encoding = encoding
        self.lines: List[Line] = lines

    @classmethod
    def open(cls, path: str = None, encoding: str = "utf-8") -> "Subtitle":
        """Open subtitle file from a path"""
        with open(path, "r") as file:
            filestring = file.read()
            lines = cls.parse(filestring)
            return cls(path=path, lines=lines)

    @classmethod
    def parse(cls, filestring: str) -> List[Line]:
        """Parse the string formatted as a srt file"""
        lines = list()
        for index, match in enumerate(regex.LINE.finditer(filestring), start=1):
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

    def save(self, path: str = None) -> str:
        """Save subtitle to a path"""
        with open(path, "w+") as file:
            file.write(self.output)

    def shift(
        self,
        index: int = None,
    ) -> None:
        """Shift all or a single line timing backward or forward"""
        raise NotImplementedError

    def search(self, keyword: str, filters: str = None) -> Line:
        """Serach a keyword in text lines, duration in timings and line index"""
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

    def __str__(self) -> str:
        return (
            f"Subtitle(path='{self.path}', "
            f"lines={len(self.lines)}, "
            f"encoding='{self.encoding}'"
        )

    @property
    def output(self) -> str:
        return "\n".join(line.output for line in self.lines)
