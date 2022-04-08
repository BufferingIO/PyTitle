import pytest
from pytitle.srt import Timing, Timestamp


def test_timing_generation():
    timing = Timing(
        start=Timestamp(hours=0, minutes=0, seconds=0, milliseconds=0),
        end=Timestamp(hours=0, minutes=0, seconds=0, milliseconds=0),
    )
    assert timing.output == "00:00:00,000 --> 00:00:00,000"


def test_timing_from_string():
    timing = Timing.from_string(start="00:00:00,000", end="00:00:00,000")
    assert timing.output == "00:00:00,000 --> 00:00:00,000"
    assert timing.start.hours == 0
    assert timing.start.minutes == 0
    assert timing.start.seconds == 0
    assert timing.start.milliseconds == 0
    assert timing.end.hours == 0
    assert timing.end.minutes == 0
    assert timing.end.seconds == 0
    assert timing.end.milliseconds == 0


def test_timing_from_string_additional():
    timing = Timing.from_string(start="01:02:03,456", end="01:02:03,456")
    assert timing.output == "01:02:03,456 --> 01:02:03,456"
    assert timing.start.hours == 1
    assert timing.start.minutes == 2
    assert timing.start.seconds == 3
    assert timing.start.milliseconds == 456
    assert timing.end.hours == 1
    assert timing.end.minutes == 2
    assert timing.end.seconds == 3
    assert timing.end.milliseconds == 456


def test_timing_formatting():
    assert Timing(
        start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
        end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
    ) == Timing.from_string(start="01:02:03,456", end="01:02:04,567")
    assert (
        Timing(
            start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
            end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
        ).output
        == "01:02:03,456 --> 01:02:04,567"
    )


def test_timing_bad_formatting():
    assert Timing.from_string(start="1:02:03,456", end="01:02:04,567") == Timing(
        start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
        end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
    )
    assert Timing.from_string(start="01:02:03,40", end="01:02:04,567") == Timing(
        start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=40),
        end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
    )
    assert Timing.from_string(start="1:2:3,456", end="01:02:04,567") == Timing(
        start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
        end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
    )


def test_timing_shift_start_and_end_none():
    t = Timing(
        start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
        end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
    )
    with pytest.raises(ValueError):
        t.shift(Timestamp(seconds=10), start=False, end=False)
