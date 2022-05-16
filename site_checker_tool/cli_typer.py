"""This module provides the Site Checker Tool CLI Functionalities"""
# cli.py

from pathlib import Path
from typing import List 
from typing import Optional

import typer

from site_checker_tool import (
    __version__, __app_name__,
)

# ============= Initializing Typer Library
app = typer.Typer()


# ============== Function Definitions
@app.command()
def read_url(
    url_list: List[str] = typer.Option(
        str(),
        "-u",
        "--urls",
        help="enter one or more website urls",
        metavar="URLs",
    )
) -> None:
    ...


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return