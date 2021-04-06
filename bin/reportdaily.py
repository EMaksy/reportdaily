#!/usr/bin/env python3
"""
add your description here
"""
import argparse
import sys


__version__ = "0.2.0"
__author__ = "Eugen Maksymenko <eugen.maksymenko@suse.com>"


def cmd_new(args):
    print("New selected", args)
    return 10


def cmd_add(args):
    print("add selected", args)
    return 0


def cmd_change(args):
    print("Change selected", args)
    return 0


def cmd_delete(args):
    print("delete sected", args)
    return 0


def cmd_list(args):
    print("list selected", args)
    return 0


def cmd_export(args):
    print("export selected", args)
    return 0


def parsecli(cliargs=None) -> argparse.Namespace:
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result

    :param cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (
                                         __version__, __author__)
                                     )
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

    return args


def main(cliargs=None) -> int:
    """Entry point for the application script

    :param cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: error code
    """
    args = parsecli(cliargs)
    print(args)
    exit_code = args.func(args)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
