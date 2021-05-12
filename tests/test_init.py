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
    # ...
}
ARGS = Namespace(cliargs=["init"], name="NameTest",
                 team="TeamName", year=int(2020))


def test_config_exists(tmp_path: pathlib.Path):
    # given
    # ARGS
    configpath = tmp_path / "reportdailyrc"

    # when = expect  a config file is created in tmp_path
    rd.create_config(ARGS, configpath)

    # then config file existence is true
    assert os.path.exists(configpath) is True


def test_config_section_option_namespace(tmp_path: pathlib.Path):
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
    # given
    # ARGS
    # STANDARD_SECTIONS
    # STANDARD_OPTIONS
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


"""
def test_config_real_section(tmp_path):
        # ...
    
    # given 

    # when
    config = ...
    real_keys = set(config.keys())
    real_keys.remove("DEFAULT")
    std_keys = set(STANDARD_CONFIG)
    
    # then 
    assert real_keys == std_keysThanks




# notion create a test if confit exist
# create a test if section and option exist
# check if value is correct
# noch ein test , modul wo du über alle sections iterieren kannst  um zu überprüfen ob alle  sections und options in config vorhanden sind
# gettattr(args var) var = bar  --> zugriff auf namespace
# Welche tests brauchen wir noch ?
# Cheat sheet was kann dict alles ?
# was ist ein set und wir nehmen die menge aus file - die menge aus globalen variablen
"""
"""
Create config mit simuliertem user input

show config  Überprüfung ob die configs correct angezeigt werden

ask_for_input test ob die eingabe verändert worden ist und oder ob es passt

# nicht sofort nötig. how to change_config  check welche Funktion ausgeführt wird

namespace_config_change soll die config datei mit gegeben argumenten korrekt überschreiben

user input_change soll die config überschreiben mit simulierter user eingabe
"""
