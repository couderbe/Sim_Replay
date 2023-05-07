# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(906, 565)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionConnect_to_sim = QAction(MainWindow)
        self.actionConnect_to_sim.setObjectName(u"actionConnect_to_sim")
        self.actionStart_Recording = QAction(MainWindow)
        self.actionStart_Recording.setObjectName(u"actionStart_Recording")
        self.actionStop_Recording = QAction(MainWindow)
        self.actionStop_Recording.setObjectName(u"actionStop_Recording")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionConnect_to_mock = QAction(MainWindow)
        self.actionConnect_to_mock.setObjectName(u"actionConnect_to_mock")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainVerticalLayout = QVBoxLayout()
        self.mainVerticalLayout.setObjectName(u"mainVerticalLayout")
        self.mainVerticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.mainTableView = QTableView(self.centralwidget)
        self.mainTableView.setObjectName(u"mainTableView")

        self.mainVerticalLayout.addWidget(self.mainTableView)

        self.commandHorizontalLayout = QHBoxLayout()
        self.commandHorizontalLayout.setObjectName(u"commandHorizontalLayout")
        self.playPausePushButton = QPushButton(self.centralwidget)
        self.playPausePushButton.setObjectName(u"playPausePushButton")

        self.commandHorizontalLayout.addWidget(self.playPausePushButton)

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.commandHorizontalLayout.addWidget(self.horizontalSlider)

        self.timeLabel = QLabel(self.centralwidget)
        self.timeLabel.setObjectName(u"timeLabel")

        self.commandHorizontalLayout.addWidget(self.timeLabel)


        self.mainVerticalLayout.addLayout(self.commandHorizontalLayout)


        self.verticalLayout.addLayout(self.mainVerticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 906, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuRecording = QMenu(self.menubar)
        self.menuRecording.setObjectName(u"menuRecording")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRecording.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionConnect_to_sim)
        self.menuFile.addAction(self.actionConnect_to_mock)
        self.menuRecording.addAction(self.actionStart_Recording)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionConnect_to_sim.setText(QCoreApplication.translate("MainWindow", u"Connect to sim", None))
        self.actionStart_Recording.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.actionStop_Recording.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionConnect_to_mock.setText(QCoreApplication.translate("MainWindow", u"Connect to mock (Dev)", None))
        self.playPausePushButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuRecording.setTitle(QCoreApplication.translate("MainWindow", u"Recording", None))
    # retranslateUi

