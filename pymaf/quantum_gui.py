from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sys

import mimaf_in
import imf_window
import mimaf_view
import utilities

from PyQt5.QtCore import Qt
import geometry_funcs as Geo
import os




class Main_Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Menu, self).__init__()
        self.ui=loadUi("main_menu.ui",self)

        self.button_imf.clicked.connect(lambda: widget.setCurrentIndex(1))
        self.button_mimaf_in.clicked.connect(lambda: self.mimaf())
        self.button_mimaf_view.clicked.connect(lambda: self.view())
        self.button_utilities.clicked.connect(lambda: self.utilities())

    def utilities(self):
        widget.setCurrentIndex(4)
        # widget.setMinimumWidth(700)
        # widget.setMinimumHeight(700)
        widget.setMaximumWidth(700)
        widget.setMaximumHeight(700)
    

    def view(self):
        widget.setCurrentIndex(3)
        widget.setMinimumWidth(1033)
        widget.setMinimumHeight(707)
        widget.setMaximumWidth(1033)
        widget.setMaximumHeight(727)


    def mimaf(self):
        #widget.setGeometry(300,300,1000,1000)
        widget.setCurrentIndex(2)
        widget.setMinimumWidth(800)
        widget.setMinimumHeight(770)
        widget.setMaximumWidth(800)
        widget.setMaximumHeight(770)
        widget.setMinimumWidth(700)
        widget.setMinimumHeight(720)
        


    def  home():
        ###might use at some point
        widget.setCurrentIndex(0)
        widget.setMinimumWidth(700)
        widget.setMinimumHeight(700)
        widget.setMaximumWidth(700)
        widget.setMaximumHeight(700)

if __name__ == '__main__':

    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()

    ### Main Menu
    mainwindow=Main_Menu()
    widget.addWidget(mainwindow)

    ### IMF window  
    imf_window=imf_window.Imf_Window()
    imf_window.ui.button_back.clicked.connect(lambda: widget.setCurrentIndex(0))
    widget.addWidget(imf_window)

    ### Mimaf_in window
    mimaf_in_window=mimaf_in.Mimaf_In_Window()
    mimaf_in_window.ui.button_home.clicked.connect(lambda: widget.setCurrentIndex(0))
    widget.addWidget(mimaf_in_window)

    ### Mimaf_View window
    mimaf_view_window=mimaf_view.Mimaf_View_Window()
    mimaf_view_window.ui.button_home.clicked.connect(lambda: Main_Menu.home())#widget.setCurrentIndex(0))
    widget.addWidget(mimaf_view_window)

    ### Utilities window
    utilites_window=utilities.Utilities()
    utilites_window.ui.button_home.clicked.connect(lambda: Main_Menu.home())#widget.setCurrentIndex(0))
    widget.addWidget(utilites_window)




    #widget.setGeometry(300,300,700,700)
    widget.setWindowTitle("PyMAF")
    widget.setMinimumWidth(700)
    widget.setMinimumHeight(700)
    widget.setMaximumWidth(700)
    widget.setMaximumHeight(700)
    widget.show()

    sys.exit(app.exec_())