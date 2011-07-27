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
        
        self.ui.action_update.setText("Downloading from IVAO status update...")
        StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + IVAO_STATUS)
        StatusFile = open(IVAO_STATUS, 'w')
        StatusFile.write(StatusURL.read())
        StatusFile.close()

        pilot_list = []
        atc_list = []
        
        self.ui.action_update.setText("Ready... Counting players...")
        
        for logged_users in open(IVAO_STATUS):
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
            realname = str(pilot_list[rows].rsplit(":")[2])
            clienttype = pilot_list[rows].split(":")[3]
            frequency = 0
            latitude = pilot_list[rows].split(":")[5]
            longitude = pilot_list[rows].split(":")[6]
            altitude = pilot_list[rows].split(":")[7]
            groundspeed = pilot_list[rows].split(":")[8]
            planned_aircraft = 0
            planned_tascruise = 0
            planned_depairport = pilot_list[rows].split(":")[11]
            planned_altitude = pilot_list[rows].split(":")[12]
            planned_destairport = pilot_list[rows].split(":")[13]
            server = pilot_list[rows].split(":")[14]
            protrevision = pilot_list[rows].split(":")[15]
            rating = pilot_list[rows].split(":")[16]
            transponder = pilot_list[rows].split(":")[17]
            facilitytype = pilot_list[rows].split(":")[18]
            visualrange = pilot_list[rows].split(":")[19]
            planned_revision = pilot_list[rows].split(":")[20]
            planned_flighttype = pilot_list[rows].split(":")[21]
            planned_deptime = 0
            planned_actdeptime = 0
            planned_hrsenroute = 0
            planned_minenroute = 0
            planned_hrsfuel = 0
            planned_minfuel = 0
            planned_altairport = 0
            planned_remarks = 0
            planned_route = 0
            planned_depairport_lat = 0
            planned_depairport_lon = 0
            planned_destairport_lat = 0
            planned_destairport_lon = 0
            atis_message = 0
            time_last_atis_received = 0
            time_connected = 0
            client_software_name = 0
            client_software_version = 0
            adminrating = 0
            atc_or_pilotrating = 0
            planned_altairport2 = 0
            planned_typeofflight = 0
            planned_pob = 0
            true_heading = 0
            onground = 0

            cursor.execute("INSERT INTO status_ivao (callsign, vid, server, clienttype\
            , latitude, longitude, groundspeed, planned_depairport, planned_altitude\
            , planned_destairport, server, protrevision, rating, transponder, facilitytype\
            , visualrange, planned_revision, planned_flighttype) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, server, clienttype, latitude, longitude, groundspeed, planned_depairport, \
             planned_altitude, planned_destairport, server, protrevision, rating, transponder, facilitytype, \
             visualrange, planned_revision, planned_flighttype))

        connection.commit()
        connection.close()
        
        self.ui.action_update.setText("Ready")

#            parser_slash = list_users[0][i].split('/')
#            
#            print "Callsign: " + parser_colons[10]
#            
#            try:
#                print "Aircraft: " + parser_slash[1]
#            except:
#                print "Aircraft: -"
#                
#            print
#        
#        StatusFile.close()

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
