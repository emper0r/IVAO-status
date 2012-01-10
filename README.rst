===============
 IVAO - STATUS
===============

:Author: Antonio Peña
:E-mail: <emperor.cu@gmail.com>
:License: GPLv3+
:Date: Jul 2011

IVAO (International Virtual Aviation Organisation ™) for its acronym in English, 
is one of the most successful networks for flight simulation. 
You can find more information: http://www.ivao.aero.

IVAO developed its own softwares, and one of them is 
The Eye of IVAO made for Windows.

IVAO - Status was developed with the intention to Linux users 
can check the status of players online on the IVAO network.

REQUIREMENTS
============

First you must have the following dependencies installed to run the application.

* python (version >= 2.6 )
* python-qt4 (version >= 4.8)

INSTALL
=======

Installing main dependencies in Debian/Ubuntu/Kubuntu

    aptitude install python-qt4

INSTALLER BINARY
================

You can download the installer from:

    https://github.com/downloads/emper0r/IVAO-status/IVAO-Status-1.0.5-Linux-x86-Install.bin

OR TRY TO GET THE SOURCE
========================

After install all dependencies download source code:

    https://github.com/emper0r/IVAO-status/archives/master

IVAO-status's git repo is available on GitHub, which can be browsed at:

    https://github.com/emper0r/IVAO-status

and run:

    python ivao_status.py

The database is located at 'database dirpath', and is downloaded with aplication,
In case of loss/crash/deleted/corrupt of the database can type this to rebuild.

    /path/where/run/IVAO-status/cat ivao_status.sql | sqlite3 database/ivao.db

ISSUE TRACKER
=============
Issues are tracked on github, please feel free to ask any question or suggestion
I will fix it or make feature as soon as possible ;-)

https://github.com/emper0r/IVAO-status/issues

SCREENSHOTS
===========

I put some screenshots to can show you how works the app at screenshots path

https://github.com/emper0r/IVAO-status/tree/master/screenshots


LICENSE
=======

See the license file.

SPECIAL THANKS
==============
- rowinggolfer (for show me how Qt works with VERY cool examples :-) ),
  and other friends at #pyqt in irc.freenode.net to help me sometimes too.

- All friends of #pyar in irc.freenode.net starting by facundobatista, StyXman, jmg,
  dlitvakb and many others :)

- Arnd Wippermann to help me at OpenLayers-list 
  for show me how javascript works and Google Layer with OpenStreetMap

- And all my friends for testing my hobbie and push me to become this for
  a better app.
