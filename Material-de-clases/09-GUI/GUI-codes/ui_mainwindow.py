# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt-designer-mainwindow.ui'
#
# Created: Mon May 11 15:47:12 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(462, 314)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton1 = QtGui.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(120, 120, 75, 23))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 60, 53, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit1 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(120, 60, 133, 20))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.lineEdit2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit2.setGeometry(QtCore.QRect(121, 90, 133, 20))
        self.lineEdit2.setObjectName(_fromUtf8("lineEdit2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 63, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 80, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 462, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_Archivo = QtGui.QMenu(self.menubar)
        self.menu_Archivo.setObjectName(_fromUtf8("menu_Archivo"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Ejecutar = QtGui.QAction(MainWindow)
        self.action_Ejecutar.setObjectName(_fromUtf8("action_Ejecutar"))
        self.action_Salir = QtGui.QAction(MainWindow)
        self.action_Salir.setObjectName(_fromUtf8("action_Salir"))
        self.menu_Archivo.addAction(self.action_Ejecutar)
        self.menu_Archivo.addAction(self.action_Salir)
        self.menubar.addAction(self.menu_Archivo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton1.setText(_translate("MainWindow", "Dividir", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>Numerador</p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "Denominador", None))
        self.label_3.setText(_translate("MainWindow", "=", None))
        self.menu_Archivo.setTitle(_translate("MainWindow", "&Archivo", None))
        self.action_Ejecutar.setText(_translate("MainWindow", "&Ejecutar", None))
        self.action_Salir.setText(_translate("MainWindow", "&Salir", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

