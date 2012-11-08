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

import SQL_queries
import distance

def status_flight(callsign):
    """This function is to get the action of the Pilot but for now I try to show using percent and
       some ground speeds of the track. I'm pretty sure with more check VARS can better this part"""
    Q_db = SQL_queries.sql_query('Get_Status', (str(callsign),))
    get_status = Q_db.fetchone()
    status = '-'
    for row_pilot in get_status:
        try:
            Q_db = SQL_queries.sql_query('Get_City', (str(get_status[2]),))
            city_orig = Q_db.fetchone()
            city_orig_point = float(city_orig[1]), float(city_orig[2])
            Q_db = SQL_queries.sql_query('Get_City', (str(get_status[3]),))
            city_dest = Q_db.fetchone()
            city_dest_point = float(city_dest[1]), float(city_dest[2])
            pilot_position = get_status[8], get_status[9]
            total_miles = distance.distance(city_orig_point, city_dest_point).miles
            dist_traveled = distance.distance(city_orig_point, pilot_position).miles
            percent = (float(dist_traveled) / float(total_miles)) * 100.0

            if percent > 105 :
                status = 'Diverted'
                return status
            else:
                if int(str(get_status[4])) == 0:
                    if (percent >= 0.0) and (percent <= 2.0):
                        status = 'Takeoff'
                    if (percent >= 2.0) and (percent <= 7.0):
                        status = 'Initial Climbing'
                    if (percent >= 7.0) and (percent <= 10.0):
                        status = 'Climbing'
                    if (percent >= 10.0) and (percent <= 80.0):
                        status = 'On Route'
                    if (percent >= 80.0) and (percent <= 90.0):
                        status = 'Descending'
                    if (percent >= 90.0) and (percent <= 97.0):
                        status = 'Initial Approach'
                    if (97.0 <= percent <= 105.0) and (360 >= get_status[6] >= 30):
                        status = 'Final Approach'
                    return status
                else:
                    if (0 < get_status[6] <= 30) and (percent < 1.0):
                        status = 'Departing'
                    if (get_status[6] > 30) and (get_status[6] < 150) and (percent < 1.0):
                        status = 'Takeoff'
                    if (97.0 <= percent <= 105.0) and (270 >= get_status[6] >= 30):
                        status = 'Landed'
                    if (get_status[6] < 30) and (percent > 99.0):
                        status = 'Taxing to Gate'
                    if (get_status[6] == 0) and (percent > 99.0):
                        status = 'On Blocks'
                    if (get_status[6] == 0) and (percent <= 1.0):
                        status = 'Boarding'
                    if (get_status[6] == 0) and (10.0 <= percent <= 90.0):
                        status = 'Altern Airport'
                    return status
        except:
            status = 'Fill Flight Plan'
            return status

def get_color(status_plane):
    """This function is implemented with status_plane"""
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