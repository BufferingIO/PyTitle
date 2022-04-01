from pytitle.srt import Line, Timing, Timestamp


def test_line_generation():
    line = Line(
        index=1,
        timing=Timing(
            start=Timestamp(hours=0, minutes=12, seconds=34, milliseconds=567),
            end=Timestamp(hours=0, minutes=12, seconds=36, milliseconds=890),
        ),
        text="Hello, World!",
    )
    assert line.index == 1
    assert line.timing.start.output == "00:12:34,567"
    assert line.timing.end.output == "00:12:36,890"
    assert line.output == "1\n00:12:34,567 --> 00:12:36,890\nHello, World!\n"


def test_line_from_string():
    line = Line.from_string("1\n00:12:34,567 --> 00:12:36,890\nHello, World!\n")
    assert line.index == 1
    assert line.timing == Timing(
        start=Timestamp(hours=0, minutes=12, seconds=34, milliseconds=567),
        end=Timestamp(hours=0, minutes=12, seconds=36, milliseconds=890),
    )
    assert line.timing.start.output == "00:12:34,567"
    assert line.timing.end.output == "00:12:36,890"
    assert line.timing.start.hours == 0
    assert line.timing.end.milliseconds == 890
    assert line.output == "1\n00:12:34,567 --> 00:12:36,890\nHello, World!\n"


def test_line_formatting():
    assert Line(
        index=1,
        timing=Timing(
            start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
            end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
        ),
        text="Hello, World!",
    ) == Line.from_string("1\n01:02:03,456 --> 01:02:04,567\nHello, World!\n")
    assert (
        Line(
            index=1,
            timing=Timing(
                start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
                end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
            ),
            text="Hello, World!",
        ).output
        == "1\n01:02:03,456 --> 01:02:04,567\nHello, World!\n"
    )


def test_line_bad_formatting():
    assert Line.from_string(
        "1\n01:02:03,456 --> 01:02:04,567\n\nHello, World!\n\n\n"
    ) == Line(
        index=1,
        timing=Timing(
            start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=456),
            end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
        ),
        text="Hello, World!",
    )
    assert Line.from_string("1\n1:02:3,40 --> 01:2:04,567\nHello, World!\n") == Line(
        index=1,
        timing=Timing(
            start=Timestamp(hours=1, minutes=2, seconds=3, milliseconds=40),
            end=Timestamp(hours=1, minutes=2, seconds=4, milliseconds=567),
        ),
        text="Hello, World!",
    )
