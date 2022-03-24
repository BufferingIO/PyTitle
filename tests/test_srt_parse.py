import os

from pytitle.srt import SrtSubtitle

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
