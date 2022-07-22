# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_files\result_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResultDialog(object):
    def setupUi(self, ResultDialog):
        ResultDialog.setObjectName("ResultDialog")
        ResultDialog.resize(539, 122)
        font = QtGui.QFont()
        font.setFamily("Monaco")
        font.setPointSize(12)
        ResultDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(ResultDialog)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelResult = QtWidgets.QLabel(ResultDialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelResult.setFont(font)
        self.labelResult.setText("")
        self.labelResult.setObjectName("labelResult")
        self.verticalLayout.addWidget(self.labelResult)
        self.buttonBox = QtWidgets.QDialogButtonBox(ResultDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ResultDialog)
        self.buttonBox.accepted.connect(ResultDialog.accept)
        self.buttonBox.rejected.connect(ResultDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ResultDialog)

    def retranslateUi(self, ResultDialog):
        _translate = QtCore.QCoreApplication.translate
        ResultDialog.setWindowTitle(_translate("ResultDialog", "Magasin"))

