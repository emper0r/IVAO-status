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
# Pilot Class

import os
import SQL_queries
import PilotInfo_UI
import StatusFlight
import Friends
import sqlite3
import distance
import datetime

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

class PilotInfo(QMainWindow):
    closed = pyqtSignal()
    '''The PilotInfo Class is to show selected player from Pilots Tables to see the status of the flight, like
       departure, destination, miles, route, type of aircraft and flight, etc'''
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = PilotInfo_UI.Ui_QPilotInfo()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        image_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'ivao_status_splash.png')
        self.setWindowIcon(QIcon(image_icon))
        self.callsign = ''
        QObject.connect(self.ui.AddFriend, SIGNAL('clicked()'), self.add_button)

    def status(self, callsign):
        self.callsign = callsign
        Q_db = SQL_queries.sql_query('Get_Pilot_data', (str(callsign),))
        info = Q_db.fetchall()
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../flags')
        ImageAirlines = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../airlines')
        ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ratings')
        if info[0][19] == 'FOLME':
            pass
        else:
            try:
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(info[0][5]),))
                flagCodeOrig = Q_db.fetchone()
                flagCodePath_orig = (ImageFlags + '/%s.png') % flagCodeOrig
                Pixmap = QPixmap(flagCodePath_orig)
                self.ui.DepartureImage.setPixmap(Pixmap)
                Q_db = SQL_queries.sql_query('Get_Airport_Location', (str(info[0][5]),))
                city_orig = Q_db.fetchone()
                self.ui.DepartureText.setText(str(city_orig[0].encode('latin-1')))
                city_orig_point = city_orig[1], city_orig[2]
            except:
                self.ui.DepartureText.setText('Pending...')
                city_orig_point = None

        try:
            Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(info[0][6]),))
            flagCodeDest = Q_db.fetchone()
            flagCodePath_dest = (ImageFlags + '/%s.png') % flagCodeDest
            Pixmap = QPixmap(flagCodePath_dest)
            self.ui.DestinationImage.setPixmap(Pixmap)
            Q_db = SQL_queries.sql_query('Get_Airport_Location', (str(info[0][6]),))
            city_dest = Q_db.fetchone()
            self.ui.DestinationText.setText(str(city_dest[0].encode('latin-1')))
            city_dest_point = city_dest[1], city_dest[2]
        except:
            self.ui.DestinationText.setText('Pending...')
            city_dest_point = None

        self.ui.vidText.setText(str(info[0][0]))
        try:
            code_airline = callsign[:3]
            airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
            if os.path.exists(airlineCodePath) is True:
                Pixmap = QPixmap(airlineCodePath)
                airline = QLabel(self)
                self.ui.airline_image.setPixmap(Pixmap)
            else:
                Q_db = SQL_queries.sql_query('Get_Airline', str(callsign[:3]))
                airline_code = Q_db.fetchone()
                self.ui.airline_image.setText(str(airline_code[0]))
        except:
            pass
        self.ui.callsign_text.setText(callsign)
        self.ui.PilotNameText.setText(str(info[0][1][:-4].encode('latin-1')))
        self.ui.RouteText.setText(str(info[0][9]))
        self.ui.GroundSpeedNumber.setText(str(info[0][3]))
        self.ui.AltitudeNumber.setText(str(info[0][2]))
        self.ui.PobText.setText(str(info[0][8]))
        self.ui.TransponderText.setText(str(info[0][11]))
        self.ui.GSFiledText.setText(str(info[0][17]))
        self.ui.FLText.setText(str(info[0][7]))
        Q_db = SQL_queries.sql_query('Get_Airport_from_ICAO', (str(info[0][15]),))
        altern_city_1 = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_Airport_from_ICAO', (str(info[0][16]),))
        altern_city_2 = Q_db.fetchone()
        if altern_city_1 is None:
            self.ui.Altern_Airport_Text.setText(str('-'))
        else:
            self.ui.Altern_Airport_Text.setText(str(altern_city_1[0]))
        if altern_city_2 is None:
            self.ui.Altern_Airport_Text_2.setText(str('-'))
        else:
            self.ui.Altern_Airport_Text_2.setText(str(altern_city_2[0]))
        try:
            if str(info[0][4]) != '':
                Q_db = SQL_queries.sql_query('Get_Model', ((info[0][4].split('/')[1]),))
                data = Q_db.fetchall()
                self.ui.AirplaneText.setText('Model: %s Fabricant: %s Description: %s' \
                                             % (str(data[0][0]), str(data[0][1]), str(data[0][2])))
        except:
            self.ui.AirplaneText.setText('Pending...')
        Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(info[0][1][-4:]),))
        flagCodeHome = Q_db.fetchone()
        flagCodePath = (ImageFlags + '/%s.png') % flagCodeHome
        Pixmap = QPixmap(flagCodePath)
        self.ui.HomeFlag.setPixmap(Pixmap)
        ratingImage = ImageRatings + '/pilot_level%d.gif' % int(info[0][10])
        Pixmap = QPixmap(ratingImage)
        self.ui.rating_img.setPixmap(Pixmap)
        player_point = info[0][13], info[0][14]
        if city_orig_point is None or city_dest_point is None:
            self.ui.nauticalmiles.setText('Pending...')
            self.ui.progressBarTrack.setValue(0)
        if str(info[0][5]) == str(info[0][6]):
                self.ui.progressBarTrack.setValue(0)
                self.ui.nauticalmiles.setText('Local Flight')
                eta = '00:00:00.000000'
        else:
            try:
                total_miles = distance.distance(city_orig_point, city_dest_point).miles
                dist_traveled = distance.distance(city_orig_point, player_point).miles
                percent = float((dist_traveled / total_miles) * 100.0)
                eta = str(datetime.timedelta(hours=((total_miles - dist_traveled) / float(info[0][3]))))
            except:
                if city_orig_point or city_dest_point is None:
                    percent = 0.0
                eta = '00:00:00.000000'
            self.ui.nauticalmiles.setText('%.1f / %.1f miles - %.1f%%' % (float(dist_traveled), float(total_miles), float(percent)))
            self.ui.progressBarTrack.setValue(int(percent))
        status_plane = StatusFlight.status_flight(callsign)
        self.ui.FlightStatusDetail.setText(str(status_plane))
        self.ui.ETA_Arrive.setText(str(eta)[:-7])
        try:
            start_connected = datetime.datetime(int(str(info[0][18])[:4]), int(str(info[0][18])[4:6]) \
                                                , int(str(info[0][18])[6:8]), int(str(info[0][18])[8:10]) \
                                                , int(str(info[0][18])[10:12]), int(str(info[0][18])[12:14]))
            diff = datetime.datetime.utcnow() - start_connected
            self.ui.time_online_text.setText(str(diff)[:-7])
        except:
            self.ui.time_online_text.setText('Pending...')

    def add_button(self):
        Friends.Friends().add(str(self.ui.vidText.text()).encode('latin-1'))

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
