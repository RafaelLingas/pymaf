#from msilib.schema import Error
from PyQt5 import QtWidgets#,QtGui
from PyQt5.uic import loadUi
#import sys
import imf_code.adf_nlmo
import imf_code.adf_cmo
import imf_code.adf_nbo
import imf_code.gaussian_cmo
import imf_code.gaussian_nbo
import imf_code.gaussian_no_analysis
import utility_code.symmetry
import os

class Imf_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Imf_Window, self).__init__()
        self.ui=loadUi("imf_window.ui",self)

        self.ui.adf_radio.clicked.connect(lambda: self.ui.stacked_method.setCurrentIndex(1) )
        self.ui.gaussian_radio.clicked.connect(lambda: self.ui.stacked_method.setCurrentIndex(2) )
        # self.ui.orca_radio.clicked.connect(lambda: self.ui.stacked_method.setCurrentIndex(3) )

        self.ui.button_browse.clicked.connect(lambda: self.pick_new())
        self.ui.button_run.clicked.connect(lambda: self.check())


    def pick_new(self):
        dialog = QtWidgets.QFileDialog()
        folder_path=dialog.getOpenFileName(None,"Select any file in the folder that contains the outs")
        cut_path=folder_path[0].rfind("/")
        folder_path=folder_path[0][:cut_path]
        self.ui.folder_path_line_edit.setText(folder_path)
        return folder_path


    def check(self):
        self.path=self.ui.folder_path_line_edit.text()
        if self.ui.adf_radio.isChecked():
            if self.ui.adf_nbo_radio.isChecked():
                try:
                    self.ui.textBrowser.setText("Calculating..")
                    imf_code.adf_nbo.nbo(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
                ### Run adf program
            elif self.ui.adf_nlmo_radio.isChecked():
                try:
                    self.ui.textBrowser.setText("Calculating..")
                    imf_code.adf_nlmo.nlmo(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
                #self.ui.textBrowser
            elif self.ui.adf_cmo_radio.isChecked():
                self.ui.textBrowser.setText("Calculating..")
                try:
                    imf_code.adf_cmo.cmo(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
                ### Run adf cmo
            else:
                self.ui.textBrowser.setText("Choose Method")

        elif self.ui.gaussian_radio.isChecked():
            if self.ui.gaussian_nbo_radio.isChecked():
                self.ui.textBrowser.setText("Calculating..")
                ###this to check error in terminal####
                # imf_code.gaussian_nbo.gaussian_nbo(self.path,self.ui.textBrowser)
                try:
                    imf_code.gaussian_nbo.gaussian_nbo(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
                ### Run gaussian program
            elif self.ui.gaussian_cmo_radio.isChecked():
                self.ui.textBrowser.setText("Calculating..")
                ### Run gaussian cmo
                # imf_code.gaussian_cmo.gaussian_cmo(self.path,self.ui.textBrowser)
                try:
                    imf_code.gaussian_cmo.gaussian_cmo(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
            elif self.ui.gaussian_nmr_radio.isChecked():
                self.ui.textBrowser.setText("Calculating..")
                ### Run gaussian no analysis
                ###this to check error in terminal####
                # imf_code.gaussian_no_analysis.gaussian_nmr(self.path,self.ui.textBrowser)
                try:
                    imf_code.gaussian_no_analysis.gaussian_nmr(self.path,self.ui.textBrowser)
                except Exception as e:
                    self.ui.textBrowser.setText(str(e))
            else:
                self.ui.textBrowser.setText("Choose Method")

        # elif self.ui.orca_radio.isChecked():
        #     ### Sometime Implement orca program...........
        #     self.ui.textBrowser.setText("Not yet")
        #     pass
        else:
            self.ui.textBrowser.setText("Choose Program")


        try:
            symmetry_flag=True
            with open("gridspecs.txt","r") as input_data:
                for line in input_data:
                    if 'GRID' in line:
                        symmetry_flag=False
                        break
            
            if symmetry_flag:
                utility_code.symmetry.Symm(os.getcwd(),self.ui.textBrowser)
        except Exception as e:
            self.ui.textBrowser.append("Symmetry not done. Is gridspecs in the folder? "+str(e))
            # print(e)
            

