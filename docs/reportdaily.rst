:orphan:

reportdaily|version|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Synopsis
~~~~~~~~~~~~~~

.. _invocation:

.. code:: bash

   reportdaily [<GLOBAL_OPTIONS>]  <Command>  [<CMD_OPTIONS>] [<TEXT>]


Description
~~~~~~~~~~~~~~

The reportdaily script provides a command line tool to create edit and export daily weekly or monthly reports.
:command:`reportdaily` to make the functionality accessible for shell
scripts. The script supports several subcommands.


Global Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. program:: reportdaily

.. option:: -h, --help

   Display usage summary.

.. option:: -v

   Set optional  level for the logging module.



CMD_OPTIONS Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WORK IN PROGRESS


Commands
~~~~~~~~~~~~~~

.. HINT: Sort the subcommands alphabetically

new
~~~~~~~~~~~~~

Creates a new day for incoming entries

.. code:: bash

   reportdaily new


add <TEXT>
~~~~~~~~~~~~~

Add a new entry with a timestamp

.. code:: bash

   reportdaily add <TEXT>


change <ID> <TEXT>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

change the text of an  entry by id 

.. code:: bash

   reportdaily  change <ID> <TEXT>

delete <ID> 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

delete entry  by id

.. code:: bash

   reportdaily  delete <ID> 

list <ID> 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

list all entries of the day by id

.. code:: bash

   reportdaily  list <ID> 


export <ID>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

export the day by id

.. code:: bash

   reportdaily  export <ID> 

See also
--------

:Documentation: https://reportdaily.duckdns.org
:Source code:   https://github.com/SchleichsSalaticus/reportdaily


