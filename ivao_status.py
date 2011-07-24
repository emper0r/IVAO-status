#!/bin/python -W
# IVAO-status
# Author: Antonio P. Diaz <emperor.cu@gmail.com>
# Date Jul 2011
# License GPLv3+
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import MainWindow_UI
import urllib2

class Main(QtGui.QMainWindow):
    def __init__(self):
        
        QtGui.QMainWindow.__init__(self)
       
        self.ui = MainWindow_UI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

#        self.connect(self.ui.pushButton_quit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        
#        ivao_status = 'whazzup.txt'
#           
#        StatusURL = urllib2.urlopen('http://de3.www.ivao.aero/' + ivao_status)
#        StatusFile = open(ivao_status, 'w')
#        StatusFile.write(StatusURL.read())
#        StatusFile.close()
#        
#        StatusFile = open(ivao_status)
#        total_lines = StatusFile.read().split('\n')
#        print len(total_lines)
#        StatusFile.close()
#        
#        StatusFile = open(ivao_status)
#        list_users = []
#        for i in range(8, (len(total_lines) - 13)):
#            list_users.append(StatusFile.readlines())
#           
#            parser_colons = list_users[0][i].split(':')
#            parser_slash = list_users[0][i].split('/')
#            
#            print "Callsign: " + parser_colons[10]
#            
#            try:
#                print "Aircraft: " + parser_slash[1]
#            except:
#                print "Aircraft: -"
#                
#            print "Name: " + str(parser_colons[2].rsplit(" ", 1)[0])
#            print "Conected from: " + str(parser_colons[2].rsplit(" ", 1)[1])
#            print "Departure: " + parser_colons[11]
#            print "Arrive: " + parser_colons[13]
#            print "Flight Level: " + parser_colons[12]
#            print
#        
#        StatusFile.close()

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
