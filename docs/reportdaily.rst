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

..code:: bash 
   
   reportdaily init

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

:Source code:   https://github.com/SchleichsSalaticus/reportdaily


