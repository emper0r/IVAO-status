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
    """At this function should be to set all SQL queries to database, missing some ones yet but here is the major"""
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    if args == 'Get_Flags':
        Q_db = cursor.execute("SELECT DISTINCT(country) FROM countries ORDER BY country ASC;")
    if args == 'Get_ICAO_codes':
        Q_db = cursor.execute("SELECT airports.icao, airports.latitude, airports.longitude, airports.city, countries.country FROM airports JOIN countries ON airports.country = countries.id_country;")
    if args == 'Get_Country_from_ICAO':
        Q_db = cursor.execute('SELECT countries.country FROM airports JOIN countries ON airports.country = countries.id_country WHERE airports.icao=?;', (str(var[0]),))
    if args == 'Get_ICAO_from_Country':
        Q_db = cursor.execute("SELECT airports.icao FROM airports JOIN countries ON airports.country = countries.id_country WHERE countries.country=?;", (str(var[0]),))
    if args == 'Get_Controller':
        Q_db = cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM recent \
                               WHERE clienttype='ATC' AND callsign LIKE ? ORDER BY vid DESC;", (('%'+var[0]+'%'),))
    if args == 'Get_Pilot':
        Q_db = cursor.execute("SELECT callsign, planned_aircraft, rating, realname, planned_depairport, planned_destairport, \
                               time_connected FROM recent WHERE clienttype='PILOT' \
                               AND realname LIKE ? ORDER BY vid DESC;", (('%'+str(var[0])),))
    if args == 'Get_Outbound_Traffic':
        Q_db= cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM recent WHERE planned_depairport LIKE ?",
                       (str(var[0]),))
    if args == 'Get_Inbound_Traffic':
        Q_db = cursor.execute("SELECT callsign, planned_depairport, planned_destairport FROM recent WHERE planned_destairport LIKE ?",
                       (str(var[0]),))
    if args == 'Get_Schedule_ATC':
        Q_db = cursor.execute("SELECT Name, Position, StartDateUTC, EndDateUTC, Voice, Training, Event FROM schedule_controllers;")
    if args == 'Get_Schedule_Flights':
        Q_db = cursor.execute("SELECT Callsign, Name, Airplane, Departure, DepTime, Destination, DestTime, \
                               Altitude, CruisingSpeed, Route, Voice, Training, Event FROM schedule_pilots;")
    if args == 'Get_Pilots':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='PILOT';")
    if args == 'Get_Controllers':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='ATC';")
    if args == 'Get_FollowMeCarService':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='FOLME';")
    if args == 'Get_Observers':
        Q_db = cursor.execute("SELECT COUNT(clienttype) FROM recent WHERE clienttype='ATC' AND callsign like '%OBS%';")
    if args == 'Get_POB':
        Q_db = cursor.execute("SELECT SUM(planned_pob) FROM recent;")
    if args == 'Get_Controller_List':
        Q_db = cursor.execute("SELECT callsign, frequency, realname, rating, facilitytype, time_connected FROM recent \
                               WHERE clienttype='ATC' ORDER BY vid DESC;")
    if args == 'Get_Pilot_Lists':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, rating, realname, planned_depairport, \
                               planned_destairport, time_connected, clienttype FROM recent \
                               WHERE clienttype='PILOT' ORDER BY vid ASC;")
    if args == 'Get_Country_from_FIR':
        Q_db = cursor.execute('SELECT distinct(countries.country) FROM countries JOIN firs ON firs.id_country = countries.id_country WHERE firs.fir=?;', (str(var[0]),))
    if args == 'Get_Country_by_Id':
        Q_db = cursor.execute("SELECT DISTINCT(country) FROM countries WHERE id_country=?;", (str(var[0]),))
    if args == 'Get_FMC_List':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), rating, realname, time_connected, clienttype \
                               FROM recent WHERE clienttype='FOLME';")
    if args == 'Get_Status':
        Q_db = cursor.execute("SELECT DISTINCT(callsign), planned_aircraft, planned_depairport, \
                               planned_destairport, onground, time_connected, groundspeed, planned_altitude, \
                               Latitude, Longitude FROM recent WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Airline':
        Q_db = cursor.execute('SELECT airline_name FROM airlines WHERE code=?;', (str(var[0]),))
    if args == 'Get_City':
        Q_db = cursor.execute("SELECT city, latitude, longitude FROM airports WHERE icao=?;", (str(var[0]),))
    if args == 'Search_vid':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype FROM recent WHERE vid like ?;",
                              (str(var[0]),))
    if args == 'Search_callsign':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype FROM recent WHERE callsign like ?;",
                              (str(var[0]),))
    if args == 'Search_realname':
        Q_db = cursor.execute("SELECT vid, callsign, realname, rating, clienttype FROM recent WHERE realname like ?;",
                              (str(var[0]),))
    if args == 'Get_Controller_data':
        Q_db = cursor.execute("SELECT vid, realname, server, clienttype, frequency, rating, facilitytype, atis_message, \
                               time_connected, client_software_name, client_software_version FROM recent \
                               WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Pilot_data':
        Q_db = cursor.execute("SELECT vid, realname, altitude, groundspeed, planned_aircraft, planned_depairport, \
                            planned_destairport, planned_altitude, planned_pob, planned_route, rating, transponder, onground,\
                            latitude, longitude, planned_altairport, planned_altairport2, planned_tascruise, time_connected, clienttype \
                            FROM recent WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Airport_from_ICAO':
        Q_db = cursor.execute("SELECT city FROM airports WHERE icao=?", (str(var[0]),))
    if args == 'Get_FIR_from_ICAO':
        Q_db = cursor.execute("SELECT city FROM firs WHERE fir=?", (str(var[0]),))
    if args == 'Get_Country_from_Prefix':
        Q_db = cursor.execute('SELECT countries.country FROM countries JOIN cprefix ON cprefix.id_country = countries.id_country WHERE cprefix.icao_initial=?', (str(var[0]),))
    if args == 'Get_Airport_Location':
        Q_db = cursor.execute("SELECT city, latitude, longitude FROM airports WHERE icao=?", (str(var[0]),))
    if args == 'Get_Model':
        Q_db = cursor.execute("SELECT model, fabricant, code FROM aircraft WHERE icao=?;", ((var[0]),))
    if args == 'Get_FMC_data':
        Q_db = cursor.execute("SELECT vid, realname, server, clienttype, rating, time_connected, client_software_name, \
                               client_software_version FROM recent WHERE callsign=?;", (str(var[0]),))
    if args == 'Get_Location_from_ICAO':
        Q_db = cursor.execute("SELECT longitude, latitude FROM airports WHERE icao=?;", (str(var[0]),))
    if args == 'Get_Player_Location':
        Q_db = cursor.execute("SELECT latitude, longitude, callsign, true_heading, clienttype \
                               FROM recent WHERE callsign=?;",  (str(var[0]),))
    if args == 'Get_Players_Locations':
        Q_db = cursor.execute("SELECT longitude, latitude, callsign, true_heading, clienttype FROM recent;")
    if args == 'Get_borders_FIR':
        Q_db = cursor.execute("SELECT longitude, latitude FROM fir where fir=?;", (str(var[0]),))
    if args == 'Clear_Scheduling_tables':
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM schedule_controllers;")
        cursor.execute("DELETE FROM schedule_pilots;")
        connection.commit()
        return
    if args == 'Add_Schedule_ATC':
        Q_db = cursor.execute("INSERT INTO schedule_controllers (Name, Position, StartDateUTC, EndDateUTC, Voice, Training, Event) \
                               VALUES (?,?,?,?,?,?,?);", (var[1], str(var[3]), str(var[4]), str(var[5]),
                                str(var[6]), str(var[7]), str(var[8]),))
        connection.commit()
        return
    if args == 'Add_Schedule_Flights':
        Q_db = cursor.execute("INSERT INTO schedule_pilots (Callsign, Name, Airplane, Departure, DepTime, Destination, DestTime, \
                               Altitude, CruisingSpeed, Route, Voice, Training, Event) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);",
                                (str(var[4]), var[1], str(var[5]), str(var[6]), str(var[7]), str(var[8]),
                                 str(var[9]), int(var[10]), int(var[11]), str(var[12]), str(var[13]), str(var[14]), str(var[15]),))
        connection.commit()
        return
    return Q_db

def update_db(pilots, controllers, vehicles):
    """This function insert the data got it in memory downloaded from IVAO to parse the players for controllers,
       pilots, and FMC to insert into database, separate by field ':' as NOTAM and Logistic explain what field means"""
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("DELETE FROM recent;")

    for rows in pilots:
        fields = rows.split(":")
        callsign = fields[0]
        vid = fields[1]
        realname = rows.rsplit(":")[2].decode('latin-1')
        clienttype = fields[3]
        latitude = fields[5]
        longitude = fields[6]
        altitude = fields[7]
        groundspeed = fields[8]
        planned_aircraft = fields[9].decode('latin-1')
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
        cursor.execute("INSERT INTO recent (callsign, vid, realname, clienttype \
        , latitude, longitude, altitude, groundspeed, planned_aircraft, planned_tascruise \
        , planned_depairport, planned_altitude, planned_destairport, server, protrevision \
        , rating, transponder, visualrange, planned_revision, planned_flighttype \
        , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel \
        , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat \
        , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon \
        , time_last_atis_received, time_connected, client_software_name, client_software_version \
        , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading \
        , onground) \
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
        (callsign, vid, realname, clienttype, latitude, longitude, altitude, groundspeed, planned_aircraft
         , planned_tascruise, planned_depairport, planned_altitude, planned_destairport, server, protrevision
         , rating, transponder, visualrange, planned_revision, planned_flighttype
         , planned_deptime, planned_actdeptime, planned_hrsenroute, planned_minenroute, planned_hrsfuel
         , planned_minfuel, planned_altairport, planned_remarks, planned_route, planned_depairport_lat
         , planned_depairport_lon, planned_destairport_lat, planned_destairport_lon
         , time_last_atis_received, time_connected, client_software_name, client_software_version
         , adminrating, atc_or_pilotrating, planned_altairport2, planned_typeofflight, planned_pob, true_heading
         , onground))
    connection.commit()

    for rows in controllers:
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
        atc_or_pilotrating = fields[41]

        cursor.execute("INSERT INTO recent (callsign, vid, realname, clienttype, frequency \
        , latitude, longitude, altitude, server, protrevision, rating, facilitytype, visualrange \
        , time_last_atis_received, time_connected, client_software_name, client_software_version \
        , adminrating, atc_or_pilotrating, atis_message) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",
        (callsign, vid, realname, clienttype, frequency, latitude, longitude, altitude, server
         , protrevision, rating, facilitytype, visualrange, time_last_atis_received, time_connected
         , client_software_name, client_software_version, adminrating, atc_or_pilotrating, atis_message))
    connection.commit()

    for row in vehicles:
        fields = rows.split(":")
        callsign = fields[0]
        vid = fields[1]
        realname = rows.rsplit(":")[2].decode('latin-1')
        clienttype = fields[3]
        server = fields[14]
        time_connected = fields[37]

        cursor.execute("INSERT INTO recent (callsign, vid, realname, clienttype, server, time_connected) VALUES (?,?,?,?,?,?);",
                   (callsign, vid, realname, clienttype, server, time_connected))
    connection.commit()
    return