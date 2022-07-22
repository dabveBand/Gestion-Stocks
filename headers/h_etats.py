# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_files\etats.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Etats(object):
    def setupUi(self, Etats):
        Etats.setObjectName("Etats")
        Etats.resize(400, 131)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(11)
        Etats.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Etats)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtWidgets.QLabel(Etats)
        self.labelTitle.setMinimumSize(QtCore.QSize(0, 70))
        self.labelTitle.setStyleSheet("background-color: rgb(124, 124, 124);")
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxDate = QtWidgets.QComboBox(Etats)
        self.comboBoxDate.setMinimumSize(QtCore.QSize(0, 35))
        self.comboBoxDate.setObjectName("comboBoxDate")
        self.horizontalLayout.addWidget(self.comboBoxDate)
        self.pushButtonSaveEtats = QtWidgets.QPushButton(Etats)
        self.pushButtonSaveEtats.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButtonSaveEtats.setObjectName("pushButtonSaveEtats")
        self.horizontalLayout.addWidget(self.pushButtonSaveEtats)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Etats)
        QtCore.QMetaObject.connectSlotsByName(Etats)

    def retranslateUi(self, Etats):
        _translate = QtCore.QCoreApplication.translate
        Etats.setWindowTitle(_translate("Etats", "Etats"))
        self.labelTitle.setText(_translate("Etats", "Etats"))
        self.pushButtonSaveEtats.setText(_translate("Etats", "Enregistrer"))

