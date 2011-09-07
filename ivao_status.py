#!/bin/python
# Copyright (c) 2011 by Antonio (emper0r) P. Diaz <emperor.cu@gmail.com>
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
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.Qt import *
import MainWindow_UI
import PilotInfo_UI
import SettingWindow_UI
import urllib2
import sqlite3
import os
import datetime

data_access = 'whazzup.txt'
DataBase = './database/ivao.db'
time_update = 300000

__version__ = '1.0'

rating_pilot = {"0":"OBS - Observer", "2":"SFO - Second Flight Officer", "3":"FFO - First Flight Officer" \
                , "4":"C - Captain", "5":"FC - Flight Captain", "6":"SC - Senior Captain" \
                , "7":"SFC - Senior Flight Captain", "8":"CC - Commercial Captain" \
                , "9":"CFC - Commercial Flight Captain", "10":"CSC - Commercial Senior Captain" \
                , "11":"SUP - Supervisor", "12":"ADM - Administrator"}

rating_atc = {"0":"OBS - Observer", "2":"S1 - Student 1", "3":"S2 - Student 2" \
              , "4":"S3 - Student 3", "5":"C1 - Controller 1", "6":"C2 - Controller 2" \
              , "7":"C3 - Controller 3", "8":"I1 - Instructor 1", "9":"I2 - Instructor 2" \
              , "10":"I3 - Instructor 3", "11":"SUP - Supervisor", "12":"ADM - Administrator"}

position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                , "3":"Ground", "4":"Tower", "5":"Approach", "6":"Center", "7":"Departure"}

class Main(QMainWindow):
    def __init__(self,):
        QMainWindow.__init__(self)
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao.png'))
        self.connect(self.ui.searchpushButton, SIGNAL('clicked()'), self.searchpushButton)
        self.connect(self.ui.METARFindButton, SIGNAL('clicked()'), self.metar)
        self.connect(self.ui.country_list, SIGNAL('activated(QString)'), self.country_view)
        self.connect(self.ui.METARHelpButton, SIGNAL('clicked()'), self.metarHelp)
        self.ui.PILOT_FullList.setColumnWidth(0, 90)
        self.ui.PILOT_FullList.setColumnWidth(1, 65)
        self.ui.PILOT_FullList.setColumnWidth(2, 60)
        self.ui.PILOT_FullList.setColumnWidth(3, 180)
        self.ui.PILOT_FullList.setColumnWidth(4, 160)
        self.ui.PILOT_FullList.setColumnWidth(5, 105)
        self.ui.PILOT_FullList.setColumnWidth(6, 70)
        self.ui.PILOT_FullList.setColumnWidth(7, 75)
        self.ui.PILOT_FullList.setColumnWidth(8, 70)
        self.ui.PilottableWidget.setColumnWidth(0, 90)
        self.ui.PilottableWidget.setColumnWidth(1, 65)
        self.ui.PilottableWidget.setColumnWidth(2, 60)
        self.ui.PilottableWidget.setColumnWidth(3, 180)
        self.ui.PilottableWidget.setColumnWidth(4, 160)
        self.ui.PilottableWidget.setColumnWidth(5, 105)
        self.ui.PilottableWidget.setColumnWidth(6, 70)
        self.ui.PilottableWidget.setColumnWidth(7, 75)
        self.ui.PilottableWidget.setColumnWidth(8, 65)
        self.ui.ATC_FullList.setColumnWidth(1, 70)
        self.ui.ATC_FullList.setColumnWidth(2, 60)
        self.ui.ATC_FullList.setColumnWidth(3, 140)
        self.ui.ATC_FullList.setColumnWidth(4, 190)
        self.ui.ATCtableWidget.setColumnWidth(1, 70)
        self.ui.ATCtableWidget.setColumnWidth(2, 60)
        self.ui.ATCtableWidget.setColumnWidth(3, 240)
        self.ui.ATCtableWidget.setColumnWidth(4, 110)
        self.ui.ATCtableWidget.setColumnWidth(6, 110)
        self.ui.SearchtableWidget.setColumnWidth(0, 50)
        self.ui.SearchtableWidget.setColumnWidth(1, 100)
        self.ui.SearchtableWidget.setColumnWidth(2, 170)
        self.ui.FriendstableWidget.setColumnWidth(0, 50)
        self.ui.FriendstableWidget.setColumnWidth(1, 170)
        self.ui.FriendstableWidget.setColumnWidth(2, 100)
        self.ui.dbTableWidget_1.setColumnWidth(0, 30)
        self.ui.dbTableWidget_2.setColumnWidth(0, 45)
        self.ui.dbTableWidget_2.setColumnWidth(1, 80)
        self.ui.dbTableWidget_2.setColumnWidth(2, 80)
        self.ui.dbTableWidget_2.setColumnWidth(3, 140)
        self.ui.InboundTableWidget.setColumnWidth(0, 90)
        self.ui.InboundTableWidget.setColumnWidth(1, 34)
        self.ui.InboundTableWidget.setColumnWidth(2, 110)
        self.ui.InboundTableWidget.setColumnWidth(3, 30)
        self.ui.InboundTableWidget.setColumnWidth(4, 110)
        self.ui.OutboundTableWidget.setColumnWidth(0, 90)
        self.ui.OutboundTableWidget.setColumnWidth(1, 34)
        self.ui.OutboundTableWidget.setColumnWidth(2, 110)
        self.ui.OutboundTableWidget.setColumnWidth(3, 30)
        self.ui.OutboundTableWidget.setColumnWidth(4, 110)
        self.ui.PILOT_FullList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.ATC_FullList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.FriendstableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.PilottableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.ATCtableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.SearchtableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.METARtableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.OutboundTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.InboundTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.IVAOStatustableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.SearchtableWidget.selectionModel().selectedRows()
        self.ui.SearchtableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.ATC_FullList.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.PILOT_FullList.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.ATCtableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.ui.PilottableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        showInfo_Action = QAction("Show Info", self)
        showInfo_Action.triggered.connect(self.show_pilot_info)
        self.ui.SearchtableWidget.addAction(showInfo_Action)
        self.ui.ATC_FullList.addAction(showInfo_Action)
        self.ui.PILOT_FullList.addAction(showInfo_Action)
        self.ui.ATCtableWidget.addAction(showInfo_Action)
        self.ui.PilottableWidget.addAction(showInfo_Action)
        Pixmap = QPixmap('./images/departures.png')
        self.ui.departures_icon.setPixmap(Pixmap)
        self.ui.departures_icon.show()
        Pixmap = QPixmap('./images/arrivals.png')
        self.ui.arrivals_icon.setPixmap(Pixmap)
        self.ui.arrivals_icon.show()
        self.timer = QTimer(self)
        self.timer.setInterval(time_update)
        self.timer.timeout.connect(self.UpdateDB)
        self.timer.start()
        QTimer.singleShot(1000, self.initial_load)
        self.progress = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress)
        self.progress.hide()
        self.progress.setValue(0)
        self._maptab = None
        
    @property
    def maptab(self):
        if self._maptab is None:
            self._maptab = QWebView()
            self.ui.tabWidget.insertTab(5, self.maptab, 'Map')
        if self.ui.tabWidget.currentIndex() == 0:
            self.ui.tabWidget.setCurrentIndex(5)
        return self._maptab

    def initial_load(self):
        self.statusBar().showMessage('Populating Database', 2000)
        qApp.processEvents()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        db_t1 = cursor.execute("SELECT DISTINCT(Country) FROM icao_codes DESC;")
        db_t1 = cursor.fetchall()
        connection.commit()
        startrow_dbt1 = 0
        db_t2 = cursor.execute("SELECT icao, Latitude, Longitude, City_Airport, Country FROM icao_codes DESC;")
        db_t2 = cursor.fetchall()
        connection.commit()
        startrow_dbt2 = 0

        for line in db_t1:
            if line[0] == None:
                self.ui.dbTableWidget_1.removeRow(self.ui.dbTableWidget_1.rowCount())
            else:
                pass
            country = "%s" % line[0]
            self.ui.country_list.addItem(country)
            self.ui.dbTableWidget_1.insertRow(self.ui.dbTableWidget_1.rowCount())
            flagCodePath = ('./flags/%s.png') % line
            if os.path.exists(flagCodePath) is True:
                Pixmap = QPixmap(flagCodePath)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.dbTableWidget_1.setCellWidget(startrow_dbt1, 0, flag_country)
            else:
                pass
            country = QTableWidgetItem(str(line[0]).encode('utf-8'), 0)
            self.ui.dbTableWidget_1.setItem(startrow_dbt1, 1, country)
            startrow_dbt1 += 1

        for line in db_t2:
            if line[0] == None:
                self.ui.dbTableWidget_2.removeRow(self.ui.dbTableWidget_2.rowCount())
            else:
                pass
            self.ui.dbTableWidget_2.insertRow(self.ui.dbTableWidget_2.rowCount())
            icao = QTableWidgetItem(str(line[0]), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 0, icao)
            latitude = QTableWidgetItem(str(line[1]), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 1, latitude)
            longitude = QTableWidgetItem(str(line[2]), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 2, longitude)
            AirportName = QTableWidgetItem(str(line[3].encode('utf-8')), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 3, AirportName)
            try:
                Country = QTableWidgetItem(str(line[4].encode('utf-8')), 0)
                self.ui.dbTableWidget_2.setItem(startrow_dbt2, 4, Country)
            except:
                pass
            startrow_dbt2 += 1

        connection.close()
        self.ivao_friend()
        qApp.restoreOverrideCursor()

    def UpdateDB(self):
        self.statusBar().showMessage('Downloading info from IVAO', 2000)
        qApp.processEvents()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM status_ivao;")

        try:
            StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + data_access)
        except:
            self.statusBar().showMessage('Error!, when trying to download database status from IVAO. Check your connection to Internet.' \
                                         , 5000)
            sys.exit(1)

        pilot_list = []
        atc_list = []

        for logged_users in StatusURL.readlines():
            if "PILOT" in logged_users:
                pilot_list.append(logged_users)
            if "ATC" in logged_users:
                atc_list.append(logged_users)

        self.ui.IVAOStatustableWidget.setCurrentCell(0, 0)
        pilots_ivao = QTableWidgetItem(str(len(pilot_list)))
        self.ui.IVAOStatustableWidget.setItem(0, 0, pilots_ivao)

        for rows in pilot_list:
            fields = rows.split(":")
            callsign = fields[0]
            vid = fields[1]
            realname = rows.rsplit(":")[2].decode('latin-1')
            clienttype = fields[3]
            latitude = fields[5]
            longitude = fields[6]
            altitude = fields[7]
            groundspeed = fields[8]
            planned_aircraft = fields[9]
            planned_tascruise = fields[10]
            planned_depairport = fields[11]
            planned_altitude = fields[12]
            planned_destairport = fields[13]
            server = fields[14]
            protrevision = fields[15]
            rating = fields[16]
            transponder = fields[17]
            visualrange = fields[19]
            planned_revision = fields[20]
            planned_flighttype = fields[21]
            planned_deptime = fields[22]
            planned_actdeptime = fields[23]
            planned_hrsenroute = fields[24]
            planned_minenroute = fields[25]
            planned_hrsfuel = fields[26]
            planned_minfuel = fields[27]
            planned_altairport = fields[28]
            planned_remarks = fields[29]
            planned_route = fields[30]
            planned_depairport_lat = fields[31]
            planned_depairport_lon = fields[32]
            planned_destairport_lat = fields[33]
            planned_destairport_lon = fields[34]
            time_last_atis_received = fields[36]
            time_connected = fields[37]
            client_software_name = fields[38]
            client_software_version = fields[39]
            adminrating = fields[40]
            atc_or_pilotrating = fields[41]
            planned_altairport2 = fields[42]
            planned_typeofflight = fields[43]
            planned_pob = fields[44]
            true_heading = fields[45]
            onground = fields[46]

            cursor.execute("INSERT INTO status_ivao (callsign, vid, realname, server, clienttype \
            , latitude, longitude, altitude, groundspeed, planned_aircraft, planned_tascruise \
            , planned_depairport, planned_altitude, planned_destairport, server, protrevision \
            , rating, transponder, visualrange, planned_revision, planned_flighttype \
            , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel \
            , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat \
            , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading \
            , onground) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, realname, server, clienttype, latitude, longitude, altitude, groundspeed, planned_aircraft \
             , planned_tascruise, planned_depairport, planned_altitude, planned_destairport, server, protrevision \
             , rating, transponder, visualrange, planned_revision, planned_flighttype \
             , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel \
             , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat \
             , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon \
             , time_last_atis_received, time_connected, client_software_name, client_software_version \
             , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading \
             , onground))
        connection.commit()

        for rows in atc_list:
            fields = rows.split(":")
            callsign = fields[0]
            vid = fields[1]
            realname = rows.rsplit(":")[2].decode('latin-1')
            clienttype = fields[3]
            frequency = fields[4]
            latitude = fields[5]
            longitude = fields[6]
            altitude = fields[7]
            server = fields[14]
            protrevision = fields[15]
            rating = fields[16]
            facilitytype = fields[18]
            visualrange = fields[19]
            atis_message = fields[35]
            time_last_atis_received = fields[36]
            time_connected = fields[37]
            client_software_name = fields[38]
            client_software_version = fields[39]
            adminrating = fields[40]
            atc_or_atcrating = fields[41]

            cursor.execute("INSERT INTO status_ivao (callsign, vid, realname, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision \
            , rating, facilitytype, visualrange \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, realname, server, clienttype, frequency, latitude, longitude, altitude, server \
             , protrevision, rating, facilitytype, visualrange, time_last_atis_received, time_connected \
             , client_software_name, client_software_version, adminrating, atc_or_pilotrating))
        connection.commit()
        
        cursor.execute("SELECT SUM(planned_pob) FROM status_ivao;")
        connection.commit()
        pob = cursor.fetchone()
        pob_ivao = QTableWidgetItem(str(int(pob[0])))
        self.ui.IVAOStatustableWidget.setItem(0, 5, pob_ivao)
        cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC' AND callsign like '%OBS%';")
        connection.commit()
        obs = cursor.fetchone()
        obs_ivao = QTableWidgetItem(str(int(obs[0])))
        cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC';")
        connection.commit()
        atc = cursor.fetchone()
        atcs_ivao = QTableWidgetItem(str((int(atc[0]) - int(obs[0]))))
        self.ui.IVAOStatustableWidget.setItem(0, 1, atcs_ivao)
        self.ui.IVAOStatustableWidget.setItem(0, 2, obs_ivao)
        total_ivao = QTableWidgetItem(str(atc[0] + len(pilot_list)))
        self.ui.IVAOStatustableWidget.setItem(0, 3, total_ivao)
        connection.close()
        self.statusBar().showMessage('Done', 2000)
        qApp.processEvents()
        self.show_tables()
        
    def show_tables(self):
        self.statusBar().showMessage('Populating Controllers and Pilots', 4000)
        self.progress.show()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
                        WHERE clienttype='ATC' ORDER BY vid DESC;")
        rows_atcs = cursor.fetchall()
        startrow = 0
        self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
        while self.ui.ATC_FullList.rowCount () > 0:
            self.ui.ATC_FullList.removeRow(0)

        for row_atc in rows_atcs:
            self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
            col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
            self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
            col_frequency = QTableWidgetItem(str(row_atc[1]), 0)
            self.ui.ATC_FullList.setItem(startrow, 1, col_frequency)
            code_icao = str(row_atc[0][:4])
            cursor.execute("SELECT DISTINCT(Country) FROM icao_codes WHERE ICAO=?", (str(code_icao),))
            flagCode = cursor.fetchone()
            connection.commit()
            flagCodePath = ('./flags/%s.png') % flagCode
            if row_atc[5] == '1.1.14':
                pass
            else:
                try:
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                    else:
                        col_country = QTableWidgetItem(str(flagCode).encode('latin-1'), 0)
                        self.ui.ATC_FullList.setItem(startrow, 2, col_country)
                except:
                    pass
                try:
                    col_facility = QTableWidgetItem(str(position_atc[row_atc[4]]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 3, col_facility)
                except:
                    pass
                col_realname = QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
                self.ui.ATC_FullList.setItem(startrow, 4, col_realname)
                code_atc_rating = row_atc[3]
                ratingImagePath = './ratings/atc_level%d.gif' % int(code_atc_rating)
                try:
                    if os.path.exists(ratingImagePath) is True:
                        Pixmap = QPixmap(ratingImagePath)
                        ratingImage = QLabel(self)
                        ratingImage.setPixmap(Pixmap)
                        self.ui.ATC_FullList.setCellWidget(startrow, 6, ratingImage)
                        col_rating = QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATC_FullList.setItem(startrow, 5, col_rating)
                    else:
                        col_rating = QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATC_FullList.setItem(startrow, 5, col_rating)
                except:
                    pass
                try:
                    start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6]) \
                                                        , int(str(row_atc[5])[6:8]), int(str(row_atc[5])[8:10]) \
                                                        , int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
                except:
                    pass
                diff = abs(datetime.datetime.now() - start_connected)
                col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.ATC_FullList.setItem(startrow, 7, col_time)
            self.progress.setValue(int(float(startrow) / float(self.ui.ATC_FullList.rowCount()) * 100.0))
            startrow += 1
            qApp.processEvents()

        cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, rating, realname, planned_depairport \
                      , planned_destairport, onground, time_connected, groundspeed FROM status_ivao \
                      where clienttype='PILOT' order by vid desc;")
        rows_pilots = cursor.fetchall()
        startrow = 0
        self.ui.PILOT_FullList.insertRow(self.ui.PILOT_FullList.rowCount())

        while self.ui.PILOT_FullList.rowCount () > 0:
            self.ui.PILOT_FullList.removeRow(0)

        for row_pilot in rows_pilots:
            self.ui.PILOT_FullList.setCurrentCell(0, 0)
            self.ui.PILOT_FullList.insertRow(self.ui.PILOT_FullList.rowCount())
            code_airline = row_pilot[0][:3]
            airlineCodePath = './airlines/%s.gif' % code_airline
            try:
                if os.path.exists(airlineCodePath) is True:
                    Pixmap = QPixmap(airlineCodePath)
                    airline = QLabel(self)
                    airline.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setCellWidget(startrow, 0, airline)
                else:
                    code_airline = '-'
                    col_airline = QTableWidgetItem(code_airline, 0)
                    self.ui.PILOT_FullList.setItem(startrow, 0, col_airline)
            except:
                pass
            col_callsign = QTableWidgetItem(str(row_pilot[0]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 1, col_callsign)

            try:
                aircraft = row_pilot[1].split('/')[1]
                if aircraft != '-':
                    pass
            except:
                aircraft = '-'
            col_aircraft = QTableWidgetItem(aircraft, 0)
            self.ui.PILOT_FullList.setItem(startrow, 2, col_aircraft)
            col_realname = QTableWidgetItem(str(row_pilot[3][:-5].encode('latin-1')), 0)
            self.ui.PILOT_FullList.setItem(startrow, 3, col_realname)
            col_rating = QTableWidgetItem(str(rating_pilot[row_pilot[2]]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 4, col_rating)

            code_pilot_rating = row_pilot[2]
            ratingImagePath = './ratings/pilot_level%d.gif' % int(code_pilot_rating)
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QPixmap(ratingImagePath)
                    ratingImage = QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setCellWidget(startrow, 5, ratingImage)
                else:
                    pass
            except:
                pass

            col_departure = QTableWidgetItem(str(row_pilot[4]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 6, col_departure)
            col_destination = QTableWidgetItem(str(row_pilot[5]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 7, col_destination)
            groundspeed = '-'
            try:
                if int(str(row_pilot[6])) == 0:
                    if (row_pilot[8] > 20) and (row_pilot[8] < 100):
                        groundspeed = 'Taking Off'
                    if (row_pilot[8] > 100) and (row_pilot[8] < 150):
                        groundspeed = 'Initial Climbing'
                    if (row_pilot[8] > 150):
                        groundspeed = 'On Route'
                else:
                    if (row_pilot[8] > 0) and (row_pilot[8] < 20):
                        groundspeed = 'Taxing'
                    if (row_pilot[8] == 0):
                        groundspeed = 'On Blocks'
            except:
                if not row_pilot[6]:
                    groundspeed = '-'
            col_status = QTableWidgetItem(groundspeed, 0)
            self.ui.PILOT_FullList.setItem(startrow, 8, col_status)
            start_connected = datetime.datetime(int(str(row_pilot[7])[:4]), int(str(row_pilot[7])[4:6]), int(str(row_pilot[7])[6:8]) \
                , int(str(row_pilot[7])[8:10]), int(str(row_pilot[7])[10:12]), int(str(row_pilot[7])[12:14]))
            diff = abs(datetime.datetime.now() - start_connected)
            col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.PILOT_FullList.setItem(startrow, 9, col_time)
            self.progress.setValue(int(float(startrow) / float(self.ui.PILOT_FullList.rowCount()) * 100.0))
            startrow += 1
            qApp.processEvents()
        connection.close()
        self.progress.hide()
        self.statusBar().showMessage('Done', 2000)
        qApp.processEvents()

    def country_view(self):
        country_selected = self.ui.country_list.currentText()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT(Country) FROM icao_codes WHERE Country=?", (str(country_selected),))
        flagCode = cursor.fetchone()
        connection.commit()
        flagCodePath = ('./flags/%s.png') % country_selected
        Pixmap = QPixmap(flagCodePath)
        self.ui.flagIcon.setPixmap(Pixmap)
        cursor.execute("SELECT icao FROM icao_codes where country=?;", (str(country_selected),))
        icao_country = cursor.fetchall()
        connection.commit()
        self.ui.Inbound_traffic.setText('Inbound Traffic in %s Airports' % (country_selected))
        self.ui.Outbound_traffic.setText('Outbound Traffic in %s Airports' % (country_selected))
        
        self.ui.PilottableWidget.insertRow(self.ui.PilottableWidget.rowCount())
        self.ui.ATCtableWidget.insertRow(self.ui.ATCtableWidget.rowCount())
        
        while self.ui.ATCtableWidget.rowCount() > 0:
            self.ui.ATCtableWidget.removeRow(0)
            
        while self.ui.PilottableWidget.rowCount() > 0:
            self.ui.PilottableWidget.removeRow(0)

        while self.ui.InboundTableWidget.rowCount() > 0:
            self.ui.InboundTableWidget.removeRow(0)
            
        while self.ui.OutboundTableWidget.rowCount() > 0:
            self.ui.OutboundTableWidget.removeRow(0)
            
        startrow_atc = 0
        startrow_pilot = 0
        startrow_in = 0
        startrow_out = 0

        for codes in icao_country:
            cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
            WHERE clienttype='ATC' AND callsign LIKE ? ORDER BY vid DESC;", (('%'+str(codes[0])+'%'),))
            rows_atcs = cursor.fetchall()
            connection.commit()

            cursor.execute("SELECT callsign, planned_aircraft, rating, realname, planned_depairport \
                          , planned_destairport, onground, time_connected, groundspeed FROM status_ivao \
                          WHERE clienttype='PILOT' AND realname LIKE ? ORDER BY vid DESC;", (('%'+str(codes[0])),))
            rows_pilots = cursor.fetchall()
            
            cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_depairport LIKE ?", \
                           (('%'+str(codes[0])),))
            OutboundTrafficAirport = cursor.fetchall()
            
            cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_destairport LIKE ?", \
                           (('%'+str(codes[0])),))
            InboundTrafficAirport = cursor.fetchall()

            connection.commit()

            for row_atc in rows_atcs:
                self.ui.ATCtableWidget.insertRow(self.ui.ATCtableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 0, col_callsign)
                col_frequency = QTableWidgetItem(str(row_atc[1]), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 1, col_frequency)
                col_facility = QTableWidgetItem(str(position_atc[row_atc[4]]), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 2, col_facility)
                col_realname = QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 3, col_realname)
                code_atc_rating = row_atc[3]
                ratingImagePath = './ratings/atc_level%d.gif' % int(code_atc_rating)
                try:
                    if os.path.exists(ratingImagePath) is True:
                        Pixmap = QPixmap(ratingImagePath)
                        ratingImage = QLabel(self)
                        ratingImage.setPixmap(Pixmap)
                        self.ui.ATCtableWidget.setCellWidget(startrow_atc, 6, ratingImage)
                        col_rating = QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATCtableWidget.setItem(startrow_atc, 4, col_rating)
                    else:
                        col_rating = QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATCtableWidget.setItem(startrow_atc, 4, col_rating)
                except:
                    pass
                try:
                    start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6]) \
                                                        , int(str(row_atc[5])[6:8]), int(str(row_atc[5])[8:10]) \
                                                        , int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
                except:
                    pass
                diff = abs(datetime.datetime.now() - start_connected)
                col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 5, col_time)
                qApp.processEvents()
                startrow_atc += 1

            for row_pilot in rows_pilots:
                self.ui.PilottableWidget.setCurrentCell(0, 0)
                self.ui.PilottableWidget.insertRow(self.ui.PilottableWidget.rowCount())

                code_airline = row_pilot[0][:3]
                airlineCodePath = './airlines/%s.gif' % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QPixmap(airlineCodePath)
                        airline = QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.PilottableWidget.setCellWidget(startrow_pilot, 0, airline)
                    else:
                        code_airline = '-'
                        col_airline = QTableWidgetItem(code_airline, 0)
                        self.ui.PilottableWidget.setItem(startrow_pilot, 0, col_airline)
                except:
                    pass

                col_callsign = QTableWidgetItem(str(row_pilot[0]), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 1, col_callsign)

                try:
                    aircraft = row_pilot[1].split('/')[1]
                    if aircraft != '-':
                        pass
                except:
                    aircraft = '-'

                col_aircraft = QTableWidgetItem(aircraft, 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 2, col_aircraft)
                col_realname = QTableWidgetItem(str(row_pilot[3][:-5].encode('latin-1')), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 3, col_realname)
                col_rating = QTableWidgetItem(str(rating_pilot[row_pilot[2]]), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 4, col_rating)

                code_pilot_rating = row_pilot[2]
                ratingImagePath = './ratings/pilot_level%d.gif' % int(code_pilot_rating)
                try:
                    if os.path.exists(ratingImagePath) is True:
                        Pixmap = QPixmap(ratingImagePath)
                        ratingImage = QLabel(self)
                        ratingImage.setPixmap(Pixmap)
                        self.ui.PilottableWidget.setCellWidget(startrow_pilot, 5, ratingImage)
                    else:
                        pass
                except:
                    pass

                col_departure = QTableWidgetItem(str(row_pilot[4]), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 6, col_departure)
                col_destination = QTableWidgetItem(str(row_pilot[5]), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 7, col_destination)
                groundspeed = '-'
                try:
                    if int(str(row_pilot[6])) == 0:
                        if (row_pilot[8] > 20) and (row_pilot[8] < 100):
                            groundspeed = 'Taking Off'
                        if (row_pilot[8] > 100) and (row_pilot[8] < 150):
                            groundspeed = 'Initial Climbing'
                        if (row_pilot[8] > 150):
                            groundspeed = 'On Route'
                    else:
                        if (row_pilot[8] > 0) and (row_pilot[8] < 20):
                            groundspeed = 'Taxing'
                        if (row_pilot[8] == 0):
                            groundspeed = 'On Blocks'
                except:
                    if not row_pilot[6]:
                        col_status = '-'
                col_status = QTableWidgetItem(groundspeed, 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 8, col_status)
                start_connected = datetime.datetime(int(str(row_pilot[7])[:4]), int(str(row_pilot[7])[4:6]) \
                                                    , int(str(row_pilot[7])[6:8]), int(str(row_pilot[7])[8:10]) \
                                                    , int(str(row_pilot[7])[10:12]), int(str(row_pilot[7])[12:14]))
                diff = abs(datetime.datetime.now() - start_connected)
                col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 9, col_time)
                startrow_pilot += 1
                qApp.processEvents()
                
            for inbound in InboundTrafficAirport:
                self.ui.InboundTableWidget.insertRow(self.ui.InboundTableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(inbound[0]), 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 0, col_callsign)
                code_airline = inbound[0][:3]
                airlineCodePath = './airlines/%s.gif' % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QPixmap(airlineCodePath)
                        airline = QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.InboundTableWidget.setCellWidget(startrow_in, 0, airline)
                    else:
                        code_airline = '-'
                        col_airline = QTableWidgetItem(code_airline, 0)
                        self.ui.InboundTableWidget.setItem(startrow_in, 0, col_airline)
                except:
                    pass
                cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(inbound[1]),))
                flagCode = cursor.fetchone()
                connection.commit()
                flagCodePath_orig = ('./flags/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_orig)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.InboundTableWidget.setCellWidget(startrow_in, 1, flag_country)
                cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(inbound[1]),))
                city = cursor.fetchone()
                col_city = ''
                if city == None:
                    col_city = '-'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 2, col_country)
                cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(inbound[2]),))
                flagCode = cursor.fetchone()
                connection.commit()
                flagCodePath_dest = ('./flags/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_dest)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.InboundTableWidget.setCellWidget(startrow_in, 3, flag_country)
                cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(inbound[2]),))
                city = cursor.fetchone()
                col_city = ''
                if city == None:
                    col_city = '-'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 4, col_country)
                if  flagCodePath_orig == flagCodePath_dest:
                    status_flight = 'National'
                else:
                    status_flight = 'International'
                col_flight = QTableWidgetItem(status_flight, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 5, col_flight)
                startrow_in += 1
            
            for outbound in OutboundTrafficAirport:
                self.ui.OutboundTableWidget.insertRow(self.ui.OutboundTableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(outbound[0]), 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 0, col_callsign)
                code_airline = outbound[0][:3]
                airlineCodePath = './airlines/%s.gif' % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QPixmap(airlineCodePath)
                        airline = QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.OutboundTableWidget.setCellWidget(startrow_out, 0, airline)
                    else:
                        code_airline = '-'
                        col_airline = QTableWidgetItem(code_airline, 0)
                        self.ui.OutboundTableWidget.setItem(startrow_out, 0, col_airline)
                except:
                    pass
                cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(outbound[1]),))
                flagCode = cursor.fetchone()
                connection.commit()
                flagCodePath_orig = ('./flags/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_orig)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.OutboundTableWidget.setCellWidget(startrow_out, 1, flag_country)
                cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(outbound[1]),))
                city = cursor.fetchone()
                col_city = ''
                if city == None:
                    col_city = '-'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 2, col_country)
                cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(outbound[2]),))
                flagCode = cursor.fetchone()
                connection.commit()
                flagCodePath_dest = ('./flags/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_dest)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.OutboundTableWidget.setCellWidget(startrow_out, 3, flag_country)
                cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(outbound[2]),))
                city = cursor.fetchone()
                col_city = ''
                if city == None:
                    col_city = '-'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 4, col_country)
                if  flagCodePath_orig == flagCodePath_dest:
                    status_flight = 'National'
                else:
                    status_flight = 'International'
                col_flight = QTableWidgetItem(status_flight, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 5, col_flight)
                startrow_out += 1
            
            qApp.processEvents()
        connection.close()

    def searchpushButton(self):
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        arg = self.ui.SearchEdit.text()
        item = self.ui.SearchcomboBox.currentIndex()

        if item == 0:
            cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where vid like ?;" \
                           , ('%'+str(arg)+'%',))
        elif item == 1:
            cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where callsign like ?;" \
                           , ('%'+str(arg)+'%',))
        elif item == 2:
            cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where realname like ?;" \
                           , ('%'+str(arg)+'%',))
        connection.commit()
        search = cursor.fetchall()

        self.ui.SearchtableWidget.insertRow(self.ui.SearchtableWidget.rowCount())
        while self.ui.SearchtableWidget.rowCount () > 0:
            self.ui.SearchtableWidget.removeRow(0)

        startrow = 0
        for row in search:
            self.ui.SearchtableWidget.insertRow(self.ui.SearchtableWidget.rowCount())
            col_vid = QTableWidgetItem(str(row[0]), 0)
            self.ui.SearchtableWidget.setItem(startrow, 0, col_vid)
            col_callsign = QTableWidgetItem(str(row[1]), 0)
            self.ui.SearchtableWidget.setItem(startrow, 1, col_callsign)
            if row[4] == 'PILOT':
                col_realname = QTableWidgetItem(str(row[2][:-4].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'pilot_level'
            else:
                col_realname = QTableWidgetItem(str(row[2].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'atc_level'
            ratingImagePath = './ratings/%s%d.gif' % (player, int(row[3]))
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QPixmap(ratingImagePath)
                    ratingImage = QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.SearchtableWidget.setCellWidget(startrow, 3, ratingImage)
                else:
                    pass
            except:
                pass

            startrow += 1
            qApp.processEvents()
        connection.close()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.ui.SearchtableWidget.selectRow(self.ui.SearchtableWidget.currentRow()) \
           or Qt.RightButton and self.ui.ATC_FullList.selectRow(self.ui.ATC_FullList.currentRow()):
            self.show_player_info()

    def ivao_friend(self):
        self.statusBar().showMessage('Showing friends list', 2000)
        qApp.processEvents()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM friends_ivao;')
        roster = cursor.fetchall()

        self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
        while self.ui.FriendstableWidget.rowCount () > 0:
            self.ui.FriendstableWidget.removeRow(0)

        startrow = 0
        for row in roster:
            self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
            col_vid = QTableWidgetItem(str(row[0]), 0)
            self.ui.FriendstableWidget.setItem(startrow, 0, col_vid)
            col_realname = QTableWidgetItem(str(row[2].encode('latin-1')), 0)
            self.ui.FriendstableWidget.setItem(startrow, 1, col_realname)
            col_rating = QTableWidgetItem('-', 0)
            self.ui.FriendstableWidget.setItem(startrow, 2, col_rating)
            startrow += 1
        cursor.execute('select friends_ivao.vid, status_ivao.vid from status_ivao \
        , friends_ivao where status_ivao.vid=friends_ivao.vid;')
        friends_parts = cursor.fetchall()
        connection.close()

    def addFriend(self, event):
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("SELECT vid from friends_ivao;")
        vid = cursor.fetchall()
        current_row = self.ui.SearchtableWidget.currentRow()
        current_vid = self.ui.SearchtableWidget.item(current_row, 0)
        current_realname = self.ui.SearchtableWidget.item(current_row, 2)
        total_vid = len(vid)
        insert = True
        if total_vid >= 0:
            for i in range(0, total_vid):
                if int(str(current_vid.text())) == vid[i][0]:
                    msg = 'The friend is already in the list'
                    QMessageBox.information(None, 'Friend of IVAO list', msg)
                    i += 1
                    insert = False
            try:
                if insert is True:
                    vid = current_vid.text()
                    realname = unicode(current_realname.text(), 'latin-1')
                    cursor.execute('INSERT INTO friends_ivao (vid, realname, rating) VALUES (?, ?);', (int(str(vid)), str(realname)), int(rating))
                    connection.commit()
                    self.ivao_friend()
                    self.statusBar().showMessage('Friend Added', 2000)
            except:
                pass
        connection.close()

    def metar(self):
        self.statusBar().showMessage('Downloading METAR', 2000)
        qApp.processEvents()
        icao_airport = self.ui.METAREdit.text()
        METAR = urllib2.urlopen('http://wx.ivao.aero/metar.php?id=%s' % icao_airport)

        if self.ui.METARtableWidget.rowCount() == 0:
            self.ui.METARtableWidget.insertRow(self.ui.METARtableWidget.rowCount())
            col_icao_airport = QTableWidgetItem(str(icao_airport), 0)
            self.ui.METARtableWidget.setItem(0, 0, col_icao_airport)
            col_metar = QTableWidgetItem(str(METAR.readlines()[0]), 0)
            self.ui.METARtableWidget.setItem(0, 1, col_metar)
            startrow = 1
        else:
            self.ui.METARtableWidget.rowCount() > 0
            startrow = self.ui.METARtableWidget.rowCount()
            self.ui.METARtableWidget.insertRow(self.ui.METARtableWidget.rowCount())
            col_icao_airport = QTableWidgetItem(str(icao_airport), 0)
            self.ui.METARtableWidget.setItem(startrow, 0, col_icao_airport)
            col_metar = QTableWidgetItem(str(METAR.readlines()[0]), 0)
            self.ui.METARtableWidget.setItem(startrow, 1, col_metar)
            startrow += 1
            
    def ShowAtMap(self, event):
        current_row = self.ui.SearchtableWidget.currentRow()
        current_vid = self.ui.SearchtableWidget.item(current_row, 0)        
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("SELECT latitude, longitude, callsign, true_heading, clienttype from status_ivao where vid=?;" \
                       ,  (int(current_vid.text()),))
        player = cursor.fetchall()
        latitude, longitude, heading = player[0][0], player[0][1], player[0][3]
        player_location = open('./player_location.html', 'w')
        player_location.write('<html><body>\n')
        player_location.write('  <div id="mapdiv"></div>\n')
        player_location.write('  <script src="http://www.openlayers.org/api/OpenLayers.js"></script>\n')
        player_location.write('  <script>\n')
        player_location.write('    map = new OpenLayers.Map("mapdiv");\n')
        player_location.write('    map.addLayer(new OpenLayers.Layer.OSM());\n')
        player_location.write('    var lonLat = new OpenLayers.LonLat( %f ,%f )\n' % (longitude, latitude))
        player_location.write('         .transform(\n')
        player_location.write('            new OpenLayers.Projection("EPSG:4326"),\n')
        player_location.write('            map.getProjectionObject()\n')
        player_location.write('            );\n')
        if player[0][2][-4:] == '_OBS' or player[0][2][-4:] == '_DEP' or player[0][2][-4:] == '_GND':
            player_location.write('    var zoom = 15;\n')
        elif player[0][2][-4:] == '_TWR' or player[0][2][-4:] == '_APP':
            player_location.write('    var zoom = 14;\n')
        elif player[0][2][-4:] == '_CTR':
            player_location.write('    var zoom = 12;\n')
        else:
            player_location.write('    var zoom = 6;\n')
        player_location.write('    var player=new OpenLayers.Layer.Vector("Player",\n')
        player_location.write('    {\n')
        player_location.write('    styleMap: new OpenLayers.StyleMap({\n')
        player_location.write('         "default": {\n')
        if player[0][4] == 'PILOT':
            player_location.write('         externalGraphic: "./images/airplane.gif",\n')
        else:
            player_location.write('         externalGraphic: "./images/tower.png",\n')
        player_location.write('         graphicWidth: 28,\n')
        player_location.write('         graphicHeight: 28,\n')
        player_location.write('         graphicYOffset: 0,\n')
        player_location.write('         rotation: "${angle}",\n')
        player_location.write('         fillOpacity: "${opacity}"\n')
        player_location.write('         }\n')
        player_location.write('     })\n')
        player_location.write(' });\n')
        player_location.write('   var feature=new OpenLayers.Feature.Vector(\n')
        if player[0][4] == 'PILOT':
            player_location.write('    new OpenLayers.Geometry.Point( lonLat.lon, lonLat.lat), {"angle": %d, opacity: 100});\n' % (heading))
        else:
            player_location.write('    new OpenLayers.Geometry.Point( lonLat.lon, lonLat.lat), {"angle": 0, opacity: 100});\n')
        player_location.write('    player.addFeatures([feature]);\n')
        player_location.write('    map.addLayer(player);\n')
        player_location.write('    map.setCenter (lonLat, zoom);\n')
        player_location.write('  </script>\n')
        player_location.write('</body></html>\n')
        player_location.close()
        self.maptab.load(QUrl('./player_location.html'))

    def metarHelp(self):
        msg = 'Must be entered 4-character alphanumeric code designated for each airport around the world'
        QMessageBox.information(None, 'METAR Help', msg)

    def about(self):
        QMessageBox.about(self, "About IVAO :: Status",
                                """<b>IVAO::Status</b>  version %s<p>License: GPL3+<p>
                                This Aplication can be used to see IVAO operational network.<p>
                                July 2011 Tony P. Diaz  --  emperor.cu@gmail.com <p>"""
                                % (__version__))
    
    def show_pilot_info(self):
        self.pilot_window = PilotInfo(self)
        self.pilot_window.closed.connect(self.show)
        self.pilot_window.show()

    def show_settings(self):
        self.setting_window = Settings(self)
        self.setting_window.closed.connect(self.show)
        self.setting_window.show()

class PilotInfo(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = PilotInfo_UI.Ui_QPilotInfo()
        self.ui.setupUi(self)
        self.parent = parent
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao.png'))

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
        
class Settings(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = SettingWindow_UI.Ui_SettingWindow()
        self.ui.setupUi(self)
        self.parent = parent
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao.png'))
        self.connect(self.ui.SettingAccepButton, SIGNAL('clicked()'), self.settings)
        self.connect(self.ui.Setting_checkBox, SIGNAL("clicked()"), self.set_proxy)
        self.connect(self.ui.Setting_auth, SIGNAL("clicked()"), self.set_auth)
    
    def set_proxy(self):
        if self.ui.Setting_checkBox.isChecked() is True:
            self.ui.proxy_host.setEnabled(True)
            self.ui.proxy_port.setEnabled(True)
            self.ui.lineEdit_host.setEnabled(True)
            self.ui.lineEdit_port.setEnabled(True)
            self.ui.Setting_auth.setEnabled(True)
        else:
            self.ui.proxy_host.setEnabled(False)
            self.ui.proxy_port.setEnabled(False)
            self.ui.lineEdit_host.setEnabled(False)
            self.ui.lineEdit_port.setEnabled(False)
            self.ui.Setting_auth.setEnabled(False)
    
    def set_auth(self):
        if self.ui.Setting_auth.isChecked() is True:
            self.ui.proxy_user.setEnabled(True)
            self.ui.proxy_pass.setEnabled(True)
            self.ui.lineEdit_user.setEnabled(True)
            self.ui.lineEdit_pass.setEnabled(True)
        else:
            self.ui.proxy_user.setEnabled(False)
            self.ui.proxy_pass.setEnabled(False)
            self.ui.lineEdit_user.setEnabled(False)
            self.ui.lineEdit_pass.setEnabled(False)
            
    
    def settings(self):
        minutes = self.ui.spinBox.value()
        time_update = minutes * 60 * 1000
        self.close()
    
    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
        
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()