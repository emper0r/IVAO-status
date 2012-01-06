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
import etree
import StringIO
import calendar
import datetime

def Scheduling():
    '''This part is a parse HTML from Schedule website from IVAO, because i can't access 
       directly to IVAO database to download schedule, so I have to get by other way where users can 
       see the schedule for controllers and pilots'''
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    SQL_queries.sql_query('Clear_Scheduling_tables')
    parser = etree.HTMLParser()
    try:
        SchedATC_URL = urllib2.urlopen(config.get('Info', 'scheduling_atc')).read()
        tree = etree.parse(StringIO.StringIO(SchedATC_URL), parser)
        table_atc = tree.xpath("/html/body/div/center/table")[0]
    
        for line_atc_table in table_atc[1:]:
            if calendar.month_name[datetime.datetime.now().month] in line_atc_table[4][0].text: 
                columns = [td[0].text for td in line_atc_table]
                SQL_queries.sql_query('Add_Schedule_ATC', columns)
    except IOError:
            print('Error! when trying to download info from IVAO. Check your connection to Internet.')

    try:
        SchedFlights_URL = urllib2.urlopen(config.get('Info', 'scheduling_flights')).read()
        tree = etree.parse(StringIO.StringIO(SchedFlights_URL), parser)
        table_flights = tree.xpath("/html/body/div/div/center/table")[0]

        for line_flights_table in table_flights[2:]:
            if calendar.month_name[datetime.datetime.now().month] in line_flights_table[7][0].text:
                columns = [td[0].text for td in line_flights_table]
                SQL_queries.sql_query('Add_Schedule_Flights', columns)
    except IOError:
            print('Error! when trying to download info from IVAO. Check your connection to Internet.')
    return
