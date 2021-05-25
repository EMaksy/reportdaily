# import configparser
import configparser

import reportdaily as rd
# required for fixture
import pathlib
import os

from datetime import date
# import namespace
from argparse import Namespace


# monkey patching
from unittest.mock import patch
import builtins
# grab os output
import subprocess

import pytest

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

ARGS_CHANGE_CMD = Namespace(cliargs=["init"], change=True, name="ChangeName",
                            team="ChangeTeamName", year="2020")

ARGS_CHANGE = Namespace(
    cliargs=["init"], name=None,  team=None, year=None, change=True)


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


def test_change_config_namespace(tmp_path: pathlib):
    """This test will check if the change option works"""
# GIVEN
# given values for config creation ARGS: name="NameTest",team="TeamName", year=int(2020)
# given values for change ARGS_CHANGE_CMD:  cliargs=["init -c"], name="ChangeName", team="ChangeTeamName", year=int(2020)
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
    print(ARGS_CHANGE_CMD)
    # use change config with namespace
    rd.namespace_config_change(ARGS_CHANGE_CMD, configpath)
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


@pytest.mark.parametrize("user_category,user_change,user_key",
                         [("Name", "TestInputName", "name"),
                          ("Team", "TestInputTeam", "team"),
                          ("Year", "TestInputYear", "start_year"),
                          ])
def test_change_by_input(tmp_path: pathlib.Path,  user_category, user_change, user_key):
 #   #This test will simulate user input and check if  the changes were done correctly

    # GIVEN
    # ARGS to create  a config file in the first place
    configpath = tmp_path / "reportdailyrc"
    # simulated user input
    # user_category
    # no need in this variable , dont forget to delete!!!
    user_input_str = user_change
    user_keys = user_key

    # WHEN
    # create a config file
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    # open config and save it for visability
    with open(configpath, 'r') as configfile:
        configs_before_change = dict(config.items("settings"))
    # save dict before changes
    print(configs_before_change)

    # patch your input
    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        if txt.lower().startswith("name"):
            print(user_category)
            return user_category

        elif txt.lower().startswith("enter"):
            print(user_input_str)
            return user_input_str

    with patch.object(builtins, 'input', mock_input):
        rd.user_input_change(ARGS_CHANGE, configpath)
    # read changed value
    config.read(configpath)
    configs_after_change = dict(config.items("settings"))
    print(configs_after_change.get(user_keys))

    # THEN
    assert configs_after_change.get(user_keys) == user_input_str


"""
def test_wrong_input_change(tmp_path: pathlib):
    
    # GIVEN
    user_wrong_input = "TEST"
    user_right_input = "Name"
    user_canged_value = "TESTNAME"
    awaited_output = "No key in config found --> Try again"

    # path
    configpath = tmp_path / "reportdailyrc"
    # Given Namespace for the change command
    # ARGS_CHANGE = Namespace(
    # cliargs=["init"], name=None,  team=None, year=None, change=True)
    # Use this Namespace so create a config for the test
    # ARGS = Namespace(cliargs=["init"], name="NameTest",
    #             team="TeamName", year="2020")
    # Grab sdtout

    # WHEN
    # create a config file
    rd.create_config(ARGS, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    # open config and save it for visability
    with open(configpath, 'r') as configfile:
        configs_before_change = dict(config.items("settings"))
    # save dict before changes
    print(configs_before_change)

    # simultate input of user

    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        run_once = int(0)
        while 1:
            if txt.lower().startswith("name") and run_once == 0:
                print("wrong input")
                run_once += 1
                return user_wrong_input
            if txt.lower().startswith("name") and run_once == 1:
                print("Right input")
                run_once += 1
                return user_right_input
            if txt.lower().startswith("enter") and run_once == 2:
                run_once += 1
                return user_canged_value
            break
            # patch the input
    with patch.object(builtins, 'input', mock_input):
        # run config input function
        rd.user_input_change(ARGS_CHANGE, configpath)
    # THEN
    #assert awaited_output in given_output
"""


def test_create_config_user_input(tmp_path: pathlib):

    # GIVEN
    name = "TESTNAME"
    team = "TESTTEAM"
    year = "2020"
    ARGS_USER_INPUT = Namespace(
        cliargs=["init"], name=None,  team=None, year=None)
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    # patch the input of user
    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        if txt.lower().startswith("enter your name"):
            return name
        if txt.lower().startswith("enter your team"):
            return team
        if txt.lower().startswith("in which"):
            return year

    with patch.object(builtins, 'input', mock_input):
        rd.create_config(ARGS_USER_INPUT, configpath)

    # open configs
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_after_creation = dict(config.items("settings"))

    # THEN
    assert configs_after_creation.get("name") == name
    assert configs_after_creation.get("team") == team
    assert configs_after_creation.get("start_year") == year
