#!/bin/python -W
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

IVAO_STATUS = 'whazzup.txt'

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
        self.connect(self.ui.country_list, QtCore.SIGNAL('activated(QString)'), self.country_view)

        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()
        countries = cursor.execute("SELECT DISTINCT(Country) FROM iata_icao_codes desc;")
        connection.commit()

        for line in countries:
            country = "%s" % line
            self.ui.country_list.addItem(country)

        connection.close()

    def UpdateDB(self):

        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()

        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM status_ivao;")

        StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + IVAO_STATUS)
        
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
        atcs_ivao = QtGui.QTableWidgetItem(str(len(atc_list)))
        self.ui.IVAOStatustableWidget.setItem(0, 1, atcs_ivao)
        total_ivao = QtGui.QTableWidgetItem(str(len(atc_list) + len(pilot_list)))
        self.ui.IVAOStatustableWidget.setItem(0, 3, total_ivao)
        
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

        rating_atc = {"1":"OBS - Observer", "2":"S1 - Student 1", "3":"S2 - Student 2" \
                  , "4":"S3 - Student 3", "5":"C1 - Controller 1", "6":"C2 - Controller 2" \
                  , "7":"C3 - Controller 3", "8":"I1 - Instructor 1", "9":"I2 - Instructor 2" \
                  , "10":"I3 - Instructor 3", "11":"SUP - Supervisor", "12":"ADM - Administrator"}
        
        position_atc = {"0":"Observer", "1":"Flight Service Station", "2":"Clearance Delivery" \
                        , "3":"Ground", "4":"Tower", "5":"Approach/Departure", "6":"Center"}
        
        for row_atc in rows_atcs:
            self.ui.ATC_FullList.insertRow(self.ui.ATC_FullList.rowCount())
            col_callsign = QtGui.QTableWidgetItem(str(row_atc[0]), 0)
            self.ui.ATC_FullList.setItem(startrow, 0, col_callsign)
            col_frequency = QtGui.QTableWidgetItem(str(row_atc[1]), 0)
            self.ui.ATC_FullList.setItem(startrow, 1, col_frequency)
            col_realname = QtGui.QTableWidgetItem(str(row_atc[2].encode('latin-1')), 0)
            self.ui.ATC_FullList.setItem(startrow, 2, col_realname)
            col_rating = QtGui.QTableWidgetItem(str(rating_atc[row_atc[3]]), 0)
            self.ui.ATC_FullList.setItem(startrow, 3, col_rating)            
            col_facility = QtGui.QTableWidgetItem(str(position_atc[row_atc[4]]), 0)
            self.ui.ATC_FullList.setItem(startrow, 4, col_facility)
#           col_country = QtGui.QTableWidgetItem(str(row[1]), 0)
#           self.ui.ATC_FullList.setItem(self.ui.ATC_FullList.rowCount()-1, 5, "col_country")
            col_time = QtGui.QTableWidgetItem(str(row_atc[5]), 0)
            self.ui.ATC_FullList.setItem(startrow, 6, col_time)
            startrow += 1

        cursor.execute("SELECT callsign, planned_aircraft, rating, realname, planned_depairport \
                      , planned_destairport, time_connected FROM status_ivao \
                      where clienttype='PILOT' order by vid desc;")
        rows_pilots = cursor.fetchall()

        startrow = 0
        rating_pilot = {"1":"OBS - Observer", "2":"SFO - Second Flight Officer", "3":"FFO - First Flight Officer" \
                        , "4":"C - Captain", "5":"FC - Flight Captain", "6":"SC - Senior Captain" \
                        , "7":"SFC - Senior Flight Captain", "8":"CC - Commercial Captain" \
                        , "9":"CFC - Commercial Flight Captain", "10":"CSC - Commercial Senior Captain" \
                        , "11":"SUP - Supervisor", "12":"ADM - Administrator"}
        
        for row in rows_pilots:
            self.ui.PILOT_FullList.setCurrentCell(0, 0)
            self.ui.PILOT_FullList.insertRow(self.ui.PILOT_FullList.rowCount())
        
            code_airline = row[0][:3]
            airlineCodePath = './airlines/%s.gif' % code_airline
            try:
                if os.path.exists(airlineCodePath) is True:
                    airline = QtGui.QLabel()
                    Pixmap = QtGui.QPixmap(airlineCodePath)
                    airline.fileName = airlineCodePath
                    col_airline = QtGui.QLabel.setPixmap(Pixmap)
                    self.ui.PILOT_FullList.setItem(startrow, 0, col_airline)
                else:
                    code_airline = '-'
                    col_airline = QtGui.QTableWidgetItem(code_airline, 0)
                    self.ui.PILOT_FullList.setItem(startrow, 0, col_airline)   
            except:
                pass         

            col_callsign = QtGui.QTableWidgetItem(str(row[0]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 1, col_callsign)
            
            try:
                aircraft = row[1].split('/')[1]
                if aircraft != '-':
                    pass
            except:
                aircraft = '-'
            
            col_aircraft = QtGui.QTableWidgetItem(aircraft, 0)
            self.ui.PILOT_FullList.setItem(startrow, 2, col_aircraft)
            
            col_realname = QtGui.QTableWidgetItem(str(row[3].encode('latin-1')), 0)
            self.ui.PILOT_FullList.setItem(startrow, 3, col_realname)  
            col_rating = QtGui.QTableWidgetItem(str(rating_pilot[row[2]]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 4, col_rating)                     
#           col_country = QtGui.QTableWidgetItem(str(row[4]), 0)
#           self.ui.PILOT_FullList.setItem(self.ui.PILOT_FullList.rowCount()-1, 4, "col_country")
            col_departure = QtGui.QTableWidgetItem(str(row[4]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 5, col_departure)
            col_destination = QtGui.QTableWidgetItem(str(row[5]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 6, col_destination)
            col_time = QtGui.QTableWidgetItem(str(row[6]), 0)
            self.ui.PILOT_FullList.setItem(startrow, 8, col_time)
            startrow += 1
        
        connection.close()
        self.ui.action_update.setText("Ready")
        
    def  country_view(self):

        country_selected = self.ui.country_list.currentText()
        connection = sqlite3.connect('database/ivao.db')
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT(flagCode) FROM iata_icao_codes WHERE Country=?", (str(country_selected),))
        flagCode = cursor.fetchone()
        connection.commit()

        flagCodePath = ('./flags/%s.gif') % flagCode
        Pixmap = QtGui.QPixmap(flagCodePath)
        self.ui.flagIcon.fileName = flagCodePath
        self.ui.flagIcon.setPixmap(Pixmap)
        connection.close()
        
        # TODO:
        # - Show only Controllers and Pilots selected from countries.
		
def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
