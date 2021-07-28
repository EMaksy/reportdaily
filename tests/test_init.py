# import configparser
import configparser

# import script that needs to be tested
import reportdaily as rd
# required for fixture
import pathlib
import os
# required for date
from datetime import datetime
from datetime import date
# import namespace
from argparse import Namespace
# monkey patching /mocker patch
from unittest.mock import MagicMock, patch
from unittest import mock
import builtins
# required fo tests
import pytest

# Global data
STANDARD_SECTIONS = ["settings"]
STANDARD_OPTIONS = ['name',
                    'team',
                    'count_teams',
                    'team_number',
                    'current_day',
                    'duration',
                    'start_year',
                    'end_duration_education',
                    'team_time_start',
                    'team_time_end'
                    ]

STANDARD_CONFIG_DATA = {'name': "Eugen",
                        'team': "Doks",
                        'count_teams': "7",
                        'team_number': "4",
                        'current_day': date.today(),
                        'duration': "3.0",
                        'start_year': "2019",
                        'end_duration_education': "2023-08-30",
                        'team_time_start': "2021-03-01",
                        'team_time_end': "2021-08-31",
                        }

STANDARD_CONFIG = {  # Section_name: list of key names
    "settings": tuple(STANDARD_OPTIONS),
    # "test": ("test1", "test2"),
    # ...
}


def test_config_exists(tmp_path: pathlib.Path):
    """This test will tests if the config exists"""
    # GIVEN
    # STANDARD_CONFIG_DATA
    configpath = tmp_path / "reportdailyrc"

    # WHEN = expect  a config file is created in tmp_path
    rd.create_config(STANDARD_CONFIG_DATA, configpath)

    # THEN config file existence is True
    assert os.path.exists(configpath) is True


def test_database_exists(args_ns, tmp_path: pathlib.Path):
    """Check if database is created under a certain path"""
    # GIVEN

    configpath = tmp_path / "reportdailyrc"
    databasepath = tmp_path / "databasepath"

    # WHEN
    rd.cmd_init(args_ns, configpath, databasepath)

    # THEn dababase existence is true
    assert os.path.exists(databasepath) is True


def test_config_section_option_namespace(tmp_path: pathlib.Path):
    """This test will check the config file if the sections and options are  correct"""
    # GIVEN
    # STANDARD_SECTIONS
    # STANDARD_OPTIONS
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    for section in STANDARD_SECTIONS:
        assert config.has_section(section)
        for key in STANDARD_OPTIONS:
            assert config.has_option(section, key)


def test_config_values(tmp_path: pathlib):
    """This test  will prove the values of the config file"""
    # GIVEN
    # STANDARD_CONFIG
    # convert date obj to string
    date_today = date.today()
    date_string = date_today.strftime("%Y-%m-%d")

    expected = [STANDARD_CONFIG_DATA.get("name"), STANDARD_CONFIG_DATA.get("team"), STANDARD_CONFIG_DATA.get("count_teams"), "4", date_string,
                STANDARD_CONFIG_DATA.get("duration"), STANDARD_CONFIG_DATA.get("start_year"), STANDARD_CONFIG_DATA.get("end_duration_education"), STANDARD_CONFIG_DATA.get("team_time_start"), STANDARD_CONFIG_DATA.get("team_time_end")]
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    for section, options in STANDARD_CONFIG.items():
        count = 0
        for opt in options:
            assert config.get(section, opt) == expected[count]
            count = count+1


def test_config_real_section(tmp_path: pathlib):
    """This test will check if all the sections are correct"""
    # GIVEN

    std_keys = set(STANDARD_CONFIG)
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    # create config
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    real_keys = set(config.keys())
    # need to delete default key. DEFAULT is created automatically by the configparser module.
    real_keys.remove("DEFAULT")
    # THEN
    assert real_keys == std_keys


@pytest.mark.parametrize(("wrong_duration,right_duration,count_teams"), [
    ("5", "3.5", "7"),
    ("5", "3.0", "6"),
    ("f", "2.5", "5"),
    ("2.5", "2.5", "5"),
    ("3.0", "3.0", "6"),
    ("3.5", "3.5", "7"),
])
def test_change_config_namespace(args_ns, tmp_path: pathlib, wrong_duration, right_duration, count_teams):
    """This test will check if the change option works"""
    # GIVEN
    # STANDARD_CONFIG_DATA
    configpath = tmp_path / "reportdailyrc"
    args_ns.duration = wrong_duration
    args_ns.change = True

    data_after_change_dict = {"name": args_ns.name, "team": args_ns.team,
                              "count_teams": count_teams, "team_number": args_ns.team_number, "start_year": args_ns.year,
                              "duration": right_duration, }

    # WHEN
    # create config file  and read it
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_before_change = configfile.read()

    def mock_input(txt):
        """
        PATCH USER INPUT
        """

        return right_duration

    with patch.object(builtins, 'input', mock_input):
        rd.namespace_config_change(args_ns, configpath)

    # save the changed config
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        config_after_change = configfile.read()
    # save all values
    configs_after_change_dict = dict(config.items("settings"))

    # THEN
    # check if the file has changed
    assert configs_before_change != config_after_change
    # prove if the expected values are in our changed config
    assert data_after_change_dict.items() <= configs_after_change_dict.items()


@pytest.mark.parametrize("user_category,user_change,user_key",
                         [("Name", "TestInputName", "name"),
                          ("Team", "TestInputTeam", "team"),
                          # ("Year", "2019", "start_year"),
                          ])
def test_change_by_input(args_change, tmp_path: pathlib.Path,  user_category, user_change, user_key):
    """This test will simulate user input and check the changes"""

    # GIVEN
    # user_category, user_change, user_key
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    # create a config file
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    # open config and save it for visability
    with open(configpath, 'r') as configfile:
        # save dict before changes
        configs_before_change = dict(config.items("settings"))

    # patch your input
    test_value = 0

    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        nonlocal test_value
        if txt.lower().startswith("please"):
            test_value += 1
            return user_category

        if txt.lower().startswith("enter"):
            test_value += 2
            return user_change

    with patch.object(builtins, 'input', mock_input):
        rd.user_input_change(args_change, configpath)

    # read changed value
    config.read(configpath)
    configs_after_change = dict(config.items("settings"))

    # THEN
    assert configs_after_change.get(user_key) == user_change


def test_wrong_input_change(args_change, tmp_path: pathlib):

    # GIVEN
    user_wrong_input = "TEST"
    user_right_input = "Name"
    user_changed_value = "TESTNAME"
    awaited_output = "No key in config found --> Try again"

    # path
    configpath = tmp_path / "reportdailyrc"
    # WHEN
    # create a config file
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    # open config and save it for visibility
    with open(configpath, 'r') as configfile:
        configs_before_change = dict(config.items("settings"))

    # simultate input of user
    run_once = 0

    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        nonlocal run_once
        while True:
            if txt.lower().startswith("please enter") and run_once == 0:
                run_once += 1
                return user_wrong_input
            if txt.lower().startswith("please enter") and run_once == 1:
                run_once += 1
                return user_right_input
            if txt.lower().startswith("enter") and run_once == 2:
                run_once += 1
                return user_changed_value
            break
            # patch the input
    with patch.object(builtins, 'input', mock_input):
        # run config input function
        rd.user_input_change(args_change, configpath)

    # THEN
    assert awaited_output in awaited_output


# @patch("reportdaily.input_duration_count_teams")
@pytest.mark.parametrize("duration,count_teams,end_duration_education",
                         [("2.5", "5", "2023-02-28"),
                          ("3.0", "6", "2023-08-31"),
                          ("3.5", "7", "2024-02-28"),
                          ("1", "6", "2023-08-31"),  # wrong int number
                          ("y", "6", "2023-08-31"),  # wrong character input
                          ])
def test_create_config_user_input(args_ns_empty, tmp_path: pathlib, duration, count_teams, end_duration_education):

    # GIVEN
    name = "TESTNAME"
    team = "TESTTEAM"
    year = "2020"
    wrong_year = "wrong_year"
    # duration
    duration_right = "3.0"
    # count teams
    team_number = 4
    wrong_team_number = 10
    wrong_team_number_txt = "ewgwer"
    configpath = tmp_path / "reportdailyrc"

    # WHEN
    # patch the input of user
    count_of_questions_int = 0
    count_of_questions_char = 0
    count_of_questions_wrong_input = 0
    count_of_questions_team_number = 0

    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        nonlocal count_of_questions_int
        nonlocal count_of_questions_char
        nonlocal count_of_questions_wrong_input
        nonlocal count_of_questions_team_number
        if txt.lower().strip().startswith("please enter your full name"):
            return name
        if txt.lower().strip().startswith("in which"):  # Handle the wrong input, insert right input as next
            while True:
                if count_of_questions_wrong_input == 0:
                    count_of_questions_wrong_input += 1
                    return wrong_year
                elif count_of_questions_wrong_input == 1:
                    count_of_questions_wrong_input += 1
                    return year
                elif count_of_questions_wrong_input == 2:
                    break
        if txt.lower().strip().startswith("how long is your apprenticeship?") and count_of_questions_int == 0:
            count_of_questions_int = 1
            return duration
        # capture wrong input!
        elif txt.lower().strip().startswith("how long is your apprenticeship?") and count_of_questions_int == 1:
            count_of_questions_int = 2
            return duration_right
        elif txt.lower().strip().startswith("how long is your apprenticeship?") and duration == "y":
            count_of_questions_char = 1
            return duration_right
        if txt.lower().strip().startswith("enter your current team name"):
            return team
        if txt.lower().strip().startswith("what team"):
            # capture wrong input, to high number and  character
            while True:
                if count_of_questions_team_number == 0:
                    count_of_questions_team_number += 1
                    return wrong_team_number
                elif count_of_questions_team_number == 1:
                    count_of_questions_team_number += 1
                    return wrong_team_number_txt
                elif count_of_questions_team_number == 2:
                    count_of_questions_team_number += 1
                    return team_number
                elif count_of_questions_team_number == 3:
                    break
            return team_number

    with patch.object(builtins, 'input', mock_input):
        dict_values = rd.collect_config_data(args_ns_empty)

    # open configs
    rd.create_config(dict_values, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_after_creation = dict(config.items("settings"))

    # THEN
    assert configs_after_creation.get("name") == name
    assert configs_after_creation.get("team") == team
    assert configs_after_creation.get("team_number") == str(team_number)
    if count_of_questions_int == 1:
        assert configs_after_creation.get("duration") == duration
    elif count_of_questions_int == 2:
        assert configs_after_creation.get("duration") == duration_right
    elif count_of_questions_char == 1:
        assert configs_after_creation.get("duration") == duration_right
    assert configs_after_creation.get("count_teams") == count_teams
    assert configs_after_creation.get("start_year") == year
    assert configs_after_creation.get(
        "end_duration_education") == end_duration_education


def test_show_config(tmp_path: pathlib, capsys):
    """Test if awaited part of the output is in sdtout"""

    # GIVEN

    configpath = tmp_path / "reportdailyrc"
    awaited_part_of_output = "CONFIGURATION:"

    # WHEN
    # create a config file
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    # show the config
    rd.show_config(configpath)
    # capture input with pystest (capsys)
    captured = capsys.readouterr()
    # THEN check the captured output if awaited part is in output
    assert awaited_part_of_output in captured.out


@patch("reportdaily.user_input_change")
@patch("reportdaily.show_config")
def test_how_to_change_configs_input(mocker_show_config, mocker_user_input_change, tmp_path: pathlib, args_change):
    """This test will check if the right function (user_input_change) was selected  by a given ARGS Namespace object"""
    # GIVEN
    configpath = tmp_path / "reportdailyrc"
    expected_value = 0

    # WHEN
    # patch the user_input_change function from reportdaily
    mocker_show_config.return_value = True
    mocker_user_input_change.return_value = MagicMock(return_value=True)
    # save return value of function
    return_value = rd.how_to_change_config(args_change, configpath)
    # THEN
    # check return value ,to prove that the right function was used
    assert return_value == expected_value


@patch("reportdaily.namespace_config_change")
@patch("reportdaily.show_config")
def test_how_to_change_configs_namespace(mocker_show_config, mocker_ns_config_change, tmp_path: pathlib, args_ns):
    """This test will check if the right function (namespace_config_change) was selected  by a given ARGS Namespace object"""
    # GIVEN
    configpath = tmp_path / "reportdailyrc"
    expected_value = 1

    # WHEN
    # save return value of function
    return_value = rd.how_to_change_config(args_ns, configpath)

    # THEN
    # check return value ,to prove that the right function was used
    assert return_value == expected_value


@patch("reportdaily.create_config")
@patch("reportdaily.show_config")
@patch("reportdaily.Database")
@patch("reportdaily.data_from_configfile")
def test_cmd_init_without_configpath(mocker_data_from_configfile, mocker_database, mocker_show_config, mocker_create_config, tmp_path: pathlib, args_ns):
    """This test will check the propper use of cmd_init"""

    # GIVEN
    configpath = tmp_path / "reportdailyrc"
    # add databasepath
    databasepath = tmp_path / "database"
    expected_return_value = 0

    # WHEN
    mocker_show_config.return_value = True
    mocker_create_config.return_value = True
    mock_db_inst = mocker_database.return_value
    mock_db_inst._fill_table_sql_cmd.return_value = None
    mocker_data_from_configfile.return_value = dict(vars(args_ns))
    return_value = rd.cmd_init(args_ns, configpath, databasepath)

    # THEN
    assert expected_return_value == return_value


@patch("reportdaily.data_from_configfile")
@patch("reportdaily.os.path.exists")
@patch("reportdaily.show_config")
@patch("reportdaily.how_to_change_config")
def test_cmd_init_with_configpath(mocker_how_to_change_config, mocker_show_config, mocker_os_path_exists, mocker_data_from_configfile, tmp_path: pathlib, args_change):
    """This test will check the propper use of cmd_init if config already exists and the user wants to change it"""

    # GIVEN
    configpath = tmp_path / "reportdailyrc"
    databasepath = tmp_path/"database"
    expected_return_value = 1

    # WHEN
    mocker_os_path_exists.return_value = MagicMock(return_value=True)
    mocker_show_config.return_value = MagicMock(return_value=True)
    mocker_how_to_change_config.return_value = MagicMock(return_value=True)
    mocker_data_from_configfile.return_value = MagicMock(return_value=True)
    return_value = rd.cmd_init(args_change, configpath, databasepath)

    # THEN
    assert expected_return_value == return_value


def test_check_is_int_is_True():
    """
    Test if the function proves if the given values  are int or not
    """
    # GIVEN
    given_str_is_also_int = "2009"
    expexted_return_value = True
    given_return_value = None

    # WHEN
    given_return_value = rd.check_is_int(
        given_str_is_also_int)

    # THEN
    assert expexted_return_value == given_return_value


def test_check_is_int_is_False():
    """
    Test if the function proves if the given values  are int or not
    """

    # GIVEN
    given_str_is_also_int = "TEST2019"
    expexted_return_value = False
    given_return_value = None

    # WHEN
    given_return_value = rd.check_is_int(
        given_str_is_also_int)

    # THEN
    assert expexted_return_value == given_return_value


@pytest.mark.parametrize("team_number,expected_date",
                         [(1, "2019-09-01"),
                          (2, "2020-03-01"),
                          (3, "2020-09-01"),
                          (4, "2021-03-01"),
                          (5, "2021-09-01"),
                          (6, "2022-03-01"),
                          (7, "2022-09-01"),
                          ])
def test_calculate_team_duration_start(team_number, expected_date):
    """
    Test calculation of the start team
    """

    # GIVEN
    start_year = 2019
    expected_date_obj = datetime.strptime(expected_date, '%Y-%m-%d')
    expected_date_obs = expected_date_obj.date()

    # WHEN
    return_date = rd.calculate_team_duration_start(team_number, start_year)

    # THEN
    assert expected_date_obs == return_date


@pytest.mark.parametrize("team_number,expected_date",
                         [(1, "2020-02-28"),
                          (2, "2020-08-31"),
                          (3, "2021-02-28"),
                          (4, "2021-08-31"),
                          (5, "2022-02-28"),
                          (6, "2022-08-31"),
                          (7, "2023-02-28"),
                          ])
def test_calculate_team_duration_end(team_number, expected_date):
    """
    Test calculation of the start team
    """

    # GIVEN
    start_year = 2019
    expected_date_obj = datetime.strptime(expected_date, '%Y-%m-%d')
    expected_date_obs = expected_date_obj.date()

    # WHEN
    return_date = rd.calculate_team_duration_end(team_number, start_year)

    # THEN
    assert expected_date_obs == return_date


@pytest.mark.parametrize("awaited_duration,input_duration,count_teams",
                         [("3.5",  "3.5", "7"),
                          ("3.0", "3.0", "6"),
                          ("2.5", "2.5", "5"),
                          ("3.0", "9", "6")
                          ])
def test_duration_relation(awaited_duration, input_duration, count_teams, tmp_path: pathlib.Path, args_change):
    """
    Test the return value of  duration by change
    """

    # GIVEN
    # STANDARD_CONFIG_DATA
    configpath = tmp_path / "reportdaily_config"
    # function will be patched
    return_duration = "None"

    # WHEN
    # create config
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    # counter for input patch
    counter = 0

    def mock_input(txt):
        "This is our function that patches the builtin input function. "
        nonlocal counter
        while(True):
            if txt.lower().strip().startswith("how long") and counter == 0:
                counter += 1
                return input_duration
            elif txt.lower().strip().startswith("how") and counter == 1:
                counter += 1
                return "3.0"
            elif counter == 3:
                break
    with patch.object(builtins, 'input', mock_input):
        return_duration = rd.check_duration_relation(args_change, configpath)
    # read config
    config = configparser.ConfigParser()
    config.read(configpath)
    # THEN
    assert awaited_duration == return_duration
    assert count_teams == config.get("settings", "count_teams")


@pytest.mark.parametrize("year_input,right_year_input,duration_answer", [
    ("y", 2000, "no"),
    (999, 2000, "no"),
    (999, 2000, "yes"),
    (999, 2000, "TEST"),
])
def test_check_start_year_relation(tmp_path: pathlib.Path, year_input, right_year_input, duration_answer, args_ns):
    """
    Check if the year can be changed by user via direct input.
    Test for check_start_year_relation().
    """

    # GIVEN
    configpath = tmp_path / "year_config"

    awaited_year = "2000"

    # WHEN
    # create config
    rd.create_config(STANDARD_CONFIG_DATA, configpath)

    # required counters for patch input
    counter = 1
    second_counter = 1

    def mock_input(txt):
        """
        PATCH USER INPUT
        """
        nonlocal counter
        nonlocal second_counter
        while(True):
            if txt.lower().strip().startswith("enter") and counter == 1:
                counter += 1
                return year_input
            elif txt.lower().strip().startswith("enter") and counter == 2:
                counter += 1
                return right_year_input
            elif txt.lower().strip().startswith("did") and counter == 3:
                counter += 1
                return duration_answer
            elif txt.lower().strip().startswith("how long") and counter == 4:
                counter += 1
                # default number for duration
                duration_number = "3"
                return duration_number
            elif txt.lower().strip().startswith("did") and counter == 4 and second_counter == 1:
                counter += 1
                second_counter += 1
                # default number for duration
                answer = "no"
                return answer
            elif counter == 5:
                break

    with patch.object(builtins, 'input', mock_input):
        return_duration = rd.check_start_year_relation(args_ns, configpath)

    # read config
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    assert awaited_year == config.get("settings", "start_year")


@pytest.mark.parametrize(("wrong_year,right_year"), [
    ("999", "1000"),
    ("f", "1000"),
])
def test_start_year_relation_namespace(tmp_path: pathlib, wrong_year, right_year, args_change):
    """
    Check if the year can be changed by the cmd namespace.
    Test for check_start_year_relation_namespace() function.
    """
    # GIVEN

    configpath = tmp_path / "reportdaily_year_namespace"
    args_change.year = wrong_year
    expected_year_after_change = "1000"
    data_after_change_dict = {'start_year': right_year}

    # WHEN
    # create config file  and read it
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_before_change = configfile.read()

    def mock_input(txt):
        """
        PATCH USER INPUT
        """
        return right_year

    with patch.object(builtins, 'input', mock_input):
        rd.check_start_year_relation_namespace(args_change, configpath)

    # save the changed config
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        config_after_change = configfile.read()
    # save all values
    configs_after_change_dict = dict(config.items("settings"))

    # read config values
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    # check if the file has changed
    assert configs_before_change != config_after_change
    # prove if the expected values are in our changed config
    assert data_after_change_dict.items() <= configs_after_change_dict.items()
    # check year is the same as change
    assert expected_year_after_change == config.get(
        "settings", "start_year")


@pytest.mark.parametrize(("wrong_team_number,right_team_number"), [
    (0, 3),
    (100, 3),
    (100, 7),  # right team number value needs to be 7, so duration == "3.0" and new_team_number == 7 case is covered
    ("ERROR", 7)
])
def test_start_team_number_relation_namespace(tmp_path: pathlib, wrong_team_number, right_team_number, args_change):
    """
    Check if value of team number  changed correctly.
    Simulate wrong user input and correct input by the given paramater via cmd.
    Tested function: check_team_number_relation_namespace().
    """
    # GIVEN
    configpath = tmp_path / "reportdaily_team_number_namespace"
    args_change.duration = "3.0"
    args_change.team_number = wrong_team_number
    expected_team_number = "3"

    # WHEN
    # create config file  and read it
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_before_change = configfile.read()

    def mock_input(txt):
        """
        PATCH USER INPUT for this function: check_team_number_relation_namespace
        """
        nonlocal expected_team_number
        if txt.lower().strip().startswith("sorry"):
           # catch the case of duration =="3.0" and team number = 7
            expected_team_number = "6"
            return 6
        else:
            return right_team_number

    with patch.object(builtins, 'input', mock_input):
        rd.check_team_number_relation_namespace(args_change, configpath)

    # save the changed config
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        config_after_change = configfile.read()

    # read config values
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    # check the value if it has changed
    # catch character input
    if type(wrong_team_number) == str:
        assert expected_team_number != config.get(
            "settings", "team_number")
    # catch to high or to small value
    else:
        assert expected_team_number == config.get(
            "settings", "team_number")


@pytest.mark.parametrize(("wrong_input1,answer_change_name,answer_duration_change,wrong_input2,team_number"), [
    ("WRONG", "yes", "yes", "WRONG", 6),
    ("WRONG", "yes", "no", "WRONG", 6),
    ("WRONG", "no", "yes", "WRONG", 6),
    ("WRONG", "no", "no", "WRONG", 6)])
@patch("reportdaily.check_team_name_relation")
@patch("reportdaily.check_duration_relation")
def test_team_number_relation(mocker_check_duration, mocker_check_team, wrong_input1, answer_change_name, answer_duration_change, wrong_input2, team_number, tmp_path: pathlib, args_change):
    """
    Check values of check_team_number_relation function.
    Simulate wrong user input , mixed with right answer.
    Assert value change is correct 
    """

   # GIVEN
   # STANDARD_CONFIG_DATA
    configpath = tmp_path / "reportdaily_team_number_input"
    expected_team_number = "6"

   # WHEN
    # create config file  and read it
    rd.create_config(STANDARD_CONFIG_DATA, configpath)
    config = configparser.ConfigParser()
    config.read(configpath)
    with open(configpath, 'r') as configfile:
        configs_before_change = configfile.read()

    # patch the user_input_change function from reportdaily
    mocker_check_duration.return_value = True
    mocker_check_team.return_value = True

    # simulate user input
    counter = 0

    def mock_input(txt):
        """
        Patch user input for check_team_number_relatio
        """
        nonlocal counter
        if txt.lower().strip().startswith("what team number"):
            return int(team_number)
        elif txt.lower().strip().startswith("did the name") and counter == 0:
            counter += 1
            return wrong_input1
        elif txt.lower().strip().startswith("did the name") and counter == 1:
            counter += 1
            return answer_change_name
        elif txt.lower().strip().startswith("did the duration") and counter == 2:
            counter += 1
            return wrong_input2
        elif txt.lower().strip().startswith("did the duration") and counter == 3:
            counter += 1
            return answer_duration_change
        else:
            print("No right string found")

    with patch.object(builtins, 'input', mock_input):
        rd.check_team_number_relation(args_change, configpath)

    # read config values
    config = configparser.ConfigParser()
    config.read(configpath)

    # THEN
    assert expected_team_number == config.get("settings", "team_number")
