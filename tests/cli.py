import click
from click.testing import CliRunner
from click_app import configure, cli

def test_command_configure():
    runner = CliRunner()
    result = runner.invoke(cli, ["configure"])
    assert result.exit_code == 0
    assert result.output == 'configure'