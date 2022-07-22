# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_files\log_in.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogIn(object):
    def setupUi(self, LogIn):
        LogIn.setObjectName("LogIn")
        LogIn.resize(399, 264)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        LogIn.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogIn)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(LogIn)
        self.label_3.setMinimumSize(QtCore.QSize(0, 110))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(LogIn)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEditUserName = QtWidgets.QLineEdit(LogIn)
        self.lineEditUserName.setObjectName("lineEditUserName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditUserName)
        self.label_2 = QtWidgets.QLabel(LogIn)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEditPwd = QtWidgets.QLineEdit(LogIn)
        self.lineEditPwd.setObjectName("lineEditPwd")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditPwd)
        self.pushButtonDissmiss = QtWidgets.QPushButton(LogIn)
        self.pushButtonDissmiss.setObjectName("pushButtonDissmiss")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.pushButtonDissmiss)
        self.pushButtonLogin = QtWidgets.QPushButton(LogIn)
        self.pushButtonLogin.setDefault(True)
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.pushButtonLogin)
        self.labelErrorMsg = QtWidgets.QLabel(LogIn)
        self.labelErrorMsg.setText("")
        self.labelErrorMsg.setObjectName("labelErrorMsg")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labelErrorMsg)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(LogIn)
        self.pushButtonDissmiss.clicked.connect(LogIn.close)
        QtCore.QMetaObject.connectSlotsByName(LogIn)

    def retranslateUi(self, LogIn):
        _translate = QtCore.QCoreApplication.translate
        LogIn.setWindowTitle(_translate("LogIn", "Log In"))
        self.label_3.setText(_translate("LogIn", "Log In"))
        self.label.setText(_translate("LogIn", "User Name"))
        self.label_2.setText(_translate("LogIn", "Password"))
        self.pushButtonDissmiss.setText(_translate("LogIn", "Annuler"))
        self.pushButtonLogin.setText(_translate("LogIn", "Log-in"))

