#!/bin/python
# IVAO-status
# Author: Tony P. Diaz
# Date Jul 2011
# License GPLv3+
# -*- coding: ISO-8859-15 -*-

import urllib2

ivao_status = 'whazzup.txt'
    
StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + ivao_status)
StatusFile = open(ivao_status, 'w')
StatusFile.write(StatusURL.read())
StatusFile.close()

StatusFile = open(ivao_status)
total_lines = StatusFile.read().split('\n')
print len(total_lines)
StatusFile.close()

StatusFile = open(ivao_status)
list_users = []
for i in range(8, (len(total_lines) - 13)):
    list_users.append(StatusFile.readlines())
    
    parser_colons = list_users[0][i].split(':')
    parser_slash = list_users[0][i].split('/')
    
    print "Callsign: " + parser_colons[10]
    
    try:
        print "Aircraft: " + parser_slash[1]
    except:
        print "Aircraft: -"
        
    print "Name: " + str(parser_colons[2].rsplit(" ", 1)[0])
    print "Conected from: " + str(parser_colons[2].rsplit(" ", 1)[1])
    print "Departure: " + parser_colons[11]
    print "Arrive: " + parser_colons[13]
    print "Flight Level: " + parser_colons[12]
    print

StatusFile.close()