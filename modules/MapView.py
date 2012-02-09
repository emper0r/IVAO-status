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

'''Importing Python's native modules'''
import os
import ConfigParser
import sqlite3

'''Importing the libraries from modules directory'''
from modules import SQL_queries

def GMapsLayer(vid, icao_orig, icao_dest):
    '''This function is for see the single player in GoogleMaps, if  is ATC, see with more or less zoom depends
       from ATC level and the PILOT, I implemented this before show up webeye, so i made the middle stuff,
       now with webeye, I want use it here, to make strong those 2 tools'''
    latitude, longitude, heading = vid[0][0], vid[0][1], vid[0][3]
    mapfileplayer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    player_location = open(mapfileplayer_path +'/player_location.html', 'w')
    player_location.write('<html><body>\n')
    player_location.write('  <div id="mapdiv"></div>\n')
    player_location.write('  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAjpkAC9ePGem0lIq5XcMiuhR_wWLPFku8Ix9i2SXYRVK3e45q1BQUd_beF8dtzKET_EteAjPdGDwqpQ"></script>\n')
    player_location.write('  <script src="%s/../OpenLayers/OpenLayers.js"></script>\n' % (mapfileplayer_path))
    player_location.write('  <script>\n')
    player_location.write('\n')
    player_location.write('    map = new OpenLayers.Map("mapdiv",\n')
    player_location.write('             {   projection : new OpenLayers.Projection("EPSG:900913"),\n')
    player_location.write('                 maxResolution:156543.0339,\n')
    player_location.write('                 maxExtent:new OpenLayers.Bounds(-20037508, -20037508,20037508, 20037508.34)\n')
    player_location.write('             });\n')
    player_location.write('\n')
    player_location.write('    ghyb = new OpenLayers.Layer.Google(\n')
    player_location.write('         "Google Satellite",\n')
    player_location.write('         {type: G_HYBRID_MAP, sphericalMercator:true, numZoomLevels: 22}\n')
    player_location.write('         );\n')
    player_location.write('\n')
    player_location.write('    map.addLayers([ghyb]);\n')
    player_location.write('\n')
    player_location.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % (longitude, latitude))
    player_location.write('         .transform(\n')
    player_location.write('            new OpenLayers.Projection("EPSG:4326"),\n')
    player_location.write('            map.getProjectionObject()\n')
    player_location.write('            );\n')
    if str(vid[0][2][4:]) == "_GND":
        player_location.write('    var zoom = 15;\n')
    if str(vid[0][2][4:]) == "_DEP":
        player_location.write('    var zoom = 15;\n')
    if str(vid[0][2][4:]) == "_TWR":
        player_location.write('    var zoom = 14;\n')
    if str(vid[0][2][4:]) == "_APP":
        player_location.write('    var zoom = 13;\n')
    if str(vid[0][2][4:]) == '_OBS':
        player_location.write('    var zoom = 12;\n')
    if str(vid[0][2][4:]) == '_CTR':
        player_location.write('    var zoom = 5;\n')
    if vid[0][4] == 'PILOT':
        player_location.write('    var zoom = 5;\n')
    else:
        player_location.write('    var zoom = 12;\n')
    player_location.write('    var player=new OpenLayers.Layer.Vector("Player",\n')
    player_location.write('    {\n')
    player_location.write('    styleMap: new OpenLayers.StyleMap({\n')
    player_location.write('         "default": {\n')
    if vid[0][4] == 'PILOT':
        player_location.write('         externalGraphic: "../images/airplane.gif",\n')
    else:
        player_location.write('         externalGraphic: "../images/tower.png",\n')
    player_location.write('         graphicWidth: 20,\n')
    player_location.write('         graphicHeight: 20,\n')
    player_location.write('         graphicYOffset: 0,\n')
    player_location.write('         rotation: "${angle}",\n')
    if vid[0][4] == 'ATC':
        player_location.write('         fillColor: "white",\n')
        player_location.write('         strokeColor: "white",\n')
        player_location.write('         fillOpacity: "0.05",\n')
    else:
        player_location.write('         fillOpacity: "${opacity}",\n')
    player_location.write('         label: "%s",\n' % str(vid[0][2]))
    player_location.write('         fontColor: "white",\n')
    player_location.write('         fontSize: "10px",\n')
    player_location.write('         fontFamily: "Courier New, monospace",\n')
    player_location.write('         labelAlign: "cm",\n')
    player_location.write('         labelXOffset: 30,\n')
    player_location.write('         labelYOffset: 5\n')
    if str(vid[0][2][-4:]) == '_CTR':
        player_location.write('         }\n')
        player_location.write('      })\n')
        player_location.write('   });\n\n')
        player_location.write('   var vectorLayer = new OpenLayers.Layer.Vector("Vector Layer");\n')
        player_location.write('   var style_controller = {\n')
        player_location.write('       strokeColor: "white",\n')
        player_location.write('       strokeOpacity: 1.0,\n')
        player_location.write('       strokeWidth: 2,\n')
        player_location.write('       label: "%s",\n' % str(vid[0][2]))
        player_location.write('       fontWeight: "bold",\n')
        player_location.write('       fontColor: "white",\n')
        player_location.write('       fontSize: "12px",\n')
        player_location.write('       fontFamily: "Courier New, monospace",\n')
        player_location.write('       labelAlign: "cm",\n')
        player_location.write('       labelXOffset: 30,\n')
        player_location.write('       labelYOffset: 5\n')
        player_location.write('   };\n\n')
        Q_db = SQL_queries.sql_query('Get_borders_FIR', (str(vid[0][2][:4]),))
        points_ctr = Q_db.fetchall()
        player_location.write('    var points = [];\n')
        for position in range(0, len(points_ctr)):
            player_location.write('    var point_orig = new OpenLayers.Geometry.Point(%f, %f);\n'
                                  % (points_ctr[position][0], points_ctr[position][1]))
            if position == len(points_ctr) - 1:
                continue
            else:
                player_location.write('    var point_dest = new OpenLayers.Geometry.Point(%f, %f);\n'
                                      % (points_ctr[position+1][0], points_ctr[position+1][1]))
                player_location.write('    points.push(point_orig);\n')
                player_location.write('    points.push(point_dest);\n')
        player_location.write('\n')
        player_location.write('    var player_String = new OpenLayers.Geometry.LineString(points);\n')
        player_location.write('    player_String.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());\n')
        player_location.write('    var DrawFeature = new OpenLayers.Feature.Vector(player_String, null, style_controller);\n')
        player_location.write('    vectorLayer.addFeatures([DrawFeature]);\n')
        player_location.write('    map.addLayer(vectorLayer);\n')
        player_location.write('    map.addLayer(player);\n')
    else:
        player_location.write('         }\n')
        player_location.write('      })\n')
        player_location.write('   });\n')
        if str(vid[0][4]) == 'ATC':
            player_location.write('   var ratio = OpenLayers.Geometry.Polygon.createRegularPolygon(\n')
            player_location.write('     new OpenLayers.Geometry.Point(position.lon, position.lat),\n')
            if str(vid[0][2][-4:]) == '_OBS' or str(vid[0][2][-4:]) == '_DEP' or str(vid[0][2][-4:]) == '_GND':
                player_location.write('        20000,\n')
            elif str(vid[0][2][4:8]) == '_OBS' or str(vid[0][2][-4:]) == '_DEP' or str(vid[0][2][-4:]) == '_GND':
                player_location.write('        20000,\n')
            elif str(vid[0][2][-4:]) == '_TWR':
                player_location.write('        40000,\n')
            elif str(vid[0][2][-4:]) == '_APP':
                player_location.write('        60000,\n')
            else:
                player_location.write('        20000,\n')
            player_location.write('        360\n')
            player_location.write('     );\n')
            player_location.write('   var controller_ratio = new OpenLayers.Feature.Vector(ratio);\n')
            player_location.write('   player.addFeatures([controller_ratio]);\n')
        player_location.write('\n')
        if str(vid[0][4]) == 'PILOT':
            player_location.write('    var vectorLayer = new OpenLayers.Layer.Vector("Vector Layer");\n')
            player_location.write('    var style_green = {\n')
            player_location.write('     strokeColor: "#00FF00",\n')
            player_location.write('     strokeOpacity: 0.7,\n')
            player_location.write('     strokeWidth: 2\n')
            player_location.write('    };\n')
            player_location.write('    var style_red = {\n')
            player_location.write('     strokeColor: "#FF0000",\n')
            player_location.write('     strokeOpacity: 0.7,\n')
            player_location.write('     strokeWidth: 2\n')
            player_location.write('    };\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var points = [];\n')
                player_location.write('    var point_plane = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('    points.push(point_plane);\n')
            else:
                player_location.write('    var points_green = [];\n')
                player_location.write('    var point_orig = new OpenLayers.Geometry.Point(%f, %f);\n' % (icao_orig[0], icao_orig[1]))
                player_location.write('    var point_orig_f = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('\n')
                player_location.write('    var points_red = [];\n')
                player_location.write('    var point_dest = new OpenLayers.Geometry.Point(%f, %f);\n' % (longitude, latitude))
                player_location.write('    var point_dest_f = new OpenLayers.Geometry.Point(%f, %f);\n' % (icao_dest[0], icao_dest[1]))
                player_location.write('\n')
                player_location.write('    points_green.push(point_orig);\n')
                player_location.write('    points_green.push(point_orig_f);\n')
                player_location.write('\n')
                player_location.write('    points_red.push(point_dest);\n')
                player_location.write('    points_red.push(point_dest_f);\n')
            player_location.write('\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var lineString = new OpenLayers.Geometry.LineString(points);\n')
                player_location.write('    lineString.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
            else:
                player_location.write('    var lineString_green = new OpenLayers.Geometry.LineString(points_green);\n')
                player_location.write('    lineString_green.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
                player_location.write('    var lineString_red = new OpenLayers.Geometry.LineString(points_red);\n')
                player_location.write('    lineString_red.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject()); \n')
            player_location.write('\n')
            if icao_orig is None or icao_dest is None:
                player_location.write('    var lineFeature = new OpenLayers.Feature.Vector(lineString, null, null);\n')
                player_location.write('    vectorLayer.addFeatures([lineFeature]);\n')
            else:
                player_location.write('    var lineFeature_green = new OpenLayers.Feature.Vector(lineString_green, null, style_green);\n')
                player_location.write('    var lineFeature_red = new OpenLayers.Feature.Vector(lineString_red, null, style_red);\n')
                player_location.write('    vectorLayer.addFeatures([lineFeature_green, lineFeature_red]);\n')
            player_location.write('\n')
            player_location.write('   map.addLayer(vectorLayer);\n')
            player_location.write('\n')
        player_location.write('   var feature=new OpenLayers.Feature.Vector(\n')
        if str(vid[0][4]) == 'PILOT':
            player_location.write('     new OpenLayers.Geometry.Point(position.lon, position.lat), {"angle": %d, opacity: 100});\n'
                                  % (heading))
        else:
            player_location.write('     new OpenLayers.Geometry.Point(position.lon, position.lat), {"angle": 0, opacity: 100});\n')
        player_location.write('   player.addFeatures([feature]);\n')
        player_location.write('   map.addLayer(player);\n')
        player_location.write('\n')
    player_location.write('   map.setCenter (position, zoom);\n')
    player_location.write('  </script>\n')
    player_location.write('</body></html>\n')
    player_location.close()
    return

def all2map():
    '''This function is for see the whole map, all player in GoogleMaps, I implemented this before show up webeye,
       now with webeye, I want to use it here, to make strong those 2 tools'''
    config = ConfigParser.RawConfigParser()
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Config.cfg')
    config.read(config_file)
    database = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../database', config.get('Database', 'db'))
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    label_Pilots = config.getint('Map', 'label_Pilots')
    label_ATCs = config.getint('Map', 'label_ATCs')
    Q_db = SQL_queries.sql_query('Get_Players_Locations')
    players = Q_db.fetchall()
    mapfileall_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    all_in_map = open(mapfileall_path + '/all_in_map.html', 'w')
    all_in_map.write('<html><body>\n')
    all_in_map.write('  <div id="mapdiv"></div>\n')
    all_in_map.write('  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAjpkAC9ePGem0lIq5XcMiuhR_wWLPFku8Ix9i2SXYRVK3e45q1BQUd_beF8dtzKET_EteAjPdGDwqpQ"></script>\n')
    all_in_map.write('  <script src="%s/../OpenLayers/OpenLayers.js"></script>\n' % (mapfileall_path))
    all_in_map.write('  <script>\n')
    all_in_map.write('\n')
    all_in_map.write('    map = new OpenLayers.Map("mapdiv",\n')
    all_in_map.write('             {   projection : new OpenLayers.Projection("EPSG:900913"),\n')
    all_in_map.write('                 maxResolution:156543.0339,\n')
    all_in_map.write('                 maxExtent:new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34)\n')
    all_in_map.write('             });\n')
    all_in_map.write('    ghyb = new OpenLayers.Layer.Google(\n')
    all_in_map.write('         "Google Satellite",\n')
    all_in_map.write('         {type: G_SATELLITE_MAP, sphericalMercator:true, numZoomLevels: 22}\n')
    all_in_map.write('         );\n')
    all_in_map.write('\n')
    all_in_map.write('    map.addLayers([ghyb]);\n')
    all_in_map.write('\n')
    for callsign in range(0, len(players)):
        if str(players[callsign][4]) == 'PILOT':
            if (str(players[callsign][0]) and str(players[callsign][1])) == '':
                pass
            elif players[callsign][2] is None or players[callsign][3] is None:
                pass
            else:
                all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % \
                                 (float(players[callsign][0]), float(players[callsign][1])))
                all_in_map.write('         .transform(\n')
                all_in_map.write('            new OpenLayers.Projection("EPSG:4326"),\n')
                all_in_map.write('            map.getProjectionObject()\n')
                all_in_map.write('            );\n')
                all_in_map.write('\n')
                all_in_map.write('    var player_%s=new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]))
                all_in_map.write('    {\n')
                all_in_map.write('      styleMap: new OpenLayers.StyleMap({\n')
                all_in_map.write('         "default": {\n')
                all_in_map.write('          externalGraphic: "../images/airplane.gif",\n')
                all_in_map.write('          graphicWidth: 15,\n')
                all_in_map.write('          graphicHeight: 15,\n')
                all_in_map.write('          graphicYOffset: 0,\n')
                all_in_map.write('          rotation: "${angle}",\n')
                all_in_map.write('          fillOpacity: 100,\n')
                if label_Pilots == 2:
                    all_in_map.write('          label: "%s",\n' % str(players[callsign][2]))
                    all_in_map.write('          fontColor: "yellow",\n')
                    all_in_map.write('          fontSize: "10px",\n')
                    all_in_map.write('          fontFamily: "Courier New, monospace",\n')
                    all_in_map.write('          labelAlign: "cm",\n')
                    all_in_map.write('          labelXOffset: 30,\n')
                    all_in_map.write('          labelYOffset: 5\n')
                all_in_map.write('         }\n')
                all_in_map.write('      })\n')
                all_in_map.write('   });\n')
                all_in_map.write('\n')
                all_in_map.write('    var feature = new OpenLayers.Feature.Vector(\n')
                all_in_map.write('      new OpenLayers.Geometry.Point( position.lon, position.lat), {"angle": %d});\n'
                                 % int(players[callsign][3]))
                all_in_map.write('    player_%s.addFeatures([feature]);\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
                all_in_map.write('\n')
        if str(players[callsign][4]) == 'ATC':
            if players[callsign][0] == '' or players[callsign][1] == '':
                continue
        if str(players[callsign][2][-4:]) == '_OBS' \
           or str(players[callsign][4][-4:]) == '_DEP' or str(players[callsign][2][-4:]) == '_GND' \
           or str(players[callsign][2][-4:]) == '_TWR' or str(players[callsign][2][-4:]) == '_APP':
            if players[callsign][0] is None:
                continue
            all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n' % \
                             (float(players[callsign][0]), float(players[callsign][1])))
            all_in_map.write('         .transform(\n')
            all_in_map.write('            new OpenLayers.Projection("EPSG:4326"),\n')
            all_in_map.write('            map.getProjectionObject()\n')
            all_in_map.write('            );\n')
            all_in_map.write('\n')
            all_in_map.write('    var player_%s = new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]).replace('-',''))
            all_in_map.write('    {\n')
            all_in_map.write('    styleMap: new OpenLayers.StyleMap({\n')
            all_in_map.write('         "default": {\n')
            all_in_map.write('         externalGraphic: "../images/tower.png",\n')
            all_in_map.write('         rotation: "${angle}",\n')
            all_in_map.write('         graphicWidth: 15,\n')
            all_in_map.write('         graphicHeight: 15,\n')
            all_in_map.write('         graphicYOffset: 0,\n')
            if str(players[callsign][2][-4:]) == '_OBS' or str(players[callsign][4][-4:]) == '_DEP' \
               or str(players[callsign][2][-4:]) == '_GND':
                all_in_map.write('         fillColor: "white",\n')
                all_in_map.write('         strokeColor: "white",\n')
            elif str(players[callsign][2][-4:]) == '_TWR':
                all_in_map.write('         fillColor: "white",\n')
                all_in_map.write('         strokeColor: "white",\n')
            elif str(players[callsign][2][-4:]) == '_APP':
                all_in_map.write('         fillColor: "white",\n')
                all_in_map.write('         strokeColor: "white",\n')
            all_in_map.write('         fillOpacity: "0.2",\n')
            if label_ATCs == 2:
                all_in_map.write('         label: "%s",\n' % str(players[callsign][2]))
                all_in_map.write('         fontColor: "white",\n')
                all_in_map.write('         fontSize: "10px",\n')
                all_in_map.write('         fontFamily: "Courier New, monospace",\n')
                all_in_map.write('         labelAlign: "cm",\n')
                all_in_map.write('         labelXOffset: 30,\n')
                all_in_map.write('         labelYOffset: 5\n')
            all_in_map.write('         }\n')
            all_in_map.write('       })\n')
            all_in_map.write('    });\n')
            all_in_map.write('\n')
            all_in_map.write('     var ratio = OpenLayers.Geometry.Polygon.createRegularPolygon(\n')
            all_in_map.write('        new OpenLayers.Geometry.Point(position.lon, position.lat),\n')
            if str(players[callsign][2][-4:]) == '_OBS' or str(players[callsign][4][-4:]) == '_DEP' \
               or str(players[callsign][2][-4:]) == '_GND':
                all_in_map.write('        20000,\n')
            elif str(players[callsign][2][-4:]) == '_TWR':
                all_in_map.write('        40000,\n')
            elif str(players[callsign][2][-4:]) == '_APP':
                all_in_map.write('        60000,\n')
            all_in_map.write('        360\n')
            all_in_map.write('    );\n')
            all_in_map.write('    var controller_ratio = new OpenLayers.Feature.Vector(ratio);\n')
            all_in_map.write('    player_%s.addFeatures([controller_ratio]);\n' % str(players[callsign][2]).replace('-',''))
            all_in_map.write('\n')
            all_in_map.write('    var feature = new OpenLayers.Feature.Vector(\n')
            all_in_map.write('        new OpenLayers.Geometry.Point( position.lon, position.lat), {"angle": 0, opacity: 100});\n')
            all_in_map.write('    player_%s.addFeatures([feature]);\n' % str(players[callsign][2]).replace('-',''))
            all_in_map.write('\n')
            all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
            all_in_map.write('\n')
        if str(players[callsign][2][-4:]) == '_CTR':
            try:
                Q_db = SQL_queries.sql_query('Get_borders_FIR', (str(players[callsign][2][:4]),))
                position = Q_db.fetchall()
                if position == []:
                    continue
            except:
                pass
            all_in_map.write('    var position = new OpenLayers.LonLat( %f, %f )\n'
                             % (float(position[0][0]), float(position[0][1])))
            all_in_map.write('    var player_%s = new OpenLayers.Layer.Vector("Player",\n' % str(players[callsign][2]).replace('-',''))
            all_in_map.write('    {\n')
            all_in_map.write('    styleMap: new OpenLayers.StyleMap({\n')
            all_in_map.write('         "default": {\n')
            all_in_map.write('         externalGraphic: "../images/tower.png",\n')
            all_in_map.write('         rotation: "${angle}",\n')
            all_in_map.write('         fillOpacity: "1.00",\n')
            all_in_map.write('         }\n')
            all_in_map.write('       })\n')
            all_in_map.write('    });\n')
            all_in_map.write('\n')
            all_in_map.write('    var vectorLayer = new OpenLayers.Layer.Vector("Vector Layer");\n')
            all_in_map.write('    var style_controller = {\n')
            all_in_map.write('        strokeColor: "white",\n')
            all_in_map.write('        strokeOpacity: 1.0,\n')
            all_in_map.write('        strokeWidth: 2,\n')
            if label_ATCs == 2:
                all_in_map.write('        label: "%s",\n' % str(players[callsign][2]))
                all_in_map.write('        fontColor: "white",\n')
                all_in_map.write('        fontSize: "12px",\n')
                all_in_map.write('        fontWeight: "bold",\n')
                all_in_map.write('        fontFamily: "Courier New, monospace",\n')
                all_in_map.write('        labelAlign: "cm",\n')
                all_in_map.write('        labelXOffset: 30,\n')
                all_in_map.write('        labelYOffset: 5\n')
            all_in_map.write('    };\n\n')
            try:
                cursor.execute("SELECT ID_FIRCOASTLINE FROM fir_data_list WHERE ICAO = ?;", (str(players[callsign][2][:-4]),))
                id_ctr = cursor.fetchone()
                if id_ctr is None:
                    cursor.execute("SELECT ID_FIRCOASTLINE FROM fir_data_list WHERE ICAO = ?;", (str(players[callsign][2][:4]),))
                    id_ctr = cursor.fetchone()
            except:
                pass
            Q_db = SQL_queries.sql_query('Get_borders_FIR', (str(players[callsign][2][:4]),))
            points_ctr = Q_db.fetchall()
            all_in_map.write('    var points = [];\n')
            for position in range(0, len(points_ctr)):
                all_in_map.write('    var point_orig = new OpenLayers.Geometry.Point(%f, %f);\n'
                                 % (points_ctr[position][0], points_ctr[position][1]))
                if position == len(points_ctr) - 1:
                    continue
                else:
                    all_in_map.write('    var point_dest = new OpenLayers.Geometry.Point(%f, %f);\n'
                                     % (points_ctr[position+1][0], points_ctr[position+1][1]))
                all_in_map.write('    points.push(point_orig);\n')
                all_in_map.write('    points.push(point_dest);\n')
            all_in_map.write('\n')
            all_in_map.write('    var %s_String = new OpenLayers.Geometry.LineString(points);\n'
                             % str(players[callsign][2][:-4]))
            all_in_map.write('    %s_String.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());\n'
                             % str(players[callsign][2][:-4]))
            all_in_map.write('\n')
            all_in_map.write('    var DrawFeature = new OpenLayers.Feature.Vector(%s_String, null, style_controller);\n'
                             % str(players[callsign][2][:-4]))
            all_in_map.write('    vectorLayer.addFeatures([DrawFeature]);\n')
            all_in_map.write('    map.addLayer(vectorLayer);\n')
            all_in_map.write('    map.addLayer(player_%s);\n' % str(players[callsign][2]).replace('-',''))
    all_in_map.write('   map.setCenter ((0, 0), 2);\n')
    all_in_map.write('  </script>\n')
    all_in_map.write('</body></html>\n')
    all_in_map.close()
    return
