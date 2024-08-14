# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patternTrainingWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSlider,
    QWidget)

class Ui_PatternTrainingWindow(object):
    def setupUi(self, PatternTrainingWindow):
        if not PatternTrainingWindow.objectName():
            PatternTrainingWindow.setObjectName(u"PatternTrainingWindow")
        PatternTrainingWindow.resize(692, 412)
        self.widget = QWidget(PatternTrainingWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(290, 20, 51, 151))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet(u"border-color: rgb(8, 8, 8);\n"
"background-color: rgb(149, 149, 149);")
        self.qfuLabel = QLabel(self.widget)
        self.qfuLabel.setObjectName(u"qfuLabel")
        self.qfuLabel.setGeometry(QRect(0, 120, 49, 16))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.qfuLabel.setFont(font)
        self.qfuLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.qfuLabel.setScaledContents(False)
        self.qfuLabel.setAlignment(Qt.AlignCenter)
        self.revertQFUPushButton = QPushButton(self.widget)
        self.revertQFUPushButton.setObjectName(u"revertQFUPushButton")
        self.revertQFUPushButton.setGeometry(QRect(5, 3, 41, 24))
        self.airportComboBox = QComboBox(PatternTrainingWindow)
        self.airportComboBox.setObjectName(u"airportComboBox")
        self.airportComboBox.setGeometry(QRect(10, 10, 71, 22))
        self.leftHandRadioButton = QRadioButton(PatternTrainingWindow)
        self.leftHandRadioButton.setObjectName(u"leftHandRadioButton")
        self.leftHandRadioButton.setGeometry(QRect(250, 10, 31, 20))
        self.leftHandRadioButton.setChecked(True)
        self.rightHandradioButton = QRadioButton(PatternTrainingWindow)
        self.rightHandradioButton.setObjectName(u"rightHandradioButton")
        self.rightHandradioButton.setGeometry(QRect(360, 10, 89, 20))
        self.widget_2 = QWidget(PatternTrainingWindow)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(210, 90, 71, 171))
        self.finaleDistanceVerticalSlider = QSlider(self.widget_2)
        self.finaleDistanceVerticalSlider.setObjectName(u"finaleDistanceVerticalSlider")
        self.finaleDistanceVerticalSlider.setGeometry(QRect(40, 0, 22, 160))
        self.finaleDistanceVerticalSlider.setMaximum(100)
        self.finaleDistanceVerticalSlider.setSliderPosition(50)
        self.finaleDistanceVerticalSlider.setOrientation(Qt.Vertical)
        self.finaleDistanceLabel = QLabel(self.widget_2)
        self.finaleDistanceLabel.setObjectName(u"finaleDistanceLabel")
        self.finaleDistanceLabel.setGeometry(QRect(10, 70, 21, 16))
        self.widget_3 = QWidget(PatternTrainingWindow)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(180, 260, 271, 41))
        self.crossDistanceHorizontalSlider = QSlider(self.widget_3)
        self.crossDistanceHorizontalSlider.setObjectName(u"crossDistanceHorizontalSlider")
        self.crossDistanceHorizontalSlider.setGeometry(QRect(0, 0, 271, 22))
        self.crossDistanceHorizontalSlider.setMaximum(100)
        self.crossDistanceHorizontalSlider.setValue(50)
        self.crossDistanceHorizontalSlider.setOrientation(Qt.Horizontal)
        self.crossDistanceLabel = QLabel(self.widget_3)
        self.crossDistanceLabel.setObjectName(u"crossDistanceLabel")
        self.crossDistanceLabel.setGeometry(QRect(110, 20, 49, 16))
        self.crossDistanceLabel.setAlignment(Qt.AlignCenter)
        self.teleportPushButton = QPushButton(PatternTrainingWindow)
        self.teleportPushButton.setObjectName(u"teleportPushButton")
        self.teleportPushButton.setGeometry(QRect(280, 380, 75, 24))

        self.retranslateUi(PatternTrainingWindow)

        QMetaObject.connectSlotsByName(PatternTrainingWindow)
    # setupUi

    def retranslateUi(self, PatternTrainingWindow):
        PatternTrainingWindow.setWindowTitle(QCoreApplication.translate("PatternTrainingWindow", u"Dialog", None))
        self.qfuLabel.setText(QCoreApplication.translate("PatternTrainingWindow", u"09", None))
        self.revertQFUPushButton.setText(QCoreApplication.translate("PatternTrainingWindow", u"XQFU", None))
        self.leftHandRadioButton.setText(QCoreApplication.translate("PatternTrainingWindow", u"L", None))
        self.rightHandradioButton.setText(QCoreApplication.translate("PatternTrainingWindow", u"R", None))
        self.finaleDistanceLabel.setText(QCoreApplication.translate("PatternTrainingWindow", u"0", None))
        self.crossDistanceLabel.setText(QCoreApplication.translate("PatternTrainingWindow", u"0", None))
        self.teleportPushButton.setText(QCoreApplication.translate("PatternTrainingWindow", u"teleport", None))
    # retranslateUi

