from click.testing import CliRunner

from wakeword_training_record.__main__ import create


def test_create_cli(tmpdir):

    runner = CliRunner()
    result = runner.invoke(create, [str(tmpdir), "testordet", "sv"])
    assert result.exit_code == 0
    assert len(tmpdir.listdir()) == 1
