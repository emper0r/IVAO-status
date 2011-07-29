#!/Bin/python -W
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

        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()
        countries = cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes desc;")
        connection.commit()

        for line in countries:
            country = "%s" % line
            self.ui.country_list.addItem(country)

        connection.close()
        PopulateAll(self)

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

        for rows in pilot_list:
            fields = rows.split(":")
            callsign = fields[0]
            vid = fields[1]
            realname = rows.rsplit(":")[2]
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

            cursor.execute("INSERT INTO status_ivao (callsign, vid, server, clienttype \
            , latitude, longitude, altitude, groundspeed, planned_aircraft, planned_tascruise \
            , planned_depairport, planned_altitude, planned_destairport, server, protrevision \
            , rating, transponder, visualrange, planned_revision, planned_flighttype \
            , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel \
            , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat \
            , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading \
            , onground) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, server, clienttype \
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

        for rows in atc_list:
            fields = rows.split(":")
            callsign = fields[0]
            vid = fields[1]
            realname = rows.rsplit(":")[2]
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

            cursor.execute("INSERT INTO status_ivao (callsign, vid, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision \
            , rating, facilitytype, visualrange \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (callsign, vid, server, clienttype, frequency \
            , latitude, longitude, altitude, server, protrevision \
            , rating, facilitytype, visualrange \
            , time_last_atis_received, time_connected, client_software_name, client_software_version \
            , adminrating, atc_or_pilotrating))

        connection.commit()
        connection.close()

        self.ui.action_update.setText("Ready")
        table = PopulateAll(mystruct, 5, 3)

class PopulateAll(QtGui.QTableWidget):
    def __init__(self, mystruct, *args):
        QTableWidget.__init__(self, *args)
        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()
        vid = cursor.execute("SELECT vid FROM status_ivao;")
        connection.commit()
        rows = []
        for line in vid:
            rows.append(line)
   
        thestruct = {}
     
        self.data = thestruct
        #self.data = thestruct
        self.setmydata()

    def setmydata(self):
        for n, key in enumerate(self.data):
            for m, item in enumerate(self.data[key]):
                newitem = self.ui.ATCtableWidgetItem(item)
                self.setItem(m, n, newitem)

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
