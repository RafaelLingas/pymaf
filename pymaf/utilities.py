#from msilib.schema import Error
from PyQt5 import QtWidgets#,QtGui
from PyQt5.uic import loadUi
#import sys
# import imf_code.adf_nlmo
import utility_code.symmetry

class Utilities(QtWidgets.QMainWindow):
    def __init__(self):
        super(Utilities, self).__init__()
        self.ui=loadUi("utilities.ui",self)

        self.ui.button_symmetry.clicked.connect(lambda: self.Symmetry())

        self.ui.button_log.clicked.connect(lambda: self.Log())


    def Symmetry(self):
        dialog = QtWidgets.QFileDialog()
        folder_path=dialog.getOpenFileName(None,"Select the geometry file that was created after the IMF calculation")
        cut_path=folder_path[0].rfind("/")
        folder_path=folder_path[0][:cut_path]
        #try:
        utility_code.symmetry.Symm(folder_path,self.ui.textBrowser)
        #except Exception as e:
         #   self.ui.textBrowser.setText(str(e))

    def Log(self):
        self.ui.stackedWidget.setCurrentIndex(1)

        log="""
        Version 1.05 beta
        ------1.05-------
        -fixed CMO issues (non existent core)
        ------1.04-------
        -fixed issues with nbo
        -fixed nics and isolated
        ------1.03------
        -created log page. needs work
        -fixed gjf issue
        -fixed B-B bonds and c60_hexa
        -fixed scientific notation problem in geometry
        -fixed crash issues before loading molecule
        -fixed append textbrowser
        -added all atoms for IMF
        -fixed size of B and Ca
        -updated NBO gaussian
        -fixed sorting issue in CMO
        -"""
        self.ui.label_log.setText(log)