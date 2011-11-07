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

import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtWebKit import *
    from PyQt4.Qt import *
except:
    print ('\nNot Have Qt Module for Python, please run command as root: "aptitude install python-qt4"')
    print ('with all dependencies.\n\n')
    print  ('If you has installed before, it\'s pretty sure your system made an update for python package so,\n')
    print  ('You have to reinstall again GeoPy.\n')
    sys.exit(2)
try:
    from geopy import distance
except:
    print ('\nNot Have GeoPy installed, please download from "http://code.google.com/p/geopy/" or can hit it')
    print ('into tools path, read README.rst for more info to install it.\n')
    sys.exit(2)

import MainWindow_UI
import PilotInfo_UI
import ControllerInfo_UI
import SettingWindow_UI
import urllib2

try:
    import sqlite3
except:
    print ('\nNot have installed sqlite3 module for Python, please runn command')
    print ('as root: "aptitude install sqlite3 libsqlite3-0"\n')
    sys.exit(2)

import os
import datetime
import ConfigParser
import time

__version__ = '1.0'
url = 'http://de1.www.ivao.aero/'

class Main(QMainWindow):
    def __init__(self,):
        QMainWindow.__init__(self)
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao_status_splash.png'))
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
        self.ui.PilottableWidget.setColumnWidth(7, 80)
        self.ui.PilottableWidget.setColumnWidth(8, 65)
        self.ui.ATC_FullList.setColumnWidth(1, 70)
        self.ui.ATC_FullList.setColumnWidth(2, 40)
        self.ui.ATC_FullList.setColumnWidth(3, 180)
        self.ui.ATC_FullList.setColumnWidth(4, 70)
        self.ui.ATC_FullList.setColumnWidth(5, 128)
        self.ui.ATC_FullList.setColumnWidth(8, 40)
        self.ui.ATCtableWidget.setColumnWidth(1, 70)
        self.ui.ATCtableWidget.setColumnWidth(2, 60)
        self.ui.ATCtableWidget.setColumnWidth(3, 240)
        self.ui.ATCtableWidget.setColumnWidth(4, 110)
        self.ui.ATCtableWidget.setColumnWidth(5, 108)
        self.ui.ATCtableWidget.setColumnWidth(6, 110)
        self.ui.SearchtableWidget.setColumnWidth(0, 50)
        self.ui.SearchtableWidget.setColumnWidth(1, 100)
        self.ui.SearchtableWidget.setColumnWidth(2, 170)
        self.ui.FriendstableWidget.setColumnWidth(0, 50)
        self.ui.FriendstableWidget.setColumnWidth(1, 290)
        self.ui.FriendstableWidget.setColumnWidth(2, 105)
        self.ui.dbTableWidget_1.setColumnWidth(0, 30)
        self.ui.dbTableWidget_2.setColumnWidth(0, 45)
        self.ui.dbTableWidget_2.setColumnWidth(1, 80)
        self.ui.dbTableWidget_2.setColumnWidth(2, 80)
        self.ui.dbTableWidget_2.setColumnWidth(3, 140)
        self.ui.InboundTableWidget.setColumnWidth(0, 90)
        self.ui.InboundTableWidget.setColumnWidth(1, 34)
        self.ui.InboundTableWidget.setColumnWidth(2, 120)
        self.ui.InboundTableWidget.setColumnWidth(3, 30)
        self.ui.InboundTableWidget.setColumnWidth(4, 120)
        self.ui.OutboundTableWidget.setColumnWidth(0, 90)
        self.ui.OutboundTableWidget.setColumnWidth(1, 34)
        self.ui.OutboundTableWidget.setColumnWidth(2, 120)
        self.ui.OutboundTableWidget.setColumnWidth(3, 30)
        self.ui.OutboundTableWidget.setColumnWidth(4, 120)
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
        self.ui.FriendstableWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.showInfo_Action = QAction("Show Info", self)
        self.showMap_Action = QAction("Show at Map", self)
        self.showDelete_Action = QAction("Delete Friend", self)
        self.ui.SearchtableWidget.addAction(self.showInfo_Action)
        self.ui.SearchtableWidget.addAction(self.showMap_Action)
        self.ui.ATC_FullList.addAction(self.showInfo_Action)
        self.ui.ATC_FullList.addAction(self.showMap_Action)
        self.ui.PILOT_FullList.addAction(self.showInfo_Action)
        self.ui.PILOT_FullList.addAction(self.showMap_Action)
        self.ui.ATCtableWidget.addAction(self.showInfo_Action)
        self.ui.ATCtableWidget.addAction(self.showMap_Action)
        self.ui.PilottableWidget.addAction(self.showInfo_Action)
        self.ui.PilottableWidget.addAction(self.showMap_Action)
        self.ui.FriendstableWidget.addAction(self.showInfo_Action)
        self.ui.FriendstableWidget.addAction(self.showMap_Action)
        self.ui.FriendstableWidget.addAction(self.showDelete_Action)
        self.showInfo_Action.triggered.connect(self.action_click)
        self.showMap_Action.triggered.connect(self.action_click)
        self.showDelete_Action.triggered.connect(self.action_click)
        Pixmap = QPixmap('./images/departures.png')
        self.ui.departures_icon.setPixmap(Pixmap)
        self.ui.departures_icon.show()
        Pixmap = QPixmap('./images/arrivals.png')
        self.ui.arrivals_icon.setPixmap(Pixmap)
        self.ui.arrivals_icon.show()
        QTimer.singleShot(1000, self.initial_load)
        self.progress = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress)
        self.progress.hide()
        self.progress.setValue(0)
        self._maptab = None
        self.rating_pilot = {"0":"OBS - Observer", "2":"SFO - Second Flight Officer", "3":"FFO - First Flight Officer" \
                , "4":"C - Captain", "5":"FC - Flight Captain", "6":"SC - Senior Captain" \
                , "7":"SFC - Senior Flight Captain", "8":"CC - Commercial Captain" \
                , "9":"CFC - Commercial Flight Captain", "10":"CSC - Commercial Senior Captain" \
                , "11":"SUP - Supervisor", "12":"ADM - Administrator"}

        self.rating_atc = {"0":"OBS - Observer", "2":"S1 - Student 1", "3":"S2 - Student 2" \
                      , "4":"S3 - Student 3", "5":"C1 - Controller 1", "6":"C2 - Controller 2" \
                      , "7":"C3 - Controller 3", "8":"I1 - Instructor 1", "9":"I2 - Instructor 2" \
                      , "10":"I3 - Instructor 3", "11":"SUP - Supervisor", "12":"ADM - Administrator"}

        self.position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                        , "3":"Ground", "4":"Tower", "5":"Approach", "6":"Center", "7":"Departure"}

        config = ConfigParser.RawConfigParser()
        if os.path.exists('Config.cfg'):
            config.read('Config.cfg')
            self.timer = QTimer(self)
            self.timer.setInterval(config.getint('Time_Update', 'time'))
            self.timer.timeout.connect(self.connect)
            self.timer.start()
        else:
            config.add_section('Settings')
            config.set('Settings', 'use_proxy', '0')
            config.set('Settings', 'host', '')
            config.set('Settings', 'port', '')
            config.set('Settings', 'auth', '0')
            config.set('Settings', 'user', '')
            config.set('Settings', 'pass', '')
            config.add_section('Info')
            config.set('Info', 'data_access', 'whazzup.txt')
            config.set('Info', 'url', url)
            config.add_section('Database')
            config.set('Database', 'db', 'ivao.db')
            config.add_section('Time_Update')
            config.set('Time_Update', 'time', '300000')
            config.add_section('Map')
            config.set('Map', 'auto_refresh', '0')
            config.set('Map', 'label_Pilots', '0')
            config.set('Map', 'label_ATCs', '0')
            with open('Config.cfg', 'wb') as configfile:
                config.write(configfile)
        self.pilot_list = []
        self.atc_list = []
        self.ui.tabWidget.currentChanged.connect(self.ivao_friend)

    @property
    def maptab(self):
        if self._maptab is None and self.ui.tabWidget.currentIndex() != 5:
            self._maptab = QWebView()
            self.ui.tabWidget.insertTab(5, self.maptab, 'Map')
        else:
            self.ui.tabWidget.setCurrentIndex(5)
        return self._maptab

    def initial_load(self):
        self.statusBar().showMessage('Populating Database', 2000)
        qApp.processEvents()
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        db_t1 = cursor.execute("SELECT DISTINCT(Country) FROM icao_codes ORDER BY Country ASC;")
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
        qApp.processEvents()
        self.statusBar().showMessage('Showing friends list', 2000)
        self.ivao_friend()
        self.country_view()
        qApp.restoreOverrideCursor()

    def connect(self):
        self.statusBar().showMessage('Trying connecting to IVAO', 3000)
        qApp.processEvents()
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')        
        try:
            use_proxy = config.getint('Settings', 'use_proxy')
            auth = config.getint('Settings', 'auth')
            host = config.get('Settings', 'host')
            port = config.get('Settings', 'port')
            user = config.get('Settings', 'user')
            pswd = config.get('Settings', 'pass')
            if use_proxy == 2 and auth == 2:
                passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
                passmgr.add_password(None, 'http://' + host + ':' + port, user, pswd)
                authinfo = urllib2.ProxyBasicAuthHandler(passmgr)
                proxy_support = urllib2.ProxyHandler({"http" : "http://" + host + ':' + port})
                opener = urllib2.build_opener(proxy_support, authinfo)
                urllib2.install_opener(opener)
                StatusURL = urllib2.urlopen(config.get('Info', 'url') + config.get('Info', 'data_access'))
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port), str(user), str(pswd)))
                qApp.processEvents()
            if use_proxy == 2 and auth == 0:
                proxy_support = urllib2.ProxyHandler({"http" : "http://" + host + ':' + port})
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                StatusURL = urllib2.urlopen(config.get('Info', 'url') + config.get('Info', 'data_access'))
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port)))
                qApp.processEvents()
            if use_proxy == 0 and auth == 0:
                StatusURL = urllib2.urlopen(config.get('Info', 'url') + config.get('Info', 'data_access'))
                qApp.processEvents()

            self.statusBar().showMessage('Downloading info from IVAO', 2000)
            qApp.processEvents()
            self.pilot_list = []
            self.atc_list = []
            for logged_users in StatusURL.readlines():
                if "PILOT" in logged_users:
                    self.pilot_list.append(logged_users)
                if "ATC" in logged_users:
                    self.atc_list.append(logged_users)

            self.update_db()

        except IOError:
            self.statusBar().showMessage('Error! when trying to download info from IVAO. Check your connection to Internet.')

    def update_db(self):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM status_ivao;")
        qApp.processEvents()

        for rows in self.pilot_list:
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
            , onground) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
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

        for rows in self.atc_list:
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
            atis_message = fields[35].decode('latin-1')
            time_last_atis_received = fields[36]
            time_connected = fields[37]
            client_software_name = fields[38]
            client_software_version = fields[39]
            adminrating = fields[40]
            atc_or_atcrating = fields[41]

            cursor.execute("INSERT INTO status_ivao (callsign, vid, realname, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision, rating, facilitytype, visualrange \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, atis_message) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, realname, server, clienttype, frequency, latitude, longitude, altitude, server \
             , protrevision, rating, facilitytype, visualrange, time_last_atis_received, time_connected \
             , client_software_name, client_software_version, adminrating, atc_or_pilotrating, atis_message))
        connection.commit()
        pilots_ivao = atcs_ivao = obs_ivao = 0
        cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='PILOT';")
        connection.commit()
        pilots = cursor.fetchone()
        cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC';")
        connection.commit()
        atc = cursor.fetchone()
        cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC' AND callsign like '%OBS%';")
        connection.commit()
        obs = cursor.fetchone()
        cursor.execute("SELECT SUM(planned_pob) FROM status_ivao;")
        connection.commit()
        pob = cursor.fetchone()
        self.ui.IVAOStatustableWidget.setCurrentCell(-1, -1)
        pilots_ivao = QTableWidgetItem(str(pilots[0]))
        atcs_ivao = QTableWidgetItem(str((int(atc[0]) - int(obs[0]))))
        obs_ivao = QTableWidgetItem(str(int(obs[0])))
        total_ivao = QTableWidgetItem(str(atc[0] + pilots[0]))
        if pob[0] is None:
            pob_ivao = QTableWidgetItem(str(0))
        else:
            pob_ivao = QTableWidgetItem(str(int(pob[0])))

        self.ui.IVAOStatustableWidget.setItem(0, 0, pilots_ivao)
        self.ui.IVAOStatustableWidget.setItem(1, 0, atcs_ivao)
        self.ui.IVAOStatustableWidget.setItem(2, 0, obs_ivao)
        self.ui.IVAOStatustableWidget.setItem(3, 0, total_ivao)
        self.ui.IVAOStatustableWidget.setItem(5, 0, pob_ivao)
        connection.close()
        self.statusBar().showMessage('Done', 2000)
        qApp.processEvents()
        self.show_tables()
        self.ivao_friend()

    def status_plane(self, callsign):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, planned_depairport \
                      , planned_destairport, onground, time_connected, groundspeed, planned_altitude, Latitude, Longitude \
                      FROM status_ivao WHERE clienttype='PILOT' AND callsign = ?;", (str(callsign),))
        get_status = cursor.fetchone()
        groundspeed = '-'
        for row_pilot in get_status:
            try:
                cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?", (str(get_status[2]),))
                city_orig = cursor.fetchone()
                city_orig_point = float(city_orig[1]), float(city_orig[2])
                cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?", (str(get_status[3]),))
                city_dest = cursor.fetchone()
                city_dest_point = float(city_dest[1]), float(city_dest[2])
                pilot_position = get_status[8], get_status[9]
                total_miles = distance.distance(city_orig_point, city_dest_point).miles
                dist_traveled = distance.distance(city_orig_point, pilot_position).miles
                percent = (float(dist_traveled) / float(total_miles)) * 100.0

                if percent > 105 :
                    groundspeed = 'Diverted'
                    return groundspeed
                else:
                    if int(str(get_status[4])) == 0:
                        if (percent >= 0) and (percent <= 5):
                            groundspeed = 'Takeoff'
                        if (percent >= 5) and (percent <= 10):
                            groundspeed = 'Initial Climbing'
                        if (percent >= 10) and (percent <= 20):
                            groundspeed = 'Climbing'
                        if (percent >= 20) and (percent <= 70):
                            groundspeed = 'On Route'
                        if (percent >= 70) and (percent <= 80):
                            groundspeed = 'Descending'
                        if (percent >= 80) and (percent <= 90):
                            groundspeed = 'Initial Approach'
                        if (percent >= 90) and (percent <= 95):
                            groundspeed = 'Final Approach'
                        return groundspeed
                    else:
                        if ((get_status[6] > 0) and (get_status[6] <= 30)) and (percent < 2):
                            groundspeed = 'Departing'
                        if (percent >= 2) and (percent <= 5):
                            groundspeed = 'Taking Off'
                        if ((percent >= 98) and ((get_status[6] <= 200) and (get_status[6] >= 30))):
                            groundspeed = 'Landed'
                        if (get_status[6] < 30) and (percent > 99):
                            groundspeed = 'Taxing to Gate'
                        if (get_status[6] == 0) and (percent > 99):
                            groundspeed = 'On Blocks'
                        if (get_status[6] == 0) and (percent <= 1):
                            groundspeed = 'Boarding'
                        if (get_status[6] == 0) and (percent >= 10 and percent <= 90):
                            groundspeed = 'Altern Airport'
                        return groundspeed
            except:
                groundspeed = 'Fill Flight Plan'
                return groundspeed

    def show_tables(self):
        self.statusBar().showMessage('Populating Controllers and Pilots', 10000)
        self.progress.show()
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
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

            if str(row_atc[0][:4]) == 'IVAO':
                self.ui.ATC_FullList.setColumnWidth(2, 60)
                col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                flagCodePath = ('./images/ivao_member.png')
                Pixmap = QPixmap(flagCodePath)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                col_country = QTableWidgetItem('IVAO Member', 0)
                self.ui.ATC_FullList.setItem(startrow, 3, col_country)

            elif str(row_atc[0][2:3]) == '-' or str(row_atc[0][2:3]) == '_':
                cursor.execute('SELECT Country FROM division_ivao WHERE Division=?;', (str(row_atc[0][:2]),))
                div_ivao = cursor.fetchone()
                if row_atc is None or div_ivao is None:
                    pass
                else:
                    flagCodePath = ('./flags/%s.png') % str(div_ivao[0])
                    col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                    Pixmap = QPixmap(flagCodePath)
                    flag_country = QLabel()
                    flag_country.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                    col_country = QTableWidgetItem(str(div_ivao[0]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 3, col_country)
            else:
                code_icao = str(row_atc[0][:4])
                cursor.execute("SELECT DISTINCT(Country) FROM icao_codes WHERE ICAO=?", (str(code_icao),))
                flagCode = cursor.fetchone()
                connection.commit()
                col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                flagCodePath = ('./flags/%s.png') % flagCode
                if os.path.exists(flagCodePath) is True:
                    Pixmap = QPixmap(flagCodePath)
                    flag_country = QLabel()
                    flag_country.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                    col_country = QTableWidgetItem(str(flagCode[0]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 3, col_country)
                    self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                else:
                    col_country = QTableWidgetItem(str(flagCode).encode('latin-1'), 0)
                    self.ui.ATC_FullList.setItem(startrow, 2, col_country)
                    self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
            col_frequency = QTableWidgetItem(str(row_atc[1]), 0)
            self.ui.ATC_FullList.setItem(startrow, 1, col_frequency)
            if row_atc[5] == '1.1.14':
                pass
            try:
                col_facility = QTableWidgetItem(str(self.position_atc[row_atc[4]]), 0)
                self.ui.ATC_FullList.setItem(startrow, 4, col_facility)
            except:
                pass
            col_realname = QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
            self.ui.ATC_FullList.setItem(startrow, 5, col_realname)
            code_atc_rating = row_atc[3]
            ratingImagePath = './ratings/atc_level%d.gif' % int(code_atc_rating)
            try:
                if os.path.exists(ratingImagePath) is True:
                    Pixmap = QPixmap(ratingImagePath)
                    ratingImage = QLabel(self)
                    ratingImage.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 7, ratingImage)
                    col_rating = QTableWidgetItem(str(self.rating_atc[row_atc[3]]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 6, col_rating)
                else:
                    col_rating = QTableWidgetItem(str(self.rating_atc[row_atc[3]]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 7, col_rating)
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
            self.ui.ATC_FullList.setItem(startrow, 8, col_time)
            self.progress.setValue(int(float(startrow) / float(len(rows_atcs)) * 100.0))
            startrow += 1
            qApp.processEvents()

        cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, rating, realname, planned_depairport \
                      , planned_destairport, time_connected FROM status_ivao \
                      WHERE clienttype='PILOT' ORDER BY vid desc;")
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
                    cursor.execute('SELECT Airline FROM airlines_codes WHERE Code = ?', (str(row_pilot[0][:3]),))
                    airline_code = cursor.fetchone()
                    if airline_code is None:
                        col_airline = QTableWidgetItem(str(row_pilot[0]))
                    else:
                        col_airline = QTableWidgetItem(str(airline_code[0]), 0)
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
            col_rating = QTableWidgetItem(str(self.rating_pilot[row_pilot[2]]), 0)
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
            status_plane = self.status_plane(row_pilot[0])
            col_status = QTableWidgetItem(str(status_plane), 0)
            col_status.setForeground(QBrush(QColor(self.get_color(status_plane))))
            self.ui.PILOT_FullList.setItem(startrow, 8, col_status)
            start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]), int(str(row_pilot[6])[6:8]) \
                                , int(str(row_pilot[6])[8:10]), int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
            diff = abs(datetime.datetime.now() - start_connected)
            col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.PILOT_FullList.setItem(startrow, 9, col_time)
            self.progress.setValue(int(float(startrow) / float(len(rows_pilots)) * 100.0))
            startrow += 1
            qApp.processEvents()
        connection.close()
        self.progress.hide()
        self.statusBar().showMessage('Done', 2000)
        qApp.processEvents()
        if config.getint('Map', 'auto_refresh') == 2:
            self.all2map()
        else:
            pass
        self.country_view()

    def country_view(self):
        country_selected = self.ui.country_list.currentText()
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
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
                          , planned_destairport, time_connected FROM status_ivao \
                          WHERE clienttype='PILOT' AND realname LIKE ? ORDER BY vid DESC;", (('%'+str(codes[0])),))
            rows_pilots = cursor.fetchall()

            cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_depairport LIKE ?", \
                           ((str(codes[0])),))
            OutboundTrafficAirport = cursor.fetchall()

            cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_destairport LIKE ?", \
                           ((str(codes[0])),))
            InboundTrafficAirport = cursor.fetchall()

            connection.commit()

            for row_atc in rows_atcs:
                self.ui.ATCtableWidget.insertRow(self.ui.ATCtableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 0, col_callsign)
                col_frequency = QTableWidgetItem(str(row_atc[1]), 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 1, col_frequency)
                col_facility = QTableWidgetItem(str(self.position_atc[row_atc[4]]), 0)
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
                        self.ui.ATCtableWidget.setCellWidget(startrow_atc, 5, ratingImage)
                        col_rating = QTableWidgetItem(str(self.rating_atc[row_atc[3]]), 0)
                        self.ui.ATCtableWidget.setItem(startrow_atc, 4, col_rating)
                    else:
                        col_rating = QTableWidgetItem(str(self.rating_atc[row_atc[3]]), 0)
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
                self.ui.ATCtableWidget.setItem(startrow_atc, 6, col_time)
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
                        cursor.execute('SELECT Airline FROM airlines_codes WHERE Code = ?', (str(row_pilot[0][:3]),))
                        airline_code = cursor.fetchone()
                        if airline_code is None:
                            col_airline = QTableWidgetItem(str(row_pilot[0]))
                        else:
                            col_airline = QTableWidgetItem(str(airline_code[0]), 0)
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
                col_rating = QTableWidgetItem(str(self.rating_pilot[row_pilot[2]]), 0)
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
                status_plane = self.status_plane(row_pilot[0])
                col_status = QTableWidgetItem(str(status_plane), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 8, col_status)
                col_status.setForeground(QBrush(QColor(self.get_color(status_plane))))
                start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]) \
                                                    , int(str(row_pilot[6])[6:8]), int(str(row_pilot[6])[8:10]) \
                                                    , int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
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
                        code_airline = str(inbound[0])
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
                    col_city = 'Pending...'
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
                    col_city = 'Pending...'
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
                        code_airline = str(outbound[0])
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
                    col_city = 'Pending...'
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
                    col_city = 'Pending...'
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
        self.ui.PilottableWidget.setCurrentCell(-1, -1)
        self.ui.ATCtableWidget.setCurrentCell(-1, -1)

    def get_color(self, status_plane):
        color = 'black'
        if status_plane == 'Boarding':
            color = 'green'
        if status_plane == 'Departing':
            color = 'green'
        if status_plane == 'Takeoff':
            color = 'dark cyan'
        if status_plane == 'Initial Climbing':
            color = 'dark cyan'
        if status_plane == 'Climbing':
            color = 'blue'
        if status_plane == 'On Route':
            color = 'dark blue'
        if status_plane == 'Descending':
            color = 'blue'
        if status_plane == 'Initial Approach':
            color = 'orange'
        if status_plane == 'Final Approach':
            color = 'orange'
        if status_plane == 'Landed':
            color = 'red'
        if status_plane == 'Taxing to Gate':
            color = 'dark magenta'
        if status_plane == 'On Blocks':
            color = 'dark red'
        if status_plane == 'Fill Flight Plan':
            color = 'black'
        if status_plane == 'Diverted':
            color = 'dark gray'
        return color

    def search_button(self):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
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

    def action_click(self, event=None):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        sender = self.sender()
        if self.ui.SearchtableWidget.currentRow() >= 0:
            row = self.ui.SearchtableWidget.currentIndex().row()
            if row == -1:
                pass
            else:
                current_row = self.ui.SearchtableWidget.currentRow()
                current_callsign = self.ui.SearchtableWidget.item(current_row, 1)
                self.ui.SearchtableWidget.setCurrentCell(-1, -1)
                cursor.execute('SELECT clienttype FROM status_ivao WHERE callsign=?;', ((str(current_callsign.text())),))
                clienttype = cursor.fetchone()
                if sender == self.showInfo_Action:
                    if str(clienttype[0]) == 'PILOT':
                        self.show_pilot_info(current_callsign.text())
                    else:
                        self.show_controller_info(current_callsign.text())
                if sender == self.showMap_Action:
                    cursor.execute('SELECT planned_depairport, planned_destairport FROM status_ivao WHERE callsign=?;' \
                                   , ((str(current_callsign.text())),))
                    icao_depdest = cursor.fetchall()
                    self.view_map(current_callsign.text(), icao_depdest[0][0], icao_depdest[0][1])
        if self.ui.ATC_FullList.currentRow() >= 0:
            row = self.ui.ATC_FullList.currentIndex().row()
            if row == -1:
                pass
            else:
                current_row = self.ui.ATC_FullList.currentRow()
                current_callsign = self.ui.ATC_FullList.item(current_row, 0)
                self.ui.ATC_FullList.setCurrentCell(-1, -1)
                if sender == self.showInfo_Action:
                    if current_callsign is None:
                        pass
                    else:
                        self.show_controller_info(current_callsign.text())
                if sender == self.showMap_Action:
                    self.view_map(current_callsign.text(), None, None)
        if self.ui.ATCtableWidget.currentRow() >= 0:
            row = self.ui.ATCtableWidget.currentIndex().row()
            if row == -1:
                pass
            else:
                current_row = self.ui.ATCtableWidget.currentRow()
                current_callsign = self.ui.ATCtableWidget.item(current_row, 0)
                if sender == self.showInfo_Action:
                    self.show_controller_info(current_callsign.text())
                if sender == self.showMap_Action:
                    self.view_map(current_callsign.text(), None, None)
                self.ui.ATCtableWidget.setCurrentCell(-1, -1)
        if self.ui.PILOT_FullList.currentRow() >= 0:
            row = self.ui.PILOT_FullList.currentIndex().row()
            if row == -1:
                pass
            else:
                current_row = self.ui.PILOT_FullList.currentRow()
                current_callsign = self.ui.PILOT_FullList.item(current_row, 1)
                icao_orig = self.ui.PILOT_FullList.item(current_row, 6)
                icao_dest = self.ui.PILOT_FullList.item(current_row, 7)
                if sender == self.showInfo_Action:
                    self.show_pilot_info(current_callsign.text())
                if sender == self.showMap_Action:
                    self.view_map(current_callsign.text(), icao_orig.text(), icao_dest.text())
                self.ui.PILOT_FullList.setCurrentCell(-1, -1)
        if self.ui.PilottableWidget.currentRow() >= 0:
            row = self.ui.PilottableWidget.currentIndex().row()
            if row == -1:
                pass
            else:
                current_row = self.ui.PilottableWidget.currentRow()
                current_callsign = self.ui.PilottableWidget.item(current_row, 1)
                icao_orig = self.ui.PilottableWidget.item(current_row, 6)
                icao_dest = self.ui.PilottableWidget.item(current_row, 7)
                if sender == self.showInfo_Action:
                    self.show_pilot_info(current_callsign.text())
                if sender == self.showMap_Action:
                    self.view_map(current_callsign.text(), icao_orig.text(), icao_dest.text())
                self.ui.PilottableWidget.setCurrentCell(-1, -1)
        if self.ui.FriendstableWidget.currentRow() >= 0:
            current_row = self.ui.FriendstableWidget.currentIndex().row()
            current_vid = self.ui.FriendstableWidget.item(current_row, 0)
            cursor.execute('SELECT clienttype, callsign FROM status_ivao WHERE vid=?;', ((int(current_vid.text())),))
            friend_data = cursor.fetchall()
            if current_row == -1:
                pass
            else:
                try:
                    if sender == self.showInfo_Action:
                            if str(friend_data[0][0]) == 'PILOT':
                                self.show_pilot_info(str(friend_data[0][1]))
                            else:
                                self.show_controller_info(str(friend_data[0][1]))
                    if sender == self.showMap_Action:
                        cursor.execute('SELECT planned_depairport, planned_destairport FROM status_ivao WHERE callsign=?;' \
                                       , ((str(friend_data[0][1])),))
                        icao_depdest = cursor.fetchall()
                        self.view_map(str(friend_data[0][1]), icao_depdest[0][0], icao_depdest[0][1])
                    if sender == self.showDelete_Action:
                        cursor.execute('DELETE FROM friends_ivao WHERE vid=?;', (int(current_vid.text()),))
                        self.statusBar().showMessage('Friend Deleted', 2000)
                        connection.commit()
                        connection.close()
                        self.ivao_friend()
                except:
                    if friend_data == []:
                        msg = "The user %d is off-line, can't see any info" % (int(current_vid.text()))
                        QMessageBox.information(None, 'Friends List', msg)

    def ivao_friend(self):
        self.ui.PILOT_FullList.setCurrentCell(-1, -1)
        self.ui.ATC_FullList.setCurrentCell(-1, -1)
        self.ui.PilottableWidget.setCurrentCell(-1, -1)
        self.ui.ATCtableWidget.setCurrentCell(-1, -1)
        self.ui.SearchtableWidget.setCurrentCell(-1, -1)
        self.ui.FriendstableWidget.setCurrentCell(-1, -1)
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute('SELECT vid, realname, rating, clienttype FROM friends_ivao;')
        roster = cursor.fetchall()
        self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
        while self.ui.FriendstableWidget.rowCount () > 0:
            self.ui.FriendstableWidget.removeRow(0)

        startrow = 0
        roster_row = 0
        for row in roster:
            self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
            col_vid = QTableWidgetItem(str(row[0]), 0)
            self.ui.FriendstableWidget.setItem(startrow, 0, col_vid)
            cursor.execute('SELECT vid FROM status_ivao where vid=?;', (int(row[0]),))
            check = cursor.fetchone()
            try:
                if check[0] == row[0]:
                    Pixmap = QPixmap('./images/airplane_online.png')
                    online = QLabel(self)
                    online.setPixmap(Pixmap)
                    self.ui.FriendstableWidget.setCellWidget(startrow, 3, online)
                    roster_row += 1
            except:
                Pixmap = QPixmap('./images/airplane_offline.png')
                offline = QLabel(self)
                offline.setPixmap(Pixmap)
                self.ui.FriendstableWidget.setCellWidget(startrow, 3, offline)
                roster_row += 1
            col_realname = QTableWidgetItem(str(row[1].encode('latin-1')), 0)
            self.ui.FriendstableWidget.setItem(startrow, 1, col_realname)
            if str(row[2]) != '-':
                if str(row[3]) == 'ATC':
                    ratingImagePath = './ratings/atc_level%d.gif' % int(row[2])
                else:
                    ratingImagePath = './ratings/pilot_level%d.gif' % int(row[2])
                Pixmap = QPixmap(ratingImagePath)
                ratingImage = QLabel(self)
                ratingImage.setPixmap(Pixmap)
                col_rating = self.ui.FriendstableWidget.setCellWidget(startrow, 2, ratingImage)
            else:
                col_rating = QTableWidgetItem('-', 0)
                self.ui.FriendstableWidget.setItem(startrow, 2, col_rating)
            startrow += 1
        qApp.processEvents()
        connection.close()                

    def metar(self):
        self.statusBar().showMessage('Downloading METAR', 2000)
        qApp.processEvents()
        icao_airport = self.ui.METAREdit.text()
        try:
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
        except:
            self.statusBar().showMessage('Error! during try get Metar info, check your internet connection...', 4000)

    def view_map(self, vid, icao_orig=None, icao_dest=None):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT longitude, latitude FROM icao_codes WHERE ICAO=?;", (str(icao_orig),))
        icao_orig = cursor.fetchone()
        cursor.execute("SELECT longitude, latitude FROM icao_codes WHERE ICAO=?;", (str(icao_dest),))
        icao_dest = cursor.fetchone()
        cursor.execute("SELECT latitude, longitude, callsign, true_heading, clienttype FROM status_ivao WHERE callsign=?;" \
                       ,  (str(vid),))
        player = cursor.fetchall()
        latitude, longitude, heading = player[0][0], player[0][1], player[0][3]
        player_location = open('./player_location.html', 'w')
        player_location.write('<html><body>\n')
        player_location.write('  <div id="mapdiv"></div>\n')
        player_location.write('  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAjpkAC9ePGem0lIq5XcMiuhR_wWLPFku8Ix9i2SXYRVK3e45q1BQUd_beF8dtzKET_EteAjPdGDwqpQ"></script>\n')
        player_location.write('  <script src="./OpenLayers/OpenLayers.js"></script>\n')
        player_location.write('  <script>\n')
        player_location.write('\n')
        player_location.write('    map = new OpenLayers.Map("mapdiv",\n')
        player_location.write('             {   projection : new OpenLayers.Projection("EPSG:900913"),\n')
        player_location.write('                 maxResolution:156543.0339,\n')
        player_location.write('                 maxExtent:new OpenLayers.Bounds(-20037508, -20037508,20037508, 20037508.34)\n')
        player_location.write('             });\n')
        player_location.write('\n')
        player_location.write('    ghyb = new OpenLayers.Layer.Google(\n')
        player_location.write('         "Google Satellite",\n')
        player_location.write('         {type: G_SATELLITE_MAP, sphericalMercator:true, numZoomLevels: 22}\n')
        player_location.write('         );\n')
        player_location.write('\n')
        player_location.write('    map.addLayers([ghyb]);\n')
        player_location.write('\n')
        player_location.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % (longitude, latitude))
        player_location.write('         .transform(\n')
        player_location.write('            new OpenLayers.Projection("EPSG:4326"),\n')
        player_location.write('            map.getProjectionObject()\n')
        player_location.write('            );\n')
        if player[0][2][-4:] == '_OBS' or player[0][2][-4:] == '_DEP' or player[0][2][-4:] == '_GND' \
           or icao_orig is None or icao_dest is None:
            player_location.write('    var zoom = 15;\n')
        elif player[0][2][-4:] == '_TWR' or player[0][2][-4:] == '_APP':
            player_location.write('    var zoom = 14;\n')
        elif player[0][2][-4:] == '_CTR':
            player_location.write('    var zoom = 12;\n')
        else:
            player_location.write('    var zoom = 5;\n')
        player_location.write('    var player=new OpenLayers.Layer.Vector("Player",\n')
        player_location.write('    {\n')
        player_location.write('    styleMap: new OpenLayers.StyleMap({\n')
        player_location.write('         "default": {\n')
        if player[0][4] == 'PILOT':
            player_location.write('         externalGraphic: "./images/airplane.gif",\n')
        else:
            player_location.write('         externalGraphic: "./images/tower.png",\n')
        player_location.write('         graphicWidth: 20,\n')
        player_location.write('         graphicHeight: 20,\n')
        player_location.write('         graphicYOffset: 0,\n')
        player_location.write('         rotation: "${angle}",\n')
        if player[0][4] == 'ATC':
            player_location.write('         fillColor: "white",\n')
            player_location.write('         strokeColor: "white",\n')
            player_location.write('         fillOpacity: "0.05",\n')
        else:
            player_location.write('         fillOpacity: "${opacity}",\n')
        player_location.write('             label: "%s",\n' % str(player[0][2]))
        player_location.write('             fontColor: "white",\n')
        if str(player[0][2][-4:]) == '_CTR':
            player_location.write('             fontSize: "12px",\n')
            player_location.write('             fontWeight: "bold",\n')
        else:
            player_location.write('             fontSize: "10px",\n')
        player_location.write('             fontFamily: "Courier New, monospace",\n')
        player_location.write('             labelAlign: "cm",\n')
        player_location.write('             labelXOffset: 30,\n')
        player_location.write('             labelYOffset: 5\n')
        player_location.write('         }\n')
        player_location.write('      })\n')
        player_location.write('   });\n')
        if str(player[0][4]) == 'ATC':
            player_location.write('     var ratio = OpenLayers.Geometry.Polygon.createRegularPolygon(\n')
            player_location.write('        new OpenLayers.Geometry.Point(position.lon, position.lat),\n')
            if str(player[0][2][-4:]) == '_OBS' or str(player[0][2][-4:]) == '_DEP' or str(player[0][2][-4:]) == '_GND':
                player_location.write('       20000,\n')
            elif str(player[0][2][-4:]) == '_TWR':
                player_location.write('       40000,\n')
            elif str(player[0][2][-4:]) == '_APP':
                player_location.write('       60000,\n')
            elif str(player[0][2][-4:]) == '_CTR':
                pass
            else:
                player_location.write('       60000,\n')
            player_location.write('        360\n')
            player_location.write('     );\n')
            player_location.write('   var controller_ratio = new OpenLayers.Feature.Vector(ratio);\n')
            player_location.write('   player.addFeatures([controller_ratio]);\n')
        player_location.write('\n')
        if str(player[0][4]) == 'PILOT':
            player_location.write('    var vectorLayer = new OpenLayers.Layer.Vector("Vector Layer");\n')
            player_location.write('    var style_green = {\n')
            player_location.write('     strokeColor: "#00FF00",\n')
            player_location.write('     strokeOpacity: 0.7,\n')
            player_location.write('     strokeWidth: 2\n')
            player_location.write('    };\n')
            player_location.write('    var style_red = {\n')
            player_location.write('     strokeColor: "#FF0000",\n')
            player_location.write('     strokeOpacity: 0.7,\n')
            player_location.write('     strokeWidth: 2\n')
            player_location.write('    };\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var points = [];\n')
                player_location.write('    var point_plane = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('    points.push(point_plane);\n')
            else:
                player_location.write('    var points_green = [];\n')
                player_location.write('    var point_orig = new OpenLayers.Geometry.Point(%f, %f);\n' % (icao_orig[0], icao_orig[1]))
                player_location.write('    var point_orig_f = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('\n')
                player_location.write('    var points_red = [];\n')
                player_location.write('    var point_dest = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('    var point_dest_f = new OpenLayers.Geometry.Point(%f, %f);\n' % (icao_dest[0], icao_dest[1]))
                player_location.write('\n')
                player_location.write('    points_green.push(point_orig);\n')
                player_location.write('    points_green.push(point_orig_f);\n')
                player_location.write('\n')
                player_location.write('    points_red.push(point_dest);\n')
                player_location.write('    points_red.push(point_dest_f);\n')
            player_location.write('\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var lineString = new OpenLayers.Geometry.LineString(points);\n')
                player_location.write('    lineString.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
            else:
                player_location.write('    var lineString_green = new OpenLayers.Geometry.LineString(points_green);\n')
                player_location.write('    lineString_green.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
                player_location.write('    var lineString_red = new OpenLayers.Geometry.LineString(points_red);\n')
                player_location.write('    lineString_red.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
            player_location.write('\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var lineFeature = new OpenLayers.Feature.Vector(lineString, null, null);\n')
                player_location.write('    vectorLayer.addFeatures([lineFeature]);\n')
            else:
                player_location.write('    var lineFeature_green = new OpenLayers.Feature.Vector(lineString_green, null, style_green);\n')
                player_location.write('    var lineFeature_red = new OpenLayers.Feature.Vector(lineString_red, null, style_red);\n')
                player_location.write('    vectorLayer.addFeatures([lineFeature_green, lineFeature_red]);\n')
            player_location.write('\n')
            player_location.write('   map.addLayer(vectorLayer);\n')
            player_location.write('\n')
        player_location.write('   var feature=new OpenLayers.Feature.Vector(\n')
        if str(player[0][4]) == 'PILOT':
            player_location.write('     new OpenLayers.Geometry.Point(position.lon, position.lat), {"angle": %d, opacity: 100});\n' 
                                  % (heading))
        else:
            player_location.write('     new OpenLayers.Geometry.Point(position.lon, position.lat), {"angle": 0, opacity: 100});\n')
        player_location.write('   player.addFeatures([feature]);\n')
        player_location.write('   map.addLayer(player);\n')
        player_location.write('\n')
        player_location.write('   map.setCenter (position, zoom);\n')
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
                          July 2011 Tony (emper0r) P. Diaz  --  emperor.cu@gmail.com <p>"""
                          % (__version__))

    def show_pilot_info(self, callsign):
        self.pilot_window = PilotInfo()
        self.pilot_window.status(callsign)
        self.pilot_window.closed.connect(self.show)
        self.pilot_window.show()

    def show_controller_info(self, callsign):
        self.controller_window = ControllerInfo()
        self.controller_window.status(callsign)
        self.controller_window.closed.connect(self.show)
        self.controller_window.show()

    def show_settings(self):
        self.setting_window = Settings(self)
        self.setting_window.closed.connect(self.show)
        self.setting_window.show()

    def all2map(self):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        label_Pilots = config.getint('Map', 'label_Pilots')
        label_ATCs = config.getint('Map', 'label_ATCs')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT longitude, latitude, callsign, true_heading, clienttype FROM status_ivao;")
        players = cursor.fetchall()
        self.statusBar().showMessage('Populating all players in the Map', 10000)
        qApp.processEvents()
        all_in_map = open('./all_in_map.html', 'w')
        all_in_map.write('<html><body>\n')
        all_in_map.write('  <div id="mapdiv"></div>\n')
        all_in_map.write('  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAjpkAC9ePGem0lIq5XcMiuhR_wWLPFku8Ix9i2SXYRVK3e45q1BQUd_beF8dtzKET_EteAjPdGDwqpQ"></script>\n')
        all_in_map.write('  <script src="./OpenLayers/OpenLayers.js"></script>\n')
        all_in_map.write('  <script>\n')
        all_in_map.write('\n')
        all_in_map.write('    map = new OpenLayers.Map("mapdiv",\n')
        all_in_map.write('             {   projection : new OpenLayers.Projection("EPSG:900913"),\n')
        all_in_map.write('                 maxResolution:156543.0339,\n')
        all_in_map.write('                 maxExtent:new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34)\n')
        all_in_map.write('             });\n')
        all_in_map.write('    ghyb = new OpenLayers.Layer.Google(\n')
        all_in_map.write('         "Google Satellite",\n')
        all_in_map.write('         {type: G_SATELLITE_MAP, sphericalMercator:true, numZoomLevels: 22}\n')
        all_in_map.write('         );\n')
        all_in_map.write('\n')
        all_in_map.write('    map.addLayers([ghyb]);\n')
        all_in_map.write('\n')
        for callsign in range(0, len(players)):
            if str(players[callsign][4]) == 'PILOT':
                if (str(players[callsign][0]) and str(players[callsign][1])) == '':
                    pass
                elif players[callsign][2] is None or players[callsign][3] is None:
                    pass
                else:
                    all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % \
                                     (float(players[callsign][0]), float(players[callsign][1])))
                    all_in_map.write('         .transform(\n')
                    all_in_map.write('            new OpenLayers.Projection("EPSG:4326"),\n')
                    all_in_map.write('            map.getProjectionObject()\n')
                    all_in_map.write('            );\n')
                    all_in_map.write('\n')
                    all_in_map.write('    var player_%s=new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]))
                    all_in_map.write('    {\n')
                    all_in_map.write('      styleMap: new OpenLayers.StyleMap({\n')
                    all_in_map.write('         "default": {\n')
                    all_in_map.write('          externalGraphic: "./images/airplane.gif",\n')
                    all_in_map.write('          graphicWidth: 15,\n')
                    all_in_map.write('          graphicHeight: 15,\n')
                    all_in_map.write('          graphicYOffset: 0,\n')
                    all_in_map.write('          rotation: "${angle}",\n')
                    all_in_map.write('          fillOpacity: 100,\n')
                    if label_Pilots == 2:
                        all_in_map.write('          label: "%s",\n' % str(players[callsign][2]))
                        all_in_map.write('          fontColor: "yellow",\n')
                        all_in_map.write('          fontSize: "10px",\n')
                        all_in_map.write('          fontFamily: "Courier New, monospace",\n')
                        all_in_map.write('          labelAlign: "cm",\n')
                        all_in_map.write('          labelXOffset: 30,\n')
                        all_in_map.write('          labelYOffset: 5\n')
                    all_in_map.write('         }\n')
                    all_in_map.write('      })\n')
                    all_in_map.write('   });\n')
                    all_in_map.write('\n')
                    all_in_map.write('    var feature = new OpenLayers.Feature.Vector(\n')
                    all_in_map.write('      new OpenLayers.Geometry.Point( position.lon, position.lat), {"angle": %d});\n' 
                                     % int(players[callsign][3]))
                    all_in_map.write('    player_%s.addFeatures([feature]);\n' % str(players[callsign][2]).replace('-',''))
                    all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
                    all_in_map.write('\n')
            if str(players[callsign][4]) == 'ATC':
                if players[callsign][0] == '' or players[callsign][1] == '':
                    continue
            if str(players[callsign][2][-4:]) == '_OBS' \
               or str(players[callsign][4][-4:]) == '_DEP' or str(players[callsign][2][-4:]) == '_GND' \
               or str(players[callsign][2][-4:]) == '_TWR' or str(players[callsign][2][-4:]) == '_APP':
                all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % \
                                 (float(players[callsign][0]), float(players[callsign][1])))
                all_in_map.write('         .transform(\n')
                all_in_map.write('            new OpenLayers.Projection("EPSG:4326"),\n')
                all_in_map.write('            map.getProjectionObject()\n')
                all_in_map.write('            );\n')
                all_in_map.write('\n')
                all_in_map.write('    var player_%s = new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('    {\n')
                all_in_map.write('    styleMap: new OpenLayers.StyleMap({\n')
                all_in_map.write('         "default": {\n')
                all_in_map.write('         externalGraphic: "./images/tower.png",\n')
                all_in_map.write('         rotation: "${angle}",\n')
                all_in_map.write('         graphicWidth: 15,\n')
                all_in_map.write('         graphicHeight: 15,\n')
                all_in_map.write('         graphicYOffset: 0,\n')
                if str(players[callsign][2][-4:]) == '_OBS' or str(players[callsign][4][-4:]) == '_DEP' \
                   or str(players[callsign][2][-4:]) == '_GND':
                    all_in_map.write('         fillColor: "white",\n')
                    all_in_map.write('         strokeColor: "white",\n')
                elif str(players[callsign][2][-4:]) == '_TWR':
                    all_in_map.write('         fillColor: "white",\n')
                    all_in_map.write('         strokeColor: "white",\n')
                elif str(players[callsign][2][-4:]) == '_APP':
                    all_in_map.write('         fillColor: "white",\n')
                    all_in_map.write('         strokeColor: "white",\n')
                all_in_map.write('         fillOpacity: "0.2",\n')
                if label_ATCs == 2:
                    all_in_map.write('         label: "%s",\n' % str(players[callsign][2]))
                    all_in_map.write('         fontColor: "white",\n')
                    all_in_map.write('         fontSize: "10px",\n')
                    all_in_map.write('         fontFamily: "Courier New, monospace",\n')
                    all_in_map.write('         labelAlign: "cm",\n')
                    all_in_map.write('         labelXOffset: 30,\n')
                    all_in_map.write('         labelYOffset: 5\n')
                all_in_map.write('         }\n')
                all_in_map.write('       })\n')
                all_in_map.write('    });\n')
                all_in_map.write('\n')
                all_in_map.write('     var ratio = OpenLayers.Geometry.Polygon.createRegularPolygon(\n')
                all_in_map.write('        new OpenLayers.Geometry.Point(position.lon, position.lat),\n')
                if str(players[callsign][2][-4:]) == '_OBS' or str(players[callsign][4][-4:]) == '_DEP' \
                   or str(players[callsign][2][-4:]) == '_GND':
                    all_in_map.write('        20000,\n')
                elif str(players[callsign][2][-4:]) == '_TWR':
                    all_in_map.write('        40000,\n')
                elif str(players[callsign][2][-4:]) == '_APP':
                    all_in_map.write('        60000,\n')
                all_in_map.write('        360\n')
                all_in_map.write('    );\n')
                all_in_map.write('    var controller_ratio = new OpenLayers.Feature.Vector(ratio);\n')
                all_in_map.write('    player_%s.addFeatures([controller_ratio]);\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('\n')
                all_in_map.write('    var feature = new OpenLayers.Feature.Vector(\n')
                all_in_map.write('        new OpenLayers.Geometry.Point( position.lon, position.lat), {"angle": 0, opacity: 100});\n')
                all_in_map.write('    player_%s.addFeatures([feature]);\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('\n')
                all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('\n')
            if str(players[callsign][2][-4:]) == '_CTR':
                cursor.execute("SELECT Latitude, Longitude FROM fir_data_list WHERE ICAO = ?;", (str(players[callsign][2][:4]),))
                position = cursor.fetchall()
                all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n' 
                                 % (float(position[0][0]), float(position[0][1])))
                all_in_map.write('    var player_%s = new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('    {\n')
                all_in_map.write('    styleMap: new OpenLayers.StyleMap({\n')
                all_in_map.write('         "default": {\n')
                all_in_map.write('         externalGraphic: "./images/tower.png",\n')
                all_in_map.write('         rotation: "${angle}",\n')
                all_in_map.write('         fillOpacity: "1.00",\n')
                all_in_map.write('         }\n')
                all_in_map.write('       })\n')
                all_in_map.write('    });\n')
                all_in_map.write('\n')
                all_in_map.write('    var vectorLayer = new OpenLayers.Layer.Vector("Vector Layer");\n')
                all_in_map.write('    var style_controller = {\n')
                all_in_map.write('        strokeColor: "white",\n')
                all_in_map.write('        strokeOpacity: 1.0,\n')
                all_in_map.write('        strokeWidth: 2,\n')
                if label_ATCs == 2:
                    all_in_map.write('        label: "%s",\n' % str(players[callsign][2]))
                    all_in_map.write('        fontColor: "white",\n')
                    all_in_map.write('        fontSize: "12px",\n')
                    all_in_map.write('        fontWeight: "bold",\n')                
                    all_in_map.write('        fontFamily: "Courier New, monospace",\n')
                    all_in_map.write('        labelAlign: "cm",\n')
                    all_in_map.write('        labelXOffset: 30,\n')
                    all_in_map.write('        labelYOffset: 5\n')
                all_in_map.write('    };\n\n')
                try:
                    cursor.execute("SELECT ID_FIRCOASTLINE FROM fir_data_list WHERE ICAO = ?;", (str(players[callsign][2][:-4]),))
                    id_ctr = cursor.fetchone()
                    if id_ctr is None:
                        cursor.execute("SELECT ID_FIRCOASTLINE FROM fir_data_list WHERE ICAO = ?;", (str(players[callsign][2][:4]),))
                        id_ctr = cursor.fetchone()
                except:
                    pass
                cursor.execute("SELECT Longitude, Latitude FROM fir_coastlines_list where ID_FIRCOASTLINE = ?;", (int(id_ctr[0]),))
                points_ctr = cursor.fetchall()
                all_in_map.write('    var points = [];\n')
                for position in range(0, len(points_ctr)):
                    all_in_map.write('    var point_orig = new OpenLayers.Geometry.Point(%f, %f);\n' 
                                     % (points_ctr[position][0], points_ctr[position][1]))
                    if position == len(points_ctr) - 1:
                        continue
                    else:
                        all_in_map.write('    var point_dest = new OpenLayers.Geometry.Point(%f, %f);\n' 
                                         % (points_ctr[position+1][0], points_ctr[position+1][1]))
                    all_in_map.write('    points.push(point_orig);\n')
                    all_in_map.write('    points.push(point_dest);\n')
                all_in_map.write('\n')
                all_in_map.write('    var %s_String = new OpenLayers.Geometry.LineString(points);\n' 
                                 % str(players[callsign][2][:-4]))
                all_in_map.write('    %s_String.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());\n' 
                                 % str(players[callsign][2][:-4]))
                all_in_map.write('\n')
                all_in_map.write('    var DrawFeature = new OpenLayers.Feature.Vector(%s_String, null, style_controller);\n' 
                                 % str(players[callsign][2][:-4]))
                all_in_map.write('    vectorLayer.addFeatures([DrawFeature]);\n')
                all_in_map.write('    map.addLayer(vectorLayer);\n')
                all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
        all_in_map.write('   map.setCenter ((0, 0), 2);\n')
        all_in_map.write('  </script>\n')
        all_in_map.write('</body></html>\n')
        all_in_map.close()
        self.maptab.load(QUrl('./all_in_map.html'))

class AddFriend():
    def add_friend(self, vid2add):
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT vid FROM friends_ivao;")
        vid = cursor.fetchall()
        total_vid = len(vid)
        insert = True
        if total_vid >= 0:
            for i in range(0, total_vid):
                if int(vid2add) == vid[i][0]:
                    msg = 'The friend is already in the list'
                    QMessageBox.information(None, 'Friend of IVAO list', msg)
                    i += 1
                    insert = False
            try:
                if insert is True:
                    cursor.execute("SELECT vid, realname, rating, clienttype from status_ivao WHERE vid=?;", ((int(vid2add),)))
                    data = cursor.fetchall()
                    cursor.execute('INSERT INTO friends_ivao (vid, realname, rating, clienttype) VALUES (?, ?, ?, ?);' \
                                   , (int(str(data[0][0])), str(data[0][1][:-4].encode('latin-1')), int(data[0][2]), str(data[0][3])))
                    connection.commit()
            except:
                pass
        connection.close()

class PilotInfo(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = PilotInfo_UI.Ui_QPilotInfo()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao_status_splash.png'))
        self.callsign = ''
        QObject.connect(self.ui.AddFriend, SIGNAL('clicked()'), self.add_button)

    def status(self, callsign):
        self.callsign = callsign
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT vid, realname, altitude, groundspeed, planned_aircraft, planned_depairport, \
        planned_destairport, planned_altitude, planned_pob, planned_route, rating, transponder, \
        onground, latitude, longitude, planned_altairport, planned_altairport2, planned_tascruise \
        FROM status_ivao WHERE callsign = ? AND clienttype='PILOT' ;", (str(callsign),))
        info = cursor.fetchall()
        try:
            cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(info[0][5]),))
            flagCodeOrig = cursor.fetchone()
            connection.commit()
            flagCodePath_orig = ('./flags/%s.png') % flagCodeOrig
            Pixmap = QPixmap(flagCodePath_orig)
            self.ui.DepartureImage.setPixmap(Pixmap)
            cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?", (str(info[0][5]),))
            city_orig = cursor.fetchone()
            self.ui.DepartureText.setText(str(city_orig[0].encode('latin-1')))
            city_orig_point = city_orig[1], city_orig[2]
        except:
            self.ui.DepartureText.setText('Pending...')
            city_orig_point = None

        try:
            cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(info[0][6]),))
            flagCodeDest = cursor.fetchone()
            connection.commit()
            flagCodePath_dest = ('./flags/%s.png') % flagCodeDest
            Pixmap = QPixmap(flagCodePath_dest)
            self.ui.DestinationImage.setPixmap(Pixmap)
            cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?", (str(info[0][6]),))
            city_dest = cursor.fetchone()
            self.ui.DestinationText.setText(str(city_dest[0].encode('latin-1')))
            city_dest_point = city_dest[1], city_dest[2]
        except:
            self.ui.DestinationText.setText('Pending...')
            city_dest_point = None

        self.ui.vidText.setText(str(info[0][0]))
        try:
            code_airline = callsign[:3]
            airlineCodePath = './airlines/%s.gif' % code_airline
            if os.path.exists(airlineCodePath) is True:
                Pixmap = QPixmap(airlineCodePath)
                airline = QLabel(self)
                self.ui.airline_image.setPixmap(Pixmap)
            else:
                cursor.execute('SELECT Airline FROM airlines_codes WHERE Code = ?', str(callsign[:3]))
                airline_code = cursor.fetchone()
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
        altern_airport_1 = cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(info[0][15]),))
        altern_city_1 = cursor.fetchone()
        altern_airport_2 = cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(info[0][16]),))
        altern_city_2 = cursor.fetchone()
        if altern_city_1 is None:
            self.ui.Altern_Airport_Text.setText(str('-'))
        else:
            self.ui.Altern_Airport_Text.setText(str(altern_city_1[0]))
        if altern_city_2 is None:
            self.ui.Altern_Airport_Text_2.setText(str('-'))
        else:
            self.ui.Altern_Airport_Text_2.setText(str(altern_city_2[0]))
        if str(info[0][4]) != '':
            cursor.execute("SELECT Model, Fabricant, Description FROM icao_aircraft WHERE Model=?;", ((info[0][4].split('/')[1]),))
            data = cursor.fetchall()
            self.ui.AirplaneText.setText('Model: %s Fabricant: %s Description: %s' % (str(data[0][0]), str(data[0][1]), str(data[0][2])))
        else:
            self.ui.AirplaneText.setText('Pending...')
        cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(info[0][1][-4:]),))
        flagCodeHome = cursor.fetchone()
        connection.commit()
        flagCodePath_orig = ('./flags/%s.png') % flagCodeHome
        Pixmap = QPixmap(flagCodePath_orig)
        self.ui.HomeFlag.setPixmap(Pixmap)
        ratingPath = ('./ratings/pilot_level%d.gif') % int(info[0][10])
        Pixmap = QPixmap(ratingPath)
        self.ui.rating_img.setPixmap(Pixmap)
        player_point = info[0][13], info[0][14]
        if city_orig_point is None or city_dest_point is None:
            self.ui.nauticalmiles.setText('Pending...')
            self.ui.progressBarTrack.setValue(0)
        else:
            total_miles = distance.distance(city_orig_point, city_dest_point).miles
            dist_traveled = distance.distance(city_orig_point, player_point).miles
            percent = float((dist_traveled / total_miles) * 100.0)
            self.ui.nauticalmiles.setText('%.1f / %.1f miles - %.1f%%' % (float(dist_traveled), float(total_miles), float(percent)))
            if str(info[0][5]) == str(info[0][6]):
                self.ui.progressBarTrack.setValue(0)
                self.ui.nauticalmiles.setText('Local Flight')
            else:
                self.ui.progressBarTrack.setValue(int(percent))
        status_plane = Main().status_plane(callsign)
        self.ui.FlightStatusDetail.setText(str(status_plane))

    def add_button(self):
        add2friend = AddFriend()
        add2friend.add_friend(str(self.ui.vidText.text()).encode('latin-1'))
        self.statusBar().showMessage('Friend Added', 3000)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

class ControllerInfo(QMainWindow):
    closed = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = ControllerInfo_UI.Ui_QControllerInfo()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QIcon('./images/ivao_status_splash.png'))
        QObject.connect(self.ui.AddFriend, SIGNAL('clicked()'), self.add_button)

    def status(self, callsign):
        self.callsign = callsign
        self.position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                             , "3":"Ground", "4":"Tower", "5":"Approach", "6":"Center", "7":"Departure"}
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        connection = sqlite3.connect('./database/' + config.get('Database', 'db'))
        cursor = connection.cursor()
        cursor.execute("SELECT vid, realname, server, clienttype, frequency \
            , rating, facilitytype, atis_message, time_connected, \
            client_software_name, client_software_version FROM status_ivao \
            WHERE callsign = ? AND clienttype='ATC';", (str(callsign),))
        info = cursor.fetchall()
        self.ui.VidText.setText(str(info[0][0]))
        self.ui.ControllerText.setText(str(info[0][1].encode('latin-1')))
        self.ui.SoftwareText.setText('%s %s' % (str(info[0][9]), str(info[0][10])))
        self.ui.ConnectedText.setText(str(info[0][2]))
        self.ui.ATISInfo.setText(str(info[0][7].encode('latin-1')).replace('^\xa7', '\n'))
        try:
            cursor.execute("SELECT Country FROM icao_codes WHERE icao=?", (str(callsign[:4]),))
            flagCodeOrig = cursor.fetchone()
            connection.commit()
            flagCodePath_orig = ('./flags/%s.png') % flagCodeOrig
            Pixmap = QPixmap(flagCodePath_orig)
            self.ui.Flag.setPixmap(Pixmap)
            cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(callsign[:4]),))
            city_orig = cursor.fetchone()
            self.ui.ControllingText.setText(str(city_orig[0].encode('latin-1')))
        except:
            self.ui.ControllingText.setText('Pending...')
        ratingPath = ('./ratings/atc_level%d.gif') % int(info[0][5])
        Pixmap = QPixmap(ratingPath)
        self.ui.rating_img.setPixmap(Pixmap)
        self.ui.facility_freq_Text.setText(str(self.position_atc[str(info[0][6])]) + ' ' + str(info[0][4]) + ' MHz')
        try:
            start_connected = datetime.datetime(int(str(info[0][8])[:4]), int(str(info[0][8])[4:6]) \
                                                , int(str(info[0][8])[6:8]), int(str(info[0][8])[8:10]) \
                                                , int(str(info[0][8])[10:12]), int(str(info[0][8])[12:14]))
            diff = abs(datetime.datetime.now() - start_connected)
            self.ui.TimeOnLineText.setText('Time on line: ' + str(diff)[:-7])
        except:
            self.ui.TimeOnLineText.setText('Pending...')

    def add_button(self):
        add2friend = AddFriend()
        add2friend.add_friend(str(self.ui.VidText.text()).encode('latin-1'))
        self.statusBar().showMessage('Friend Added', 3000)

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
        self.setWindowIcon(QIcon('./images/ivao_status_splash.png'))
        self.connect(self.ui.SettingAccepButton, SIGNAL('clicked()'), self.options)
        config = ConfigParser.RawConfigParser()
        config.read('Config.cfg')
        self.ui.spinBox.setValue(config.getint('Time_Update', 'time') / 60000)
        use_proxy = config.getint('Settings', 'use_proxy')
        if use_proxy == 2:
            self.ui.Setting_checkBox.setChecked(True)
        else:
            self.ui.Setting_checkBox.setChecked(False)
        host = config.get('Settings', 'host')
        self.ui.lineEdit_host.setText(host)
        port = config.get('Settings', 'port')
        self.ui.lineEdit_port.setText(port)
        auth = config.getint('Settings', 'auth')
        if auth == 2:
            self.ui.Setting_auth.setChecked(True)
        else:
            self.ui.Setting_auth.setChecked(False)
        user = config.get('Settings', 'user')
        self.ui.lineEdit_user.setText(user)
        pswd = config.get('Settings', 'pass')
        self.ui.lineEdit_pass.setText(pswd)
        map_refresh = config.getint('Map', 'auto_refresh')
        label_pilot = config.getint('Map', 'label_Pilots')
        label_atcs = config.getint('Map', 'label_ATCs')
        if map_refresh == 2:
            self.ui.AutoRefreshMap.setChecked(True)
        else:
            self.ui.AutoRefreshMap.setChecked(False)
        if label_pilot == 2:
            self.ui.ShowLabelPilots.setChecked(True)
        else:
            self.ui.ShowLabelPilots.setChecked(False)
        if label_atcs == 2:
            self.ui.ShowLabelControllers.setChecked(True)
        else:
            self.ui.ShowLabelControllers.setChecked(False)

    def options(self):
        minutes = self.ui.spinBox.value()
        time_update = minutes * 60000
        config = ConfigParser.RawConfigParser()
        config.add_section('Settings')
        config.set('Settings', 'use_proxy', self.ui.Setting_checkBox.checkState())
        config.set('Settings', 'host', self.ui.lineEdit_host.text())
        config.set('Settings', 'port', self.ui.lineEdit_port.text())
        config.set('Settings', 'auth', self.ui.Setting_auth.checkState())
        config.set('Settings', 'user', self.ui.lineEdit_user.text())
        config.set('Settings', 'pass', self.ui.lineEdit_pass.text())
        config.add_section('Info')
        config.set('Info', 'data_access', 'whazzup.txt')
        config.set('Info', 'url', url)
        config.add_section('Database')
        config.set('Database', 'db', 'ivao.db')
        config.add_section('Time_Update')
        config.set('Time_Update', 'time', time_update)
        config.add_section('Map')
        if self.ui.AutoRefreshMap.checkState() == 2:
            config.set('Map', 'auto_refresh', '2')
        else:
            config.set('Map', 'auto_refresh', '0')
        if self.ui.ShowLabelPilots.checkState() == 2:
            config.set('Map', 'label_Pilots', '2')
        else:
            config.set('Map', 'label_Pilots', '0')
        if self.ui.ShowLabelControllers.checkState() == 2:
            config.set('Map', 'label_ATCs', '2')
        else:
            config.set('Map', 'label_ATCs', '0')
        with open ('Config.cfg', 'wb') as configfile:
            config.write(configfile)

        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

def main():
    import sys, time
    QApplication.setStyle(QStyleFactory.create("Cleanlooks"))
    QApplication.setPalette(QApplication.style().standardPalette())
    app = QApplication(sys.argv)
    splash_pix = QPixmap('./images/ivao_status_splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    qApp.processEvents()
    time.sleep(4)
    window = Main()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
