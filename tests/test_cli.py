from lodestar_veritas import cli


def test_cli_has_main():
    assert callable(cli.main)