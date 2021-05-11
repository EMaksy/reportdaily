import pytest
import sys
import reportdaily as rd
from reportdaily import CONFIGPATH
from datetime import date

# import monkey patching
from unittest.mock import patch
import builtins

import os

#import namespace
from argparse import Namespace

#import configparser
import configparser

# required for fixture
import pathlib


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


def test_show_config():
    """Check if the config file is displayed correctly"""

    # given the user  see his existing config  the displayed data  should be correct


def test_create_config_with_given_namespace(tmp_path: pathlib.Path):
    # was müssen wir testen  ?
    # hat die funktion eine datei erstellt im configpath ?
    # ist der inhalt dieser datei der selbe wie unsere angaben

    # given

    today_date = date.today()

    args = Namespace(cliargs=["init"], name="NameTest",
                     team="TeamName", year=int(2020))
    find_section = ["settings"]
    find_options = ["name", "team", "start_year", "current_day"]
    configpath = tmp_path / "reportdailyrc"

    # required mock_input
    # def mock_input(txt):
    #    return name, team, year

    # when
    # when = expect  output of the help option

    rd.create_config(args, configpath)

    config = configparser.ConfigParser()
    config.read(configpath)

    # then
    assert os.path.exists(configpath) is True
    # assert config.has_section(find_section)
    for section in find_section:
        assert config.has_section(section)
        for key in find_options:
            assert config.has_option(section, key)

            #assert args.__dict__[key] in config[section][key]
           # assert args.name in config[find_section]["name"]
           # assert args.team in config[find_section]
            #assert args.year in config[find_section]
