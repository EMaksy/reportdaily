:orphan:

reportdaily 
===========

Synopsis
--------

.. _invocation:

.. code:: bash

   reportdaily [<GLOBAL_OPTIONS>]  <Command>  [<CMD_OPTIONS>] [<TEXT>]


Description
-----------

The reportdaily script provides a command line tool to create edit and export daily weekly or monthly reports.
:command:`reportdaily` to make the functionality accessible for shell
scripts. The script supports several subcommands.


Global Options
--------------

.. program:: reportdaily

.. option:: -h, --help

   Display usage summary.

.. option:: -v

   Increase verbosity (can be repeated).

.. option:: --version

   Display the software version.



Subcommands
-----------

.. HINT: Sort the subcommands alphabetically

init
~~~~

Is required for the first time use of the programm
User can enter his data directly or he need to answer some questions provided by this command
.. code:: bash 
reportdaily init [-h]
[--name NAME]
[--year YEAR]
[--duration DURATION]
[--count-teams COUNT_TEAMS]
[--team TEAM]
[--team-number TEAM_NUMBER]
[--change]

.. option:: --change

    Allow to make changes to the existing config/database

    First way: --change without additonal options
    
    Example: reportdaily init --change
    
    The exisiting config is shown to the user.
    User is asked to select an  option of the configs which requires changes.
    User is asked for the new values.
    After answering the questions the changes take effect and a changed config file is displayed for the user

    Second way: --change + additional options allow to make changes direct via the command line
    
    Example: reportdaily init --change --name "TEST_NAME"

    The exisiting config is shown to the user.
    If the the arguments are properly chosen then changes are directly taken to the config 
    If the arguments are wrong, the user is asked to try again. 
    The altered config file is displayed  in the command line so the user can check the new configs.

.. option:: --duration=DURATION

   Allow to change the duration of the education by inputing the argument in the command line

   CARE: Only usable with the --change option


.. option:: --team=TEAM

   Allow to change the team name by inputing the argument in the command line

   CARE: Only usable with the --change option

.. option:: --team-number=TEAM_NUMBER

   Allow to change the team number by inputing the argument in the command line
   
   CARE: Only usable with the --change option        

.. option:: --year=YEAR

   Allow to change  the start year of the education  by inputing the argument in the command line

   CARE: Only usable with the --change option 
new
~~~

Creates a new day for incoming entries

.. code:: bash

   reportdaily new


add <TEXT>
~~~~~~~~~~

Add a new entry with a timestamp

.. code:: bash

   reportdaily add <TEXT>


change <ID> <TEXT>
~~~~~~~~~~~~~~~~~~

change the text of an  entry by id 

.. code:: bash

   reportdaily  change <ID> <TEXT>

delete <ID> 
~~~~~~~~~~~

delete entry  by id

.. code:: bash

   reportdaily  delete <ID> 

list <ID> 
~~~~~~~~~

list all entries of the day by id

.. code:: bash

   reportdaily  list <ID> 


export <ID>
~~~~~~~~~~~
export the day by id

.. code:: bash

   reportdaily  export <ID> 

See also
--------

:Source code:   https://github.com/EMaksy/reportdaily


