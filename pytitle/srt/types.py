import os
import sys
from typing import Literal, Optional, Union, List

from pydantic import BaseModel, Field

from . import regex
from . import exceptions

if sys.version_info >= (3, 9):
    PathType = Union[Union[str, bytes, os.PathLike[str], os.PathLike[bytes]], int]
else:
    PathType = Union[str, bytes, os.PathLike]


class Timestamp(BaseModel):
    """The Timestamp object is used to store the start or end of a subtitle
    the Timestamp is rendered as 00:00:00,000 from the ``output`` property
    """

    hours: int = Field(0, ge=0)
    minutes: int = Field(0, lt=60, ge=0)
    seconds: int = Field(0, lt=60, ge=0)
    milliseconds: int = Field(0, lt=1000, ge=0)

    def __repr__(self) -> str:
        return (
            f"Timestamp(hours={self.hours}, minutes={self.minutes}, "
            f"seconds={self.seconds}, milliseconds={self.milliseconds})"
        )

    def __add__(self, obj: "Timestamp") -> "Timestamp":
        """
        Add two Timestamp objects together with + operator
        """
        overflow_const = [1000, 60, 60, float("inf")]
        attrs = ["milliseconds", "seconds", "minutes", "hours"]
        overflow = 0
        for attr, ov_const in zip(attrs, overflow_const):
            # loop through each attribute in order and add the
            # attribute value of self + attribute value of obj + overflow
            # if the result is greater than the overflow constant,
            # add 1 to the overflow and subtract the overflow constant from the result
            # this way we can make sure that the values stay in range
            # for example if the result of seconds is 70,,
            # set the seconds to 10 and add 1 to minutes
            t = getattr(self, attr) + getattr(obj, attr) + overflow
            overflow = 0
            if t >= ov_const:
                overflow = t // ov_const
            setattr(self, attr, int(t % ov_const))
        return self

    def __sub__(self, obj: "Timestamp") -> "Timestamp":
        """
        Subtract a Timestamp object from another with - oberator
        """
        milliseconds = self.milliseconds - obj.milliseconds
        if milliseconds < 0:
            milliseconds += 1000
            self.seconds -= 1
        seconds = self.seconds - obj.seconds
        if seconds < 0:
            seconds += 60
            self.minutes -= 1
        minutes = self.minutes - obj.minutes
        if minutes < 0:
            minutes += 60
            self.hours -= 1
        hours = self.hours - obj.hours
        if hours < 0:
            raise exceptions.NegativeTimestampError(
                "Timestamp subtraction reached negative value"
            )

        return Timestamp(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
        )

    def __gt__(self, obj: "Timestamp") -> bool:
        """
        Check if a Timestamp object is greater than another with > operator
        """
        if (
            self.hours > obj.hours
            or (self.hours == obj.hours and self.minutes > obj.minutes)
            or (
                self.hours == obj.hours
                and self.minutes == obj.minutes
                and self.seconds > obj.seconds
            )
            or (
                self.hours == obj.hours
                and self.minutes == obj.minutes
                and self.seconds == obj.seconds
                and self.milliseconds > obj.milliseconds
            )
        ):
            return True
        return False

    def __lt__(self, obj: "Timestamp") -> bool:
        """
        Check if a Timestamp object is less than another with < operator
        """
        if (
            self.hours < obj.hours
            or (self.hours == obj.hours and self.minutes < obj.minutes)
            or (
                self.hours == obj.hours
                and self.minutes == obj.minutes
                and self.seconds < obj.seconds
            )
            or (
                self.hours == obj.hours
                and self.minutes == obj.minutes
                and self.seconds == obj.seconds
                and self.milliseconds < obj.milliseconds
            )
        ):
            return True
        return False

    def __ge__(self, obj: "Timestamp") -> bool:
        """
        Check if a Timestamp object is greater than or equal to another with >= operator
        """
        if self.__gt__(obj) or self.__eq__(obj):
            return True
        return False

    def __le__(self, obj: "Timestamp") -> bool:
        """
        Check if a Timestamp object is less than or equal to another with <= operator
        """
        if self.__lt__(obj) or self.__eq__(obj):
            return True
        return False

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
        else:
            raise ValueError(f"{property} is not a valid property")

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

    def __repr__(self) -> str:
        return f"Timing(start={repr(self.start)}, end={repr(self.end)})"

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

    def shift(
        self,
        shift_by: Timestamp,
        backward: bool = False,
        start: bool = True,
        end: bool = True,
    ) -> None:
        """Shift the timing by a Timestamp

        :param shift_by: the Timestamp to shift the timing by
        :type shift_by: Timestamp
        :param backward: shift the timing backward instead of forward
        :type backward: bool
        :param start: shift the start Timestamp
        :type start: bool
        :param end: shift the end Timestamp
        :type end: bool
        :return: None
        :rtype: None
        """
        if all([not start, not end]):
            raise ValueError("At least one of start or end must be True")
        if backward:
            if start:
                self.start -= shift_by
            if end:
                self.end -= shift_by
        else:
            if start:
                self.start += shift_by
            if end:
                self.end += shift_by


class Line(BaseModel):
    """Line object for a subtitle

    Line consists of ``index``, ``timing`` and ``text``
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
        """
        output the line in the format of::

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

    @classmethod
    def get_lines(
        cls, lines: List["Line"], index: List[int], check_contains: bool = False
    ) -> List["Line"]:
        """
        get line objects from index of them

        :param lines: the index of the lines to get
        :type lines: List[int]
        :param index: the index of the lines to get
        :type index: List[int]
        :param check_contains: check if all the indexes are in the lines
        :type check_contains: bool
        :return: the lines
        :rtype: List[Line]
        """
        lines = [line for line in lines if line.index in set(index)]
        if check_contains and len(lines) != len(index):
            raise IndexError(
                f"{index} contains lines that do not exist in the subtitle"
            )
        if len(lines) < 1:
            raise IndexError("No lines were found")
        return lines
