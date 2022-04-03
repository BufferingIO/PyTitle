import re

LINE_RE = (
    # group 1
    r"^\s*(\d+:\d+:\d+,\d+)"  # line starts with any number of whitespace
    # and followed by a time format like 00:00:00,000
    r"[^\S\n]+-{2,3}>[^\S\n]+"  # match for --> with one or more spaces before and after
    # group 2:
    r"(\d+:\d+:\d+,\d+)\n\s*"  # time format again
    # ended with a new line(\n) and any number of spaces
    # group 3:
    r"((?:(?!\d+:\d+:\d+,\d+\b|\n+\d+$).*(?:\n|$))*)"
    # non-capturing group with negative lookahead to
    # assert that it doesn't hit a timestamp or a line with only a number on it
    # everything between that and
    # non capturing group that matches a new line or an empty line
)
LINE = re.compile(
    LINE_RE,
    re.MULTILINE,
)

ONE_LINER_RE = r"^\s*(\d+)\s*\n" + LINE_RE

ONE_LINER = re.compile(ONE_LINER_RE, re.MULTILINE)
