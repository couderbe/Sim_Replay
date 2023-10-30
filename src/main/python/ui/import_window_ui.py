# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableView, QVBoxLayout, QWidget)

class Ui_ImportWindow(object):
    def setupUi(self, ImportWindow):
        if not ImportWindow.objectName():
            ImportWindow.setObjectName(u"ImportWindow")
        ImportWindow.resize(1051, 616)
        self.verticalLayout_2 = QVBoxLayout(ImportWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.fileGroup = QGroupBox(ImportWindow)
        self.fileGroup.setObjectName(u"fileGroup")
        self.horizontalLayout_2 = QHBoxLayout(self.fileGroup)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fileLineEdit = QLineEdit(self.fileGroup)
        self.fileLineEdit.setObjectName(u"fileLineEdit")

        self.horizontalLayout_2.addWidget(self.fileLineEdit)

        self.filePushButton = QPushButton(self.fileGroup)
        self.filePushButton.setObjectName(u"filePushButton")

        self.horizontalLayout_2.addWidget(self.filePushButton)


        self.verticalLayout_2.addWidget(self.fileGroup)

        self.fileFormatGroup = QGroupBox(ImportWindow)
        self.fileFormatGroup.setObjectName(u"fileFormatGroup")
        self.horizontalLayout = QHBoxLayout(self.fileFormatGroup)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.GPXRadioButton = QRadioButton(self.fileFormatGroup)
        self.GPXRadioButton.setObjectName(u"GPXRadioButton")
        self.GPXRadioButton.setEnabled(True)
        self.GPXRadioButton.setCheckable(True)
        self.GPXRadioButton.setChecked(False)

        self.horizontalLayout.addWidget(self.GPXRadioButton)

        self.CSVRadioButton = QRadioButton(self.fileFormatGroup)
        self.CSVRadioButton.setObjectName(u"CSVRadioButton")

        self.horizontalLayout.addWidget(self.CSVRadioButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.encodingLabel = QLabel(self.fileFormatGroup)
        self.encodingLabel.setObjectName(u"encodingLabel")

        self.horizontalLayout.addWidget(self.encodingLabel)

        self.encodingComboBox = QComboBox(self.fileFormatGroup)
        self.encodingComboBox.setObjectName(u"encodingComboBox")
        self.encodingComboBox.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.encodingComboBox)


        self.verticalLayout_2.addWidget(self.fileFormatGroup)

        self.configurationGroup = QGroupBox(ImportWindow)
        self.configurationGroup.setObjectName(u"configurationGroup")
        self.verticalLayout_3 = QVBoxLayout(self.configurationGroup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.delimiterLayout = QHBoxLayout()
        self.delimiterLayout.setObjectName(u"delimiterLayout")
        self.delimiterLabel = QLabel(self.configurationGroup)
        self.delimiterLabel.setObjectName(u"delimiterLabel")

        self.delimiterLayout.addWidget(self.delimiterLabel)

        self.semiclonRadioButton = QRadioButton(self.configurationGroup)
        self.semiclonRadioButton.setObjectName(u"semiclonRadioButton")

        self.delimiterLayout.addWidget(self.semiclonRadioButton)

        self.commaRadioButton = QRadioButton(self.configurationGroup)
        self.commaRadioButton.setObjectName(u"commaRadioButton")
        self.commaRadioButton.setChecked(True)

        self.delimiterLayout.addWidget(self.commaRadioButton)

        self.spaceRadioButton = QRadioButton(self.configurationGroup)
        self.spaceRadioButton.setObjectName(u"spaceRadioButton")

        self.delimiterLayout.addWidget(self.spaceRadioButton)

        self.tabulationRadioButton = QRadioButton(self.configurationGroup)
        self.tabulationRadioButton.setObjectName(u"tabulationRadioButton")

        self.delimiterLayout.addWidget(self.tabulationRadioButton)


        self.verticalLayout_3.addLayout(self.delimiterLayout)

        self.otherFieldConfigurationLayout = QHBoxLayout()
        self.otherFieldConfigurationLayout.setObjectName(u"otherFieldConfigurationLayout")
        self.ligneIgnoreLabel = QLabel(self.configurationGroup)
        self.ligneIgnoreLabel.setObjectName(u"ligneIgnoreLabel")

        self.otherFieldConfigurationLayout.addWidget(self.ligneIgnoreLabel)

        self.ligneIgnoreSpinBox = QSpinBox(self.configurationGroup)
        self.ligneIgnoreSpinBox.setObjectName(u"ligneIgnoreSpinBox")

        self.otherFieldConfigurationLayout.addWidget(self.ligneIgnoreSpinBox)

        self.columnFirstLineCheckBox = QCheckBox(self.configurationGroup)
        self.columnFirstLineCheckBox.setObjectName(u"columnFirstLineCheckBox")

        self.otherFieldConfigurationLayout.addWidget(self.columnFirstLineCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.otherFieldConfigurationLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.otherFieldConfigurationLayout)


        self.verticalLayout_2.addWidget(self.configurationGroup)

        self.parametersDefinitionGroup = QGroupBox(ImportWindow)
        self.parametersDefinitionGroup.setObjectName(u"parametersDefinitionGroup")
        self.verticalLayout = QVBoxLayout(self.parametersDefinitionGroup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.timeLayout = QHBoxLayout()
        self.timeLayout.setObjectName(u"timeLayout")
        self.timeLabel = QLabel(self.parametersDefinitionGroup)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setMinimumSize(QSize(47, 0))

        self.timeLayout.addWidget(self.timeLabel)

        self.timeComboBox = QComboBox(self.parametersDefinitionGroup)
        self.timeComboBox.setObjectName(u"timeComboBox")
        self.timeComboBox.setMinimumSize(QSize(200, 0))

        self.timeLayout.addWidget(self.timeComboBox)

        self.timeFormatLabel = QLabel(self.parametersDefinitionGroup)
        self.timeFormatLabel.setObjectName(u"timeFormatLabel")
        self.timeFormatLabel.setMinimumSize(QSize(39, 0))

        self.timeLayout.addWidget(self.timeFormatLabel)

        self.timeFormatComboBox = QComboBox(self.parametersDefinitionGroup)
        self.timeFormatComboBox.setObjectName(u"timeFormatComboBox")
        self.timeFormatComboBox.setMinimumSize(QSize(200, 0))

        self.timeLayout.addWidget(self.timeFormatComboBox)

        self.timeFormatLineEdit = QLineEdit(self.parametersDefinitionGroup)
        self.timeFormatLineEdit.setObjectName(u"timeFormatLineEdit")
        self.timeFormatLineEdit.setEnabled(False)

        self.timeLayout.addWidget(self.timeFormatLineEdit)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.timeLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.timeLayout)

        self.horizontalPositionLayout = QHBoxLayout()
        self.horizontalPositionLayout.setObjectName(u"horizontalPositionLayout")
        self.longitudeLabel = QLabel(self.parametersDefinitionGroup)
        self.longitudeLabel.setObjectName(u"longitudeLabel")

        self.horizontalPositionLayout.addWidget(self.longitudeLabel)

        self.lontitudeComboBox = QComboBox(self.parametersDefinitionGroup)
        self.lontitudeComboBox.setObjectName(u"lontitudeComboBox")
        self.lontitudeComboBox.setMinimumSize(QSize(200, 0))

        self.horizontalPositionLayout.addWidget(self.lontitudeComboBox)

        self.latitudeLabel = QLabel(self.parametersDefinitionGroup)
        self.latitudeLabel.setObjectName(u"latitudeLabel")

        self.horizontalPositionLayout.addWidget(self.latitudeLabel)

        self.latitudeComboBox = QComboBox(self.parametersDefinitionGroup)
        self.latitudeComboBox.setObjectName(u"latitudeComboBox")
        self.latitudeComboBox.setMinimumSize(QSize(200, 0))

        self.horizontalPositionLayout.addWidget(self.latitudeComboBox)

        self.horizFormatLabel = QLabel(self.parametersDefinitionGroup)
        self.horizFormatLabel.setObjectName(u"horizFormatLabel")
        self.horizFormatLabel.setMinimumSize(QSize(40, 0))

        self.horizontalPositionLayout.addWidget(self.horizFormatLabel)

        self.horizFormatComboBox = QComboBox(self.parametersDefinitionGroup)
        self.horizFormatComboBox.setObjectName(u"horizFormatComboBox")
        self.horizFormatComboBox.setMinimumSize(QSize(200, 0))

        self.horizontalPositionLayout.addWidget(self.horizFormatComboBox)

        self.horizFormatlineEdit = QLineEdit(self.parametersDefinitionGroup)
        self.horizFormatlineEdit.setObjectName(u"horizFormatlineEdit")
        self.horizFormatlineEdit.setEnabled(False)

        self.horizontalPositionLayout.addWidget(self.horizFormatlineEdit)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalPositionLayout.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalPositionLayout)

        self.verticalPositionLayout = QHBoxLayout()
        self.verticalPositionLayout.setObjectName(u"verticalPositionLayout")
        self.altitudeLabel = QLabel(self.parametersDefinitionGroup)
        self.altitudeLabel.setObjectName(u"altitudeLabel")
        self.altitudeLabel.setMinimumSize(QSize(47, 0))

        self.verticalPositionLayout.addWidget(self.altitudeLabel)

        self.altitudeComboBox = QComboBox(self.parametersDefinitionGroup)
        self.altitudeComboBox.setObjectName(u"altitudeComboBox")
        self.altitudeComboBox.setMinimumSize(QSize(200, 0))

        self.verticalPositionLayout.addWidget(self.altitudeComboBox)

        self.meterRadioButton = QRadioButton(self.parametersDefinitionGroup)
        self.meterRadioButton.setObjectName(u"meterRadioButton")
        self.meterRadioButton.setChecked(True)

        self.verticalPositionLayout.addWidget(self.meterRadioButton)

        self.feetRadioButton_2 = QRadioButton(self.parametersDefinitionGroup)
        self.feetRadioButton_2.setObjectName(u"feetRadioButton_2")
        self.feetRadioButton_2.setChecked(False)

        self.verticalPositionLayout.addWidget(self.feetRadioButton_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalPositionLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.verticalPositionLayout)

        self.attitudeLayout = QHBoxLayout()
        self.attitudeLayout.setObjectName(u"attitudeLayout")
        self.bankLabel = QLabel(self.parametersDefinitionGroup)
        self.bankLabel.setObjectName(u"bankLabel")
        self.bankLabel.setMinimumSize(QSize(47, 0))

        self.attitudeLayout.addWidget(self.bankLabel)

        self.bankComboBox = QComboBox(self.parametersDefinitionGroup)
        self.bankComboBox.setObjectName(u"bankComboBox")
        self.bankComboBox.setMinimumSize(QSize(200, 0))

        self.attitudeLayout.addWidget(self.bankComboBox)

        self.pitchLabel = QLabel(self.parametersDefinitionGroup)
        self.pitchLabel.setObjectName(u"pitchLabel")
        self.pitchLabel.setMinimumSize(QSize(39, 0))

        self.attitudeLayout.addWidget(self.pitchLabel)

        self.pitchComboBox = QComboBox(self.parametersDefinitionGroup)
        self.pitchComboBox.setObjectName(u"pitchComboBox")
        self.pitchComboBox.setMinimumSize(QSize(200, 0))

        self.attitudeLayout.addWidget(self.pitchComboBox)

        self.headingLabel = QLabel(self.parametersDefinitionGroup)
        self.headingLabel.setObjectName(u"headingLabel")
        self.headingLabel.setMinimumSize(QSize(40, 0))

        self.attitudeLayout.addWidget(self.headingLabel)

        self.headingComboBox = QComboBox(self.parametersDefinitionGroup)
        self.headingComboBox.setObjectName(u"headingComboBox")
        self.headingComboBox.setMinimumSize(QSize(200, 0))

        self.attitudeLayout.addWidget(self.headingComboBox)

        self.degRadioButton = QRadioButton(self.parametersDefinitionGroup)
        self.degRadioButton.setObjectName(u"degRadioButton")
        self.degRadioButton.setChecked(True)

        self.attitudeLayout.addWidget(self.degRadioButton)

        self.radRadioButton = QRadioButton(self.parametersDefinitionGroup)
        self.radRadioButton.setObjectName(u"radRadioButton")

        self.attitudeLayout.addWidget(self.radRadioButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.attitudeLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.attitudeLayout)


        self.verticalLayout_2.addWidget(self.parametersDefinitionGroup)

        self.groupBox = QGroupBox(ImportWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setEnabled(True)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_4.addWidget(self.checkBox)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.tableView = QTableView(ImportWindow)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.closeButton = QPushButton(ImportWindow)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_3.addWidget(self.closeButton)

        self.importButton = QPushButton(ImportWindow)
        self.importButton.setObjectName(u"importButton")

        self.horizontalLayout_3.addWidget(self.importButton)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ImportWindow)

        QMetaObject.connectSlotsByName(ImportWindow)
    # setupUi

    def retranslateUi(self, ImportWindow):
        ImportWindow.setWindowTitle(QCoreApplication.translate("ImportWindow", u"Import File", None))
        self.fileGroup.setTitle(QCoreApplication.translate("ImportWindow", u"File", None))
        self.filePushButton.setText(QCoreApplication.translate("ImportWindow", u"...", None))
        self.fileFormatGroup.setTitle(QCoreApplication.translate("ImportWindow", u"File format", None))
        self.GPXRadioButton.setText(QCoreApplication.translate("ImportWindow", u"GPX", None))
        self.CSVRadioButton.setText(QCoreApplication.translate("ImportWindow", u"CSV", None))
        self.encodingLabel.setText(QCoreApplication.translate("ImportWindow", u"Encoding", None))
        self.configurationGroup.setTitle(QCoreApplication.translate("ImportWindow", u"Configuration", None))
        self.delimiterLabel.setText(QCoreApplication.translate("ImportWindow", u"Delimiter :", None))
        self.semiclonRadioButton.setText(QCoreApplication.translate("ImportWindow", u"Semicolon", None))
        self.commaRadioButton.setText(QCoreApplication.translate("ImportWindow", u"Comma", None))
        self.spaceRadioButton.setText(QCoreApplication.translate("ImportWindow", u"Space", None))
        self.tabulationRadioButton.setText(QCoreApplication.translate("ImportWindow", u"Tabulation", None))
        self.ligneIgnoreLabel.setText(QCoreApplication.translate("ImportWindow", u"Number of line to ignore", None))
        self.columnFirstLineCheckBox.setText(QCoreApplication.translate("ImportWindow", u"Column names on the first line", None))
        self.parametersDefinitionGroup.setTitle(QCoreApplication.translate("ImportWindow", u"Parameters Definition", None))
        self.timeLabel.setText(QCoreApplication.translate("ImportWindow", u"Time", None))
        self.timeFormatLabel.setText(QCoreApplication.translate("ImportWindow", u"Format", None))
        self.timeFormatLineEdit.setText(QCoreApplication.translate("ImportWindow", u"python format", None))
        self.longitudeLabel.setText(QCoreApplication.translate("ImportWindow", u"Longitude", None))
        self.latitudeLabel.setText(QCoreApplication.translate("ImportWindow", u"Latitude", None))
        self.horizFormatLabel.setText(QCoreApplication.translate("ImportWindow", u"Format", None))
        self.altitudeLabel.setText(QCoreApplication.translate("ImportWindow", u"Altitude", None))
        self.meterRadioButton.setText(QCoreApplication.translate("ImportWindow", u"m", None))
        self.feetRadioButton_2.setText(QCoreApplication.translate("ImportWindow", u"ft", None))
        self.bankLabel.setText(QCoreApplication.translate("ImportWindow", u"Bank", None))
        self.pitchLabel.setText(QCoreApplication.translate("ImportWindow", u"Pitch", None))
        self.headingLabel.setText(QCoreApplication.translate("ImportWindow", u"Heading", None))
        self.degRadioButton.setText(QCoreApplication.translate("ImportWindow", u"deg", None))
        self.radRadioButton.setText(QCoreApplication.translate("ImportWindow", u"rad", None))
        self.groupBox.setTitle(QCoreApplication.translate("ImportWindow", u"Data Enhancement", None))
        self.checkBox.setText(QCoreApplication.translate("ImportWindow", u"Interpolation", None))
        self.closeButton.setText(QCoreApplication.translate("ImportWindow", u"Close", None))
        self.importButton.setText(QCoreApplication.translate("ImportWindow", u"Import", None))
    # retranslateUi

