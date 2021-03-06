import argparse
import re
from typing import Tuple, Optional
from datetime import timedelta

import discord
from redbot.core.commands import (
    MemberConverter,
    Context,
    BadArgument,
)  # , timedelta_converter,

__all__ = ["mute_converter"]

# I could keep this one long string, but this is much easier to read/extend.
TIME_RE_STRING = r"\s?".join(
    [
        r"((?P<days>\d+?)\s?(d(ays?)?))?",
        r"((?P<hours>\d+?)\s?(hours?|hrs|hr?))?",
        r"((?P<minutes>\d+?)\s?(minutes?|mins?|m))?",
        r"((?P<seconds>\d+?)\s?(seconds?|secs?|s))?",
    ]
)

TIME_RE = re.compile(TIME_RE_STRING, re.I)


def timedelta_converter(argument: str) -> timedelta:
    """
    Attempts to parse a user input string as a timedelta

    Arguments
    ---------
    argument: str
        String to attempt to treat as a timedelta

    Returns
    -------
    datetime.timedelta
        The parsed timedelta
    
    Raises
    ------
    ~discord.ext.commands.BadArgument
        No time was found from the given string.
    """
    matches = TIME_RE.match(argument)
    params = {k: int(v) for k, v in matches.groupdict().items() if v is not None}
    if not params:
        raise BadArgument("I couldn't turn that into a valid time period.")
    return timedelta(**params)


class NoExitArgparse(argparse.ArgumentParser):
    def error(self, message):
        raise BadArgument(None, None)


def mute_converter(argument: str) -> Tuple[Optional[str], Optional[timedelta]]:
    """
    Valid uses:
        User
        -t [timedelta]
        --reason being an ass
        -r timeout --timed 1hr
    """
    mute_parser = NoExitArgparse(
        description="Mute Parser", add_help=False, allow_abbrev=True
    )
    mute_parser.add_argument("--reason", "-r", nargs="*", dest="reason", default="")
    mute_parser.add_argument("--timed", "-t", nargs="*", dest="timed", default="")
    vals = mute_parser.parse_args(argument.split())
    reason = " ".join(vals.reason) or None
    time_interval = timedelta_converter((" ".join(vals.timed))) if vals.timed else None
    return reason, time_interval
