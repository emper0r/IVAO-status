#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Antonio (emper0r) Peña Diaz <emperor.cu@gmail.com>
#
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
# IVAO-status :: License GPLv3+
#
# AddFriend Class

import os
import SQL_queries
import ConfigParser
import sqlite3

try:
    '''Check if PyQt4 is installed or not, this library is a dependency of all,
    if not installed read the README.rst'''
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtWebKit import *
    from PyQt4.Qt import *
except:
    print ('\nYou have not installed the packages Qt Modules for Python,\n')
    print ('please run command as root:  aptitude install python-qt4\n')
    print ('with all dependencies.\n\n')
    sys.exit(2)

class Friends():
    '''The Class AddFriend is to add/remove the friend in roster at MainTab of MainWindow'''
    def add(self, vid2add):
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute("SELECT vid FROM friends;")
        vid = cursor.fetchall()
        total_vid = len(vid)
        insert = True
        if total_vid >= 0:
            for i in range(0, total_vid):
                if int(vid2add) == vid[i][0]:
                    QMessageBox.information(None, 'Friend of IVAO list', 'The friend is already in the list')
                    i += 1
                    insert = False
            try:
                if insert is True:
                    cursor.execute('INSERT INTO friends (vid, realname, rating, clienttype) \
                    SELECT vid, realname, rating, clienttype FROM status_ivao WHERE vid=?;', (vid2add,))
                    connection.commit()
                    QMessageBox.information(None, 'Friend of IVAO list', 'Friend Added!')
            except:
                pass
        connection.close()
        return insert
