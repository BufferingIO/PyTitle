from pytitle.srt import Timestamp


def test_timestamp_generation():
    timestamp = Timestamp(hours=0, minutes=0, seconds=0, milliseconds=0)
    assert timestamp.output == "00:00:00,000"


def test_timestamp_from_string():
    timestamp = Timestamp.from_string("00:00:00,000")
    assert timestamp.output == "00:00:00,000"
    assert timestamp.hours == 0
    assert timestamp.minutes == 0
    assert timestamp.seconds == 0
    assert timestamp.milliseconds == 0


def test_timestamp_from_string_additional():
    timestamp = Timestamp.from_string("01:02:03,456")
    assert timestamp.hours == 1
    assert timestamp.minutes == 2
    assert timestamp.seconds == 3
    assert timestamp.milliseconds == 456


def test_timestamp_formatting():
    assert Timestamp(
        hours=1, minutes=2, seconds=3, milliseconds=456
    ) == Timestamp.from_string("01:02:03,456")
    assert (
        Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456).output
        == "01:02:03,456"
    )


def test_timestamp_bad_formatting():
    assert Timestamp.from_string("1:02:03,456") == Timestamp(
        hours=1, minutes=2, seconds=3, milliseconds=456
    )
    assert Timestamp.from_string("01:02:03,40") == Timestamp(
        hours=1, minutes=2, seconds=3, milliseconds=40
    )
    assert Timestamp.from_string("1:2:3,456") == Timestamp(
        hours=1, minutes=2, seconds=3, milliseconds=456
    )
