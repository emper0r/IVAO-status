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
# BuildUI Class

import os
import ConfigParser
import sqlite3
import Build_UI

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

class Build_datafiles(QMainWindow):
    '''The BuildDB Class to insert into ivao.db all data from [.dat] files'''
    closed = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Build_UI.Ui_QBuildDB()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        image_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images', 'ivao_status_splash.png')
        self.setWindowIcon(QIcon(image_icon))
        self.build_db()

    def build_db(self):
        '''Using official data files of IVAO, you can build the database for the application and keep it updated,
           so it easier for those who maintain the data continue adding information. I think with a database engine
           is most useful in managing data files, so there are more opportunities to perform actions on them better.'''
        self.show()
        qApp.processEvents()
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM aircraft;')
        cursor.execute('DELETE FROM airports;')
        cursor.execute('DELETE FROM airlines;')
        cursor.execute('DELETE FROM countries;')
        cursor.execute('DELETE FROM cprefix;')
        cursor.execute('DELETE FROM fir;')
        cursor.execute('DELETE FROM firs;')
        cursor.execute('DELETE FROM ratings;')
        cursor.execute('DELETE FROM staff;')
        connection.commit()

        '''Importing aircraft.dat'''
        data = open('database/aircraft.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            icao = fields[0]
            fabricant = fields[1]
            model = fields[2].decode('latin-1')
            code = fields[3]
            category = fields[4].strip('\r\n')
            cursor.execute("INSERT INTO aircraft (icao, fabricant, model, code, category) VALUES (?, ?, ?, ?, ?);",
                           (icao, fabricant, model, code, category))
            count += 1
            self.ui.LabelFile.setText('Aircraft.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing airlines.dat'''
        data = open('database/airlines.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            code = fields[0]
            airline_name = fields[1].decode('latin-1')
            callsign = fields[2].decode('latin-1')
            reality = fields[3].strip('\r\n')
            cursor.execute("INSERT INTO airlines (code, airline_name, callsign, reality) VALUES (?, ?, ?, ?);",
                           (code, airline_name, callsign, reality))
            count += 1
            self.ui.LabelFile.setText('Airlines.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing airports.dat'''
        data = open('database/airports.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            icao = fields[0]
            airport = fields[1].decode('latin-1')
            city = fields[2].decode('latin-1')
            country = fields[3]
            fir = fields[3]
            latitude = fields[4]
            longitude = fields[5].strip('\r\n')
            cursor.execute("INSERT INTO airports (icao, airport, city, country, fir, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?);",
                           (icao, airport, city, country, fir, latitude, longitude))
            count += 1
            self.ui.LabelFile.setText('Airports.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing cprefix.dat'''
        data = open('database/cprefix.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            icao_initial = fields[0]
            id_country = fields[1].strip('\r\n')
            cursor.execute("INSERT INTO cprefix (icao_initial, id_country) VALUES (?, ?);",
                           (icao_initial, id_country))
            count += 1
            self.ui.LabelFile.setText('Cprefix.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing firs.dat'''
        data = open('database/firs.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            fir = fields[0]
            location = fields[1]
            id_country = fields[2]
            city = fields[3].decode('latin-1')
            control_type = fields[4]
            latitude = fields[5]
            longitude = fields[6]
            try:
                name = fields[7].decode('latin-1').strip('\r\n')
            except:
                name = '-'
            cursor.execute("INSERT INTO firs (fir, location, id_country, city, control_type, latitude, longitude, name) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                           (fir, location, id_country, city, control_type, latitude, longitude, name))
            count += 1
            self.ui.LabelFile.setText('Firs.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing ratings.dat'''
        data = open('database/ratings.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            id = fields[0]
            controller_level = fields[1]
            controller_rating = fields[2]
            pilot_level = fields[3]
            pilot_rating = fields[4].strip('\r\n')
            cursor.execute("INSERT INTO ratings (id, controller_level, controller_rating, pilot_level, pilot_rating) VALUES (?, ?, ?, ?, ?);",
                           (id, controller_level, controller_rating, pilot_level, pilot_rating))
            count += 1
            self.ui.LabelFile.setText('Ratings.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()

        '''Importing countries.dat'''
        data = open('database/countries.dat', 'r').readlines()
        count = 0
        for item in data:
            fields = item.split(":")
            id_country = fields[0]
            country = fields[1].decode('latin-1')
            icao = fields[2]
            latitude = fields[3]
            longitude = fields[4].strip('\r\n')
            cursor.execute("INSERT INTO countries (id_country, country, icao, latitude, longitude) VALUES (?, ?, ?, ?, ?);"
                           , (id_country, country, icao, latitude, longitude))
            count += 1
            self.ui.LabelFile.setText('Countries.dat - [ %d / %d ]' % (count, len(data)))
            self.ui.progressBar.setValue( float(count) / float(len(data)) * 100.0)
            qApp.processEvents()
        connection.commit()
