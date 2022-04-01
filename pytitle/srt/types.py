from typing import Literal, Optional
import re

from pydantic import BaseModel
from . import regex


class Timestamp(BaseModel):
    """The Timestamp object is used to store the start or end of a subtitle
    the Timestamp is rendered as 00:00:00,000 from the ``output`` property
    """

    hours: Optional[int] = 0
    minutes: Optional[int] = 0
    seconds: Optional[int] = 0
    milliseconds: Optional[int] = 0

    def __repr__(self) -> str:
        return (
            f"Timestamp(hours={self.hours}, minutes={self.minutes}, "
            f"seconds={self.seconds}, milliseconds={self.milliseconds})"
        )

    @property
    def output(self) -> str:
        """output the timestamp in the format 00:00:00,000"""
        return (
            f"{self.get_value('hours')}:{self.get_value('minutes')}:"
            f"{self.get_value('seconds')},{self.get_value('milliseconds')}"
        )

    @classmethod
    def from_string(cls, timestr: str) -> "Timestamp":
        """Create a Timestamp object from a string

        :param timestr: the string to create the Timestamp from in
            the format of 00:00:00,000
        :type timestr: srt
        :return: the Timestamp object
        :rtype: Timestamp
        """
        hours, minutes, seconds = timestr.strip().split(":")
        seconds, milliseconds = seconds.split(",")
        return cls(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
        )

    def get_value(
        self, property: Literal["hours", "minutes", "seconds", "milliseconds"]
    ) -> str:
        """get the hour, minute, second or millisecond values properly formatted

        :param property: the property to get the value of
        :type property: str
        :return: the value of the property
        :rtype: str
        """
        if property in {"hours", "minutes", "seconds"}:
            return self.beautify(property)
        elif property == "milliseconds":
            return self.beautify(property, optimal_length=3, right_append=True)

    def beautify(
        self,
        property: str,
        optimal_length: int = 2,
        right_append: bool = False,
    ):
        """Beautify the property value

            adds 0s to the left or right side of the each property
            to change them into the right format that is:
            00:00:00,000

        :param optimal_length: the length that the property should be,
             2 or 3 based on the type
        :type optimal_length: int
        :param right_append: add the 0s to the right side of the property
            instead of the left
        :type right_append: bool
        :return: the property value with the right format
        :rtype: str
        """
        property = str(getattr(self, property))
        property_length = len(property)
        if property_length == optimal_length:
            return property
        elif property_length < optimal_length:
            needs = optimal_length - property_length
            if not right_append:
                return ("0" * needs) + property
            else:
                return property + ("0" * needs)


class Timing(BaseModel):
    """Timing object for a subtitle
    Timing consists of a ``start`` and ``end`` Timestamp and is
    rendered as 00:00:00,000 --> 00:00:00,000 from the ``output`` method
    """

    start: Timestamp
    end: Timestamp

    def __str__(self) -> str:
        return f"Timing(start={self.start}, end={self.end})"

    @property
    def output(self) -> str:
        """output the timing in the format 00:00:00,000 --> 00:00:00,000"""
        return f"{self.start.output} --> {self.end.output}"

    @classmethod
    def from_string(cls, start: str, end: str) -> "Timing":
        """Create a Timing object from a string
        the ``start`` and ``end`` should be in the format of 00:00:00,000

        :param start: the start Timestamp of the subtitle
        :type start: str
        :param end: the end Timestamp of the subtitle
        :type end: str
        :return: the Timing object
        :rtype: Timing
        """
        return cls(
            start=Timestamp.from_string(start),
            end=Timestamp.from_string(end),
        )


class Line(BaseModel):
    """Line object for a subtitle

    Line consists of a ``index``, ``timing`` and ``text``
    an example formatted line would be::

        1
        00:00:00,000 --> 00:00:00,000
        This is a subtitle
    """

    index: int
    timing: Timing
    text: Optional[str] = ""

    def __repr__(self) -> str:
        return (
            f"Line(index={self.index}, "
            f"timing={repr(self.timing)}, text={repr(self.text)})"
        )

    @property
    def output(self) -> str:
        """output the line in the format of::
        1
        00:00:00,000 --> 00:00:00,000
        This is a subtitle
        """
        return f"{self.index}\n{self.timing.output}\n{self.text}\n"

    @classmethod
    def from_string(cls, linestring: str) -> "Line":
        """Create a Line object from a string

        :param linestring: the string to create the Line from
        :type linestring: str
        :return: the Line object
        :rtype: Line
        """
        line = regex.ONE_LINER.match(linestring)
        if line is None:
            raise ValueError(f"{linestring} is not a valid line")
        index, start, end, text = line.groups()
        return cls(
            index=index, timing=Timing.from_string(start, end), text=text.strip()
        )
