# import configparser
import configparser

import reportdaily as rd
# required for fixture
import pathlib
import os

from datetime import date
# import namespace
from argparse import Namespace


# Global data
STANDARD_SECTIONS = ["settings"]
STANDARD_OPTIONS = ["name", "team", "start_year", "current_day"]
STANDARD_CONFIG = {  # Section_name: list of key names
    "settings": ("name", "team", "start_year", "current_day"),
    # "test": ("test1", "test2"),
    # ...
}
ARGS = Namespace(cliargs=["init"], name="NameTest",
                 team="TeamName", year="2020")

ARGS_CHANGE = Namespace(cliargs=["init"], change=True, name="ChangeName",
                        team="ChangeTeamName", year="2020")


def test_config_exists(tmp_path: pathlib.Path):
    """This test will tests if the config exists"""
    # given
    # ARGS
    configpath = tmp_path / "reportdailyrc"

    # when = expect  a config file is created in tmp_path
    rd.create_config(ARGS, configpath)

    # then config file existence is true
    assert os.path.exists(configpath) is True


def test_config_section_option_namespace(tmp_path: pathlib.Path):
    """This test will check the config file if the sections and options are  correct"""
    # given
    # ARGS
    # STANDARD_SECTIONS
    # STANDARD_OPTIONS
    configpath = tmp_path / "reportdailyrc"

    # when
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)

    # then
    for section in STANDARD_SECTIONS:
        assert config.has_section(section)
        for key in STANDARD_OPTIONS:
            assert config.has_option(section, key)


def test_config_values(tmp_path: pathlib):
    """This test  will prove the values of the config file"""
    # given
    # ARGS
    # STANDARD_CONFIG
    # convert date obj to string
    date_today = date.today()
    date_string = date_today.strftime("%Y-%m-%d")

    expected = ["NameTest", "TeamName",  "2020", date_string]
    configpath = tmp_path / "reportdailyrc"

    # when
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)

    # then
    for section, options in STANDARD_CONFIG.items():
        count = 0
        for opt in options:
            assert config.get(section, opt) == expected[count]
            count = count+1


def test_config_real_section(tmp_path: pathlib):
    """This test will check if all the sections are correct"""
    # given
    # ARGS
    # STANDART_CONFIG
    std_keys = set(STANDARD_CONFIG)
    configpath = tmp_path / "reportdailyrc"

    # when
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    real_keys = set(config.keys())
    # need to delete default key. DEFAULT is created automatically by the configparser module.
    real_keys.remove("DEFAULT")

    # then
    assert real_keys == std_keys


def test_show_config(tmp_path: pathlib):
    """This test will check if the output is correct """
    # GIVEN
    # ARGS
    # a config file is created
    # expected output of show config
    # This will be finished in a later release

    # noch ein test , modul wo du über alle sections iterieren kannst  um zu überprüfen ob alle  sections und options in config vorhanden sind
    # gettattr(args var) var = bar  --> zugriff auf namespace
    # Welche tests brauchen wir noch ?
    # Cheat sheet was kann dict alles ?
    # was ist ein set und wir nehmen die menge aus file - die menge aus globalen variablen


def test_change_config_namespace(tmp_path: pathlib):
    """This test will check if the change option works"""
# GIVEN
# given values for config creation ARGS: name="NameTest",team="TeamName", year=int(2020)
# given values for change ARGS_CHANGE:  cliargs=["init -c"], name="ChangeName", team="ChangeTeamName", year=int(2020)
    configpath = tmp_path / "reportdailyrc"
    data_after_change_dict = {'name': 'ChangeName', 'team': 'ChangeTeamName',
                              'start_year': '2020'}

# WHEN
# the user input reportdaily init -c  with another option and their  values the config file should be changed
# create config file  and read it
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_before_change = configfile.read()
    print(configs_before_change)
    # save all values
    configs_before_change_dict = dict(config.items("settings"))

    # show the change namespace
    print(ARGS_CHANGE)
    # use change config with namespace
    rd.namespace_config_change(ARGS_CHANGE, configpath)
    # save the changed config
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        config_after_change = configfile.read()
    # output of the changed content
    print(config_after_change)
    # save all values
    configs_after_change_dict = dict(config.items("settings"))

# THEN
# check if the file has changed
    assert configs_before_change != config_after_change

# check if the  the values are changed as given
    print(configs_before_change_dict)
    print(configs_after_change_dict)
    print(data_after_change_dict)
    # prove if the expexted values are in our changed config
    assert data_after_change_dict.items() <= configs_after_change_dict.items()
