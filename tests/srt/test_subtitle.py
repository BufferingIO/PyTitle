import os
import copy
import pytest

from pytitle.srt import SrtSubtitle, Timestamp, Encodings, exceptions
from .subs.sample import sample_lines

subtitles_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "subs",
)


def test_srt_parse():
    path = os.path.join(
        subtitles_dir, "shameless.us.s03e01.720p.bluray.x264-demand.srt"
    )
    sub = SrtSubtitle.open(path)
    assert len(sub.lines) == 741


def test_srt_parse_bad_encoding():
    path = os.path.join(subtitles_dir, "Grown Ups.2010.R5.LiNE.Xvid {1337x}-Noir.srt")
    sub = SrtSubtitle.open(path)
    assert len(sub.lines) == 1373


def test_srt_parse_bad_encoding_not_detected():
    path = os.path.join(
        subtitles_dir,
        "Grown Ups.2010.R5.LiNE.Xvid {1337x}-Noir.srt",
    )
    with pytest.raises(exceptions.SrtEncodingDetectError):
        SrtSubtitle.open(path=path, fallback_encodings=Encodings(["utf-8"]))


def test_srt_parse_bad_encoding_use_chardet():
    path = os.path.join(
        subtitles_dir,
        "Grown Ups.2010.R5.LiNE.Xvid {1337x}-Noir.srt",
    )
    with pytest.raises(NotImplementedError):
        SrtSubtitle.open(
            path=path, use_chardet=True, fallback_encodings=Encodings(["utf-8"])
        )


def test_srt_save(tmpdir):
    path = os.path.join(
        subtitles_dir, "shameless.us.s03e01.720p.bluray.x264-demand.srt"
    )
    sub = SrtSubtitle.open(path)
    sub.save(path=tmpdir.join("test.srt"))
    sub2 = SrtSubtitle.open(tmpdir.join("test.srt"))
    assert len(sub2.lines) == 741


def test_srt_repr():
    path = os.path.join(
        subtitles_dir, "shameless.us.s03e01.720p.bluray.x264-demand.srt"
    )
    sub = SrtSubtitle.open(path)
    assert repr(sub) == f"SrtSubtitle(path='{path}', lines=741, encoding='utf-8'"


def test_srt_no_line_to_output():
    sub = SrtSubtitle()
    with pytest.raises(ValueError):
        sub.output


def test_srt_save_no_path():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    with pytest.raises(exceptions.SrtSaveError):
        sub.save()


# TODO: test for subtitle generation and editing


def test_srt_generate(tmpdir):
    sub = SrtSubtitle(lines=sample_lines)
    assert sub.lines[0].index == 1
    assert sub.lines[0].text == "Hello from First line!"
    sub.save(path=tmpdir.join("test_gen.srt"))
    sub2 = SrtSubtitle.open(tmpdir.join("test_gen.srt"))
    assert len(sub2.lines) == 4
    assert (
        sub.lines[3].text
        == "Hello from Fourth line!\nThis line has a second text line."
    )


def test_srt_shift_add():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift(Timestamp(seconds=10))
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=22, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=40, milliseconds=321
    )

    assert sub.lines[1].timing.start == Timestamp(
        hours=0, minutes=2, seconds=45, milliseconds=455
    )
    assert sub.lines[1].timing.end == Timestamp(
        hours=0, minutes=3, seconds=8, milliseconds=321
    )


def test_srt_shift_sub():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift(Timestamp(seconds=10), backward=True)
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=2, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=20, milliseconds=321
    )

    assert sub.lines[1].timing.start == Timestamp(
        hours=0, minutes=2, seconds=25, milliseconds=455
    )
    assert sub.lines[1].timing.end == Timestamp(
        hours=0, minutes=2, seconds=48, milliseconds=321
    )


def test_srt_shift_errors():
    sub2 = SrtSubtitle()
    with pytest.raises(ValueError):
        sub2.shift(Timestamp(seconds=10), indexes=[1, 2])
    with pytest.raises(ValueError):
        sub2.shift(Timestamp(seconds=10))


def test_srt_shift_forward_indexes():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift_forward(seconds=10, index=[1, 2])
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=22, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=40, milliseconds=321
    )

    assert sub.lines[1].timing.start == Timestamp(
        hours=0, minutes=2, seconds=45, milliseconds=455
    )
    assert sub.lines[1].timing.end == Timestamp(
        hours=0, minutes=3, seconds=8, milliseconds=321
    )


def test_srt_shift_no_time_specified():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    with pytest.raises(ValueError):
        sub.shift_forward(index=1)
    with pytest.raises(ValueError):
        sub.shift_backward(index=1)


def test_srt_shift_backward_indexes():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift_backward(seconds=10, index=[1, 2])
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=2, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=20, milliseconds=321
    )

    assert sub.lines[1].timing.start == Timestamp(
        hours=0, minutes=2, seconds=25, milliseconds=455
    )
    assert sub.lines[1].timing.end == Timestamp(
        hours=0, minutes=2, seconds=48, milliseconds=321
    )


def test_srt_shift_forward_index():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift_forward(seconds=10, index=1)
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=22, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=40, milliseconds=321
    )


def test_srt_shift_backward_index():
    sub = SrtSubtitle(lines=copy.deepcopy(sample_lines))
    sub.shift_backward(seconds=10, index=1)
    assert sub.lines[0].timing.start == Timestamp(
        hours=0, minutes=2, seconds=2, milliseconds=455
    )
    assert sub.lines[0].timing.end == Timestamp(
        hours=0, minutes=2, seconds=20, milliseconds=321
    )
