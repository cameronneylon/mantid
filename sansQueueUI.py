# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sans-reduce-queue.ui'
#
# Created: Sun Jul  4 17:31:23 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_queuedReductionsUI(object):
    def setupUi(self, queuedReductionsUI):
        queuedReductionsUI.setObjectName("queuedReductionsUI")
        queuedReductionsUI.setEnabled(True)
        queuedReductionsUI.resize(600, 400)
        self.reduceQueuePushButton = QtGui.QPushButton(queuedReductionsUI)
        self.reduceQueuePushButton.setGeometry(QtCore.QRect(470, 360, 115, 32))
        self.reduceQueuePushButton.setObjectName("reduceQueuePushButton")
        self.cancelQueuePushButton = QtGui.QPushButton(queuedReductionsUI)
        self.cancelQueuePushButton.setGeometry(QtCore.QRect(360, 360, 115, 32))
        self.cancelQueuePushButton.setObjectName("cancelQueuePushButton")
        self.reductionQueueTableView = QtGui.QTableView(queuedReductionsUI)
        self.reductionQueueTableView.setGeometry(QtCore.QRect(20, 10, 561, 251))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.reductionQueueTableView.setFont(font)
        self.reductionQueueTableView.setObjectName("reductionQueueTableView")
        self.gridLayoutWidget = QtGui.QWidget(queuedReductionsUI)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 270, 561, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.maskFilePushButtonQueue = QtGui.QPushButton(self.gridLayoutWidget)
        self.maskFilePushButtonQueue.setObjectName("maskFilePushButtonQueue")
        self.gridLayout.addWidget(self.maskFilePushButtonQueue, 0, 0, 1, 1)
        self.directBeamPushButtonQueue = QtGui.QPushButton(self.gridLayoutWidget)
        self.directBeamPushButtonQueue.setObjectName("directBeamPushButtonQueue")
        self.gridLayout.addWidget(self.directBeamPushButtonQueue, 1, 0, 1, 1)
        self.maskFileLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.maskFileLineEdit.setObjectName("maskFileLineEdit")
        self.gridLayout.addWidget(self.maskFileLineEdit, 0, 2, 1, 1)
        self.directBeamLineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.directBeamLineEdit.setObjectName("directBeamLineEdit")
        self.gridLayout.addWidget(self.directBeamLineEdit, 1, 2, 1, 1)

        self.retranslateUi(queuedReductionsUI)
        QtCore.QMetaObject.connectSlotsByName(queuedReductionsUI)

    def retranslateUi(self, queuedReductionsUI):
        queuedReductionsUI.setWindowTitle(QtGui.QApplication.translate("queuedReductionsUI", "Queued Reductions", None, QtGui.QApplication.UnicodeUTF8))
        self.reduceQueuePushButton.setText(QtGui.QApplication.translate("queuedReductionsUI", "Reduce all", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelQueuePushButton.setText(QtGui.QApplication.translate("queuedReductionsUI", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.maskFilePushButtonQueue.setText(QtGui.QApplication.translate("queuedReductionsUI", "Mask file...", None, QtGui.QApplication.UnicodeUTF8))
        self.directBeamPushButtonQueue.setText(QtGui.QApplication.translate("queuedReductionsUI", "Direct beam...", None, QtGui.QApplication.UnicodeUTF8))

