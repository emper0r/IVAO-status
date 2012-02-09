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
# Controller Class

import os
import SQL_queries
import ControllerInfo_UI
import Friends
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

class ControllerInfo(QMainWindow):
    '''The ControllerInfo Class is to show selected player from Controllers Tables to see the status of player
       at the Airport controlled like, freq, country, and ATIS info'''
    closed = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = ControllerInfo_UI.Ui_QControllerInfo()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        image_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../images', 'ivao_status_splash.png')
        self.setWindowIcon(QIcon(image_icon))
        QObject.connect(self.ui.AddFriend, SIGNAL('clicked()'), self.add_button)

    def status(self, callsign):
        self.callsign = callsign
        self.position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                             , "3":"Ground", "4":"Tower", "5":"Approach", "6":"Center", "7":"Departure"}
        Q_db = SQL_queries.sql_query('Get_Controller_data', (str(callsign),))
        info = Q_db.fetchall()
        self.ui.VidText.setText(str(info[0][0]))
        self.ui.ControllerText.setText(str(info[0][1].encode('latin-1')))
        self.ui.SoftwareText.setText('%s %s' % (str(info[0][9]), str(info[0][10])))
        self.ui.ConnectedText.setText(str(info[0][2]))
        self.ui.ATISInfo.setText(str(info[0][7].encode('latin-1')).replace('^\xa7', '\n'))
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../flags')
        ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ratings')
        try:
            Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(callsign[:4]),))
            flagCodeOrig = Q_db.fetchone()
            if flagCodeOrig is None:
                if str(callsign[-4:]) == '_CTR':
                    Q_db = SQL_queries.sql_query('Get_Country_from_FIR', (str(callsign[:4]),))
                    flagCodeOrig = Q_db.fetchone()
                else:
                    Q_db = SQL_queries.sql_query('Get_Country_by_Id', (str(callsign[:2]),))
                    flagCodeOrig = Q_db.fetchone()
                    if flagCodeOrig is None:
                        Q_db = SQL_queries.sql_query('Get_Country_from_Prefix', (str(callsign[:2]),))
                        flagCodeOrig = Q_db.fetchone()
            flagCodePath_orig = (ImageFlags + '/%s.png') % flagCodeOrig
            Pixmap = QPixmap(flagCodePath_orig)
            self.ui.Flag.setPixmap(Pixmap)
            Q_db = SQL_queries.sql_query('Get_Airport_from_ICAO', (str(callsign[:4]),))
            city_orig = Q_db.fetchone()
            if city_orig is None:
                if str(callsign[-4:]) == '_CTR':
                    Q_db = SQL_queries.sql_query('Get_FIR_from_ICAO', (str(callsign[:4]),))
                    city_orig = Q_db.fetchone()
                else:
                    Q_db = SQL_queries.sql_query('Get_Country_by_Id', (str(callsign[:2]),))
                    city_orig = Q_db.fetchone()
                    if city_orig is None:
                        Q_db = SQL_queries.sql_query('Get_Country_from_Prefix', (str(callsign[:2]),))
                        city_orig = Q_db.fetchone()
            self.ui.ControllingText.setText(str(city_orig[0].encode('latin-1')))
        except:
            self.ui.ControllingText.setText('Pending...')
        ratingImagePath = ImageRatings + '/atc_level%d.gif' % int(info[0][5])
        Pixmap = QPixmap(ratingImagePath)
        self.ui.rating_img.setPixmap(Pixmap)
        self.ui.facility_freq_Text.setText(str(self.position_atc[str(info[0][6])]) + ' ' + str(info[0][4]) + ' MHz')
        try:
            start_connected = datetime.datetime(int(str(info[0][8])[:4]), int(str(info[0][8])[4:6]) \
                                                , int(str(info[0][8])[6:8]), int(str(info[0][8])[8:10]) \
                                                , int(str(info[0][8])[10:12]), int(str(info[0][8])[12:14]))
            diff = datetime.datetime.utcnow() - start_connected
            self.ui.TimeOnLineText.setText('Time on line: ' + str(diff)[:-7])
        except:
            self.ui.TimeOnLineText.setText('Pending...')

    def add_button(self):
        Friends.Friends().add(str(self.ui.VidText.text()).encode('latin-1'))

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
