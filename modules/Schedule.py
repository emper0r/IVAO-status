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
#
# Schedule Function

import os
import SQL_queries
import ConfigParser
import urllib2
from BeautifulSoup import BeautifulSoup

def Scheduling():
    '''This part is very slowly yet, because i can't access directly to IVAO db to download schedule, 
       so I have to parse the URLs where users can see the schedule for controllers and pilots on IVAO website,
       now is made using BeautifulSoup, but I guess with other tool to parse like lxml, can check if 
       is more faster or not'''
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    SQL_queries.sql_query('Clear_Scheduling_tables')
    SchedATC_URL = urllib2.urlopen(config.get('Info', 'scheduling_atc'))
    soup_atc = BeautifulSoup(SchedATC_URL)
    SchedFlights_URL = urllib2.urlopen(config.get('Info', 'scheduling_flights'))
    soup_flights = BeautifulSoup(SchedFlights_URL)
    
    table_atc = soup_atc.find("table")
    atc_rows = table_atc.findAll('tr')
    table_flights = soup_flights.find("table")
    fligths_rows = table_flights.findAll('tr')
    
    for line_atc_table in atc_rows[1:]:
        columns = [col.find(text=True) for col in line_atc_table.findAll('td')]
        SQL_queries.sql_query('Add_Schedule_ATC', columns)

    for line_flights_table in fligths_rows[2:]:
        columns = [col.find(text=True) for col in line_flights_table.findAll('td')]
        SQL_queries.sql_query('Add_Schedule_Flights', columns)
    
    return
