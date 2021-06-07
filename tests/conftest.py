import pytest
# import namespace
from argparse import Namespace


@pytest.fixture
def args_ns():
    return Namespace(cliargs=["init"], name="NameTest", count_teams="6",
                     team="TeamName", year="2020", duration="3.0", team_number="4")


@pytest.fixture
def args_ns_empty():
    return Namespace(cliargs=["init"], name=None,  team=None, year=None, change=None, duration=None,  team_number=None)


@pytest.fixture
def args_change(args_ns_empty):
    args_ns_empty.change = True
    return args_ns_empty
