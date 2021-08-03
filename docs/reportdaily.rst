:orphan:

reportdaily 
===========

Synopsis
--------

.. _invocation:

.. code-block:: bash

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

The user is asked to answer some question. After the input is finished, two files are created:

A configuration file with all the user information and a sqlite database to hold all data.


.. code-block:: bash 

   reportdaily init
   reportdaily init  --help
   reportdaily init  --change [--duration DURATION] [--name Name][--team TEAM] [--team-number TEAM_NUMBER] [--year YEAR]

.. option:: --change, -c

Make changes to the existing config/database

Use the option  `--change` in two different  ways:

 
1. Ask for user input

   .. code-block:: bash

       reportdaily init --change
      
   The exisiting config is shown to the user.

   The user is asked to select an option of the configs which requires changes and to enter new values.

2. Provide additional options allow to make changes direct via the command line.
   
   
   .. code-block:: bash
   
      reportdaily init --change --name "TEST_NAME"

   The exisiting config is shown to the user. 

   If the the arguments are properly chosen, then changes are directly saved in the configfile.
   If the arguments are wrong, then the user is asked to try again. 
   The altered configuration is shown in the command line.


.. option:: --duration=DURATION, -d=DURATION

   .. code-block:: bash
      
      reportdaily init --change --duration "DURATION"

   Changes the duration of the education by the passing argument  ``DURATION``.

``DURATION`` argument options: 2.5, 3.0 or 3.5.

.. option:: --name=NAME, -n=NAME

   .. code-block:: bash

      reportdaily init --change --name "NAME"

   Changes the name of the trainee by the passing ``NAME`` argument.


.. option:: --team=TEAM, -t=TEAM

   .. code-block:: bash
      
      reportdaily init --change --team "TEAM"

   Changes the team name by the passing ``TEAM`` argument.

.. option:: --team-number=TEAM_NUMBER, -tn=TEAM_NUMBER

   .. code-block:: bash
      
      reportdaily init --change --team-number "TEAM_NUMBER"

   Changes the team number by the passing ``TEAM_NUMBER`` argument.


.. option:: --year=YEAR, -y=YEAR

   .. code-block:: bash
      
      reportdaily init --change --year "YEAR"

   Changes the start year of the education by the passing ``YEAR`` argument.


new
~~~

Creates a new day for incoming entries

.. code-block:: bash

   reportdaily new


add <TEXT>
~~~~~~~~~~

Add a new entry with a timestamp

.. code-block:: bash

   reportdaily add <TEXT>


change <ID> <TEXT>
~~~~~~~~~~~~~~~~~~

change the text of an  entry by id 

.. code-block:: bash

   reportdaily  change <ID> <TEXT>

delete <ID> 
~~~~~~~~~~~

delete entry  by id

.. code-block:: bash

   reportdaily  delete <ID> 

list <ID> 
~~~~~~~~~

list all entries of the day by id

.. code-block:: bash

   reportdaily  list <ID> 


export <ID>
~~~~~~~~~~~
export the day by id

.. code-block:: bash

   reportdaily  export <ID> 


Files 
----- 

* User configuration file: :file:`~/.config/reportdaily/reportdailyrc`

* SQLite database: :file:`~/.config/reportdaily/database.sqlite`



See also
--------

:Source code:   https://github.com/EMaksy/reportdaily
