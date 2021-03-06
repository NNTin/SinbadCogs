import yaml
import discord

from redbot.core import commands
from .serialize import template, deserialize_embed
from .utils import parse_time


async def embed_from_userstr(ctx: commands.Context, string: str) -> discord.Embed:
    ret = {"initable": {}, "settable": {}, "fields": []}
    string = string.strip()
    if string.startswith("```") and string.endswith("```"):
        string = "\n".join(string.split("\n")[1:-1])

    parsed = yaml.safe_load(string)
    ret["fields"] = [x[1] for x in sorted(parsed.get("fields", {}).items())]

    for outer_key in ["initable", "settable"]:
        for inner_key in template[outer_key].keys():
            to_set = parsed.get(inner_key, {})
            if to_set:
                if inner_key == "timestamp":
                    try:
                        to_set = parse_time(to_set).timestamp()
                    except Exception:
                        x = float(to_set)

                if inner_key in ["color", "colour"]:
                    try:
                        x = (
                            await commands.converter.ColourConverter().convert(
                                ctx, to_set
                            )
                        ).value
                    except Exception:
                        try:
                            to_set = int(to_set)
                        except Exception:
                            raise
                    else:
                        to_set = x

                ret[outer_key][inner_key] = to_set

    return deserialize_embed(ret)
