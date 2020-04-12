# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inter.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 538)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Qlist_usuarios = QtWidgets.QListWidget(self.centralwidget)
        self.Qlist_usuarios.setGeometry(QtCore.QRect(11, 97, 256, 381))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Qlist_usuarios.setFont(font)
        self.Qlist_usuarios.setObjectName("Qlist_usuarios")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 60, 71, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.boton_enviar_mensaje = QtWidgets.QPushButton(self.centralwidget)
        self.boton_enviar_mensaje.setGeometry(QtCore.QRect(710, 440, 80, 41))
        self.boton_enviar_mensaje.setObjectName("boton_enviar_mensaje")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(274, 11, 129, 37))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 60, 200, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.Qlist_chat = QtWidgets.QListWidget(self.centralwidget)
        self.Qlist_chat.setGeometry(QtCore.QRect(280, 100, 511, 331))
        self.Qlist_chat.setObjectName("Qlist_chat")
        self.boton_enviar_archivo = QtWidgets.QPushButton(self.centralwidget)
        self.boton_enviar_archivo.setGeometry(QtCore.QRect(610, 440, 92, 41))
        self.boton_enviar_archivo.setObjectName("boton_enviar_archivo")
        self.act_usuarios = QtWidgets.QPushButton(self.centralwidget)
        self.act_usuarios.setGeometry(QtCore.QRect(80, 480, 111, 21))
        self.act_usuarios.setObjectName("act_usuarios")
        self.Mensaje_a_enviar = QtWidgets.QLineEdit(self.centralwidget)
        self.Mensaje_a_enviar.setGeometry(QtCore.QRect(280, 440, 321, 41))
        self.Mensaje_a_enviar.setObjectName("Mensaje_a_enviar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "WhatsApp-Rangel"))
        self.label.setText(_translate("MainWindow", "Usuarios"))
        self.boton_enviar_mensaje.setText(_translate("MainWindow", "Enviar"))
        self.label_2.setText(_translate("MainWindow", "Whatsapp"))
        self.label_3.setText(_translate("MainWindow", "Chat"))
        self.boton_enviar_archivo.setText(_translate("MainWindow", "Archivos"))
        self.act_usuarios.setText(_translate("MainWindow", "Actualizar"))
