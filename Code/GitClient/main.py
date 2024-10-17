from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Window
        MainWindow.setObjectName("GitBit")
        MainWindow.resize(900, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Commit history
        self.commitHistory = QtWidgets.QListView(self.centralwidget)
        self.commitHistory.setGeometry(QtCore.QRect(490, 10, 401, 541))
        self.commitHistory.setObjectName("commitHistory")

        # Branch box
        self.branchBox = QtWidgets.QComboBox(self.centralwidget)
        self.branchBox.setGeometry(QtCore.QRect(320, 50, 161, 31))
        self.branchBox.setObjectName("branchBox")

        # Branch label
        self.branchLabel = QtWidgets.QLabel(self.centralwidget)
        self.branchLabel.setGeometry(QtCore.QRect(320, 10, 101, 41))
        self.branchLabel.setObjectName("branchLabel")

        # Tree
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(320, 90, 161, 461))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")

        # Title
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(100, 10, 81, 41))
        self.titleLabel.setObjectName("titleLabel")

        # Commit button
        self.commitButton = QtWidgets.QPushButton(self.centralwidget)
        self.commitButton.setGeometry(QtCore.QRect(10, 100, 75, 23))
        self.commitButton.setObjectName("commitButton")

        self.commitButton.clicked.connect(self.commitClicked)

        # Push Button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.pushClicked)

        # Pull Button
        self.pullButton = QtWidgets.QPushButton(self.centralwidget)
        self.pullButton.setGeometry(QtCore.QRect(10, 160, 75, 23))
        self.pullButton.setObjectName("pullButton")

        self.pullButton.clicked.connect(self.pullClicked)

        # Set the central widget for the main window
        MainWindow.setCentralWidget(self.centralwidget)

        # Create the menubar (optional)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Create the status bar (optional)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Set the text for all UI elements
        self.retranslateUi(MainWindow)

        # Automatically connect signals to slots
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Define the text and labels for the UI elements
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.branchLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">Branch:</span></p></body></html>"))
        self.titleLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600;\">GitBit</span></p></body></html>"))
        self.commitButton.setText(_translate("MainWindow", "Commit"))
        self.pushButton.setText(_translate("MainWindow", "Push"))
        self.pullButton.setText(_translate("MainWindow", "Pull"))

    def commitClicked(self):
        print("Commit")
    
    def pushClicked(self):
        print("Push")

    def pullClicked(self):
        print("Pull")

# Main entry point for the application
if __name__ == "__main__":
    import sys
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)
    
    # Create the main window object
    MainWindow = QtWidgets.QMainWindow()
    
    # Create the UI and set it up
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Show the main window
    MainWindow.show()
    
    # Execute the application
    sys.exit(app.exec_())
