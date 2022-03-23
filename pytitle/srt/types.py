from pydantic import BaseModel
from typing import Optional


class Duration:
    def __init__(
        self,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        **kwargs,
    ) -> None:
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def __repr__(self) -> str:
        return f"Duration(hours={self.hours}, minutes={self.minutes}, " f"seconds={self.seconds}, milliseconds={self.milliseconds})"

    def __str__(self) -> str:
        return f"{self.get_value('hours')}:{self.get_value('minutes')}:" f"{self.get_value('seconds')},{self.get_value('milliseconds')}"

    @classmethod
    def from_string(cls, timestr: str) -> "Duration":
        hour, minute, second = timestr.strip().split(":")
        second, millisecond = second.split(",")
        return cls(hour, minute, second, millisecond)

    def get_value(self, property: str) -> str:
        """get the hour, minute, second, millisecond from string"""
        if property in {"hours", "minutes", "seconds"}:
            return self.beautify(property)
        elif property == "milliseconds":
            return self.beautify(property, optimal_length=3, append=True)

    def beautify(self, property: str, optimal_length: int = 2, append: bool = False):
        """Beautify the timgin
        adds 0 to the left or right side of the each property,
        to change them into the right format that is:
            00:00:00,000
        optimal_length: the length that the property should be, 2 or 3 based on the type
        append: whether to add 0's to the left or the right side of the current property
        """
        property = str(getattr(self, property))
        property_length = len(property)
        if property_length == optimal_length:
            return property
        elif property_length < optimal_length:
            needs = optimal_length - property_length
            if not append:
                return ("0" * needs) + property
            else:
                return property + ("0" * needs)


class Timing(BaseModel):
    start: Duration
    end: Duration

    def __str__(self) -> str:
        return f"Timing(start={self.start}, end={self.end})"

    @property
    def output(self) -> str:
        return f"{self.start} --> {self.end}"

    @classmethod
    def from_string(cls, start: str, end: str) -> "Timing":
        return cls(start=Duration.from_string(start), end=Duration.from_string(end))

    class Config:
        arbitrary_types_allowed = True


class Line(BaseModel):
    index: int
    timing: Timing
    text: Optional[str] = ""

    def __str__(self) -> str:
        return f"Line(index={self.index}, " f"timing={repr(self.timing)}, text={repr(self.text)})"

    @property
    def output(self) -> str:
        return f"{self.index}\n{self.timing.output}\n{self.text}\n"
