#!/bin/python
# pygtk-IVAO-status
# Author: Tony P. Diaz
# Date Jul 2011
# License GPLv3+

import urllib2

ivao_status = 'whazzup.txt'
    
StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/'+ivao_status)
StatusFile = open(ivao_status, 'w')
StatusFile.write(StatusURL.read())
StatusFile.close()

StatusFile = open(ivao_status)
list_users = []

print
print "Nombre y Apellidos    |    DEP-ICAO    |    ARR-ICAO    |    FL    |    VA-CODEFLIGHT"
print "----------------------+----------------+----------------+----------+-----------------"

for i in range(8, 10):
    list_users.append(StatusFile.readlines())
    parser = list_users[0][i].split(':')
    print parser[2]+'\t'*2+parser[11]+'\t'*2+parser[13]+'\t'*2+parser[12]+'\t'*2+parser[10]

StatusFile.close()
