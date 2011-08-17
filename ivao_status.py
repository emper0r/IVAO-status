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
from PyQt4 import QtCore, QtGui, Qt
import MainWindow_UI
import urllib2
import sqlite3
import os
import time
import datetime

IVAO_STATUS = 'whazzup.txt'
DataBase = './database/ivao.db'

rating_pilot = {"1":"OBS - Observer", "2":"SFO - Second Flight Officer", "3":"FFO - First Flight Officer" \
                , "4":"C - Captain", "5":"FC - Flight Captain", "6":"SC - Senior Captain" \
                , "7":"SFC - Senior Flight Captain", "8":"CC - Commercial Captain" \
                , "9":"CFC - Commercial Flight Captain", "10":"CSC - Commercial Senior Captain" \
                , "11":"SUP - Supervisor", "12":"ADM - Administrator"}

rating_atc = {"1":"OBS - Observer", "2":"S1 - Student 1", "3":"S2 - Student 2" \
              , "4":"S3 - Student 3", "5":"C1 - Controller 1", "6":"C2 - Controller 2" \
              , "7":"C3 - Controller 3", "8":"I1 - Instructor 1", "9":"I2 - Instructor 2" \
              , "10":"I3 - Instructor 3", "11":"SUP - Supervisor", "12":"ADM - Administrator"}

position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                , "3":"Ground", "4":"Tower", "5":"Approach/Departure", "6":"Center"}

class Main(QtGui.QMainWindow):
    def __init__(self,):
        QtGui.QMainWindow.__init__(self)
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QtGui.QIcon('./airlines/ivao.jpg'))
        self.connect(self.ui.ExitBtn, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.UpdateBtn, QtCore.SIGNAL('clicked()'), self.UpdateDB)
        self.connect(self.ui.searchpushButton, QtCore.SIGNAL('clicked()'), self.searchpushButton)
        self.connect(self.ui.METARFindButton, QtCore.SIGNAL('clicked()'), self.metar)
        self.connect(self.ui.country_list, QtCore.SIGNAL('activated(QString)'), self.country_view)
        self.connect(self.ui.METARHelpButton, QtCore.SIGNAL('clicked()'), self.metarHelp)
        self.ui.PILOT_FullList.setColumnWidth(0, 90)
        self.ui.PILOT_FullList.setColumnWidth(1, 65)
        self.ui.PILOT_FullList.setColumnWidth(2, 60)
        self.ui.PILOT_FullList.setColumnWidth(3, 180)
        self.ui.PILOT_FullList.setColumnWidth(4, 160)
        self.ui.PILOT_FullList.setColumnWidth(5, 105)
        self.ui.PILOT_FullList.setColumnWidth(6, 70)
        self.ui.PILOT_FullList.setColumnWidth(7, 75)
        self.ui.PILOT_FullList.setColumnWidth(8, 65)
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
        self.ui.ATCtableWidget.setColumnWidth(3, 140)
        self.ui.ATCtableWidget.setColumnWidth(4, 190)
        self.ui.ATCtableWidget.setColumnWidth(6, 110)
        self.ui.SearchtableWidget.setColumnWidth(0, 50)
        self.ui.SearchtableWidget.setColumnWidth(1, 100)
        self.ui.SearchtableWidget.setColumnWidth(2, 170)
        self.ui.FriendstableWidget.setColumnWidth(0, 50)
        self.ui.FriendstableWidget.setColumnWidth(1, 170)
        self.ui.FriendstableWidget.setColumnWidth(2, 100)
        self.ui.dbTableWidget_2.setColumnWidth(0, 75)
        self.ui.dbTableWidget_2.setColumnWidth(1, 70)
        self.ui.dbTableWidget_2.setColumnWidth(2, 110)
        self.ui.PILOT_FullList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.ATC_FullList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.FriendstableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.PilottableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.ATCtableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.SearchtableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.METARtableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.OutboundTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.InboundTableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.IVAOStatustableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.NearbyATCViewTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.SearchtableWidget.selectionModel().selectedRows()
        self.ui.SearchtableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        addAction = Qt.QAction("Add Friend", self)
        addAction.triggered.connect(self.addFriend)
        self.ui.SearchtableWidget.addAction(addAction)
        Pixmap = QtGui.QPixmap('./airlines/ivao.jpg')
        self.ui.logo_ivao.setPixmap(Pixmap)
        self.ui.logo_ivao.show()
        self.timer = Qt.QTimer(self)
        self.timer.setInterval(300000)
        self.timer.timeout.connect(self.UpdateDB)
        self.timer.start()

        QtCore.QTimer.singleShot(1000, self.initial_load)
        
    def initial_load(self):
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()   
        db_t1 = cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes DESC;")
        db_t1 = cursor.fetchall()
        connection.commit()
        startrow_dbt1 = 0
        db_t2 = cursor.execute("SELECT icao, iata, Airport_Name, Country FROM iata_icao_codes DESC;")
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
                Pixmap = QtGui.QPixmap(flagCodePath)
                flag_country = QtGui.QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.dbTableWidget_1.setCellWidget(startrow_dbt1, 0, flag_country)
            else:
                pass
            country = QtGui.QTableWidgetItem(str(line[0]).encode('utf-8'), 0)
            self.ui.dbTableWidget_1.setItem(startrow_dbt1, 1, country)
            startrow_dbt1 += 1

        for line in db_t2:
            if line[0] == None:
                self.ui.dbTableWidget_2.removeRow(self.ui.dbTableWidget_2.rowCount())
            else:
                pass
            self.ui.dbTableWidget_2.insertRow(self.ui.dbTableWidget_2.rowCount())
            icao = QtGui.QTableWidgetItem(str(line[0]), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 0, icao)
            iata = QtGui.QTableWidgetItem(str(line[1]), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 1, iata)
            AirportName = QtGui.QTableWidgetItem(str(line[2].encode('utf-8')), 0)
            self.ui.dbTableWidget_2.setItem(startrow_dbt2, 2, AirportName)
            try:
                Country = QtGui.QTableWidgetItem(str(line[3].encode('utf-8')), 0)
                self.ui.dbTableWidget_2.setItem(startrow_dbt2, 3, Country)
            except:
                pass
            startrow_dbt2 += 1

        connection.close()
        self.ivao_friend()
        QtGui.qApp.restoreOverrideCursor()
        
    def UpdateDB(self):

        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM status_ivao;")

        try:
            StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + IVAO_STATUS)
        except:
            msg = 'Error!, when trying to download database status from IVAO. Check your connection to Internet.'
            QtGui.QMessageBox.information(None, 'Updating DB troubles', msg)
            sys.exit(0)

        pilot_list = []
        atc_list = []

        for logged_users in StatusURL.readlines():
            if "PILOT" in logged_users:
                pilot_list.append(logged_users)
            if "ATC" in logged_users:
                atc_list.append(logged_users)

        self.ui.IVAOStatustableWidget.setCurrentCell(0, 0)
        pilots_ivao = QtGui.QTableWidgetItem(str(len(pilot_list)))
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

        cursor.execute("SELECT SUM(planned_pob) FROM status_ivao;")
        connection.commit()
        pob = cursor.fetchone()
        pob_ivao = QtGui.QTableWidgetItem(str(int(pob[0])))
        self.ui.IVAOStatustableWidget.setItem(0, 5, pob_ivao)

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

        cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
                        WHERE clienttype='ATC' ORDER BY vid DESC;")
        rows_atcs = cursor.fetchall()

        startrow = 0
        self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
        while self.ui.ATC_FullList.rowCount () > 0:
            self.ui.ATC_FullList.removeRow(0)

        for row_atc in rows_atcs:
            self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
            col_callsign = QtGui.QTableWidgetItem(str(row_atc[0]), 0)
            self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
            col_frequency = QtGui.QTableWidgetItem(str(row_atc[1]), 0)
            self.ui.ATC_FullList.setItem(startrow, 1, col_frequency)
            code_icao = str(row_atc[0][:4])
            cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes WHERE ICAO=?", (str(code_icao),))
            flagCode = cursor.fetchone()
            connection.commit()
            flagCodePath = ('./flags/%s.png') % flagCode
            try:
                if os.path.exists(flagCodePath) is True:
                    Pixmap = QtGui.QPixmap(flagCodePath)
                    flag_country = QtGui.QLabel()
                    flag_country.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                else:
                    col_country = QtGui.QTableWidgetItem(str(flagCode).encode('latin-1'), 0)
                    self.ui.ATC_FullList.setItem(startrow, 2, col_country)
            except:
                pass
            col_facility = QtGui.QTableWidgetItem(str(position_atc[row_atc[4]]), 0)
            self.ui.ATC_FullList.setItem(startrow, 3, col_facility)
            col_realname = QtGui.QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
            self.ui.ATC_FullList.setItem(startrow, 4, col_realname)            
            code_atc_rating = row_atc[3]
            ratingImagePath = './ratings/atc_level%d.gif' % int(code_atc_rating)
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QtGui.QPixmap(ratingImagePath)
                    ratingImage = QtGui.QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 6, ratingImage)
                    col_rating = QtGui.QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 5, col_rating)
                else:
                    col_rating = QtGui.QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 5, col_rating)
            except:
                pass
            try:
                start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6]), int(str(row_atc[5])[6:8]) \
                                                    , int(str(row_atc[5])[8:10]), int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
            except:
                pass
            diff = abs(datetime.datetime.now() - start_connected)
            col_time = QtGui.QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.ATC_FullList.setItem(startrow, 7, col_time)
            startrow += 1

        cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, rating, realname, planned_depairport \
                      , planned_destairport, time_connected FROM status_ivao \
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
                    Pixmap = QtGui.QPixmap(airlineCodePath)
                    airline = QtGui.QLabel(self)
                    airline.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setCellWidget(startrow, 0, airline)
                else:
                    code_airline = '-'
                    col_airline = QtGui.QTableWidgetItem(code_airline, 0)
                    self.ui.PILOT_FullList.setItem(startrow, 0, col_airline)
            except:
                pass

            col_callsign = QtGui.QTableWidgetItem(str(row_pilot[0]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 1, col_callsign)

            try:
                aircraft = row_pilot[1].split('/')[1]
                if aircraft != '-':
                    pass
            except:
                aircraft = '-'

            col_aircraft = QtGui.QTableWidgetItem(aircraft, 0)
            self.ui.PILOT_FullList.setItem(startrow, 2, col_aircraft)
            col_realname = QtGui.QTableWidgetItem(str(row_pilot[3][:-5].encode('latin-1')), 0)
            self.ui.PILOT_FullList.setItem(startrow, 3, col_realname)
            col_rating = QtGui.QTableWidgetItem(str(rating_pilot[row_pilot[2]]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 4, col_rating)

            code_pilot_rating = row_pilot[2]
            ratingImagePath = './ratings/pilot_level%d.gif' % int(code_pilot_rating)
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QtGui.QPixmap(ratingImagePath)
                    ratingImage = QtGui.QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setCellWidget(startrow, 5, ratingImage)
                else:
                    pass
            except:
                pass

            col_departure = QtGui.QTableWidgetItem(str(row_pilot[4]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 6, col_departure)
            col_destination = QtGui.QTableWidgetItem(str(row_pilot[5]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 7, col_destination)
            start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]), int(str(row_pilot[6])[6:8]) \
                                                , int(str(row_pilot[6])[8:10]), int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
            diff = abs(datetime.datetime.now() - start_connected)
            col_time = QtGui.QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.PILOT_FullList.setItem(startrow, 9, col_time)
            startrow += 1

        cursor.execute("SELECT COUNT(callsign) FROM status_ivao WHERE clienttype='ATC' AND callsign like '%OBS%';")
        connection.commit()
        obs = cursor.fetchone()
        obs_ivao = QtGui.QTableWidgetItem(str(int(obs[0])))
        cursor.execute("SELECT COUNT(callsign) FROM status_ivao WHERE clienttype='ATC';")
        connection.commit()
        atc = cursor.fetchone()
        atcs_ivao = QtGui.QTableWidgetItem(str((int(atc[0]) - int(obs[0]))))
        self.ui.IVAOStatustableWidget.setItem(0, 1, atcs_ivao)
        self.ui.IVAOStatustableWidget.setItem(0, 2, obs_ivao)
        total_ivao = QtGui.QTableWidgetItem(str(atc[0] + len(pilot_list)))
        self.ui.IVAOStatustableWidget.setItem(0, 3, total_ivao)

        connection.close()
        self.ui.action_update.setText("Ready")

    def  country_view(self):
        country_selected = self.ui.country_list.currentText()
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes WHERE Country=?", (str(country_selected),))
        flagCode = cursor.fetchone()
        connection.commit()

        flagCodePath = ('./flags/%s.png') % country_selected
        Pixmap = QtGui.QPixmap(flagCodePath)
        self.ui.flagIcon.setPixmap(Pixmap)

        cursor.execute("SELECT icao FROM iata_icao_codes where country=?;", (str(country_selected),))
        icao_country = cursor.fetchall()
        connection.commit()

        startrow = 0
        self.ui.ATCtableWidget.insertRow(self.ui.ATCtableWidget.rowCount())
        while self.ui.ATCtableWidget.rowCount () > 0:
            self.ui.ATCtableWidget.removeRow(0)

        startrow_p = 0        
        self.ui.PilottableWidget.insertRow(self.ui.PilottableWidget.rowCount())
        while self.ui.PilottableWidget.rowCount () > 0:
            self.ui.PilottableWidget.removeRow(0)

        for codes in icao_country:
            cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
            WHERE clienttype='ATC' AND callsign LIKE ? ORDER BY vid DESC;", (('%'+str(codes[0])+'%'),))
            rows_atcs = cursor.fetchall()
            connection.commit()

            cursor.execute("SELECT callsign, planned_aircraft, rating, realname, planned_depairport \
                          , planned_destairport, time_connected FROM status_ivao \
                          WHERE clienttype='PILOT' AND realname LIKE ? ORDER BY vid DESC;", (('%'+str(codes[0])),))
            rows_pilots = cursor.fetchall()       
            connection.commit()

            for row_atc in rows_atcs:
                self.ui.ATCtableWidget.insertRow(self.ui.ATCtableWidget.rowCount())
                col_callsign = QtGui.QTableWidgetItem(str(row_atc[0]), 0)
                self.ui.ATCtableWidget.setItem(startrow, 0, col_callsign)
                col_frequency = QtGui.QTableWidgetItem(str(row_atc[1]), 0)
                self.ui.ATCtableWidget.setItem(startrow, 1, col_frequency)
                code_icao = str(row_atc[0][:4])
                cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes WHERE ICAO=?", (str(code_icao),))
                flagCode = cursor.fetchone()
                connection.commit()
                flagCodePath = ('./flags/%s.png') % flagCode
                try:
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QtGui.QPixmap(flagCodePath)
                        flag_country = QtGui.QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.ATCtableWidget.setCellWidget(startrow, 2, flag_country)
                    else:
                        col_country = QtGui.QTableWidgetItem(str(flagCode).encode('latin-1'), 0)
                        self.ui.ATCtableWidget.setItem(startrow, 2, col_country)
                except:
                    pass
                col_facility = QtGui.QTableWidgetItem(str(position_atc[row_atc[4]]), 0)
                self.ui.ATCtableWidget.setItem(startrow, 3, col_facility)
                col_realname = QtGui.QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
                self.ui.ATCtableWidget.setItem(startrow, 4, col_realname)       
                code_atc_rating = row_atc[3]
                ratingImagePath = './ratings/atc_level%d.gif' % int(code_atc_rating)
                try:
                    if os.path.exists(ratingImagePath) is True:
                        Pixmap = QtGui.QPixmap(ratingImagePath)
                        ratingImage = QtGui.QLabel(self)
                        ratingImage.setPixmap(Pixmap)
                        self.ui.ATCtableWidget.setCellWidget(startrow, 6, ratingImage)
                        col_rating = QtGui.QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATCtableWidget.setItem(startrow, 5, col_rating)
                    else:
                        col_rating = QtGui.QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
                        self.ui.ATCtableWidget.setItem(startrow, 5, col_rating)
                except:
                    pass
                try:
                    start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6]), int(str(row_atc[5])[6:8]) \
                                                       , int(str(row_atc[5])[8:10]), int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
                except:
                    pass
                diff = abs(datetime.datetime.now() - start_connected)
                col_time = QtGui.QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.ATCtableWidget.setItem(startrow, 7, col_time)
                startrow += 1

            for row_pilot in rows_pilots:
                self.ui.PilottableWidget.setCurrentCell(0, 0)
                self.ui.PilottableWidget.insertRow(self.ui.PilottableWidget.rowCount())

                code_airline = row_pilot[0][:3]
                airlineCodePath = './airlines/%s.gif' % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QtGui.QPixmap(airlineCodePath)
                        airline = QtGui.QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.PilottableWidget.setCellWidget(startrow_p, 0, airline)
                    else:
                        code_airline = '-'
                        col_airline = QtGui.QTableWidgetItem(code_airline, 0)
                        self.ui.PilottableWidget.setItem(startrow_p, 0, col_airline)
                except:
                    pass

                col_callsign = QtGui.QTableWidgetItem(str(row_pilot[0]), 0)
                self.ui.PilottableWidget.setItem(startrow_p, 1, col_callsign)

                try:
                    aircraft = row_pilot[1].split('/')[1]
                    if aircraft != '-':
                        pass
                except:
                    aircraft = '-'

                col_aircraft = QtGui.QTableWidgetItem(aircraft, 0)
                self.ui.PilottableWidget.setItem(startrow_p, 2, col_aircraft)
                col_realname = QtGui.QTableWidgetItem(str(row_pilot[3][:-5].encode('latin-1')), 0)
                self.ui.PilottableWidget.setItem(startrow_p, 3, col_realname)
                col_rating = QtGui.QTableWidgetItem(str(rating_pilot[row_pilot[2]]), 0)
                self.ui.PilottableWidget.setItem(startrow_p, 4, col_rating)

                code_pilot_rating = row_pilot[2]
                ratingImagePath = './ratings/pilot_level%d.gif' % int(code_pilot_rating)
                try:
                    if os.path.exists(ratingImagePath) is True:
                        Pixmap = QtGui.QPixmap(ratingImagePath)
                        ratingImage = QtGui.QLabel(self)
                        ratingImage.setPixmap(Pixmap)
                        self.ui.PilottableWidget.setCellWidget(startrow_p, 5, ratingImage)
                    else:
                        pass
                except:
                    pass

                col_departure = QtGui.QTableWidgetItem(str(row_pilot[4]), 0)
                self.ui.PilottableWidget.setItem(startrow_p, 6, col_departure)
                col_destination = QtGui.QTableWidgetItem(str(row_pilot[5]), 0)
                self.ui.PilottableWidget.setItem(startrow_p, 7, col_destination)
                start_connected = '%d:%d:%d' % (int(str(row_pilot[6])[-6:-4]), int(str(row_pilot[6])[-4:-2]), int(str(row_pilot[6])[-2:]))
                update = time.ctime()
                start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]), int(str(row_pilot[6])[6:8]) \
                                                    , int(str(row_pilot[6])[8:10]), int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
                diff = abs(datetime.datetime.now() - start_connected)                
                col_time = QtGui.QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.PilottableWidget.setItem(startrow_p, 9, col_time)
                startrow_p += 1

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
            col_vid = QtGui.QTableWidgetItem(str(row[0]), 0)
            self.ui.SearchtableWidget.setItem(startrow, 0, col_vid)
            col_callsign = QtGui.QTableWidgetItem(str(row[1]), 0)
            self.ui.SearchtableWidget.setItem(startrow, 1, col_callsign)
            if row[4] == 'PILOT':
                col_realname = QtGui.QTableWidgetItem(str(row[2][:-4].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'pilot_level'
            else:
                col_realname = QtGui.QTableWidgetItem(str(row[2].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'atc_level'
            ratingImagePath = './ratings/%s%d.gif' % (player, int(row[3]))
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QtGui.QPixmap(ratingImagePath)
                    ratingImage = QtGui.QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.SearchtableWidget.setCellWidget(startrow, 3, ratingImage)
                else:
                    pass
            except:
                pass

            startrow += 1
        connection.close()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.addFriend(event)
    
    def ivao_friend(self):
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
            col_vid = QtGui.QTableWidgetItem(str(row[0]), 0)
            self.ui.FriendstableWidget.setItem(startrow, 0, col_vid)
            col_realname = QtGui.QTableWidgetItem(str(row[2].encode('latin-1')), 0)
            self.ui.FriendstableWidget.setItem(startrow, 1, col_realname)
            startrow += 1
        connection.close()
                    
    def addFriend(self, event):
        connection = sqlite3.connect(DataBase)
        cursor = connection.cursor()
        current_row = self.ui.SearchtableWidget.currentRow()
        current_vid = self.ui.SearchtableWidget.item(current_row, 0)
        current_realname = self.ui.SearchtableWidget.item(current_row, 2)
        if current_row >= 0:
            vid = current_vid.text()
            realname = unicode(current_realname.text(), 'latin-1')
            cursor.execute('INSERT INTO friends_ivao (vid, realname) VALUES (?, ?);', (int(str(vid)), str(realname)))
            connection.commit()
        self.ivao_friend()
        connection.close()
        
    def metar(self):
        icao_airport = self.ui.METAREdit.text()
        METAR = urllib2.urlopen('http://wx.ivao.aero/metar.php?id=%s' % icao_airport)

        if self.ui.METARtableWidget.rowCount() == 0:
            self.ui.METARtableWidget.insertRow(self.ui.METARtableWidget.rowCount())
            col_icao_airport = QtGui.QTableWidgetItem(str(icao_airport), 0)
            self.ui.METARtableWidget.setItem(0, 0, col_icao_airport)
            col_metar = QtGui.QTableWidgetItem(str(METAR.readlines()[0]), 0)
            self.ui.METARtableWidget.setItem(0, 1, col_metar)
            startrow = 1
        else:
            self.ui.METARtableWidget.rowCount() > 0
            startrow = self.ui.METARtableWidget.rowCount()
            self.ui.METARtableWidget.insertRow(self.ui.METARtableWidget.rowCount())
            col_icao_airport = QtGui.QTableWidgetItem(str(icao_airport), 0)
            self.ui.METARtableWidget.setItem(startrow, 0, col_icao_airport)
            col_metar = QtGui.QTableWidgetItem(str(METAR.readlines()[0]), 0)
            self.ui.METARtableWidget.setItem(startrow, 1, col_metar)
            startrow += 1

    def metarHelp(self):
        msg = 'Must be entered 4-character alphanumeric code designated for each airport around the world'
        QtGui.QMessageBox.information(None, 'METAR Help', msg)

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
