from typing import Optional

import click

from ..__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="arc")
@click.argument("name", required=False)
@click.pass_context
def cli(ctx: click.Context, name: Optional[str] = None) -> None:
    click.echo(f"Hello {name or 'world'}!")
