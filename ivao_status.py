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

"""Importing Python's native modules"""
import sys
import os
import sqlite3
import datetime
import ConfigParser
import urllib2
import random
import gzip
import StringIO

try:
    """Check if PyQt4 is installed or not, this library is a dependency of all,
    if not installed read the README.rst"""
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtWebKit import *
    from PyQt4.Qt import *
except ImportError:
    print ('\nYou have not installed the packages Qt Modules for Python,\n')
    print ('please run command as root:  aptitude install python-qt4\n')
    print ('with all dependencies.\n\n')
    sys.exit(2)

"""Importing the libraries from modules directory"""
from modules import MainWindow_UI
from modules import Pilots
from modules import SQL_queries
from modules import Controllers
from modules import FOLME
from modules import StatusFlight
from modules import Schedule
from modules import MapView
from modules import BuildDB
import Settings

__version__ = '1.0.8'

class Main(QMainWindow):
    """Preparing the MainWindow Class, to paint all design of the app"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        image_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'ivao_status_splash.png')
        self.setWindowIcon(QIcon(image_icon))
        self.ui.PILOT_FullList.setColumnWidth(0, 90)
        self.ui.PILOT_FullList.setColumnWidth(1, 65)
        self.ui.PILOT_FullList.setColumnWidth(2, 60)
        self.ui.PILOT_FullList.setColumnWidth(3, 170)
        self.ui.PILOT_FullList.setColumnWidth(4, 160)
        self.ui.PILOT_FullList.setColumnWidth(5, 105)
        self.ui.PILOT_FullList.setColumnWidth(6, 70)
        self.ui.PILOT_FullList.setColumnWidth(7, 80)
        self.ui.PILOT_FullList.setColumnWidth(8, 92)
        self.ui.PilottableWidget.setColumnWidth(0, 90)
        self.ui.PilottableWidget.setColumnWidth(1, 65)
        self.ui.PilottableWidget.setColumnWidth(2, 60)
        self.ui.PilottableWidget.setColumnWidth(3, 180)
        self.ui.PilottableWidget.setColumnWidth(4, 160)
        self.ui.PilottableWidget.setColumnWidth(5, 105)
        self.ui.PilottableWidget.setColumnWidth(6, 70)
        self.ui.PilottableWidget.setColumnWidth(7, 80)
        self.ui.PilottableWidget.setColumnWidth(8, 85)
        self.ui.PilottableWidget.setColumnWidth(9, 55)
        self.ui.ATC_FullList.setColumnWidth(1, 70)
        self.ui.ATC_FullList.setColumnWidth(2, 37)
        self.ui.ATC_FullList.setColumnWidth(3, 150)
        self.ui.ATC_FullList.setColumnWidth(4, 70)
        self.ui.ATC_FullList.setColumnWidth(5, 138)
        self.ui.ATC_FullList.setColumnWidth(6, 170)
        self.ui.ATC_FullList.setColumnWidth(8, 40)
        self.ui.ATCtableWidget.setColumnWidth(1, 70)
        self.ui.ATCtableWidget.setColumnWidth(2, 60)
        self.ui.ATCtableWidget.setColumnWidth(3, 240)
        self.ui.ATCtableWidget.setColumnWidth(4, 150)
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
        self.ui.Statistics.setColumnWidth(0, 30)
        self.ui.Statistics.setColumnWidth(1, 500)
        self.ui.Statistics.setColumnWidth(2, 100)
        self.ui.Statistics.setColumnWidth(3, 100)
        self.ui.SchedulingATC.setColumnWidth(0, 35)
        self.ui.SchedulingATC.setColumnWidth(1, 100)
        self.ui.SchedulingATC.setColumnWidth(2, 150)
        self.ui.SchedulingATC.setColumnWidth(3, 70)
        self.ui.SchedulingATC.setColumnWidth(4, 180)
        self.ui.SchedulingATC.setColumnWidth(5, 180)
        self.ui.SchedulingATC.setColumnWidth(6, 60)
        self.ui.SchedulingATC.setColumnWidth(7, 60)
        self.ui.SchedulingATC.setColumnWidth(8, 50)
        self.ui.SchedulingATC.setColumnWidth(9, 115)
        self.ui.SchedulingFlights.setColumnWidth(0, 90)
        self.ui.SchedulingFlights.setColumnWidth(1, 60)
        self.ui.SchedulingFlights.setColumnWidth(2, 175)
        self.ui.SchedulingFlights.setColumnWidth(3, 60)
        self.ui.SchedulingFlights.setColumnWidth(4, 30)
        self.ui.SchedulingFlights.setColumnWidth(5, 65)
        self.ui.SchedulingFlights.setColumnWidth(6, 180)
        self.ui.SchedulingFlights.setColumnWidth(7, 30)
        self.ui.SchedulingFlights.setColumnWidth(8, 70)
        self.ui.SchedulingFlights.setColumnWidth(9, 180)
        self.ui.SchedulingFlights.setColumnWidth(10, 55)
        self.ui.SchedulingFlights.setColumnWidth(11, 95)
        self.ui.SchedulingFlights.setColumnWidth(12, 150)
        self.ui.SchedulingFlights.setColumnWidth(13, 40)
        self.ui.SchedulingFlights.setColumnWidth(14, 50)
        self.ui.SchedulingFlights.setColumnWidth(15, 150)
        self.ui.network_table.setColumnWidth(0, 60)
        self.ui.network_table.setColumnWidth(1, 120)
        self.ui.network_table.setColumnWidth(2, 250)
        self.ui.network_table.setColumnWidth(3, 210)
        self.ui.network_table.setColumnWidth(4, 65)
        self.ui.network_table.setColumnWidth(5, 70)
        self.ui.network_table.setColumnWidth(6, 70)
        self.ui.network_table.setColumnWidth(7, 60)
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
        image_departure = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'departures.png')
        Pixmap = QPixmap(image_departure)
        self.ui.departures_icon.setPixmap(Pixmap)
        self.ui.departures_icon.show()
        image_arrivals = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'arrivals.png')
        Pixmap = QPixmap(image_arrivals)
        self.ui.arrivals_icon.setPixmap(Pixmap)
        self.ui.arrivals_icon.show()
        QTimer.singleShot(1000, self.initial_load)
        self.progress = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress)
        self.progress.hide()
        self.progress.setValue(0)
        self._maptab = None

        ratings = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'ratings.dat'), 'r').readlines()
        self.rating_pilot = {}
        self.rating_atc = {}
        for item in range(len(ratings)):
            self.rating_atc[ratings[item].split(':')[0]] = ratings[item].split(':')[2]
            self.rating_pilot[ratings[item].split(':')[0]] = ratings[item].split(':')[4].strip('\r\n')
        self.position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery"
                        , "3":"Ground", "4":"Tower", "5":"Approach", "6":"Center", "7":"Departure"}

        """If user delete Config.ini by error, when app start write it again the file"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        if os.path.exists(config_file):
            config.read(config_file)
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
            config.set('Info', 'data_access', 'http://www.ivao.aero/whazzup/status.txt')
            config.set('Info', 'scheduling_atc', 'http://www.ivao.aero/atcss/list.asp')
            config.set('Info', 'scheduling_flights', 'http://www.ivao.aero/flightss/list.asp')
            config.add_section('Database')
            config.set('Database', 'db', 'ivao.db')
            config.add_section('Time_Update')
            config.set('Time_Update', 'time', '300000')
            config.add_section('Map')
            config.set('Map', 'auto_refresh', '0')
            config.set('Map', 'label_Pilots', '0')
            config.set('Map', 'label_ATCs', '0')
            with open(config_file, 'wb') as configfile:
                config.write(configfile)
        self.pilot_list = []
        self.atc_list = []
        self.vehicles = []
        self.SchedATC_URL = None
        self.SchedFlights_URL = None
        self.ui.tabWidget.currentChanged.connect(self.ivao_friend)

    @property
    def maptab(self):
        if self._maptab is None and self.ui.tabWidget.currentIndex() != 8:
            self._maptab = QWebView()
            self.ui.tabWidget.insertTab(8, self.maptab, 'Map')
        else:
            self.ui.tabWidget.setCurrentIndex(8)
        return self._maptab

    def initial_load(self):
        self.statusBar().showMessage('Populating Database', 2000)
        qApp.processEvents()
        Q_db = SQL_queries.sql_query('Get_Flags')
        db_t1 = Q_db.fetchall()
        Q_db = SQL_queries.sql_query('Get_ICAO_codes')
        db_t2 = Q_db.fetchall()
        startrow_dbt1 = startrow_dbt2 = 0

        for line in db_t1:
            if line[0] is None:
                self.ui.dbTableWidget_1.removeRow(self.ui.dbTableWidget_1.rowCount())
            else:
                pass
            country = "%s" % line[0]
            self.ui.country_list.addItem(country)
            self.ui.dbTableWidget_1.insertRow(self.ui.dbTableWidget_1.rowCount())
            image_flag = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
            flagCodePath = (image_flag + '/%s.png') % line
            if os.path.exists(flagCodePath) is True:
                Pixmap = QPixmap(flagCodePath)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.dbTableWidget_1.setCellWidget(startrow_dbt1, 0, flag_country)
            else:
                pass
            country = QTableWidgetItem(str(line[0]).encode('latin-1'), 0)
            self.ui.dbTableWidget_1.setItem(startrow_dbt1, 1, country)
            startrow_dbt1 += 1

        for line in db_t2:
            if line[0] is None:
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

        qApp.processEvents()
        self.statusBar().showMessage('Loading friends list', 2000)
        qApp.processEvents()
        self.ivao_friend()
        self.network()
        self.country_view()
        self.statusBar().showMessage('Loading Schedule', 4000)
        qApp.processEvents()
        self.show_TabSched()
        qApp.restoreOverrideCursor()

    def connect(self):
        """Conecting to IVAO with only link explain in the Logistic mail rules,
        this part contain some proxy settings because at least in my country is very used"""
        self.statusBar().showMessage('Trying connecting to IVAO', 3000)
        qApp.processEvents()
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
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
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port), str(user), str(pswd)))
            if use_proxy == 2 and auth == 0:
                proxy_support = urllib2.ProxyHandler({"http" : "http://" + host + ':' + port})
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port)))
            if use_proxy == 0 and auth == 0:
                pass

            """Doing Load balance to IVAO as Logistics required"""
            StatusURL = urllib2.urlopen(config.get('Info', 'data_access'))
            shuffle = random.choice([link for link in StatusURL.readlines() if 'gzurl0' in link]).split('=')[1].strip('\r\n')
            zfilename = urllib2.urlopen(shuffle)
            content = zfilename.read()
            logged_users = gzip.GzipFile(fileobj=StringIO.StringIO(content))
            qApp.processEvents()

            self.statusBar().showMessage('Downloading info from IVAO', 2000)
            qApp.processEvents()
            pilot = []
            atc = []
            vehicles = []

            for player in logged_users.readlines():
                if "PILOT" in player:
                    pilot.append(player)
                if "ATC" in player:
                    atc.append(player)
                if "FOLME" in player:
                    vehicles.append(player)
            SQL_queries.update_db(pilot, atc, vehicles)
            self.network()
            self.ivao_friend()
            self.country_view()
            self.show_tables()

        except IOError:
            self.statusBar().showMessage('Error! when trying to download info from IVAO. Check your connection to Internet.')

    def show_tables(self):
        """Here show all data into PILOT and CONTROLLER full list"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
        ImageAirlines = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'airlines')
        ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ratings')
        self.statusBar().showMessage('Populating Controllers and Pilots', 3000)
        self.progress.show()
        pilots_ivao = atcs_ivao = obs_ivao = 0
        Q_db = SQL_queries.sql_query('Get_Pilots')
        pilots = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_Controllers')
        atc = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_FollowMeCarService')
        followme = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_Observers')
        obs = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_POB')
        pob = Q_db.fetchone()
        self.ui.IVAOStatustableWidget.setCurrentCell(-1, -1)
        pilots_ivao = QTableWidgetItem(str(pilots[0]))
        atcs_ivao = QTableWidgetItem(str((int(atc[0]) - int(obs[0]))))
        vehicles = QTableWidgetItem(str(int(followme[0])))
        obs_ivao = QTableWidgetItem(str(int(obs[0])))
        total_ivao = QTableWidgetItem(str(atc[0] + pilots[0] + followme[0]))
        if pob[0] is None:
            pob_ivao = QTableWidgetItem(str(0))
        else:
            pob_ivao = QTableWidgetItem(str(int(pob[0])))

        time_received = datetime.datetime.utcnow()
        time_board = QTableWidgetItem(str(time_received).split('.')[0] + ' - Zulu Time (UTC)')

        self.ui.IVAOStatustableWidget.setItem(0, 0, pilots_ivao)
        self.ui.IVAOStatustableWidget.setItem(1, 0, atcs_ivao)
        self.ui.IVAOStatustableWidget.setItem(2, 0, vehicles)
        self.ui.IVAOStatustableWidget.setItem(3, 0, obs_ivao)
        self.ui.IVAOStatustableWidget.setItem(4, 0, total_ivao)
        self.ui.IVAOStatustableWidget.setItem(6, 0, pob_ivao)
        self.ui.IVAOStatustableWidget.setItem(7, 0, time_board)
        qApp.processEvents()
        Q_db = SQL_queries.sql_query('Get_Controller_List')
        qApp.processEvents()
        rows_atcs = Q_db.fetchall()
        startrow = 0

        while self.ui.ATC_FullList.rowCount () > 0:
            self.ui.ATC_FullList.removeRow(0)

        for row_atc in rows_atcs:
            if row_atc[1] is None:
                continue
            else:
                self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
                col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                if str(row_atc[0][:4]) == 'IVAO':
                    self.ui.ATC_FullList.setColumnWidth(2, 60)
                    col_callsign = QTableWidgetItem(str(row_atc[0]), 0)
                    self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                    ImageIVAO = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images') + '/ivao_member.png')
                    Pixmap = QPixmap(ImageIVAO)
                    flag_country = QLabel()
                    flag_country.setPixmap(Pixmap)
                    self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                    col_country = QTableWidgetItem('IVAO Member', 0)
                    self.ui.ATC_FullList.setItem(startrow, 3, col_country)

                elif str(row_atc[0][2:3]) == '-' or str(row_atc[0][2:3]) == '_':
                    try:
                        Q_db = SQL_queries.sql_query('Get_Country_by_Id', (str(row_atc[0][:2]),))
                        div_ivao = Q_db.fetchone()
                        if div_ivao is None:
                            Q_db = SQL_queries.sql_query('Get_Country_from_Prefix', (str(row_atc[0][:2]),))
                            div_ivao = Q_db.fetchone()
                            flagCodePath = (ImageFlags + '/%s.png') % str(div_ivao[0])
                    except:
                        pass
                    if row_atc is None or div_ivao is None:
                        self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                    else:
                        flagCodePath = (ImageFlags + '/%s.png') % str(div_ivao[0])
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
                    Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(code_icao),))
                    flagCode = Q_db.fetchone()
                    if flagCode is None:
                        Q_db = SQL_queries.sql_query('Get_Country_from_FIR', (str(code_icao),))
                        flagCode = Q_db.fetchone()
                    flagCodePath = (ImageFlags + '/%s.png') % flagCode
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.ATC_FullList.setCellWidget(startrow, 2, flag_country)
                        col_country = QTableWidgetItem(str(flagCode[0]), 0)
                        self.ui.ATC_FullList.setItem(startrow, 3, col_country)
                        self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                    if flagCode is None:
                        col_country = QTableWidgetItem(str(flagCode).encode('latin-1'), 0)
                        self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
                        error_flag = QTableWidgetItem(str('None'), 0)
                        self.ui.ATC_FullList.setItem(startrow, 2, error_flag)
                        error_country = QTableWidgetItem(str('Error Callsign for IVAO'), 0)
                        error_country.setForeground(QBrush(QColor('red')))
                        self.ui.ATC_FullList.setItem(startrow, 3, error_country)
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
                ratingImagePath = ImageRatings + '/atc_level%d.gif' % int(code_atc_rating)
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
                    start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6])
                                                        , int(str(row_atc[5])[6:8]), int(str(row_atc[5])[8:10])
                                                        , int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
                    diff = datetime.datetime.utcnow() - start_connected
                    col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                    self.ui.ATC_FullList.setItem(startrow, 8, col_time)
                except:
                    pass
                self.progress.setValue(int(float(startrow) / float(len(rows_atcs)) * 100.0))
                startrow += 1
                qApp.processEvents()

        Q_db = SQL_queries.sql_query('Get_FMC_List')
        vehicles = Q_db.fetchall()

        startrow = 0
        while self.ui.PILOT_FullList.rowCount () > 0:
            self.ui.PILOT_FullList.removeRow(0)

        for followservice in vehicles:
            self.ui.PILOT_FullList.setCurrentCell(0, 0)
            self.ui.PILOT_FullList.insertRow(self.ui.PILOT_FullList.rowCount())
            followmeCodePath = (ImageAirlines + '/ZZZZ.png')
            Pixmap = QPixmap(followmeCodePath)
            FMC_img = QLabel(self)
            FMC_img.setPixmap(Pixmap)
            self.ui.PILOT_FullList.setCellWidget(startrow, 0, FMC_img)
            col_callsign = QTableWidgetItem(str(followservice[0]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 1, col_callsign)
            col_aircraft = QTableWidgetItem(str('FOLME'), 0)
            self.ui.PILOT_FullList.setItem(startrow, 2, col_aircraft)
            col_realname = QTableWidgetItem(str(followservice[2][:-5].encode('latin-1')), 0)
            self.ui.PILOT_FullList.setItem(startrow, 3, col_realname)
            col_rating = QTableWidgetItem(str(self.rating_pilot[followservice[1]]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 4, col_rating)
            code_pilot_rating = followservice[1]
            ratingImagePath = ImageRatings + '/pilot_level%d.gif' % int(code_pilot_rating)
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
            col_departure = QTableWidgetItem(str('-'), 0)
            self.ui.PILOT_FullList.setItem(startrow, 6, col_departure)
            col_destination = QTableWidgetItem(str('-'), 0)
            self.ui.PILOT_FullList.setItem(startrow, 7, col_destination)
            col_status = QTableWidgetItem(str("Follow Car Service"), 0)
            self.ui.PILOT_FullList.setItem(startrow, 8, col_status)
            start_connected = datetime.datetime(int(str(followservice[3])[:4]), int(str(followservice[3])[4:6]), int(str(followservice[3])[6:8]) \
                                , int(str(followservice[3])[8:10]), int(str(followservice[3])[10:12]), int(str(followservice[3])[12:14]))
            diff = datetime.datetime.utcnow() - start_connected
            col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.PILOT_FullList.setItem(startrow, 9, col_time)
            self.progress.setValue(int(float(startrow) / float(len(vehicles)) * 100.0))
            startrow += 1
            qApp.processEvents()

        Q_db = SQL_queries.sql_query('Get_Pilot_Lists')
        rows_pilots = Q_db.fetchall()

        for row_pilot in rows_pilots:
            self.ui.PILOT_FullList.insertRow(self.ui.PILOT_FullList.rowCount())
            code_airline = row_pilot[0][:3]
            airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
            try:
                if os.path.exists(airlineCodePath) is True:
                    Pixmap = QPixmap(airlineCodePath)
                    airline = QLabel(self)
                    airline.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setCellWidget(startrow, 0, airline)
                else:
                    Q_db = SQL_queries.sql_query('Get_Airline', (str(row_pilot[0][:3]),))
                    airline_code = Q_db.fetchone()
                    if airline_code is None:
                        col_airline = QTableWidgetItem(str('Unknown Operator'))
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
            ratingImagePath = ImageRatings + '/pilot_level%d.gif' % int(code_pilot_rating)
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
            status_plane = StatusFlight.status_flight(row_pilot[0])
            col_status = QTableWidgetItem(str(status_plane), 0)
            col_status.setForeground(QBrush(QColor(StatusFlight.get_color(status_plane))))
            self.ui.PILOT_FullList.setItem(startrow, 8, col_status)
            start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]), int(str(row_pilot[6])[6:8]) \
                                , int(str(row_pilot[6])[8:10]), int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
            diff = datetime.datetime.utcnow() - start_connected
            col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
            self.ui.PILOT_FullList.setItem(startrow, 9, col_time)
            self.progress.setValue(int(float(startrow) / float(len(rows_pilots)) * 100.0))
            startrow += 1
            qApp.processEvents()

        self.progress.hide()
        self.statusBar().showMessage('Done', 2000)
        qApp.processEvents()
        if config.getint('Map', 'auto_refresh') == 2:
            self.all2map()
        else:
            pass

    def country_view(self):
        """This function show all users connected as PILOT and CONTOLLER of Country selected,
           and all flight inbound/outbound in same country, This is my favorite part because
           is very similar like any Airport's Flights of MainBoard"""
        country_selected = self.ui.country_list.currentText()
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
        ImageAirlines = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'airlines')
        ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ratings')
        flagCodePath = (ImageFlags + '/%s.png') % country_selected
        Pixmap = QPixmap(flagCodePath)
        self.ui.flagIcon.setPixmap(Pixmap)
        Q_db = SQL_queries.sql_query('Get_ICAO_from_Country', (str(country_selected),))
        icao_country = Q_db.fetchall()
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
            Q_db = SQL_queries.sql_query('Get_Controller', (('%'+str(codes[0])+'%'),))
            rows_atcs = Q_db.fetchall()

            Q_db = SQL_queries.sql_query('Get_Pilot', (('%'+str(codes[0])),))
            rows_pilots = Q_db.fetchall()

            Q_db = SQL_queries.sql_query('Get_Outbound_Traffic', ((str(codes[0])),))
            OutboundTrafficAirport = Q_db.fetchall()

            Q_db = SQL_queries.sql_query('Get_Inbound_Traffic', ((str(codes[0])),))
            InboundTrafficAirport = Q_db.fetchall()

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
                ratingImagePath = ImageRatings + '/atc_level%d.gif' % int(code_atc_rating)
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
                    start_connected = datetime.datetime(int(str(row_atc[5])[:4]), int(str(row_atc[5])[4:6])
                                                        , int(str(row_atc[5])[6:8]), int(str(row_atc[5])[8:10])
                                                        , int(str(row_atc[5])[10:12]), int(str(row_atc[5])[12:14]))
                except:
                    pass
                diff = datetime.datetime.utcnow() - start_connected
                col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.ATCtableWidget.setItem(startrow_atc, 6, col_time)
                startrow_atc += 1
            qApp.processEvents()

            for row_pilot in rows_pilots:
                self.ui.PilottableWidget.insertRow(self.ui.PilottableWidget.rowCount())

                code_airline = row_pilot[0][:3]
                airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QPixmap(airlineCodePath)
                        airline = QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.PilottableWidget.setCellWidget(startrow_pilot, 0, airline)
                    else:
                        Q_db = SQL_queries.sql_query('Get_Airline', (str(row_pilot[0][:3]),))
                        airline_code = Q_db.fetchone()
                        if airline_code is None:
                            col_airline = QTableWidgetItem(str('Unknown Operator'))
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
                ratingImagePath = ImageRatings + '/pilot_level%d.gif' % int(code_pilot_rating)
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
                status_plane = StatusFlight.status_flight(row_pilot[0])
                col_status = QTableWidgetItem(str(status_plane), 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 8, col_status)
                col_status.setForeground(QBrush(QColor(StatusFlight.get_color(status_plane))))
                start_connected = datetime.datetime(int(str(row_pilot[6])[:4]), int(str(row_pilot[6])[4:6]) \
                                                    , int(str(row_pilot[6])[6:8]), int(str(row_pilot[6])[8:10]) \
                                                    , int(str(row_pilot[6])[10:12]), int(str(row_pilot[6])[12:14]))
                diff = datetime.datetime.utcnow() - start_connected
                col_time = QTableWidgetItem(str(diff).split('.')[0], 0)
                self.ui.PilottableWidget.setItem(startrow_pilot, 9, col_time)
                startrow_pilot += 1
            qApp.processEvents()

            for inbound in InboundTrafficAirport:
                self.ui.InboundTableWidget.insertRow(self.ui.InboundTableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(inbound[0]), 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 0, col_callsign)
                code_airline = inbound[0][:3]
                airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
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
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(inbound[1]),))
                flagCode = Q_db.fetchone()
                flagCodePath_orig = (ImageFlags + '/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_orig)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.InboundTableWidget.setCellWidget(startrow_in, 1, flag_country)
                Q_db = SQL_queries.sql_query('Get_City', (str(inbound[1]),))
                city = Q_db.fetchone()
                col_city = ''
                if city is None:
                    col_city = 'Pending...'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 2, col_country)
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(inbound[2]),))
                flagCode = Q_db.fetchone()
                flagCodePath_dest = (ImageFlags + '/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_dest)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.InboundTableWidget.setCellWidget(startrow_in, 3, flag_country)
                Q_db = SQL_queries.sql_query('Get_City', (str(inbound[2]),))
                city = Q_db.fetchone()
                col_city = ''
                if city is None:
                    col_city = 'Pending...'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 4, col_country)
                if  flagCodePath_orig == flagCodePath_dest:
                    status_flight = 'Domestic'
                else:
                    status_flight = 'International'
                col_flight = QTableWidgetItem(status_flight, 0)
                self.ui.InboundTableWidget.setItem(startrow_in, 5, col_flight)
                startrow_in += 1
            qApp.processEvents()

            for outbound in OutboundTrafficAirport:
                self.ui.OutboundTableWidget.insertRow(self.ui.OutboundTableWidget.rowCount())
                col_callsign = QTableWidgetItem(str(outbound[0]), 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 0, col_callsign)
                code_airline = outbound[0][:3]
                airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
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
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(outbound[1]),))
                flagCode = Q_db.fetchone()
                flagCodePath_orig = (ImageFlags + '/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_orig)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.OutboundTableWidget.setCellWidget(startrow_out, 1, flag_country)
                Q_db = SQL_queries.sql_query('Get_City', (str(outbound[1]),))
                city = Q_db.fetchone()
                col_city = ''
                if city is None:
                    col_city = 'Pending...'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 2, col_country)
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(outbound[2]),))
                flagCode = Q_db.fetchone()
                flagCodePath_dest = (ImageFlags + '/%s.png') % flagCode
                Pixmap = QPixmap(flagCodePath_dest)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.OutboundTableWidget.setCellWidget(startrow_out, 3, flag_country)
                Q_db = SQL_queries.sql_query('Get_City', (str(outbound[2]),))
                city = Q_db.fetchone()
                col_city = ''
                if city is None:
                    col_city = 'Pending...'
                else:
                    col_city = str(city[0].encode('latin-1'))
                col_country = QTableWidgetItem(col_city, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 4, col_country)
                if  flagCodePath_orig == flagCodePath_dest:
                    status_flight = 'Domestic'
                else:
                    status_flight = 'International'
                col_flight = QTableWidgetItem(status_flight, 0)
                self.ui.OutboundTableWidget.setItem(startrow_out, 5, col_flight)
                startrow_out += 1
            qApp.processEvents()
        self.ui.PilottableWidget.setCurrentCell(-1, -1)
        self.ui.ATCtableWidget.setCurrentCell(-1, -1)

    def search_button(self):
        """Here can search by VID, Callsign or Player Name in MainTab"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        arg = self.ui.SearchEdit.text()
        item = self.ui.SearchcomboBox.currentIndex()

        if item == 0:
            Q_db = SQL_queries.sql_query('Search_vid', ('%'+str(arg)+'%',))
        elif item == 1:
            Q_db = SQL_queries.sql_query('Search_callsign', ('%'+str(arg)+'%',))
        elif item == 2:
            Q_db = SQL_queries.sql_query('Search_realname', ('%'+str(arg)+'%',))
        search = Q_db.fetchall()

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
            ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ratings')
            if row[4] == 'PILOT':
                col_realname = QTableWidgetItem(str(row[2][:-4].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'pilot_level'
            else:
                col_realname = QTableWidgetItem(str(row[2].encode('latin-1')), 0)
                self.ui.SearchtableWidget.setItem(startrow, 2, col_realname)
                player = 'atc_level'
            try:
                ratingImagePath = ImageRatings + '/%s%d.gif' % (player, int(row[3]))
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
        """This section is for right-click mouse, and get in what table was clicked to do some action"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
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
                cursor.execute('SELECT clienttype FROM recent WHERE callsign=?;', ((str(current_callsign.text())),))
                clienttype = cursor.fetchone()
                if sender == self.showInfo_Action:
                    if str(clienttype[0]) == 'PILOT':
                        self.show_pilot_info(current_callsign.text())
                    if str(clienttype[0]) == 'FOLME':
                        self.show_followme_info(current_callsign.text())
                    if str(clienttype[0]) == 'ATC':
                        self.show_controller_info(current_callsign.text())
                if sender == self.showMap_Action:
                    cursor.execute('SELECT planned_depairport, planned_destairport FROM recent WHERE callsign=?;'
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
                cursor.execute('SELECT clienttype FROM recent WHERE callsign=?;', ((str(current_callsign.text())),))
                clienttype = cursor.fetchone()
                current_row = self.ui.PILOT_FullList.currentRow()
                current_callsign = self.ui.PILOT_FullList.item(current_row, 1)
                if sender == self.showInfo_Action:
                    if str(clienttype[0]) == 'FOLME':
                        self.show_followme_info(current_callsign.text())
                    if str(clienttype[0]) == 'PILOT':
                        self.show_pilot_info(current_callsign.text())
                if sender == self.showMap_Action:
                    if str(clienttype[0]) == 'PILOT':
                        icao_orig = self.ui.PILOT_FullList.item(current_row, 6)
                        icao_dest = self.ui.PILOT_FullList.item(current_row, 7)
                        self.view_map(current_callsign.text(), icao_orig.text(), icao_dest.text())
                    if str(clienttype[0]) == 'FOLME':
                        pass
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
            cursor.execute('SELECT clienttype, callsign FROM recent WHERE vid=?;', ((int(current_vid.text())),))
            friend_data = cursor.fetchall()
            if current_row == -1:
                pass
            else:
                try:
                    if sender == self.showInfo_Action:
                        if str(friend_data[0][0]) == 'PILOT':
                            self.show_pilot_info(str(friend_data[0][1]))
                        if str(friend_data[0][0]) == 'FOLME':
                            self.show_followme_info(str(friend_data[0][1]))
                        if str(friend_data[0][0]) == 'ATC':
                            self.show_controller_info(str(friend_data[0][1]))
                    if sender == self.showMap_Action:
                        cursor.execute('SELECT planned_depairport, planned_destairport FROM recent WHERE callsign=?;'
                                       , ((str(friend_data[0][1])),))
                        icao_depdest = cursor.fetchall()
                        self.view_map(str(friend_data[0][1]), icao_depdest[0][0], icao_depdest[0][1])
                    if sender == self.showDelete_Action:
                        cursor.execute('DELETE FROM friends WHERE vid=?;', (int(current_vid.text()),))
                        self.statusBar().showMessage('Friend Deleted', 2000)
                        connection.commit()
                        connection.close()
                        self.ivao_friend()
                except:
                    if friend_data == []:
                        msg = "The user %d is off-line, can't see any info" % (int(current_vid.text()))
                        QMessageBox.information(None, 'Friends List', msg)

    def ivao_friend(self):
        """Here can show the friend added to roster, this roster is reload after get consecutive data
           to see if player's friend is online or not"""
        self.ui.PILOT_FullList.setCurrentCell(-1, -1)
        self.ui.ATC_FullList.setCurrentCell(-1, -1)
        self.ui.PilottableWidget.setCurrentCell(-1, -1)
        self.ui.ATCtableWidget.setCurrentCell(-1, -1)
        self.ui.SearchtableWidget.setCurrentCell(-1, -1)
        self.ui.FriendstableWidget.setCurrentCell(-1, -1)
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('SELECT vid, realname, rating, clienttype FROM friends;')
        roster = cursor.fetchall()
        ImageRatings = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ratings')
        self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
        while self.ui.FriendstableWidget.rowCount () > 0:
            self.ui.FriendstableWidget.removeRow(0)

        startrow = 0
        roster_row = 0
        for row in roster:
            self.ui.FriendstableWidget.insertRow(self.ui.FriendstableWidget.rowCount())
            col_vid = QTableWidgetItem(str(row[0]), 0)
            self.ui.FriendstableWidget.setItem(startrow, 0, col_vid)
            cursor.execute('SELECT vid FROM recent where vid=?;', (int(row[0]),))
            check = cursor.fetchone()
            try:
                if check[0] == row[0]:
                    ImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'airplane_online.png')
                    Pixmap = QPixmap(ImagePath)
                    online = QLabel(self)
                    online.setPixmap(Pixmap)
                    self.ui.FriendstableWidget.setCellWidget(startrow, 3, online)
                    roster_row += 1
            except:
                ImagePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'airplane_offline.png')
                Pixmap = QPixmap(ImagePath)
                offline = QLabel(self)
                offline.setPixmap(Pixmap)
                self.ui.FriendstableWidget.setCellWidget(startrow, 3, offline)
                roster_row += 1
            if row[3] == 'ATC':
                col_realname = QTableWidgetItem(str(row[1].encode('latin-1')), 0)
            else:
                col_realname = QTableWidgetItem(str(row[1].encode('latin-1')[:-4]), 0)
            self.ui.FriendstableWidget.setItem(startrow, 1, col_realname)
            if str(row[2]) != '-':
                if str(row[3]) == 'ATC':
                    ratingImagePath = ImageRatings + '/atc_level%d.gif' % int(row[2])
                else:
                    ratingImagePath = ImageRatings + '/pilot_level%d.gif' % int(row[2])
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
        """This functions is for get the METAR balance as Logistics mail required"""
        self.statusBar().showMessage('Downloading METAR', 2000)
        qApp.processEvents()
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        icao_airport = self.ui.METAREdit.text()

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
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port), str(user), str(pswd)))
            if use_proxy == 2 and auth == 0:
                proxy_support = urllib2.ProxyHandler({"http" : "http://" + host + ':' + port})
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                QNetworkProxy.setApplicationProxy(QNetworkProxy(QNetworkProxy.HttpProxy, str(host), int(port)))
            if use_proxy == 0 and auth == 0:
                pass
            StatusURL = urllib2.urlopen(config.get('Info', 'data_access'))
            shuffle = random.choice([link for link in StatusURL.readlines() if 'metar0' in link]).split('=')[1].strip('\r\n')
            METAR = urllib2.urlopen(shuffle + '?id=%s' % icao_airport)

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
        """This function is for see the single player in GoogleMaps, if  is ATC, see with more or less zoom depends
           from ATC level and the PILOT, I implemented this before show up webeye, so i made the middle stuff,
           now with webeye, I want use it here, to make strong those 2 tools"""
        self.statusBar().showMessage('Showing player in Map', 4000)
        qApp.processEvents()
        Q_db = SQL_queries.sql_query('Get_Location_from_ICAO', (str(icao_orig),))
        icao_orig = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_Location_from_ICAO', (str(icao_dest),))
        icao_dest = Q_db.fetchone()
        Q_db = SQL_queries.sql_query('Get_Player_Location', (str(vid),))
        player = Q_db.fetchall()
        MapView.GMapsLayer(player, icao_orig, icao_dest)
        mapfileplayer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
        self.maptab.load(QUrl(mapfileplayer_path + '/player_location.html'))

    def metarHelp(self):
        msg = 'Must be entered 4-character alphanumeric code designated for each airport around the world'
        QMessageBox.information(None, 'METAR Help', msg)

    def about(self):
        QMessageBox.about(self, "About IVAO :: Status",
                          """<b>IVAO::Status</b>  version %s<p>License: GPL version 3+<p>
                          This Aplication can be used to see IVAO operational network.<p>
                          July 2011 Tony (emper0r) P. Diaz  --  emperor.cu@gmail.com<p>
                          IVAO User: 304605"""
                          % __version__)

    def show_pilot_info(self, callsign):
        """Here call the Pilot Class"""
        self.pilot_window = Pilots.PilotInfo()
        self.pilot_window.status(callsign)
        self.pilot_window.closed.connect(self.show)
        self.pilot_window.show()

    def show_controller_info(self, callsign):
        """Here call the Controller Class"""
        self.controller_window = Controllers.ControllerInfo()
        self.controller_window.status(callsign)
        self.controller_window.closed.connect(self.show)
        self.controller_window.show()

    def show_followme_info(self, callsign):
        """Here call the FOLME Class"""
        self.followme_window = FOLME.FollowMeService()
        self.followme_window.status(callsign)
        self.followme_window.closed.connect(self.show)
        self.followme_window.show()

    def show_settings(self):
        """Here call the Settings Class"""
        self.setting_window = Settings.Settings(self)
        self.setting_window.closed.connect(self.show)
        self.setting_window.show()

    def build_db(self):
        """Here call the Build database Class from files.dat"""
        self.build_update = BuildDB.Build_datafiles()
        self.build_update.closed.connect(self.show)
        self.build_update.show()

    def all2map(self):
        """This function is for see the whole map, all player in GoogleMaps, I implemented this before show up webeye,
           now with webeye, I want to use it here, to make strong those 2 tools"""
        self.statusBar().showMessage('Populating all players in the Map', 10000)
        qApp.processEvents()
        MapView.all2map()
        mapfileall_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules')
        self.maptab.load(QUrl(mapfileall_path + '/all_in_map.html'))

    def statistics(self):
        """This function is for Statistics Tab in the MainWindow, when select option at combobox appears result"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
        ImageAirlines = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'airlines')
        item = self.ui.comboBoxStatistics.currentIndex()
        qApp.processEvents()

        if item == 0:
            self.statusBar().showMessage('Counting...', 2000)
            qApp.processEvents()
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            cursor.execute("SELECT callsign FROM recent WHERE clienttype='ATC';" )
            controller_list = cursor.fetchall()

            list_all = []
            for callsign in range(0, len(controller_list)):
                try:
                    if controller_list[callsign][0][2:3] == '-' or controller_list[callsign][0][2:3] == '_':
                        Q_db = SQL_queries.sql_query('Get_Country_by_Id', (str(controller_list[callsign][0])[:2],))
                        country_icao = Q_db.fetchone()
                        if country_icao is None:
                            Q_db = SQL_queries.sql_query('Get_Country_from_Prefix', (str(controller_list[callsign][0])[:2],))
                            country_icao = Q_db.fetchone()
                    else:
                        Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(controller_list[callsign][0])[:4],))
                        country_icao = Q_db.fetchone()
                        if country_icao is None:
                            continue
                    list_all.append(str(country_icao[0]))
                except:
                    continue

            cursor.execute("SELECT realname FROM recent WHERE clienttype='PILOT';" )
            pilot_list = cursor.fetchall()

            for callsign in range(0, len(pilot_list)):
                if pilot_list[callsign][0][-4:]:
                    Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(pilot_list[callsign][0].encode('latin-1'))[-4:],))
                country_icao = Q_db.fetchone()
                if country_icao is None:
                    continue
                else:
                    list_all.append(str(country_icao[0]))

            all_countries = {}
            for item_list in set(list_all):
                all_countries[item_list] = list_all.count(item_list)

            for country in sorted(all_countries, key=all_countries.__getitem__, reverse=True):
                if country[0] == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    flagCodePath = (ImageFlags + '/%s.png') % country
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.Statistics.setCellWidget(startrow, 0, flag_country)
                    else:
                        pass
                    col_item = QTableWidgetItem(str('%s' % (country)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(all_countries[country])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(all_countries[country]) / float(len(list_all)) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 1:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            cursor.execute("SELECT callsign FROM recent WHERE clienttype='ATC';" )
            controller_list = cursor.fetchall()

            list_icao = []
            for callsign in range(0, len(controller_list)):
                try:
                    if controller_list[callsign][0][2:3] == '-' or controller_list[callsign][0][2:3] == '_':
                        Q_db = SQL_queries.sql_query('Get_Country_by_Id', (str(controller_list[callsign][0])[:2],))
                        country_icao = Q_db.fetchone()
                        if country_icao is None:
                            Q_db = SQL_queries.sql_query('Get_Country_from_Prefix', (str(controller_list[callsign][0])[:2],))
                            country_icao = Q_db.fetchone()
                    else:
                        Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(controller_list[callsign][0])[:4],))
                        country_icao = Q_db.fetchone()
                        if country_icao is None:
                            continue
                    list_icao.append(str(country_icao[0]))
                except:
                    continue

            countries = {}
            for item_list in set(list_icao):
                countries[item_list] = list_icao.count(item_list)

            for country in sorted(countries, key=countries.__getitem__, reverse=True):
                if country[0] == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    flagCodePath = (ImageFlags + '/%s.png') % country
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.Statistics.setCellWidget(startrow, 0, flag_country)
                    else:
                        pass
                    col_item = QTableWidgetItem(str('%s' % (country)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(countries[country])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(countries[country]) / float(len(controller_list)) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 2:
            self.statusBar().showMessage('Counting...', 2000)
            qApp.processEvents()
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            cursor.execute("SELECT realname FROM recent WHERE clienttype='PILOT';" )
            pilot_list = cursor.fetchall()

            list_icao = []
            for callsign in range(0, len(pilot_list)):
                if pilot_list[callsign][0][-4:]:
                    Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(pilot_list[callsign][0].encode('latin-1'))[-4:],))
                country_icao = Q_db.fetchone()
                if country_icao is None:
                    continue
                else:
                    list_icao.append(str(country_icao[0]))

            countries = {}
            for item_list in set(list_icao):
                countries[item_list] = list_icao.count(item_list)

            for country in sorted(countries, key=countries.__getitem__, reverse=True):
                if country[0] == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    flagCodePath = (ImageFlags + '/%s.png') % country
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.Statistics.setCellWidget(startrow, 0, flag_country)
                    else:
                        pass
                    col_item = QTableWidgetItem(str('%s' % (country)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(countries[country])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(countries[country]) / float(len(pilot_list)) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 3:
            self.statusBar().showMessage('Counting...', 2000)
            qApp.processEvents()
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)

            cursor.execute("SELECT planned_depairport FROM recent")
            all_airports_dep = cursor.fetchall()
            cursor.execute("SELECT planned_destairport FROM recent")
            all_airports_dest = cursor.fetchall()

            list_traffic_airport = []
            for airport in range(0, len(all_airports_dep)):
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(all_airports_dep[airport][0]),))
                country = Q_db.fetchone()
                if country is None:
                    continue
                else:
                    list_traffic_airport.append(str(country[0]))

            for airport in range(0, len(all_airports_dest)):
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(all_airports_dest[airport][0]),))
                country = Q_db.fetchone()
                if country is None:
                    continue
                else:
                    list_traffic_airport.append(str(country[0]))

            country_dict = {}
            for item_list in set(list_traffic_airport):
                country_dict[item_list] = list_traffic_airport.count(item_list)

            startrow = 0
            for country in sorted(country_dict, key=country_dict.__getitem__, reverse=True):
                if country[0] == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    flagCodePath = (ImageFlags + '/%s.png') % country
                    if os.path.exists(flagCodePath) is True:
                        Pixmap = QPixmap(flagCodePath)
                        flag_country = QLabel()
                        flag_country.setPixmap(Pixmap)
                        self.ui.Statistics.setCellWidget(startrow, 0, flag_country)
                    else:
                        pass
                    col_item = QTableWidgetItem(str('%s' % (country)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(country_dict[country])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(country_dict[country]) / float(len(list_traffic_airport)) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
            self.statusBar().showMessage('Done!', 2000)

        if item == 4:
            self.statusBar().showMessage('Counting...', 2000)
            qApp.processEvents()
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0
            cursor.execute("SELECT SUBSTR(callsign,1,3) AS prefix, COUNT(DISTINCT callsign) AS airlines FROM recent WHERE clienttype='PILOT' GROUP BY prefix ORDER BY airlines DESC;")
            items = cursor.fetchall()

            for i in range(0, len(items)):
                self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                code_airline = items[i][0]
                airlineCodePath = (ImageAirlines + '/%s.gif') % code_airline
                try:
                    if os.path.exists(airlineCodePath) is True:
                        Pixmap = QPixmap(airlineCodePath)
                        airline = QLabel(self)
                        airline.setPixmap(Pixmap)
                        self.ui.Statistics.setCellWidget(startrow, 1, airline)
                    else:
                        cursor.execute('SELECT airline_name FROM airlines WHERE code=?', (str(items[i][0]),))
                        airline_code = cursor.fetchone()
                        if airline_code is None:
                            col_airline = QTableWidgetItem(str(items[i][0]), 0)
                        else:
                            col_airline = QTableWidgetItem(str(airline_code[0]), 0)
                        self.ui.Statistics.setItem(startrow, 1, col_airline)
                except:
                    col_item = QTableWidgetItem(str(items[i][0]), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                col_total = QTableWidgetItem(str(int(items[i][1])), 0)
                self.ui.Statistics.setItem(startrow, 2, col_total)
                percent = float(items[i][1]) / float(len(items)) * 100.0
                self.progressbar = QProgressBar()
                self.progressbar.setMinimum(1)
                self.progressbar.setMaximum(100)
                self.progressbar.setValue(float(percent))
                self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                startrow += 1
            self.statusBar().showMessage('Done!', 2000)

        if item == 5:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0
            cursor.execute("SELECT planned_aircraft FROM recent WHERE clienttype='PILOT';" )
            airplane_type = cursor.fetchall()
            list_aircraft = []
            for item_list in range(0, len(airplane_type)):
                if str(airplane_type[item_list][0]) == '' or str(airplane_type[item_list][0]) == 'None':
                    continue
                else:
                    cursor.execute("SELECT fabricant FROM aircraft WHERE icao=?;", (str(airplane_type[item_list][0]).split('/')[1],))
                    fabricant = cursor.fetchall()
                    if fabricant == []:
                        continue
                    else:
                        list_aircraft.append(str(fabricant[0][0]))

            fabricant_type = {}
            for item_list in set(list_aircraft):
                fabricant_type[item_list] = list_aircraft.count(item_list)

            for item in sorted(fabricant_type, key=fabricant_type.__getitem__, reverse=True):
                if fabricant_type == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    col_item = QTableWidgetItem(str('%s' % (str(item))), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(fabricant_type[item])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(fabricant_type[item]) / float(len(list_aircraft)) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 6:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0
            cursor.execute("SELECT planned_aircraft FROM recent WHERE clienttype='PILOT';" )
            airplane_type = cursor.fetchall()
            list_aircraft = []
            for item_list in range(0, len(airplane_type)):
                if str(airplane_type[item_list][0]) == '' or str(airplane_type[item_list][0]) == 'None':
                    continue
                else:
                    list_aircraft.append(str(airplane_type[item_list]).split('/')[1])

            list_type = {}
            for item_list in set(list_aircraft):
                list_type[item_list] = list_aircraft.count(item_list)

            for item in sorted(list_type, key=list_type.__getitem__, reverse=True):
                if list_type == 0:
                    continue
                else:
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    cursor.execute("SELECT model FROM aircraft WHERE icao=?;", (item,))
                    aircraft_description = cursor.fetchone()
                    if aircraft_description is None:
                        continue
                    else:
                        col_item = QTableWidgetItem(str('%s - %s' % (str(item), str(aircraft_description[0]))), 0)
                        self.ui.Statistics.setItem(startrow, 1, col_item)
                        col_total = QTableWidgetItem(str(int(list_type[item])), 0)
                        self.ui.Statistics.setItem(startrow, 2, col_total)
                        percent = float(list_type[item]) / float(len(list_aircraft)) * 100.0
                        self.progressbar = QProgressBar()
                        self.progressbar.setMinimum(1)
                        self.progressbar.setMaximum(100)
                        self.progressbar.setValue(float(percent))
                        self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                        startrow += 1
                    qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 7:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            for min_pob, max_pob in [(1, 4), (5, 20), (21, 75), (76, 150), (151, 250), (250, 500)]:
                cursor.execute("SELECT COUNT(callsign) FROM recent WHERE clienttype='PILOT';" )
                total_items = cursor.fetchone()
                if total_items[0] == 0:
                    continue
                else:
                    cursor.execute("SELECT COUNT(callsign) FROM recent WHERE clienttype='PILOT' AND planned_pob >= ? AND planned_pob <= ?;", (min_pob, max_pob))
                    pob = cursor.fetchone()
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    col_item = QTableWidgetItem(str('Flights with Passengers on Boards: %d - %d' % (min_pob, max_pob)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(pob[0])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(pob[0]) / float(total_items[0]) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 8:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            for type_flight in ('S', 'G', 'M', 'N', 'X'):
                cursor.execute("SELECT COUNT(planned_typeofflight) FROM recent WHERE clienttype='PILOT';" )
                total_items = cursor.fetchone()
                if total_items[0] == 0:
                    continue
                else:
                    cursor.execute("SELECT COUNT(planned_typeofflight) FROM recent WHERE clienttype='PILOT' and planned_typeofflight = ?;", (type_flight,))
                    item_typeofflight = cursor.fetchone()
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    if type_flight == 'S':
                        col_item = QTableWidgetItem(str('Flights: Scheduled Services'))
                    if type_flight == 'N':
                        col_item = QTableWidgetItem(str('Flights: Non-Scheduled Services'))
                    if type_flight == 'G':
                        col_item = QTableWidgetItem(str('Flights: General Aviation'))
                    if type_flight == 'M':
                        col_item = QTableWidgetItem(str('Flights: Military'))
                    if type_flight == 'X':
                        col_item = QTableWidgetItem(str('Flights: Others'))
                    col_1 = QTableWidgetItem(str(type_flight), 0)
                    self.ui.Statistics.setItem(startrow, 0, col_1)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(item_typeofflight[0]), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(item_typeofflight[0]) / float(total_items[0]) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()

            for type_flight in ('I', 'V', 'Y', 'Z'):
                cursor.execute("SELECT COUNT(planned_flighttype) FROM recent WHERE clienttype='PILOT';" )
                total_items = cursor.fetchone()
                if total_items[0] == 0:
                    continue
                else:
                    cursor.execute("SELECT COUNT(planned_flighttype) FROM recent WHERE clienttype='PILOT' and planned_flighttype = ?;", (type_flight,))
                    item_typeofflight = cursor.fetchone()
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    if type_flight == 'I':
                        col_item = QTableWidgetItem(str('Flights: Instrumental'))
                    if type_flight == 'V':
                        col_item = QTableWidgetItem(str('Flights: Visual'))
                    if type_flight == 'Y':
                        col_item = QTableWidgetItem(str('Flights: Instrumental changing to Visual'))
                    if type_flight == 'Z':
                        col_item = QTableWidgetItem(str('Flights: Visual changing to Instrumental'))
                    col_1 = QTableWidgetItem(str(type_flight), 0)
                    self.ui.Statistics.setItem(startrow, 0, col_1)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(item_typeofflight[0]), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(item_typeofflight[0]) / float(total_items[0]) * 100.0
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 9:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0

            for facility, description in (('DEP','Departure'), ('GND','Ground'), ('TWR', 'Tower'),
                                          ('APP','Approach'), ('CTR','Center'), ('OBS','Observer')):
                cursor.execute("SELECT COUNT(callsign) FROM recent WHERE clienttype='ATC';" )
                total_items = cursor.fetchone()
                if total_items[0] == 0:
                    continue
                else:
                    cursor.execute("SELECT COUNT(callsign) FROM recent WHERE clienttype='ATC' AND callsign LIKE ?;",
                                   ('%'+str(facility)+'%',))
                    position = cursor.fetchone()
                    self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                    col_item = QTableWidgetItem(str('Controllers in: %s - (%s)' % (facility, description)), 0)
                    self.ui.Statistics.setItem(startrow, 1, col_item)
                    col_total = QTableWidgetItem(str(int(position[0])), 0)
                    self.ui.Statistics.setItem(startrow, 2, col_total)
                    percent = float(position[0]) / float(total_items[0]) * 100.0
                    QTableWidgetItem(str('%.1f' % (float(percent))), 0)
                    self.progressbar = QProgressBar()
                    self.progressbar.setMinimum(1)
                    self.progressbar.setMaximum(100)
                    self.progressbar.setValue(float(percent))
                    self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                    startrow += 1
                qApp.processEvents()
            self.statusBar().showMessage('Done!', 2000)

        if item == 10:
            self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
            while self.ui.Statistics.rowCount () > 0:
                self.ui.Statistics.removeRow(0)
            startrow = 0
            list_server = {}
            cursor.execute("SELECT COUNT(server) FROM recent")
            total_server_used = cursor.fetchone()
            for server in ('AM1', 'AM2', 'AS1', 'EU1', 'EU2', 'EU3', 'EU4', 'EU5', 'EU6',
                           'EU7', 'EU8', 'EU9', 'EU11', 'EU12', 'EU13', 'EU14', 'EU15'):
                cursor.execute("SELECT COUNT(server) FROM recent WHERE server=?;", (str(server),))
                total_items = cursor.fetchone()
                if total_items[0] == 0:
                    continue
                else:
                    list_server[server] = total_items[0]

            for item in list_server.keys():
                self.ui.Statistics.insertRow(self.ui.Statistics.rowCount())
                col_item = QTableWidgetItem(str('%s' % (str(item),)), 0)
                self.ui.Statistics.setItem(startrow, 1, col_item)
                col_total = QTableWidgetItem(str(list_server[item]), 0)
                self.ui.Statistics.setItem(startrow, 2, col_total)
                percent = float(list_server[item]) / float(total_server_used[0]) * 100.0
                self.progressbar = QProgressBar()
                self.progressbar.setMinimum(1)
                self.progressbar.setMaximum(100)
                self.progressbar.setValue(float(percent))
                self.ui.Statistics.setCellWidget(startrow, 3, self.progressbar)
                startrow += 1
                qApp.processEvents()
        self.statusBar().showMessage('Done!', 2000)

    def network(self):
        """This function is to see NetworkTab statistics"""
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        database = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', config.get('Database', 'db'))
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        startrow = 0
        for item in ('AM1', 'AM2', 'AS1', 'EU1', 'EU2', 'EU3', 'EU4', 'EU5', 'EU6', 'EU7', 'EU8', 'EU9', 'EU11', 'EU12', 'EU13', 'EU14', 'EU15'):
            cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='PILOT' AND server=?;", (str(item),))
            server_pilot = cursor.fetchone()
            cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='ATC' AND NOT callsign LIKE '%OBS%' AND server=?;", (str(item),))
            server_controller = cursor.fetchone()
            cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='ATC' AND callsign LIKE '%OBS%' AND server=?;", (str(item),))
            server_observer = cursor.fetchone()
            cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE server=?;", (str(item),))
            server_total = cursor.fetchone()
            col_pilot = QTableWidgetItem(str(server_pilot[0]), 0)
            self.ui.network_table.setItem(startrow, 4, col_pilot)
            col_controllers = QTableWidgetItem(str(server_controller[0]), 0)
            self.ui.network_table.setItem(startrow, 5, col_controllers)
            col_observers = QTableWidgetItem(str(server_observer[0]), 0)
            self.ui.network_table.setItem(startrow, 6, col_observers)
            col_total = QTableWidgetItem(str(server_total[0]), 0)
            self.ui.network_table.setItem(startrow, 7, col_total)
            startrow += 1
            qApp.processEvents()

    def Scheduling(self):
        self.statusBar().showMessage('Downloading Events for Controllers and Pilots...', 2000)
        qApp.processEvents()
        check = Schedule.Scheduling()
        if check is True:
            self.statusBar().showMessage('Refreshing Schedule...', 2000)
            self.show_TabSched()
            self.statusBar().showMessage('Schedule Done!', 2000)
        else:
            self.statusBar().showMessage('Error! when trying to download info from IVAO. Check your connection to Internet.')

    def show_TabSched(self):
        ImageFlags = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flags')
        ImageAirlines = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'airlines')

        Q_db = SQL_queries.sql_query('Get_Schedule_ATC', None)
        sched_atc = Q_db.fetchall()

        qApp.processEvents()
        while self.ui.SchedulingATC.rowCount () > 0:
            self.ui.SchedulingATC.removeRow(0)

        startrow = 0
        for atc_table in range(0, len(sched_atc)):
            self.ui.SchedulingATC.insertRow(self.ui.SchedulingATC.rowCount())
            col_Name = QTableWidgetItem(str(sched_atc[atc_table][0].encode('latin-1')), 0)
            self.ui.SchedulingATC.setItem(startrow, 2, col_Name)
            col_Position = QTableWidgetItem(sched_atc[atc_table][1], 0)
            self.ui.SchedulingATC.setItem(startrow, 3, col_Position)
            col_StartTime = QTableWidgetItem(str(sched_atc[atc_table][2]), 0)
            self.ui.SchedulingATC.setItem(startrow, 4, col_StartTime)
            col_EndTime = QTableWidgetItem(str(sched_atc[atc_table][3]), 0)
            self.ui.SchedulingATC.setItem(startrow, 5, col_EndTime)
            col_Voice = QTableWidgetItem(str(sched_atc[atc_table][4]), 0)
            self.ui.SchedulingATC.setItem(startrow, 6, col_Voice)
            col_Training = QTableWidgetItem(str(sched_atc[atc_table][5]), 0)
            self.ui.SchedulingATC.setItem(startrow, 7, col_Training)
            col_Event = QTableWidgetItem(str(sched_atc[atc_table][6]), 0)
            self.ui.SchedulingATC.setItem(startrow, 8, col_Event)
            try:
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(sched_atc[atc_table][1][:4]),))
                country = Q_db.fetchone()
                if country is None:
                    Q_db = SQL_queries.sql_query('Get_Country_from_FIR', (str(sched_atc[atc_table][1][:4]),))
                    country = Q_db.fetchone()
                col_Country = QTableWidgetItem(str(country[0]), 0)
                self.ui.SchedulingATC.setItem(startrow, 1, col_Country)
                flagCodePath = (ImageFlags + '/%s.png') % (str(country[0]))
                Pixmap = QPixmap(flagCodePath)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.SchedulingATC.setCellWidget(startrow, 0, flag_country)
            except:
                pass
            startrow += 1
            qApp.processEvents()

        Q_db = SQL_queries.sql_query('Get_Schedule_Flights')
        sched_pilots = Q_db.fetchall()

        qApp.processEvents()
        while self.ui.SchedulingFlights.rowCount () > 0:
            self.ui.SchedulingFlights.removeRow(0)

        startrow = 0
        for flights_table in range(0, len(sched_pilots)):
            self.ui.SchedulingFlights.insertRow(self.ui.SchedulingFlights.rowCount())
            code_Airline = sched_pilots[flights_table][0][:3]
            airlinePath = (ImageAirlines + '/%s.gif') % code_Airline
            try:
                if os.path.exists(airlinePath) is True:
                    Pixmap = QPixmap(airlinePath)
                    airline = QLabel(self)
                    airline.setPixmap(Pixmap)
                    self.ui.SchedulingFlights.setCellWidget(startrow, 0, airline)
                else:
                    code_airline = str(inbound[0])
                    col_airline = QTableWidgetItem(code_airline, 0)
                    self.ui.SchedulingFlights.setItem(startrow, 0, col_airline)
            except:
                pass
            col_Callsign = QTableWidgetItem(str(sched_pilots[flights_table][0]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 1, col_Callsign)
            col_Name = QTableWidgetItem(str(sched_pilots[flights_table][1].encode('latin-1')), 0)
            self.ui.SchedulingFlights.setItem(startrow, 2, col_Name)
            col_Airplane = QTableWidgetItem(str(sched_pilots[flights_table][2]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 3, col_Airplane)
            col_Departure = QTableWidgetItem(str(sched_pilots[flights_table][3]), 0)
            try:
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(sched_pilots[flights_table][3]),))
                country = Q_db.fetchone()
                if country is None:
                    Q_db = SQL_queries.sql_query('Get_Country_from_FIR',  (str(sched_pilots[flights_table][3]),))
                    country = Q_db.fetchone()
                flagCodePath = (ImageFlags + '/%s.png') % (str(country[0]))
                Pixmap = QPixmap(flagCodePath)
                flag_country = QLabel()
                flag_country.setPixmap(Pixmap)
                self.ui.SchedulingFlights.setCellWidget(startrow, 4, flag_country)
            except:
                pass
            self.ui.SchedulingFlights.setItem(startrow, 5, col_Departure)
            col_StartTime = QTableWidgetItem(str(sched_pilots[flights_table][4]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 6, col_StartTime)
            col_Destination = QTableWidgetItem(str(sched_pilots[flights_table][5]), 0)
            try:
                Q_db = SQL_queries.sql_query('Get_Country_from_ICAO', (str(sched_pilots[flights_table][5]),))
                country = Q_db.fetchone()
                if country is None:
                    Q_db = SQL_queries.sql_query('Get_Country_from_FIR', (str(sched_pilots[flights_table][5]),))
                    country = Q_db.fetchone()
                flagCodePath = (ImageFlags + '/%s.png') % (str(country[0]))
            except:
                pass
            Pixmap = QPixmap(flagCodePath)
            flag_country = QLabel()
            flag_country.setPixmap(Pixmap)
            self.ui.SchedulingFlights.setCellWidget(startrow, 7, flag_country)
            self.ui.SchedulingFlights.setItem(startrow, 8, col_Destination)
            col_EndTime = QTableWidgetItem(str(sched_pilots[flights_table][6]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 9, col_EndTime)
            col_Altitude = QTableWidgetItem(str(sched_pilots[flights_table][7]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 10, col_Altitude)
            col_CruisingSpeed = QTableWidgetItem(str(sched_pilots[flights_table][8]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 11, col_CruisingSpeed)
            col_Route = QTableWidgetItem(str(sched_pilots[flights_table][9]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 12, col_Route)
            col_Voice = QTableWidgetItem(str(sched_pilots[flights_table][10]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 13, col_Voice)
            col_Training = QTableWidgetItem(str(sched_pilots[flights_table][11]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 14, col_Training)
            col_Event = QTableWidgetItem(str(sched_pilots[flights_table][12]), 0)
            self.ui.SchedulingFlights.setItem(startrow, 15, col_Event)
            startrow += 1
            qApp.processEvents()
        self.statusBar().showMessage('Done!', 2000)

def main():
    """Next lines is for set only specific theme with Qt libraries to the app"""
    import sys, time, os
    QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
    QApplication.setPalette(QApplication.style().standardPalette())
    app = QApplication(sys.argv)
    image_splash = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'ivao_status_splash.png')
    splash_pix = QPixmap(image_splash)
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
