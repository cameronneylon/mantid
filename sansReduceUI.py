# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sans-reduce-gui.ui'
#
# Created: Fri Jul  2 10:47:43 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 399)
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 50, 451, 201))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sansRunLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.sansRunLabel.setObjectName("sansRunLabel")
        self.gridLayout.addWidget(self.sansRunLabel, 2, 0, 1, 1)
        self.transLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.transLabel.setObjectName("transLabel")
        self.gridLayout.addWidget(self.transLabel, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.sampleLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.sampleLabel.setObjectName("sampleLabel")
        self.gridLayout.addWidget(self.sampleLabel, 0, 1, 1, 1)
        self.sansRunMenu = QtGui.QComboBox(self.gridLayoutWidget)
        self.sansRunMenu.setObjectName("sansRunMenu")
        self.gridLayout.addWidget(self.sansRunMenu, 2, 1, 1, 1)
        self.sansTransMenu = QtGui.QComboBox(self.gridLayoutWidget)
        self.sansTransMenu.setObjectName("sansTransMenu")
        self.gridLayout.addWidget(self.sansTransMenu, 3, 1, 1, 1)
        self.bgdLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.bgdLabel.setObjectName("bgdLabel")
        self.gridLayout.addWidget(self.bgdLabel, 0, 2, 1, 1)
        self.bgdRunMenu = QtGui.QComboBox(self.gridLayoutWidget)
        self.bgdRunMenu.setObjectName("bgdRunMenu")
        self.gridLayout.addWidget(self.bgdRunMenu, 2, 2, 1, 1)
        self.bgdTransMenu = QtGui.QComboBox(self.gridLayoutWidget)
        self.bgdTransMenu.setObjectName("bgdTransMenu")
        self.gridLayout.addWidget(self.bgdTransMenu, 3, 2, 1, 1)
        self.gridLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(70, 130, 301, 62))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.showRawCheckBox = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.showRawCheckBox.setChecked(True)
        self.showRawCheckBox.setObjectName("showRawCheckBox")
        self.gridLayout_2.addWidget(self.showRawCheckBox, 0, 0, 1, 1)
        self.showNexusCheckBox = QtGui.QCheckBox(self.gridLayoutWidget_2)
        self.showNexusCheckBox.setObjectName("showNexusCheckBox")
        self.gridLayout_2.addWidget(self.showNexusCheckBox, 1, 0, 1, 1)
        self.maskFilePushButton = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.maskFilePushButton.setObjectName("maskFilePushButton")
        self.gridLayout_2.addWidget(self.maskFilePushButton, 0, 1, 1, 1)
        self.directBeamRunMenu = QtGui.QComboBox(self.gridLayoutWidget_2)
        self.directBeamRunMenu.setObjectName("directBeamRunMenu")
        self.directBeamRunMenu.addItem("")
        self.gridLayout_2.addWidget(self.directBeamRunMenu, 1, 1, 1, 1)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 431, 34))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inPathPushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.inPathPushButton.setObjectName("inPathPushButton")
        self.horizontalLayout.addWidget(self.inPathPushButton)
        self.inPathLineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.inPathLineEdit.setObjectName("inPathLineEdit")
        self.horizontalLayout.addWidget(self.inPathLineEdit)
        self.reducePushButton = QtGui.QPushButton(Form)
        self.reducePushButton.setGeometry(QtCore.QRect(330, 350, 141, 32))
        self.reducePushButton.setObjectName("reducePushButton")
        self.queueReductionsCheckBox = QtGui.QCheckBox(Form)
        self.queueReductionsCheckBox.setGeometry(QtCore.QRect(330, 330, 141, 21))
        self.queueReductionsCheckBox.setObjectName("queueReductionsCheckBox")
        self.gridLayoutWidget_3 = QtGui.QWidget(Form)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 260, 425, 61))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.outputLOQCheckbox = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.outputLOQCheckbox.setObjectName("outputLOQCheckbox")
        self.gridLayout_3.addWidget(self.outputLOQCheckbox, 0, 0, 1, 1)
        self.outputCansSASCheckbox = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.outputCansSASCheckbox.setChecked(True)
        self.outputCansSASCheckbox.setObjectName("outputCansSASCheckbox")
        self.gridLayout_3.addWidget(self.outputCansSASCheckbox, 1, 0, 1, 1)
        self.useRunnumberCheckbox = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.useRunnumberCheckbox.setObjectName("useRunnumberCheckbox")
        self.gridLayout_3.addWidget(self.useRunnumberCheckbox, 0, 1, 1, 1)
        self.blogReductionCheckbox = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.blogReductionCheckbox.setObjectName("blogReductionCheckbox")
        self.gridLayout_3.addWidget(self.blogReductionCheckbox, 1, 1, 1, 1)
        self.outPathPushButton = QtGui.QPushButton(self.gridLayoutWidget_3)
        self.outPathPushButton.setObjectName("outPathPushButton")
        self.gridLayout_3.addWidget(self.outPathPushButton, 1, 2, 1, 1)
        self.cancelPushButton = QtGui.QPushButton(Form)
        self.cancelPushButton.setGeometry(QtCore.QRect(200, 350, 115, 32))
        self.cancelPushButton.setObjectName("cancelPushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.sansRunLabel.setText(QtGui.QApplication.translate("Form", "SANS Run", None, QtGui.QApplication.UnicodeUTF8))
        self.transLabel.setText(QtGui.QApplication.translate("Form", "Transmission", None, QtGui.QApplication.UnicodeUTF8))
        self.sampleLabel.setText(QtGui.QApplication.translate("Form", "Sample Run", None, QtGui.QApplication.UnicodeUTF8))
        self.bgdLabel.setText(QtGui.QApplication.translate("Form", "Background", None, QtGui.QApplication.UnicodeUTF8))
        self.showRawCheckBox.setText(QtGui.QApplication.translate("Form", "Show RAW", None, QtGui.QApplication.UnicodeUTF8))
        self.showNexusCheckBox.setText(QtGui.QApplication.translate("Form", "Show Nexus", None, QtGui.QApplication.UnicodeUTF8))
        self.maskFilePushButton.setText(QtGui.QApplication.translate("Form", "Mask file...", None, QtGui.QApplication.UnicodeUTF8))
        self.directBeamRunMenu.setItemText(0, QtGui.QApplication.translate("Form", "Direct Beam Run", None, QtGui.QApplication.UnicodeUTF8))
        self.inPathPushButton.setText(QtGui.QApplication.translate("Form", "File Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.reducePushButton.setText(QtGui.QApplication.translate("Form", "Reduce", None, QtGui.QApplication.UnicodeUTF8))
        self.queueReductionsCheckBox.setText(QtGui.QApplication.translate("Form", "Queue reductions", None, QtGui.QApplication.UnicodeUTF8))
        self.outputLOQCheckbox.setText(QtGui.QApplication.translate("Form", "Output LOQ format", None, QtGui.QApplication.UnicodeUTF8))
        self.outputCansSASCheckbox.setText(QtGui.QApplication.translate("Form", "Output CanSAS 1D", None, QtGui.QApplication.UnicodeUTF8))
        self.useRunnumberCheckbox.setText(QtGui.QApplication.translate("Form", "Use sample run number", None, QtGui.QApplication.UnicodeUTF8))
        self.blogReductionCheckbox.setText(QtGui.QApplication.translate("Form", "Blog reduction...", None, QtGui.QApplication.UnicodeUTF8))
        self.outPathPushButton.setText(QtGui.QApplication.translate("Form", "Save to...", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelPushButton.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

