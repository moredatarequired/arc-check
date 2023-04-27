import json
import os
from typing import Optional

import click
from pycircleci import api

from arc_check import auth

from ..__about__ import __version__

circle_client = api.Api(token=auth.get_api_token())


ARC_ORG_NAME = os.environ.get("ORG_NAME", "wandb")
ARC_REPO_NAME = os.environ.get("ORG_NAME", "wandb")


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option("--org-name", help="organization to query about", default=ARC_ORG_NAME)
@click.option("--repo", help="repo to query about", default=ARC_REPO_NAME)
@click.version_option(version=__version__, prog_name="arc")
@click.pass_context
def cli(ctx: click.Context, org_name: str, repo: str) -> None:
    """CLI for interacting with CircleCI."""
    ctx.ensure_object(dict)
    ctx.obj["org_name"] = org_name
    ctx.obj["repo"] = repo


@cli.group()
@click.option("--user-id", help="user to get information about")
def user(user_id: Optional[str]):
    """Get information about a user. Defaults to the current user."""
    if user_id:
        user_info = circle_client.get_user_id_info(user_id)
    else:
        user_info = circle_client.get_user_info()

    click.echo(json.dumps(user_info, indent=4))


@user.command()
def collaborations():
    """Get the set of organizations that the user is a member or a collaborates with."""
    collab_info = circle_client.get_user_collaborations()

    click.echo(json.dumps(collab_info, indent=4))


@cli.group()
@click.pass_context
def pipeline(ctx: click.Context):
    pass


@pipeline.command("list")
@click.pass_context
@click.option(
    "--mine/--all",
    help="only list pipelines for the current user",
    default=False,
    is_flag=True,
)
@click.option("--limit", help="maximum number of results to return", default=100)
def list_pipelines(ctx: click.Context, mine: bool, limit: int) -> None:
    """List pipelines for an organization."""
    org_name = ctx.obj["org_name"]
    pipelines = circle_client.get_pipelines(
        org_name, mine=mine, paginate=True, limit=100
    )
    click.echo(json.dumps(pipelines, indent=4))


@pipeline.command("info")
@click.argument("pipeline_id", required=True)
def get_pipeline_by_id(pipeline_id: str):
    pipeline_info = circle_client.get_pipeline(pipeline_id)
    click.echo(json.dumps(pipeline_info, indent=4))


# TODO: invert option orders; i.e.,
# `arc list pipelines` and `arc list workflows` instead of `arc pipeline list`.
# Top level commands:
# - list (pipelines, workflows, jobs, ...)
# - info (pipeline, workflow, job, ...)
