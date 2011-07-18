#!/bin/python
# pygtk-IVAO-status
# Author: Tony P. Diaz
# Date Jul 2012
# License GPLv3+

import urllib2
    
u = urllib2.urlopen('http://de3.www.ivao.aero/whazzup.txt')
localFile = open('whazzup.txt', 'w')
localFile.write(u.read())
localFile.close()