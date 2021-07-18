#!/usr/bin/env python3
"""
Example of serving an Application using the `aiohttp.web` CLI.

Serve this app using::

    $ python -m aiohttp.web -H localhost -P 8080 --repeat 10 cli_app:init \
    > "Hello World"

Here ``--repeat`` & ``"Hello World"`` are application specific command-line
arguments. `aiohttp.web` only parses & consumes the command-line arguments it
needs (i.e. ``-H``, ``-P`` & ``entry-func``) and passes on any additional
arguments to the `cli_app:init` function for processing.
"""

from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence, TypedDict

from aiohttp import web


class StateDict(TypedDict):
    args: Namespace


async def display_message(req: web.Request[StateDict]) -> web.StreamResponse:
    args = req.app.state["args"]
    text = "\n".join([args.message] * args.repeat)
    return web.Response(text=text)


def init(argv: Optional[Sequence[str]]) -> web.Application[StateDict]:
    arg_parser = ArgumentParser(
        prog="aiohttp.web ...", description="Application CLI", add_help=False
    )

    # Positional argument
    arg_parser.add_argument("message", help="message to print")

    # Optional argument
    arg_parser.add_argument(
        "--repeat", help="number of times to repeat message", type=int, default="1"
    )

    # Avoid conflict with -h from `aiohttp.web` CLI parser
    arg_parser.add_argument(
        "--app-help", help="show this message and exit", action="help"
    )

    args = arg_parser.parse_args(argv)

    app: web.Application[StateDict] = web.Application()
    app.state["args"] = args
    app.router.add_get("/", display_message)

    return app
