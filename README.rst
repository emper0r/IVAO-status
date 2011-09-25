===============
 IVAO - STATUS
===============

Author: Antonio Peña
E-mail: <emperor.cu@gmail.com>
License: GPLv3+
Date: Jul 2011

IVAO (International Virtual Aviation Organisation ™) for its acronym in English, 
is one of the most successful networks for flight simulation. 
You can find more information: http://www.ivao.aero.

IVAO developed its own softwares, and one of them is 
The Eye of IVAO made for Windows.

IVAO - Status was developed with the intention to Linux users 
can check the status of players online on the IVAO network.

REQUIREMENTS
============

First we have the following dependencies installed to run the application.

* python-qt4 (version >= 4.8.3)
* sqlite3 (version >= 3.7.4)
* libsqlite3-0 (version >= 3.7.4)
* geopy (works with version >= 0.94.1)

INSTALL
=======

Installing main dependencies in Debian/Ubuntu/Kubuntu

    aptitude install python-qt4 sqlite3 libsqlite3-0

Second important dependency is GeoPy found in this link

http://code.google.com/p/geopy/

Download the last tarball and install with simple steps
or can get it into tool path

untar tarball

    tar zvfx geopy-0.94.1.tar.gz

    cd geopy-0.94.1

    python setup.py build

and as root:

    sudo python setup.py install

SOURCE
======

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

LICENSE
=======

See the license file.

SPECIAL THANKS
==============
- rowinggolfer at #pyqt in irc.freenode.net 
  (for show me how Qt works with VERY cool examples :-) ),

- htoothrot at #pyqt in irc.freenode.net to help me sometimes too, and

- Arnd Wippermann to help me at OpenLayers-list 
  for show me how javascript works and Google Layer with OpenStreetMap

- And all my friends for testing my hobbie and push me to become this for
  a better app.

