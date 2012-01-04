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

import os
import ConfigParser
import sqlite3

def sql_query(args=None, var=None):
    '''At this function should be to set all SQL queries to database, missing some ones yet but here is the major'''
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    if args == 'Get_All_Flags':
        Q_db = cursor.execute("SELECT DISTINCT(Country) FROM icao_codes ORDER BY Country ASC;")
    if args == 'Get_All_data_icao_codes':
        Q_db = cursor.execute("SELECT icao, Latitude, Longitude, City_Airport, Country FROM icao_codes DESC;")
    if args == 'Get_Country_from_ICAO':
        Q_db = cursor.execute('SELECT Country FROM icao_codes WHERE icao = ?;', (str(var[0]),))
    if args == 'Get_Country_from_FIR':
        Q_db = cursor.execute('SELECT Country FROM fir_data_list WHERE icao = ?;', (str(var[0]),))
    if args == 'Get_Country_from_Division':
        Q_db = cursor.execute('SELECT Country FROM division_ivao WHERE Division=?;', (str(var[0]),))
    if args == 'Get_Status':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, planned_depairport, \
                               planned_destairport, onground, time_connected, groundspeed, planned_altitude, \
                               Latitude, Longitude FROM status_ivao WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_City':
        Q_db = cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?;", (str(var[0]),))
    if args == 'Get_Pilots':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='PILOT';")
    if args == 'Get_Pilot':
        Q_db = cursor.execute("SELECT callsign, planned_aircraft, rating, realname, planned_depairport, planned_destairport, \
                               time_connected FROM status_ivao WHERE clienttype='PILOT' \
                               AND realname LIKE ? ORDER BY vid DESC;", (('%'+str(var[0])),))
    if args == 'Get_Controllers':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC';")
    if args == 'Get_FollowMeCarService':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='FOLME';")
    if args == 'Get_Observers':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM status_ivao WHERE clienttype='ATC' AND callsign like '%OBS%';")
    if args == 'Get_POB':
        Q_db = cursor.execute("SELECT SUM(planned_pob) FROM status_ivao;")
    if args == 'Get_Controller_List':
        Q_db = cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
                               WHERE clienttype='ATC' ORDER BY vid DESC;")
    if args == 'Get_Controller':
        Q_db = cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM status_ivao \
                               WHERE clienttype='ATC' AND callsign LIKE ? ORDER BY vid DESC;", (('%'+var[0]+'%'),))
    if args == 'Get_Pilot_Lists':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, rating, realname, planned_depairport, \
                               planned_destairport, time_connected, clienttype FROM status_ivao \
                               WHERE clienttype='PILOT' ORDER BY vid ASC;")
    if args == 'Get_FMC_List':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), rating, realname, time_connected, clienttype \
                               FROM status_ivao WHERE clienttype='FOLME';")
    if args == 'Get_Airline':
        Q_db = cursor.execute('SELECT Airline FROM airlines_codes WHERE Code = ?;', (str(var[0]),))
    if args == 'Get_ICAO_from_Country':
        Q_db = cursor.execute("SELECT icao FROM icao_codes WHERE country=?;", (str(var[0]),))
    if args == 'Get_Outbound_Traffic':
        Q_db= cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_depairport LIKE ?", \
                       (str(var[0]),))
    if args == 'Get_Inbound_Traffic':
        Q_db = cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM status_ivao WHERE planned_destairport LIKE ?", \
                       (str(var[0]),))
    if args == 'Search_vid':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where vid like ?;", \
                              (str(var[0]),))
    if args == 'Search_callsign':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where callsign like ?;", \
                              (str(var[0]),))
    if args == 'Search_realname':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype from status_ivao where realname like ?;", \
                              (str(var[0]),))
    if args == 'Get_Airport_from_ICAO':
        Q_db = cursor.execute("SELECT City_Airport FROM icao_codes WHERE icao=?", (str(var[0]),))
    if args == 'Get_Controller_data':
        Q_db = cursor.execute("SELECT vid, realname, server, clienttype, frequency, rating, facilitytype, atis_message, \
                               time_connected, client_software_name, client_software_version FROM status_ivao \
                               WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Pilot_data':
        Q_db = cursor.execute("SELECT vid, realname, altitude, groundspeed, planned_aircraft, planned_depairport, \
                            planned_destairport, planned_altitude, planned_pob, planned_route, rating, transponder, onground,\
                            latitude, longitude, planned_altairport, planned_altairport2, planned_tascruise, time_connected, clienttype \
                            FROM status_ivao WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_FIR_from_ICAO':
        Q_db = cursor.execute("SELECT FIR FROM fir_data_list WHERE icao=?", (str(var[0]),))
    if args == 'Get_FMC_data':
        Q_db = cursor.execute("SELECT vid, realname, server, clienttype, rating, time_connected, client_software_name, \
                               client_software_version FROM status_ivao WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Airport_Location':
        Q_db = cursor.execute("SELECT City_Airport, Latitude, Longitude FROM icao_codes WHERE icao=?", (str(var[0]),))
    if args == 'Get_Location_from_ICAO':
        Q_db = cursor.execute("SELECT longitude, latitude FROM icao_codes WHERE ICAO=?;", (str(var[0]),))
    if args == 'Get_Player_Location':
        Q_db = cursor.execute("SELECT latitude, longitude, callsign, true_heading, clienttype \
                               FROM status_ivao WHERE callsign=?;",  (str(var[0]),))
    if args == 'Get_Players_Locations':
        Q_db = cursor.execute("SELECT longitude, latitude, callsign, true_heading, clienttype FROM status_ivao;")
    if args == 'Get_IdFIR_from_ICAO':
        Q_db = cursor.execute("SELECT ID_FIRCOASTLINE FROM fir_data_list WHERE ICAO = ?;", (str(var[0]),))
    if args == 'Get_borders_FIR':
        Q_db = cursor.execute("SELECT Longitude, Latitude FROM fir_coastlines_list where ID_FIRCOASTLINE = ?;", (int(id_ctr[0]),))
    return Q_db