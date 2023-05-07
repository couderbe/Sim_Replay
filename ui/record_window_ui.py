# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recordWindow.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialogButtonBox,
    QHBoxLayout, QLabel, QListView, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_RecordWindow(object):
    def setupUi(self, RecordWindow):
        if not RecordWindow.objectName():
            RecordWindow.setObjectName(u"RecordWindow")
        RecordWindow.resize(707, 481)
        self.verticalLayout = QVBoxLayout(RecordWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(RecordWindow)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.avalaibleListView = QListView(RecordWindow)
        self.avalaibleListView.setObjectName(u"avalaibleListView")
        self.avalaibleListView.setAcceptDrops(True)
        self.avalaibleListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.avalaibleListView.setDragEnabled(True)
        self.avalaibleListView.setDragDropMode(QAbstractItemView.InternalMove)
        self.avalaibleListView.setDefaultDropAction(Qt.MoveAction)
        self.avalaibleListView.setAlternatingRowColors(True)

        self.verticalLayout_4.addWidget(self.avalaibleListView)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.addButton = QPushButton(RecordWindow)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout_3.addWidget(self.addButton)

        self.removeButton = QPushButton(RecordWindow)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout_3.addWidget(self.removeButton)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(RecordWindow)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.recordedListView = QListView(RecordWindow)
        self.recordedListView.setObjectName(u"recordedListView")
        self.recordedListView.setAcceptDrops(True)
        self.recordedListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.recordedListView.setDragEnabled(True)
        self.recordedListView.setDragDropMode(QAbstractItemView.DragDrop)
        self.recordedListView.setDefaultDropAction(Qt.MoveAction)
        self.recordedListView.setAlternatingRowColors(True)

        self.verticalLayout_2.addWidget(self.recordedListView)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(RecordWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(RecordWindow)

        QMetaObject.connectSlotsByName(RecordWindow)
    # setupUi

    def retranslateUi(self, RecordWindow):
        RecordWindow.setWindowTitle(QCoreApplication.translate("RecordWindow", u"Form", None))
        self.label.setText(QCoreApplication.translate("RecordWindow", u"Available Parameters", None))
        self.addButton.setText(QCoreApplication.translate("RecordWindow", u"Add >>>", None))
        self.removeButton.setText(QCoreApplication.translate("RecordWindow", u"<<< Remove", None))
        self.label_2.setText(QCoreApplication.translate("RecordWindow", u"Recorded Parameters", None))
    # retranslateUi

