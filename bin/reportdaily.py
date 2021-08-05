#!/usr/bin/env python3
import argparse
import logging
from logging.config import dictConfig
import sys
# configparser
from datetime import date
from configparser import ConfigParser
import os
# database
import sqlite3
from datetime import datetime
import textwrap



# GLOBALS
CONFIGPATH = os.path.expanduser("~/.config/reportdaily/reportdailyrc")
DATABASEPATH = os.path.expanduser("~/.config/reportdaily/database.sqlite")
__version__ = "0.3.1"
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

# CLASS


class MissingSubCommand(ValueError):
    pass


class Database():

    VERSION = 10

    def __init__(self, path: str, sql_data=None):

        self.path = path
        # Initialized in other functions for database connection
        self.connection = None
        # data which is send by user

        self.sql_data = {} if sql_data is None else sql_data
        """
        the previous code is equivalent to the following code
        if sql_data is None:
            self.sql_data = dict()
        else:
            self.sql_data = sql_data
        """

        # Create database sqlite....
        # create structure of database with required tables
        self.create()
        # table entry, trainee and team has been created

    def create(self):
        """
        Create a database by a given path
        """
        self.connection = sqlite3.connect(f"{self.path}")
        log.debug("Connection to database true")
        self._create_empty_database()

    def _create_empty_database(self):
        """
        Create tables to given database
        Tables: team, trainee and entry
        :param database:  path
        """
        create_users_table_team = """
        CREATE TABLE IF NOT EXISTS team (
        TEAM_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TEAM_NUMBER INTEGER NOT NULL,
        TEAM_NAME TEXT NOT NULL,
        TEAM_START TEXT NOT NULL,
        TEAM_END TEXT NOT NULL
        );
        """
        create_users_table_trainee = """
        CREATE TABLE IF NOT EXISTS trainee (
        TRAINEE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME_TRAINEE TEXT,
        START_YEAR TEXT,
        GRADUATION_YEAR INTEGER,
        DATABASE_VERSION TEXT,
        NUMBER_OF_TEAMS TEXT INTEGER,
        DURATION  INTEGER,
        CREATION_DATE TEXT,
        TEAM_ID  INTEGER,
        FOREIGN KEY(TEAM_ID) REFERENCES team(TEAM_ID)
        );
        """
        create_users_table_entry = """
        CREATE TABLE IF NOT EXISTS entry (
        ENTRY_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        ENTRY_TXT TEXT NOT NULL,
        ENTRY_DATE TEXT NOT NULL,
        DAY_ID INTEGER,
        FOREIGN KEY(DAY_ID) REFERENCES team(DAY_ID)
        );
        """
        create_users_table_day = """
        CREATE TABLE IF NOT EXISTS day (
        DAY_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
        DAY_DATE TEXT NOT NULL,
        DAY_FREE INTEGER,
        TRAINEE_ID INTEGER NOT NULL,
        FOREIGN KEY(TRAINEE_ID) REFERENCES trainee(TRAINEE_ID)
        );
        """
        # execute querys
        self._execute_sql(create_users_table_team)
        self._execute_sql(create_users_table_trainee)
        self._execute_sql(create_users_table_entry)
        self._execute_sql(create_users_table_day)


    def sql_new_day(self):
        """
        Executes sql query to add a new day for upcoming entries
        """
        error_msg=textwrap.dedent(f"""
                You are ready to add entries for this date: {self.sql_data}
                """)
       
        day=f'"{self.sql_data}"'# care dont forget the double quotes  --> " "  --> Otherwise wrong value error in dabase happen
        log.debug(f"NEW DAY DATE: {day} ")

        # create new day entry
        sql_cmd_new_day = f"""
        INSERT OR REPLACE INTO DAY  (DAY_DATE,TRAINEE_ID)
        VALUES ({day},1);
        """
        # need unique index so no duplicates happen, becaurse there is just one day 
        sql_cmd_unique_index_new= "CREATE UNIQUE INDEX index_day_on_day_date ON day(DAY_DATE);"
        
    
        try:
            self._execute_sql(sql_cmd_new_day)
            self._execute_sql(sql_cmd_unique_index_new)
        except:
           print(error_msg)
           pass     
    

    def _execute_sql(self, sql_command):
        """
        Execute a query by a given "connection"/database and a sql query
        param:
        str connection: Path to the database
        str query: A sql command you wish to execute
        """
        cursor = self.connection.cursor()

        result = cursor.execute(sql_command)
        self.connection.commit()
        return result

    def _fill_table_sql_cmd(self):
        """
        Execute a query with all the given information from script
        :param
        """
        log.debug(
            "Here we will write down all our data to database %s", self.sql_data)
        # trainee_data
        trainee_name = str(self.sql_data.get("name"))
        # print(trainee_name)
        trainee_current_day = self.sql_data.get("current_day")
        trainee_duration = float(self.sql_data.get("duration"))
        trainee_start_year = self.sql_data.get("start_year")
        trainee_end_duration = self.sql_data.get("end_duration_education")
        trainee_number_teams = int(self.sql_data.get("count_teams"))
        # team data
        team_name = self.sql_data.get("team")
        team_number = self.sql_data.get("team_number")
        # team duration
        team_start = self.sql_data.get("team_time_start")
        team_end = self.sql_data.get("team_time_end")
        team_id_fk = "1"

        # sql command
        sql_cmd_trainee = f"""
        INSERT INTO
        trainee (NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
                 NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
        VALUES
        ("{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
         "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
        """

        sql_cmd_team = f"""
        INSERT INTO
        team (TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
        VALUES
        ("{team_name}","{team_number}","{team_start}","{team_end}");
        """

        # now its time to execute sql command with data and fill the database
        self._execute_sql(sql_cmd_team)
        self._execute_sql(sql_cmd_trainee)

    def _adapt_changes_to_database(self):
        """
        """

        # We need to collect all the changed data
        log.debug(
            """Replace old values in database with the new %s""", self.sql_data)
        trainee_name = str(self.sql_data.get("name"))
        # print(trainee_name)
        trainee_current_day = self.sql_data.get("current_day")
        trainee_duration = float(self.sql_data.get("duration"))
        trainee_start_year = self.sql_data.get("start_year")
        trainee_end_duration = self.sql_data.get("end_duration_education")
        trainee_number_teams = int(self.sql_data.get("count_teams"))
        # team data
        team_name = self.sql_data.get("team")
        team_number = self.sql_data.get("team_number")
        # team duration
        team_start = self.sql_data.get("team_time_start")
        team_end = self.sql_data.get("team_time_end")
        team_id_fk = "1"
        team_pk = "1"
        trainee_pk = "1"

        # sql command
        sql_cmd_trainee = f"""
        REPLACE INTO
        trainee (TRAINEE_ID,NAME_TRAINEE, START_YEAR, GRADUATION_YEAR, DATABASE_VERSION,
                 NUMBER_OF_TEAMS, DURATION, CREATION_DATE,TEAM_ID)
        VALUES
        ("{trainee_pk}","{trainee_name}", "{trainee_start_year}" , "{trainee_end_duration}",	"{self.VERSION}",
         "{trainee_number_teams}","{trainee_duration}","{trainee_current_day}","{team_id_fk}");
        """

        sql_cmd_team = f"""
        REPLACE INTO
        team (TEAM_ID,TEAM_NAME,TEAM_NUMBER,TEAM_START,TEAM_END)
        VALUES
        ("{team_pk}","{team_name}","{team_number}","{team_start}","{team_end}");
        """

        # now its time to execute sql command with data and fill the database
        self._execute_sql(sql_cmd_team)
        self._execute_sql(sql_cmd_trainee)

        # overwrite sql database with the changes

    def sql_read_database_all_teams(self):
        """
        Open up database  and return entries
        """ 
        sql_cmd_read_all_tems="SELECT * FROM team;"  
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute(sql_cmd_read_all_tems)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def close(self):
        """
        Close database manually
        """
        log.debug("Database closed")
        self.connection.close()


def cmd_init(args, configpath, databasepath):
    """
    Initializes global user data (required for the first time).
    Either user data can be entered directly via options or user will be asked.

    :param argparse.Namespace args: Arguments given by the command line
    :param str configpath: Path where the configuration file is stored
    :return: exit code of this function
    :rtype: int
    """
    log.debug("INIT selected %s", args)
    # check if a config file already exist
    if os.path.exists(configpath):
        show_config(configpath)
        # check if the user wants to change in the existing file
        if args.change is True:
            how_to_change_config(args, configpath)
            # collect sql data
            sql_data = data_from_configfile(configpath)
            # execute database changes
            sql_database = Database(databasepath, sql_data)
            sql_database._adapt_changes_to_database()
            # close Database
            sql_database.close()
            return 1
    # create a config if there is none
    else:
        config_value = collect_config_data(args)
        log.debug(f"Return Value of config:{config_value}")
        create_config(config_value, configpath)
        show_config(configpath)
        # collect data
        sql_data = data_from_configfile(configpath)
        # init the database
        sql_database = Database(databasepath, sql_data)
        # execute sql cmd and fill the database with our values
        sql_database._fill_table_sql_cmd()
        # dont forget to close the database
        sql_database.close()
        return 0


def data_from_configfile(configpath):
    """
    Collect data from our configfile so it can be send to database

    :param str configpath: Path where the configuration file is stored
    :return: data collection from config parser
    :rtype: dict
    """
    # save data here
    data_collection = dict
    # read data from configfile
    parser = ConfigParser()
    parser.read(configpath)
    # write data from configfile to dict
    data_collection = dict(parser.items('settings'))
    return data_collection


def show_config(configpath):
    """
    Show the configs to the user

    :param str configpath: String with an absolute path for looking up the values of the configfile
    """

    # read the config
    parser = ConfigParser()
    parser.read(configpath)

    # calculate the  start and end date
    end_of_education = calculate_team_duration_end(

        int(parser.get("settings", "count_teams")),
        int(parser.get("settings", "start_year")),
    )
    start_education = calculate_team_duration_start(

        1,  # input 1 which is like the first team with the same team
        int(parser.get("settings", "start_year")),
    )

    # output of configs
    print(
        f"""
    CONFIGURATION:

    Name: {parser.get("settings","name")}
    Team: {parser.get("settings", "team")}
    Current team number: {parser.get("settings", "team_number")}
    Start date of current team: {parser.get("settings", "team_time_start")}
    End date of current team: {parser.get("settings", "team_time_end")}
    Start of Education: {start_education}
    End of Education: {end_of_education}
    Duration: {parser.get("settings", "duration")} years
    Count of teams during the education: {parser.get("settings", "count_teams")}
    Date of Initialization of the database: {parser.get("settings", "current_day")}
    """
    )
    print("If you desire to make changes to the configuration try the -c or --change option for the init command")


def input_duration_count_teams(args, year):
    """
    Input the duration of the education
    Calculates the end duration of the education

    :param argparse.Namespace args: Arguments given by the command line
    :param year int: Get year from existing Configfile
    :return: duration
    :return: count_teams
    :return: end_duration_education
    :rtype: float, int,str
    """

    txt_year = textwrap.dedent("""
                How long is your apprenticeship?
                Default is 3 years
                Optional is 2.5 years if your want to shorten it
                Failed once is 3.5 years
                """)
    # required paramater
    duration = None
    count_teams = None

    # check  relation for namespace
    while(True):

        duration = ask_for_input(args.duration, txt_year)
        if duration in ("3.0", "3"):

            duration = "3.0"
            log.debug("duration = 3.0 --> count teams = 6")
            count_teams = 6

            break

        elif duration == "2.5":
            log.debug("duration = 2.5 --> count teams = 5")
            count_teams = 5
            break

        elif duration == "3.5":
            log.debug("duration = 3.5 --> count teams = 7")
            count_teams = 7
            break
        elif duration not in ("3.5", "2.5", "3.0"):
            log.debug(
                f"Count teams: {count_teams}  Duration: {duration}  args_duration value : {args.duration}")
            print(f"Value {duration} is to high or to low")

    end_duration_education = int(year) + float(duration)
    log.debug(" This is the  year before the calculation: %s",
              end_duration_education)
    # format end_duration_education
    end_duration_education = calculate_team_duration_end(
        count_teams, int(year))
    log.debug(
        f"""duration : {duration}, count_teams : {count_teams}, end_duration : {end_duration_education}""")
    return duration, count_teams, end_duration_education


def collect_config_data(args):
    """
    Collect configuration data by user input 
    Return a dict of collected values for creating a configfile

    : param argparse.Namespace args: Attributes given by the command line
    : return: value dict with all configuration data
    : rtype: dict
    """
    # ALl input txt
    txt_name_input = textwrap.dedent(
        """Please enter your full name - -> example: 'Max Musterman'   """)
    txt_year_input = textwrap.dedent(
        "In which year did you start your apprenticeship ?: ")
    txt_year_wrong_input = "Sorry only integers are allowed , no characters, try again"
    str_team_input = "Enter your current team name:  "
    # name
    name = ask_for_input(
        args.name, txt_name_input)
    # start of the education
    while True:
        try:
            year = int(ask_for_input(
                args.year, txt_year_input))
            break
        except:
            print(txt_year_wrong_input)
            continue

    # user input of duration,count_teams and end_duration
    duration, count_teams, end_duration_education = input_duration_count_teams(
        args, year)

    # team
    team = ask_for_input(args.team, str_team_input)
    # ask for the number of the team
    team_number = config_team_number_input(args)
    # find out the teams duration
    team_date_start = calculate_team_duration_start(team_number, year)
    team_date_end = calculate_team_duration_end(team_number, year)
    # time
    today_date = date.today()
    value_dict = {'name': name,
                  'team': team,
                  'count_teams': count_teams,
                  'team_number': team_number,
                  'current_day': today_date,
                  'duration': duration,
                  'start_year': year,
                  'end_duration_education': end_duration_education,
                  'team_time_start':  team_date_start,
                  'team_time_end': team_date_end
                  }

    return value_dict


def create_config(config_values, configpath):
    """
    Create a config file by given config_values  under a given configpath

    : param dict config_values: All key and values for creating the config file
    : param str configpath: Path where the configuration file is stored

    """

    for key in config_values:
        config_values[key] = str(config_values[key])

    config = ConfigParser()
    config["settings"] = config_values
    # create a config file
    os.makedirs(os.path.dirname(configpath), exist_ok=True)
    with open(configpath, 'w') as user_config:
        config.write(user_config)
    log.debug("The file was created at this path %s" % (configpath))


def calculate_team_duration_start(team_number_now: int,  start_year_education: int):
    """
    Calculate start time in team
    Format time string to TIME iso
    Creates a date object

    : param int team_number: Team Number
    : param int year: Year
    : return: date: String object
    : rtype: date_object
    """
    start_month = None
    start_year = None
    start_day = "01"

    if team_number_now == 1:
        start_month = "09"
        start_year = start_year_education
    elif team_number_now == 2:
        start_month = "03"
        start_year = start_year_education+1
    elif team_number_now == 3:
        start_month = "09"
        start_year = start_year_education+1
    elif team_number_now == 4:
        start_month = "03"
        start_year = start_year_education+2
    elif team_number_now == 5:
        start_month = "09"
        start_year = start_year_education+2
    elif team_number_now == 6:
        start_month = "03"
        start_year = start_year_education+3
    elif team_number_now == 7:
        start_month = "09"
        start_year = start_year_education+3

    # format time string to iso
    start_str = f"{start_year}-{start_month}-{start_day}"
    date_obj = datetime.strptime(start_str, '%Y-%m-%d')   # python 3.6 required
    # create date  objects
    # start_obj = date.fromisoformat(f"{start_str}") # python 3.7
    date_string = date_obj.date()

    # create date  objects
    # start_obj = date.fromisoformat(f"{start_str}") # python 3.7
    return date_string


def calculate_team_duration_end(team_number_now: int,  start_year_education: int):
    """
    Calculate and format end value of a team

    : param int team_number: Team Number
    : param int year: Year
    """

    end_month = None
    end_year = None
    end_day = None

    if team_number_now == 1:
        end_month = "02"
        end_year = start_year_education+1
    elif team_number_now == 2:
        end_month = "08"
        end_year = start_year_education+1
    elif team_number_now == 3:
        end_month = "02"
        end_year = start_year_education+2
    elif team_number_now == 4:
        end_month = "08"
        end_year = start_year_education+2
    elif team_number_now == 5:
        end_month = "02"
        end_year = start_year_education+3
    elif team_number_now == 6:
        end_month = "08"
        end_year = start_year_education+3
    elif team_number_now == 7:
        end_month = "02"
        end_year = start_year_education+4

    # which day the team ends
    if end_month == "08":
        end_day = "31"
    elif end_month == "02":
        end_day = "28"

    # format time string to iso
    end_str = f"{end_year}-{end_month}-{end_day}"
    # create date  objects
   # end_obj = date.fromisoformat(f"{end_str}")

    date_obj = datetime.strptime(end_str, "%Y-%m-%d")
    date_string = date_obj.date()
    log.debug(f"{date_string}")

    # create date  objects
    # start_obj = date.fromisoformat(f"{start_str}")
    return date_string


def config_team_number_input(args):
    """
    Input the team number

    : param argparse.Namespace args. Arguments given by the command line
    : return: team number
    : rtype: int
    """

    # txt input messages
    txt_team_number_input = textwrap.dedent("""
                    What team number is that?
                    Deafult 1-7
                    """)
    txt_team_number_error_msg = textwrap.dedent("""
                    Sorry your number is not between 1-7
                    Try Again!
                    """)

    txt_team_number_no_char_error_msg = textwrap.dedent("""Sorry no character are allowed, only numbers: D
                    """)

    while True:
        try:
            team_number = int(ask_for_input(
                args.team_number, txt_team_number_input))
            if team_number in range(1, 8):
                break
            else:
                print(txt_team_number_error_msg)
                continue
        except:
            print(txt_team_number_no_char_error_msg)

    return int(team_number)


def ask_for_input(var, message):
    """
    Asks for input if passed variable is None, otherwise return variable value.

    : param str None var: The variable to check
    : param str message: The message to use as a prompt
    : return: Either the input from the user or the value of a variable
    : rtype: str
    """
    if var is None:
        var = input(message)
    return var


def how_to_change_config(args, configpath):
    """
    Change or overwrite the configs via direct input or cli Attributes

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    : return int: int return value for testing
    """

    if args.name is None and args.year is None and args.team is None and args.duration is None and args.team_number is None and args.change is True:
        user_input_change(args, configpath)
        result_value = 0
    else:
        namespace_config_change(args, configpath)
        result_value = 1
    show_config(configpath)
    return result_value


def namespace_config_change(args, configpath):
    """
    Input arguments direct via the console

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # FIXME i should rename this values because they are not required and redundant
    # store all the args from namespace
    name = args.name
    team = args.team
    year = args.year
    change = args.change
    duration = args.duration
    # count_teams = args.count_teams
    team_number = args.team_number

    # add config parser to file
    config = ConfigParser()
    config.read(configpath)
    log.debug("namespace_config_change")
    log.debug(f"{args}")
    if change == True:
        # overwrite if namespace is filled

        if name != None:
            log.debug(f"name != None  value:{name}")
            check_name_relation_namespace(args, configpath)
        if team != None:
            log.debug(f"team != None  value:{team}")

            check_team_name_relation_namespace(args, configpath)
        if year != None:
            log.debug(f"year != None value:{year}")
            check_start_year_relation_namespace(args,  configpath)
        if duration != None:
            log.debug(
                f"duration != None and count_teams == None  value={duration}")
            check_duration_relation_namespace(args, configpath)

        if team_number != None:
            log.debug(f"team_number != None  value={team_number}")
            check_team_number_relation_namespace(args, configpath)

           # config.set("settings", "team_number", team_number)

        # with open(configpath, "w") as configfile:
         #   config.write(configfile)
        # show config to the user , so changes are visible to the user
    log.debug("namespace_config was selected")


def check_is_int(input_str):
    """
    Prove if the given argument is an int and return True or return False

    : param str input_str: STR parameter that is checked if it can be an int
    : return: True if str is an int, False if str is not an int
    : rtype: bool
    """

    try:
        int(input_str)
        log.debug("%s is an int value", input_str)
        return True
    except ValueError:
        log.debug("%s is not an int value", input_str)
        return False


def check_duration_relation(args, configpath):
    """
    Change existing duration of education  value  to new duration  value by user input
    Calculate count_teams  and end date of education 
    Save changes to config

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    : return: duration
    : rtype: float
    """
    # txt relation variables for later change
    txt_select_duration = textwrap.dedent("""
        You selected to change the duration of your traineeship.
        """)

    duration = None
    end_duration_education = None
    count_teams = None
    # get year
    data_from_existing_config = data_from_configfile(configpath)
    year = int(data_from_existing_config.get("start_year"))

    print(txt_select_duration)
    # re-ask the user for duration and count_teams to save the relation
    duration, count_teams, end_duration_education = input_duration_count_teams(
        args, year)

    # write the changes to config
    write_into_config("duration", duration, configpath)
    write_into_config("count_teams", count_teams, configpath)
    write_into_config("end_duration_education",
                      end_duration_education, configpath)

    return duration
    # end_duration_education, count_teams


def check_duration_relation_namespace(args, configpath):
    """
    Change existing name value  to new name value by given paramater from cmd
    Calculate count of teams , depending of duration input
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # txt_variables for later changes
    txt_selection_relation = textwrap.dedent("""
        You selected to change the duration of your traineeship
        """)

    # values
    duration = args.duration

    end_duration_education = None
    count_teams = None
    # get year
    data_from_existing_config = data_from_configfile(configpath)
    year = int(data_from_existing_config.get("start_year"))
    # get old values for a visible change
    old_duration = data_from_existing_config.get("duration")
    old_count_teams = data_from_existing_config.get("count_teams")

    print(
        f"You want to change the duration from {old_duration} years  to {duration} years ")
    if duration != "3.0" or duration != "3.5" or duration != "2.5" or duration != "3":
        print(f"Sorry duration value: {duration} is not right")
    log.debug(
        f"old value: {old_count_teams}  new value: {count_teams} ")
    log.debug(f"{txt_selection_relation}")
    log.debug(f"The duration:{duration} and the count of teams: {count_teams}")

    # re-ask the user for duration and count_teams to save the relation
    if duration == "3.0" and count_teams == None or duration == "3.5" and count_teams == None or duration == "2.5" and count_teams == None:
        log.debug("duration == 3.0 and count_teams == None or duration == 3.5 and count_teams == None or duration == 2.5 and count_teams == None")
        if duration == "2.5":
            count_teams = 5
        elif duration == "3.0":

            count_teams = 6
        elif duration == "3.5":
            count_teams = 7
        end_duration_education = calculate_team_duration_end(count_teams, year)
        log.debug(
            f"We pass the duration value:{duration} , count teams {count_teams} and end_duration {end_duration_education}")

    elif duration != "3.0" or duration != "3.5" or duration != "2.5":
        log.debug("duration != 3.0 or duration != 3.5 or duration != 2.5")
        args.duration = None
        # need to set value of duration to none, so next function ask for input
        duration, count_teams, end_duration_education = input_duration_count_teams(
            args, year)

    # write the changes to config
    write_into_config("duration", duration, configpath)
    write_into_config("count_teams", count_teams, configpath)
    write_into_config("end_duration_education",
                      end_duration_education, configpath)

    return duration


def check_name_relation(args, configpath):
    """
    Change existing name value  to new name value by user input
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # txt variables for later change
    txt_input_name = "Enter the new name "

    # get old config data
    config = data_from_configfile(configpath)
    old_name = config.get("name")
    # input new name
    new_name = input(txt_input_name)
    print(f"Your name has changed from old name {old_name} to {new_name}")
    # write into configfile
    write_into_config("name", new_name, configpath)


def check_name_relation_namespace(args, configpath):
    """
    Change existing name value  to new name value by given paramater from cmd
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # get old config data
    config = data_from_configfile(configpath)
    old_name = config.get("name")

    # input new name
    new_name = args.name
    print(f"Your name has changed from old name {old_name} to {new_name}")

    # write into configfile
    write_into_config("name", new_name, configpath)


def check_start_year_relation(args, configpath):
    """
    Change existing year value  to new year value by user input
    Ask user if duration of education also changed, and process the answer
    Calculate team start and end date  as relation to the changed start year
    Calculate end duration of education date as relation to the changed start year
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # txt variables for upcoming changes
    txt_new_start_year_input = "Enter the new start year "
    txt_input_min_year = "The year cant be smaller then 1000..try again"
    txt_question_year_change = textwrap.dedent("""Did the duration of your education change?
    Please enter yes or no
    """)

    # get old config data
    config = data_from_configfile(configpath)
    old_year = config.get("start_year")
    new_year = None

    while(True):
        input_is_int = False
        new_year = input(txt_new_start_year_input)
        try:
            input_is_int = check_is_int(
                new_year)
            if int(new_year) < 1000:
                print(txt_input_min_year)
                continue

            if input_is_int == True:
                break
        except ValueError:
            print("Sorry only numbers are allowed. Try again")
            log.debug("Value error")

            continue

    print(f"The old year {old_year} was changed to the new entry {new_year}")

    # RELATION
    # print(txt_relation)
    while True:
        answer = input(txt_question_year_change)
        if "yes" in answer:
            print("We need to adopt the duration value")
            duration = check_duration_relation(args, configpath)
            end_duration_education = str(new_year) + str(duration)
            break

        elif "no" in answer:
            print("We took the old duration value")
            end_duration_education = int(
                new_year) + float(config.get("duration"))
            break

        else:
            print("Wrong answer,try again")
            continue

    # calculate team start and end as relation to the changed start year
    team_number = config.get("team_number")
    new_team_date_start = calculate_team_duration_start(
        int(team_number), int(new_year))
    new_team_date_end = calculate_team_duration_end(
        int(team_number), int(new_year))
    # calculate end duration of education
    count_of_teams = int(config.get("count_teams"))
    end_duration_education = calculate_team_duration_end(
        count_of_teams, int(new_year))
    # write into configfile
    write_into_config("start_year", new_year, configpath)
    write_into_config("end_duration_education",
                      end_duration_education, configpath)
    write_into_config("team_time_start", new_team_date_start, configpath)
    write_into_config("team_time_end", new_team_date_end, configpath)


def check_start_year_relation_namespace(args, configpath):
    """
    Change existing year value  to new year value by given paramater from cmd
    Calculate team start and end date  as relation to the changed start year
    Calculate end duration of education date as relation to the changed start year
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """

    # get old config data
    config = data_from_configfile(configpath)
    old_year = config.get("start_year")
    new_year = args.year

    # txt for later changes
    txt_new_start_year = "Enter the new start year "
    txt_smallest_input_err_msg = "The year cant be smaller then 1000..try again"

    # input year
    while(True):
        # check value for iso format  of year
        log.debug(f"{new_year}")
        input_is_int = False
        input_is_int = check_is_int(
            new_year)
        if input_is_int == False:
            print(textwrap.dedent(
                f"Sorry your Paramater: {new_year} parsed by cmd is not a correct int value, please try again:"))
            log.fatal("INPUT is NOT a number")
            new_year = input(txt_new_start_year)
            log.debug(f"NEW_YEAR INPUT is an INT: {input_is_int}")
            continue
        if int(new_year) < 1000:
            log.debug("Input NUMBER is  UNDER 1000")
            print(textwrap.dedent(
                f"Sorry your Paramater: {new_year} parsed by cmd is not a correct int value, please try again:"))
            print(txt_smallest_input_err_msg)
            new_year = input(txt_new_start_year)
            log.debug(f"NEW_YEAR INPUT is an INT: {input_is_int}")
            continue
        if input_is_int == True and int(new_year) >= 1000:
            break

    print(textwrap.dedent(
        f"The old year {old_year} was changed to the new entry {new_year}"))
    # calculate team start and end as relation to the changed start year
    team_number = config.get("team_number")
    new_team_date_start = calculate_team_duration_start(
        int(team_number), int(new_year))
    new_team_date_end = calculate_team_duration_end(
        int(team_number), int(new_year))
    # calculate end duration of education
    count_of_teams = int(config.get("count_teams"))
    end_duration_education = calculate_team_duration_end(
        count_of_teams, int(new_year))
    # write into configfile
    write_into_config("start_year", new_year, configpath)
    write_into_config("end_duration_education",
                      end_duration_education, configpath)
    write_into_config("team_time_start", new_team_date_start, configpath)
    write_into_config("team_time_end", new_team_date_end, configpath)


def check_team_name_relation(args, configpath):
    """
    Change old team name to new team name by user input
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # get old config data
    config = data_from_configfile(configpath)
    old_team_name = config.get("team")

    # NO RELATION, just input the new name
    new_team_name = input("Enter the new team name ")
    print(
        f"Change the old team name {old_team_name} to new team name {new_team_name}")

    # write the changes to config
    write_into_config("team", new_team_name, configpath)


def check_team_name_relation_namespace(args, configpath):
    """
    Change old team name to new team name by given paramater from cmd
    Save the change to configfile

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # get old config data
    config = data_from_configfile(configpath)
    old_team_name = config.get("team")

    # NO RELATION, just input the new name
    print(args.team)
    new_team_name = args.team
    print(
        f"Change the old team name {old_team_name} to new team name {new_team_name}")

    # write the changes to config
    write_into_config("team", new_team_name, configpath)


def check_team_number_relation_namespace(args, configpath):
    """
    Input new team number for change by cmd
    On wrong cmd input , ask for new input
    Calculate team time start 
    Calculate team time end
    Save changes to config

    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    : return: TRUE/FALSE
    : rtype: bool

    """
    # get old config data
    config = data_from_configfile(configpath)
    old_team_number = config.get("team_number")
    duration = config.get("duration")
    # RELATION team_name,team_start,team_end and duration

    try:
        new_team_number = int(args.team_number)
        log.debug(
            f"Old team number: {old_team_number}  new_team_number: {new_team_number}  duration: {duration}")
        while True:
            if new_team_number >= 1 and new_team_number <= 7:
                print(
                    f"You changed the team number from {old_team_number} to {new_team_number}")
                break
            elif new_team_number < 1 or new_team_number > 7:
                new_team_number = int(input(
                    "Min/Max number is to low/high --> please enter a number between 1-7  "))
                if duration == "3.0" and new_team_number == 7:
                    new_team_number = int(input(
                        "Sorry, please input a number between 1-6. The duration of the education is under 3.5 years   "))
                continue
        # calculate start and end date of the team
        year = int(config.get("start_year"))
        new_team_date_start = calculate_team_duration_start(
            new_team_number, year)
        new_team_date_end = calculate_team_duration_end(
            new_team_number, year)
        # write down the config
        write_into_config("team_number", new_team_number, configpath)
        write_into_config("team_time_start", new_team_date_start, configpath)
        write_into_config("team_time_end", new_team_date_end, configpath)
        # write_into_config("team", name, configpath)
        return True

    except ValueError:
        print(textwrap.dedent("""
        Only numbers are allowed.
        No changes to the config were made
        Just try again the -c --team-number " " option """))
        return False


def check_team_number_relation(args, configpath):
    """
    Change team number by user input.
    Check  duration of education(relation)
    Write the changes to configfile
    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    """
    # get old config data
    config = data_from_configfile(configpath)
    old_team_number = config.get("team_number")
    # RELATION team_name,team_start,team_end and duration
    print("What is the new team number?")
    new_team_number = config_team_number_input(args)
    print(f"You changed {old_team_number} to the {new_team_number}")

    # txt as variable for later changes
    txt_answer_team_change = textwrap.dedent(
        """
        Did the name of the team change?
        Please answer with a yes or no
        """)

    answer_team_change = None
    while True:
        answer_team_change = input(txt_answer_team_change)
        if "yes" in answer_team_change:
            check_team_name_relation(args, configpath)
            break
        elif "no" in answer_team_change:
            break
        else:
            print("Wrong input , try again")
            continue

    # check if count of teams and duration fits ?
    txt_answer_duration_change = textwrap.dedent(
        """
        Did the duration of the education change ?
        Please answer with a yes or no
        """)

    answer_duration_change = None
    while True:
        answer_duration_change = input(txt_answer_duration_change)
        if "yes" in answer_duration_change:
            check_duration_relation(args, configpath)
            break
        elif "no" in answer_duration_change:
            break
        else:
            print("Wrong input , try again")
            continue

    # calculate start and end date of the team
    year = int(config.get("start_year"))
    new_team_date_start = calculate_team_duration_start(
        new_team_number, year)
    new_team_date_end = calculate_team_duration_end(
        new_team_number, year)
    # write down the config
    write_into_config("team_number", new_team_number, configpath)
    write_into_config("team_time_start", new_team_date_start, configpath)
    write_into_config("team_time_end", new_team_date_end, configpath)


def write_into_config(key_input, value_input, configpath):
    """
    Write value to a given key underthe given configpath 
    : param str key_input: Key value given by the cmd line
    : param str value_input: Value given by the cmd line
    : param str configpath: Configpath to the configuration file
    : return: the ConfigParser object
    : rtype: configparse.ConfigParser
    """
    config = ConfigParser()
    config.read(configpath)
    config.set("settings", f"{key_input}", f"{value_input}")
    with open(configpath, "w") as configfile:
        config.write(configfile)
    return config


def user_input_change(args, configpath):
    """
    Input the data that is asked by function to change configs
    : param argparse.Namespace args: Attributes given by the command line
    : param str configpath: Path where the configuration file is stored
    : return: the ConfigParser object
    : rtype: configparse.ConfigParser
    """
    # txt variables for later txt changes
    txt_change_option = textwrap.dedent("""
        "What do you want to change?"
        Your options are
        Name
        Team
        Start year
        Duration
        Current Team Number
        """)

    # show and ask user what he wants to overwrite
    print(txt_change_option)
    # FIXME need a function which will check if the change is possiblee
    # check for right user input
    while(True):
        key_input = input(
            "Please enter one of the upper options ").capitalize()
        print(key_input)

        # need to map the keys  right to the settings --> from Name to name
        if key_input == "Name":
            key_input = "name"
            check_name_relation(args, configpath)
            break
        elif key_input == "Team" or key_input == "team":
            key_input = "team"
            check_team_name_relation(args, configpath)
            break
        elif "Start" in key_input:
            key_input = "start_year"
            check_start_year_relation(args, configpath)
            break
        elif key_input == "Duration":
            key_input = "duration"
            check_duration_relation(args, configpath)
            break
        # no need for user change count of teams, it is calculated now
        # elif "Count" in key_input:
        #    key_input = "count_teams"
        #    check_count_teams_relation(args, configpath)
        #    break
        elif "Current" in key_input:
            key_input = "team_number"
            check_team_number_relation(args, configpath)
            break
        else:
            print("No key in config found --> Try again")
            continue


def cmd_new(args, configpath,databasepath):
    """Creates a new day for the incoming entries"""
    log.debug("New selected %s", args)
    init_cmd=check_config_database_exist(CONFIGPATH,DATABASEPATH)
    if init_cmd ==True:
        # get todays date
        today_date_obj = datetime.today()
        # convert date obj to string 
        today_date_txt=format_date_obj_to_string(today_date_obj)
        #check_month_team_change
        check_team_change_date(today_date_txt,databasepath)

        log.debug(f"TODAY DATE: {today_date_txt}")
        # sql injection 
        sql_data=today_date_txt
        sql_database = Database(databasepath, sql_data)
        sql_database.sql_new_day()
        log.debug(f"SQL DATA: {sql_data} ")
        sql_database.close()  # FIXME Add context manager to simplify the open write close process
        #  database close
        return 0

    elif init_cmd ==False:
         return 1    

def check_month_team_change(date_string):
    """
    Check if new day is  in September or March
    Print warning message if yes
    returns date_string
    """
    month=date_string[5:7]
    month_name="None"
    if month=="08":
        month_name="September"
    elif month=="03":
        month_name="March"  
    else:
        month_name =month      

   
    warning_txt=textwrap.dedent(f"""
    Since it is the {month_name}, you should have changed the team.
    
    You can continue to use the programm.
    Please change the name of the team as soon as possible.

    Change new team name: 
    reportdaily new -t
    """)

    log.debug(f"date_string: {date_string} month: {month} month_name: {month_name}")
    if month=="08" or month=="03":
        print(warning_txt)
        return True

    else:
        log.debug(f"Month {month} is not March/September ")
        return False



def check_team_change_date(date_string,databasepath):
    """
    Check date of new cmd and ask user if it is time to update team name and number
    """
    #check if it is september or march and the team needs to change
    did_the_team_change=None
    did_the_team_change=check_month_team_change(date_string)
    sql_team_entry=None
    if did_the_team_change == True:
        sql_database = Database(databasepath,sql_team_entry)
        sql_team_entry=sql_database.sql_read_database_all_teams(databasepath,sql_team_entry)
    
        for entry in sql_team_entry:
            print(entry)
    else:
        print("TEST")

    # read old team name  and check if it is the same 
    # check team number  and if its the same

    # ask user to input new team name
    # update team number
    # add sql changes to database and add team 
   

def format_date_obj_to_string(date_obj):
    """
    Format the given obj to sql suited string
    """         

    date_string=date_obj.strftime("%Y-%m-%d")

    return date_string

def check_config_database_exist(configpath,databasepath):
    """
    execute check if the init command was used and configfile/database exists
    """
    txt_no_configpath=textwrap.dedent("""
                        No configpath exists
                        Try to use init subcommand first
                        
                        Example:
                        reportdaily init
                        """)

    txt_no_database=textwrap.dedent("""
                            No database exists
                            Try to use init subcommand first
                            
                            Example:
                            reportdaily init
                            """)
    
    # check if configfile exists
    config_exists=os.path.exists(configpath)
    
    # check if database exists 
    database_exists=os.path.exists(databasepath)


    if config_exists==True and database_exists==True:
        log.debug(f"CONFIG EXISTS: {config_exists}  DATABASE EXISTS: {database_exists}")
        return True
    
    elif config_exists == False or database_exists==False :
        # feedback if config exists for user
        if config_exists==False:
            print(txt_no_configpath)
        # feedback if database exists for user
        elif database_exists==False:
            print(txt_no_configpath)
        
        log.debug((f"CONFIG EXISTS: {config_exists}  DATABASE EXISTS: {database_exists}"))
        return False



    



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
    """Parse CLI with: class: `argparse.ArgumentParser` and return parsed result

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
    subparsers = parser.add_subparsers(help='Available sub commands')
    # init cmd
    parser_init = subparsers.add_parser(
        'init', help="Create an initial Configuration file and a sqlite database")
    parser_init.set_defaults(func=cmd_init)
    parser_init.add_argument(
        '--name', "-n", help='Adjust trainee name in the existing configfile')
    parser_init.add_argument(
        '--year', "-y", help='Adjust the start education year of the trainee in the existing config/database')
    parser_init.add_argument(
        '--duration', "-d", help='Adjust  the duration of the education of the trainee in the existing config/database')
    # This value is calculated and is not required any more
    parser_init.add_argument(
        '--team', "-t", help='Adjust the name of the current team in the existing config/database')
    parser_init.add_argument(
        '--team-number', "-tn", help='Adjust the team number of the current team in the existing config/database')
    parser_init.add_argument(
        '--change', '-c', action='store_true', help='Change an existing configuration')

    # new cmd
    parser_new = subparsers.add_parser('new', help="Creates a new day entry")
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
        exit_code = args.func(args, CONFIGPATH, DATABASEPATH)
        return exit_code

    except MissingSubCommand as error:
        log.fatal(error)
        return 888


if __name__ == "__main__":
    sys.exit(main())
