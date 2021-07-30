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

The ``init`` subcommand is required for the first time to initialize the program.

User is asked to answer some question and two files are created.

A configuration file with all the user information and sqlite database.

Configurationpath = ~/.config/reportdaily/reportdailyrc

Databasepath = ~/.config/reportdaily/database.sqlite



.. code-block:: bash 
   
   reportdaily init [-h]
                    [--change]
                    [--change] [--duration DURATION]
                    [--change] [--team TEAM]
                    [--change] [--team-number TEAM_NUMBER]
                    [--change] [--year YEAR]

.. option:: --change | -c

Make changes to the existing config/database

First way:

Use the --change | -c to make changesto the configuration file
   
Example: 

.. code-block:: bash
   

    reportdaily init --change
   
The exisiting config is shown to the user.

User is asked to select an option of the configs which requires changes.

User is asked for the new values.

After answering the questions the changes take effect and a changed config file is displayed for the user.


Second way:

Additional options allow to make changes direct via the command line.
   
Example: 

.. code-block:: bash
   
   reportdaily init --change --name "TEST_NAME"

The exisiting config is shown to the user. 

If the the arguments are properly chosen, then changes are directly saved in the configfile.

If the arguments are wrong, then the user is asked to try again. 

The altered configuration is shown in the command line.


.. option:: --duration=DURATION, -d=DURATION

Example:

.. code-block:: bash
   
   reportdaily init --change --duration "DURATION"

Changes the duration of the education by the passed argument  ""DURATION""".

DURATION argument options: 2.5, 3.0 or 3.5.



.. option:: --team=TEAM, -t=TEAM

Example:

.. code-block:: bash
   
   reportdaily init --change --team "TEAM"

Changes the team name by the passed ""TEAM"" argument.

CARE: Only usable with the --change option.

.. option:: --team-number=TEAM_NUMBER, -tn=TEAM_NUMBER

.. code-block:: bash
   
   reportdaily init --change --team-number "TEAM_NUMBER"

Example:

Changes the team number by the passed ""TEAM_NUMBER"" argument.


.. option:: --year=YEAR, -y="YEAR"

Example: 

.. code-block:: bash
   
   reportdaily init --change --year "YEAR"

Changes the start year of the education  by the passed ""YEAR"" argument.




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


