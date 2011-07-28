#!/bin/python -W
# IVAO-status
# Author: Antonio P. Diaz <emperor.cu@gmail.com>
# Date Jul 2011
# License GPLv3+
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import MainWindow_UI
import urllib2
import sqlite3
import threading

IVAO_STATUS = 'whazzup.txt'

class Main(QtGui.QMainWindow):
    def __init__(self):
        
        QtGui.QMainWindow.__init__(self)
       
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        self.setWindowIcon(QtGui.QIcon('./images/ivao.jpg'))
        self.connect(self.ui.ExitBtn, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.UpdateBtn, QtCore.SIGNAL("clicked()"), self.UpdateDB)
        
    def UpdateDB(self):
        
        action_update = threading.local()        
        action_update = self.ui.action_update.setText("Downloading from IVAO status update...")
        thread = threading.Thread(action_update)
        thread.start()
        thread.join()
        
        pilot_list = []
        atc_list = []
        
        StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + IVAO_STATUS)
        
        self.ui.action_update.setText("Ready... Counting players...")
        
        for logged_users in StatusURL.readlines():
            if "PILOT" in logged_users:
                pilot_list.append(logged_users)
            if "ATC" in logged_users:
                atc_list.append(logged_users)

        self.ui.TotalPilots.setText(str(len(pilot_list)))
        self.ui.TotalATC.setText(str(len(atc_list)))
        self.ui.TotalPlayers.setText(str(len(atc_list) + len(pilot_list)))
        
        self.ui.action_update.setText("Inserting into DB...")

        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()
        
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM status_ivao;")
        
        for rows in range(0, len(pilot_list)):
            callsign = pilot_list[rows].split(":")[0]
            vid = pilot_list[rows].split(":")[1]
            realname = pilot_list[rows].rsplit(":")[2]
            clienttype = pilot_list[rows].split(":")[3]
            latitude = pilot_list[rows].split(":")[5]
            longitude = pilot_list[rows].split(":")[6]
            altitude = pilot_list[rows].split(":")[7]
            groundspeed = pilot_list[rows].split(":")[8]
            planned_aircraft = pilot_list[rows].split(":")[9]
            planned_tascruise = pilot_list[rows].split(":")[10]
            planned_depairport = pilot_list[rows].split(":")[11]
            planned_altitude = pilot_list[rows].split(":")[12]
            planned_destairport = pilot_list[rows].split(":")[13]
            server = pilot_list[rows].split(":")[14]
            protrevision = pilot_list[rows].split(":")[15]
            rating = pilot_list[rows].split(":")[16]
            transponder = pilot_list[rows].split(":")[17]
            visualrange = pilot_list[rows].split(":")[19]
            planned_revision = pilot_list[rows].split(":")[20]
            planned_flighttype = pilot_list[rows].split(":")[21]
            planned_deptime = pilot_list[rows].split(":")[22]
            planned_actdeptime = pilot_list[rows].split(":")[23]
            planned_hrsenroute = pilot_list[rows].split(":")[24]
            planned_minenroute = pilot_list[rows].split(":")[25]
            planned_hrsfuel = pilot_list[rows].split(":")[26]
            planned_minfuel = pilot_list[rows].split(":")[27]
            planned_altairport = pilot_list[rows].split(":")[28]
            planned_remarks = pilot_list[rows].split(":")[29]
            planned_route = pilot_list[rows].split(":")[30]
            planned_depairport_lat = pilot_list[rows].split(":")[31]
            planned_depairport_lon = pilot_list[rows].split(":")[32]
            planned_destairport_lat = pilot_list[rows].split(":")[33]
            planned_destairport_lon = pilot_list[rows].split(":")[34]
            time_last_atis_received = pilot_list[rows].split(":")[36]
            time_connected = pilot_list[rows].split(":")[37]
            client_software_name = pilot_list[rows].split(":")[38]
            client_software_version = pilot_list[rows].split(":")[39]
            adminrating = pilot_list[rows].split(":")[40]
            atc_or_pilotrating = pilot_list[rows].split(":")[41]
            planned_altairport2 = pilot_list[rows].split(":")[42]
            planned_typeofflight = pilot_list[rows].split(":")[43]
            planned_pob = pilot_list[rows].split(":")[44]
            true_heading = pilot_list[rows].split(":")[45]
            onground = pilot_list[rows].split(":")[46]

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
            (callsign, vid, realname, server, clienttype \
            , latitude, longitude, altitude, groundspeed, planned_aircraft, planned_tascruise \
            , planned_depairport, planned_altitude, planned_destairport, server, protrevision \
            , rating, transponder, visualrange, planned_revision, planned_flighttype \
            , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel \
            , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat \
            , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading \
            , onground))

        connection.commit()

        for rows in range(0, len(atc_list)):
            callsign = atc_list[rows].split(":")[0]
            vid = atc_list[rows].split(":")[1]
            realname = atc_list[rows].rsplit(":")[2]
            clienttype = atc_list[rows].split(":")[3]
            frequency = atc_list[rows].split(":")[4]
            latitude = atc_list[rows].split(":")[5]
            longitude = atc_list[rows].split(":")[6]
            altitude = atc_list[rows].split(":")[7]
            server = atc_list[rows].split(":")[14]
            protrevision = atc_list[rows].split(":")[15]
            rating = atc_list[rows].split(":")[16]
            facilitytype = atc_list[rows].split(":")[18]
            visualrange = atc_list[rows].split(":")[19]
            atis_message = atc_list[rows].split(":")[35]
            time_last_atis_received = atc_list[rows].split(":")[36]
            time_connected = atc_list[rows].split(":")[37]
            client_software_name = atc_list[rows].split(":")[38]
            client_software_version = atc_list[rows].split(":")[39]
            adminrating = atc_list[rows].split(":")[40]
            atc_or_atcrating = atc_list[rows].split(":")[41]
            true_heading = atc_list[rows].split(":")[45]
            onground = atc_list[rows].split(":")[46]

            cursor.execute("INSERT INTO status_ivao (callsign, vid, realname, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision \
            , rating, facilitytype, visualrange, planned_revision, atis_message \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, true_heading \
            , onground) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, realname, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision \
            , rating, facilitytype, visualrange, atis_message \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, true_heading \
            , onground))

        connection.commit()
        connection.close()
        
        self.ui.action_update.setText("Ready")

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
