# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtUI/SettingWindow_UI.ui'
#
# Created: Tue Sep  6 13:38:55 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        SettingWindow.setObjectName(_fromUtf8("SettingWindow"))
        SettingWindow.resize(320, 293)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingWindow.sizePolicy().hasHeightForWidth())
        SettingWindow.setSizePolicy(sizePolicy)
        SettingWindow.setCursor(QtCore.Qt.PointingHandCursor)
        SettingWindow.setAnimated(False)
        self.centralwidget = QtGui.QWidget(SettingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.SettingAccepButton = QtGui.QPushButton(self.centralwidget)
        self.SettingAccepButton.setGeometry(QtCore.QRect(108, 260, 99, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SettingAccepButton.setFont(font)
        self.SettingAccepButton.setObjectName(_fromUtf8("SettingAccepButton"))
        self.SettingTimeUpdate = QtGui.QLabel(self.centralwidget)
        self.SettingTimeUpdate.setGeometry(QtCore.QRect(14, 16, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.SettingTimeUpdate.setFont(font)
        self.SettingTimeUpdate.setObjectName(_fromUtf8("SettingTimeUpdate"))
        self.spinBox = QtGui.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(250, 13, 56, 22))
        self.spinBox.setCursor(QtCore.Qt.PointingHandCursor)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(60)
        self.spinBox.setSingleStep(5)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.Setting_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.Setting_checkBox.setGeometry(QtCore.QRect(14, 46, 85, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Setting_checkBox.setFont(font)
        self.Setting_checkBox.setCursor(QtCore.Qt.PointingHandCursor)
        self.Setting_checkBox.setChecked(False)
        self.Setting_checkBox.setTristate(False)
        self.Setting_checkBox.setObjectName(_fromUtf8("Setting_checkBox"))
        self.proxy_host = QtGui.QLabel(self.centralwidget)
        self.proxy_host.setEnabled(False)
        self.proxy_host.setGeometry(QtCore.QRect(20, 79, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.proxy_host.setFont(font)
        self.proxy_host.setObjectName(_fromUtf8("proxy_host"))
        self.proxy_port = QtGui.QLabel(self.centralwidget)
        self.proxy_port.setEnabled(False)
        self.proxy_port.setGeometry(QtCore.QRect(21, 103, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.proxy_port.setFont(font)
        self.proxy_port.setObjectName(_fromUtf8("proxy_port"))
        self.proxy_user = QtGui.QLabel(self.centralwidget)
        self.proxy_user.setEnabled(False)
        self.proxy_user.setGeometry(QtCore.QRect(15, 180, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.proxy_user.setFont(font)
        self.proxy_user.setObjectName(_fromUtf8("proxy_user"))
        self.proxy_pass = QtGui.QLabel(self.centralwidget)
        self.proxy_pass.setEnabled(False)
        self.proxy_pass.setGeometry(QtCore.QRect(15, 207, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.proxy_pass.setFont(font)
        self.proxy_pass.setObjectName(_fromUtf8("proxy_pass"))
        self.Setting_auth = QtGui.QCheckBox(self.centralwidget)
        self.Setting_auth.setEnabled(False)
        self.Setting_auth.setGeometry(QtCore.QRect(14, 150, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Setting_auth.setFont(font)
        self.Setting_auth.setCursor(QtCore.Qt.PointingHandCursor)
        self.Setting_auth.setChecked(False)
        self.Setting_auth.setTristate(False)
        self.Setting_auth.setObjectName(_fromUtf8("Setting_auth"))
        self.textEdit_host = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_host.setEnabled(False)
        self.textEdit_host.setGeometry(QtCore.QRect(60, 73, 151, 27))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit_host.setFont(font)
        self.textEdit_host.setObjectName(_fromUtf8("textEdit_host"))
        self.textEdit_port = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_port.setEnabled(False)
        self.textEdit_port.setGeometry(QtCore.QRect(60, 98, 151, 27))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit_port.setFont(font)
        self.textEdit_port.setObjectName(_fromUtf8("textEdit_port"))
        self.textEdit_user = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_user.setEnabled(False)
        self.textEdit_user.setGeometry(QtCore.QRect(80, 175, 151, 27))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit_user.setFont(font)
        self.textEdit_user.setObjectName(_fromUtf8("textEdit_user"))
        self.textEdit_pass = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_pass.setEnabled(False)
        self.textEdit_pass.setGeometry(QtCore.QRect(80, 200, 151, 27))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit_pass.setFont(font)
        self.textEdit_pass.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.textEdit_pass.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.textEdit_pass.setObjectName(_fromUtf8("textEdit_pass"))
        SettingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingWindow)

    def retranslateUi(self, SettingWindow):
        SettingWindow.setWindowTitle(QtGui.QApplication.translate("SettingWindow", "Settings of IVAO :: Status", None, QtGui.QApplication.UnicodeUTF8))
        self.SettingAccepButton.setText(QtGui.QApplication.translate("SettingWindow", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.SettingTimeUpdate.setText(QtGui.QApplication.translate("SettingWindow", "Setting Time for Update Info in minutes", None, QtGui.QApplication.UnicodeUTF8))
        self.Setting_checkBox.setText(QtGui.QApplication.translate("SettingWindow", "Use Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_host.setText(QtGui.QApplication.translate("SettingWindow", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_port.setText(QtGui.QApplication.translate("SettingWindow", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_user.setText(QtGui.QApplication.translate("SettingWindow", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_pass.setText(QtGui.QApplication.translate("SettingWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.Setting_auth.setText(QtGui.QApplication.translate("SettingWindow", "Authentication", None, QtGui.QApplication.UnicodeUTF8))

