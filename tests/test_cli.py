from click.testing import CliRunner

from arc_check.cli import cli


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert result.output == "Hello world!\n"


def test_hello_name():
    runner = CliRunner()
    result = runner.invoke(cli, ["Igor"])
    assert result.exit_code == 0
    assert result.output == "Hello Igor!\n"
