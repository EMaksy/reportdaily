#!/usr/bin/env python3

import argparse
import logging
from logging.config import dictConfig
import sys
# configparser
from datetime import date
from configparser import ConfigParser
import os


class MissingSubCommand(ValueError):
    pass


CONFIGPATH = os.path.expanduser("~/.config/reportdaily/reportdailyrc")
__version__ = "0.3.0"
__author__ = "Eugen Maksymenko <eugen.maksymenko@suse.com>"

#: The dictionary, passed to :class:`logging.config.dictConfig`,
#: is used to setup your logging formatters, handlers, and loggers
#: For details, see https://docs.python.org/3.4/library/logging.config.html#configuration-dictionary-schema
DEFAULT_LOGGING_DICT = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(levelname)s] %(funcName)s: %(message)s'},
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',  # will be set later
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['default'],
            'level': 'INFO',
            # 'propagate': True
        }
    }
}


#: Map verbosity level (int) to log level
LOGLEVELS = {None: logging.WARNING,  # 0
             0: logging.ERROR,
             1: logging.WARNING,
             2: logging.INFO,
             3: logging.DEBUG,
             }


#: Instantiate our logger
log = logging.getLogger(__name__)

#: Use best practice from Hitchhiker's Guide
#: see https://docs.python-guide.org/writing/logging/#logging-in-a-library
log.addHandler(logging.NullHandler())


def cmd_init(args, CONFIGPATH):
    """
    Initializes global user data (required for the first time).
    Either user data can be entered directly via options or user will be asked.

    :param argparse.Namespace args: Arguments given by the command line
    :param str CONFIGPATH: Path where the configuration file is stored
    :return: exit code of this function
    :rtype: int
    """
    log.debug("INIT selected %s", args)

    # check if a config file already exist
    if os.path.exists(CONFIGPATH):
        show_config(CONFIGPATH)
        # check if the user wants to change in the existing file
        if args.change is True:
            how_to_change_config(args, CONFIGPATH)
            return 1
    # create a config if there is none
    else:
        create_config(args, CONFIGPATH)
        show_config(CONFIGPATH)
        return 0


def show_config(CONFIGPATH):
    """
    Show the configs to the user

    :param str CONFIGPATH: String with an absolute path for looking up the values of the configfile
    """

    # read the config
    parser = ConfigParser()
    parser.read(CONFIGPATH)

    print(
        f"""
    "Your current configuration at the moment"
    Name: {parser.get("settings","name")}
    Team: {parser.get("settings", "team")}
    Date: {parser.get("settings", "current_day")}
    Year: {parser.get("settings", "start_year")}

    If you desire to make changes to the configuration try the -c or --change option for the init command
    """
    )


def create_config(args, CONFIGPATH):
    """
    Create a config file, from users input, where the user data is stored as a dict
    :param argparser.Namespace args: Arguments given by the command line
    :param str CONFIGPATH: Path where the configuration file is stored
    """
    # name
    print("Please enter your full name --> example: 'Max Musterman'")
    name = ask_for_input(args.name, "Enter your Name: ")
    # team
    team = ask_for_input(args.team, "Enter your Team: ")
    year = int(ask_for_input(
        args.year, "In which year did your start your apprenticeship ?: "))
    # time
    today_date = date.today()
    # create a config file
    config = ConfigParser()
    config["settings"] = {'name': name,
                          'team': team, 'current_day': today_date, 'start_year': year}
    # create a config file
    os.makedirs(os.path.dirname(CONFIGPATH), exist_ok=True)
    with open(CONFIGPATH, 'w') as user_config:
        config.write(user_config)
    print(f"The file was created at this path {CONFIGPATH}")


def ask_for_input(var, message):
    """
    Asks for input if passed variable is None, otherwise return variable value.

    :param str|None var: The variable to check
    :param str message: The message to use as a prompt
    :return: Either the input from the user or the value of a variable
    :rtype: str
    """
    if var is None:
        var = input(message)
    return var


def how_to_change_config(args, CONFIGPATH):
    """
    Change or overwrite the configs via direct input or cli Attributes

    :param argparse.Namespace args: Attributes given by the command line
    :param str CONFIGPATH: Path where the configuration file is stored
    :return int: int return value for testing
    """
    if args.name is None and args.year is None and args.team is None and args.change:
        user_input_change(args, CONFIGPATH)
        result_value = 0
    else:
        namespace_config_change(args, CONFIGPATH)

        result_value = 1
    show_config(CONFIGPATH)
    return result_value


def namespace_config_change(args, CONFIGPATH):
    """
    Input arguments direct via the console
    :param  namespace: Attributes given by the command line
    :param  str: Path where the configuration file is stored
    """
    # store all the args from namespace
    name = args.name
    team = args.team
    year = args.year
    change = args.change

    # add config parser to file
    config = ConfigParser()
    config.read(CONFIGPATH)
    if change is True:
        # overwrite if namespace is filled
        if name is not None:
            config.set("settings", "name", name)
        if team is not None:
            config.set("settings", "team", team)
        if year is not None:
            config.set("settings", "start_year", year)

        with open(CONFIGPATH, "w") as configfile:
            config.write(configfile)
        # show config to the user , so changes are visible to the user
    log.debug("namespace_config was selected")


def check_is_int(input_str, input_is_int):
    """
    Prove if the given argument is an int and return True or decline and return False
    :param  str: String given that needs to be checked
    :param  bool: bool value default False
    :return bool value, True if str is an int, False if str is not an int
    """

    if input_str.strip().isdigit():
        print("Year is a int value")
        input_is_int = True
        return input_is_int
    else:
        print("Input is not a int sorry, try again")
        input_is_int = False
        return input_is_int


def user_input_change(args, CONFIGPATH):
    """
    Input the data that is asked by function tp change configs

    :param argparse.Namespace args: Attributes given by the command line
    :param str CONFIGPATH: Path where the configuration file is stored
    :return: the ConfigParser object
    :rtype: configparse.ConfigParser
    """
    # all user options
    choice_table = {"Name": "t1", "Team": "t2", "Year": "t3"}
    tmp_input = ''
    overwrite_input = ' '

    # show and ask user what he wants to overwrite
    print("""
        "What do you want to change?"
        Your options are
        Name
        Team
        Year
        """)

    # check for right user input
    while(True):
        tmp_input = input("Name, Team, Year? ").capitalize()
        if tmp_input in choice_table:
            # need to map the keys  right to the settings --> from Name to name
            if tmp_input == "Name":
                tmp_input = "name"
            elif tmp_input == "Team":
                tmp_input = "team"
            elif tmp_input == "Year":
                tmp_input = "start_year"
            break
        else:
            print("No key in config found --> Try again")
            continue

    input_is_int = False
    while(True):
        overwrite_input = input("Enter the change ")
        if tmp_input == "start_year" and input_is_int == False:
            input_is_int = check_is_int(
                overwrite_input, input_is_int)
            if input_is_int == True:
                break
        elif tmp_input != "start_year":
            break

    # add config parser to file
    config = ConfigParser()
    config.read(CONFIGPATH)
    config.set("settings", f"{tmp_input}", f"{overwrite_input}")
    with open(CONFIGPATH, "w") as configfile:
        config.write(configfile)
    # show config to the user , so changes are visible to the user
    return config


def cmd_new(args):
    """Creates a new day for the incoming entries"""
    log.debug("New selected %s", args)
    print("New selected", args)
    return 0


def cmd_add(args):
    """add a new entry"""
    log.debug("Add selected %s", args)
    print("Add selected", args)
    return 0


def cmd_change(args):
    """change a entry by id"""
    log.debug("Change selected %s", args)
    print("Change selected", args)
    return 0


def cmd_delete(args):
    """delete an entry by id"""
    log.debug("Delete selected %s", args)
    print("Delete selected", args)
    return 0


def cmd_list(args):
    """list all entries of the day by id"""
    log.debug("List selected %s", args)
    print("List selected", args)
    return 0


def cmd_export(args):
    """export the day by id"""
    log.debug("Export selected %s", args)
    print("Export selected", args)
    return 0


def parsecli(cliargs=None) -> argparse.Namespace:
    """Parse CLI with: class:`argparse.ArgumentParser` and return parsed result

    : param cliargs: Arguments to parse or None (=use sys.argv)
    : return: parsed CLI result
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (
                                         __version__, __author__)
                                     )

    # option verbose
    parser.add_argument('-v', action='count',
                        dest="verbose", default=0, help="Add a verbosity level for the logger  from ""-v"" to ""-vvvv""")
    # option version
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )

    # subparser
    subparsers = parser.add_subparsers(help='available sub commands')
    # init cmd
    parser_init = subparsers.add_parser(
        'init', help="Create an initial Configuration file")
    parser_init.set_defaults(func=cmd_init)
    parser_init.add_argument(
        '--name', "-n", help='User Name')
    parser_init.add_argument(
        '--year', "-y", help='Start year of the trainee')
    parser_init.add_argument(
        '--team', "-t", help='Current team name')
    parser_init.add_argument(
        '--change', '-c', action='store_true', help='Change an existing configuration')

    # new cmd
    parser_new = subparsers.add_parser('new', help="creates a new day entry")
    parser_new.set_defaults(func=cmd_new)
    # add cmd
    parser_add = subparsers.add_parser(
        "add", help="adds a new commit to your day")
    parser_add.set_defaults(func=cmd_add)
    parser_add.add_argument(
        "commit", type=str, help=" the commit message which describes your tasks in work")
    # change cmd
    parser_change = subparsers.add_parser(
        "change", help="change an existing entry")
    parser_change.set_defaults(func=cmd_change)
    parser_change.add_argument(
        "id", help=" change the entry by id")
    # delete cmd
    parser_delete = subparsers.add_parser(
        "delete", help="deletes an entry by id")
    parser_delete.set_defaults(func=cmd_delete)
    parser_delete.add_argument(
        "id", help=" change the entry by id")
    # list cmd
    parser_list = subparsers.add_parser(
        "list", help="displays a list of today entries")
    parser_list.set_defaults(func=cmd_list)
    parser_list.add_argument(
        "id", help=" display a list with correct id")
    # export cmd
    parser_export = subparsers.add_parser(
        "export", help="exports todays changes and saves it to a file")
    parser_export.set_defaults(func=cmd_export)
    # end cmd
    args = parser.parse_args(cliargs)

    # help for the user when no subcommand was passed
    if "func" not in args:
        parser.print_help()
        raise MissingSubCommand("Expected subcommand")

    # Setup logging and the log level according to the "-v" option
    dictConfig(DEFAULT_LOGGING_DICT)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.DEBUG))
    log.debug("CLI result: %s", args)

    return args


def main(cliargs=None) -> int:
    """Entry point for the application script
    :param cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    """

    try:
        args = parsecli(cliargs)
        # do some useful things here...
        # If everything was good, return without error:
        # log.info("I'm an info message")
        # log.debug("I'm a debug message.")
        # log.warning("I'm a warning message.")
        # log.error("I'm an error message.")
        # log.fatal("I'm a really fatal massage!")
        exit_code = args.func(args, CONFIGPATH)
        return exit_code

    except MissingSubCommand as error:
        log.fatal(error)
        return 888


if __name__ == "__main__":
    sys.exit(main())
