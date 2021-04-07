#!/usr/bin/env python3

import argparse
import logging
from logging.config import dictConfig
import sys

__version__ = "0.2.0"
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


def cmd_new(args):
    """Creates a new day for the incoming entries"""
    log.debug("New selected %s", args)
    print("New selected", args)
    return 100


def cmd_add(args):
    """add a new entry"""
    log.debug("New selected %s", args)
    print("add selected", args)
    return 200


def cmd_change(args):
    """change a entry by id"""
    log.debug("New selected %s", args)
    print("Change selected", args)
    return 300


def cmd_delete(args):
    """delete an entry by id"""
    log.debug("New selected %s", args)
    print("delete sected", args)
    return 400


def cmd_list(args):
    """list all entries of the day by id"""
    log.debug("New selected %s", args)
    print("list selected", args)
    return 500


def cmd_export(args):
    """export the day by id"""
    log.debug("New selected %s", args)
    print("export selected", args)
    return 600


def parsecli(cliargs=None) -> argparse.Namespace:
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result

    :param cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (
                                         __version__, __author__)
                                     )

    parser.add_argument('-v', action='count',
                        dest="verbose", default=0, help="Add a verbosity level for the logger  from ""-v"" to ""-vvvv""")

    # subparser
    subparsers = parser.add_subparsers(help='available sub commands')
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
        exit_code = args.func(args)
        return exit_code

    except Exception as error:
        log.fatal(error)
        return 999


if __name__ == "__main__":
    sys.exit(main())
