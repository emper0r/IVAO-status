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
# Setting Class

import os
import ConfigParser
from modules import SettingWindow_UI

try:
    '''Check if PyQt4 is installed or not, this library is a dependency of all,
    if not installed read the README.rst'''
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4.QtWebKit import *
    from PyQt4.Qt import *
except:
    print ('\nYou have not installed the packages Qt Modules for Python,\n')
    print ('please run command as root:  aptitude install python-qt4\n')
    print ('with all dependencies.\n\n')
    sys.exit(2)

class Settings(QMainWindow):
    '''The Settings Class is to set options like interval time to update, show labels of the players when see in the map,
       set proxy, this will write into Config.ini, this re-build the config if user delete it by error'''
    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = SettingWindow_UI.Ui_SettingWindow()
        self.ui.setupUi(self)
        self.parent = parent
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move ((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
        image_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'ivao_status_splash.png')
        self.setWindowIcon(QIcon(image_icon))
        self.connect(self.ui.SettingAccepButton, SIGNAL('clicked()'), self.options)
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.read(config_file)
        self.ui.spinBox.setValue(config.getint('Time_Update', 'time') / 60000)
        use_proxy = config.getint('Settings', 'use_proxy')
        if use_proxy == 2:
            self.ui.Setting_checkBox.setChecked(True)
        else:
            self.ui.Setting_checkBox.setChecked(False)
        host = config.get('Settings', 'host')
        self.ui.lineEdit_host.setText(host)
        port = config.get('Settings', 'port')
        self.ui.lineEdit_port.setText(port)
        auth = config.getint('Settings', 'auth')
        if auth == 2:
            self.ui.Setting_auth.setChecked(True)
        else:
            self.ui.Setting_auth.setChecked(False)
        user = config.get('Settings', 'user')
        self.ui.lineEdit_user.setText(user)
        pswd = config.get('Settings', 'pass')
        self.ui.lineEdit_pass.setText(pswd)
        map_refresh = config.getint('Map', 'auto_refresh')
        label_pilot = config.getint('Map', 'label_Pilots')
        label_atcs = config.getint('Map', 'label_ATCs')
        if map_refresh == 2:
            self.ui.AutoRefreshMap.setChecked(True)
        else:
            self.ui.AutoRefreshMap.setChecked(False)
        if label_pilot == 2:
            self.ui.ShowLabelPilots.setChecked(True)
        else:
            self.ui.ShowLabelPilots.setChecked(False)
        if label_atcs == 2:
            self.ui.ShowLabelControllers.setChecked(True)
        else:
            self.ui.ShowLabelControllers.setChecked(False)

    def options(self):
        minutes = self.ui.spinBox.value()
        time_update = minutes * 60000
        config = ConfigParser.RawConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Config.cfg')
        config.add_section('Settings')
        config.set('Settings', 'use_proxy', self.ui.Setting_checkBox.checkState())
        config.set('Settings', 'host', self.ui.lineEdit_host.text())
        config.set('Settings', 'port', self.ui.lineEdit_port.text())
        config.set('Settings', 'auth', self.ui.Setting_auth.checkState())
        config.set('Settings', 'user', self.ui.lineEdit_user.text())
        config.set('Settings', 'pass', self.ui.lineEdit_pass.text())
        config.add_section('Info')
        config.set('Info', 'data_access', 'http://www.ivao.aero/whazzup/status.txt')
        config.set('Info', 'scheduling_atc', 'http://www.ivao.aero/atcss/list.asp')
        config.set('Info', 'scheduling_flights', 'http://www.ivao.aero/flightss/list.asp')
        config.add_section('Database')
        config.set('Database', 'db', 'ivao.db')
        config.add_section('Time_Update')
        config.set('Time_Update', 'time', time_update)
        config.add_section('Map')
        if self.ui.AutoRefreshMap.checkState() == 2:
            config.set('Map', 'auto_refresh', '2')
        else:
            config.set('Map', 'auto_refresh', '0')
        if self.ui.ShowLabelPilots.checkState() == 2:
            config.set('Map', 'label_Pilots', '2')
        else:
            config.set('Map', 'label_Pilots', '0')
        if self.ui.ShowLabelControllers.checkState() == 2:
            config.set('Map', 'label_ATCs', '2')
        else:
            config.set('Map', 'label_ATCs', '0')
        with open (config_file, 'wb') as configfile:
            config.write(configfile)

        self.close()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
