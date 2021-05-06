[![Pages](https://github.com/SchleichsSalaticus/reportdaily/actions/workflows/manpage-build.yml/badge.svg)](https://github.com/SchleichsSalaticus/reportdaily/actions/workflows/manpage-build.yml)

[![pytest](https://github.com/SchleichsSalaticus/reportdaily/actions/workflows/pytest.yml/badge.svg)](https://github.com/SchleichsSalaticus/reportdaily/actions/workflows/pytest.yml)

# Reportdaily

A command line tool to create edit and export daily, weekly, or monthly reports.

## Purpose of the project

To make life for trainees easier
This script will help you to create weekly reports and also to manage your time need.

## Status

Work in Progress

## Requirements

Python3

## How to use reportdaily

Just clone the repository and cd into the directory

`python3 bin/reportdaily.py [commands] [arguments]`

## Commands

`-h` : help information

### Subcommands

- `init` : initialize and create config on first time
- `new` : new day for entries
- `add` : creates a new entry
- `change` :change an existing entry
- `delete` : delete an entry
- `list`: listing all existing entries
- `export` : export all entries in a file format

## Example

```bash
    git clone [this project]
    cd reportdaily
    python3 bin/reportdaily.py init
    # create user config
    python3 bin/reportdaily.py new
    # a new day has been added.
    python3 bin/reportdaily.py add "message"
    # adds your message to your new day
    python3 bin/reportdaily.py list
    # show all the entries from this day with id
    python3 bin/reportdaily export
    # exports all the entries
```
