from pytitle.srt import Line, Timing, Timestamp

sample_lines = [
    Line(
        index=1,
        timing=Timing(
            start=Timestamp(hours=0, minutes=2, seconds=12, milliseconds=455),
            end=Timestamp(hours=0, minutes=2, seconds=30, milliseconds=321),
        ),
        text="Hello from First line!",
    ),
    Line(
        index=2,
        timing=Timing(
            start=Timestamp(hours=0, minutes=2, seconds=35, milliseconds=455),
            end=Timestamp(hours=0, minutes=2, seconds=58, milliseconds=321),
        ),
        text="Hello from Second line!",
    ),
    Line(
        index=3,
        timing=Timing(
            start=Timestamp(hours=0, minutes=3, seconds=0, milliseconds=455),
            end=Timestamp(hours=0, minutes=3, seconds=30, milliseconds=321),
        ),
        text="Hello from Third line!",
    ),
    Line(
        index=4,
        timing=Timing(
            start=Timestamp(hours=0, minutes=6, seconds=12, milliseconds=455),
            end=Timestamp(hours=0, minutes=6, seconds=30, milliseconds=321),
        ),
        text="Hello from Fourth line!\nThis line has a second text line.",
    ),
]
