import pytest
import sys

import reportdaily as rd


def test_version(capsys):
    """
    test if the version is correct 
    """
    # given the user use the --version option
    cliargs = ["--version"]
    version = rd.__version__

    # when = expect the output of the actual version
    with pytest.raises(SystemExit):
        rd.parsecli(cliargs)
    captured = capsys.readouterr()

    # then
    assert version in captured.out


def test_help(capsys):
    """
    test if the help option is working
    """
    # given the user inputs the --help command without a subcommand
    cliargs = ["--help"]
    expected_output = "usage: "

    # when = expect  output of the help option
    with pytest.raises(SystemExit):
        rd.parsecli(cliargs)
    captured = capsys.readouterr()

    # then  check bash output if help is shown correctly
    assert expected_output in captured.out


@pytest.mark.parametrize("verbose_count", ["", "-v", "-vv", "-vvv", "-vvvv"])
def test_verbosity(verbose_count):
    """
    Test if the verbosity option was used correctly 
    """
    # given the user inputs the -v option  to add verbosity level for the logger from -v to -vvvv with an subcommand
    # example cmd  -vvvv and new
    cliargs = ["new"] if not verbose_count else [verbose_count, "new"]
    count = cliargs[0].count("v")
    search_for = "verbose"

    # when = expect  the execution of the option  + subcommand
    result = rd.parsecli(cliargs)
    # then "verbose" should be in the given namespace
    assert search_for in result
    assert result.verbose == count
