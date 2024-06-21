from PyQt5 import QtWidgets#,QtCore
from PyQt5.uic import loadUi
import sys

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor#, QOpenGLVersionProfile
from PyQt5.QtWidgets import QOpenGLWidget #(QApplication, QHBoxLayout, , QSlider,
        #QWidget)

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import geometry_funcs as Geo
import geometry_code.mimaf_adf as Adf


class Mimaf_In_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mimaf_In_Window, self).__init__()
        self.ui=loadUi("mimaf_in_window.ui",self)

        ### thats kind of stupid probably
        display_0=self.ui.openGLWidget.width()
        display_1=self.ui.openGLWidget.height()
        ### stupid

        self.ui.openGLWidget = GLWidget(self.ui.openGLWidget)

         ### thats kind of stupid probably
        self.ui.openGLWidget.display_0=display_0
        self.ui.openGLWidget.display_1=display_1
         ### stupid

        #self.setCentralWidget(self.ui.centralwidget)

        self.ui.button_import_molecule.clicked.connect(lambda: self.pick_molecule())

        self.ui.radio_xy2d.clicked.connect(lambda: self.change_plane("xy"))
        self.ui.radio_xz2d.clicked.connect(lambda: self.change_plane("xz"))
        self.ui.radio_yz2d.clicked.connect(lambda: self.change_plane("yz"))

        self.ui.radio_full2d_sym.clicked.connect(lambda: self.change_sym("Full"))
        self.ui.radio_2dtop_sym.clicked.connect(lambda: self.change_sym("z"))
        self.ui.radio_2dside_sym.clicked.connect(lambda: self.change_sym("x"))
        self.ui.radio_2dxyz_sym.clicked.connect(lambda: self.change_sym("xyz"))

        self.ui.radio_full_sym.clicked.connect(lambda: self.change_sym("Full"))
        self.ui.radio_z_sym.clicked.connect(lambda: self.change_sym("z"))
        self.ui.radio_y_sym.clicked.connect(lambda: self.change_sym("y"))
        self.ui.radio_x_sym.clicked.connect(lambda: self.change_sym("x"))
        self.ui.radio_xy_sym.clicked.connect(lambda: self.change_sym("xy"))
        self.ui.radio_xz_sym.clicked.connect(lambda: self.change_sym("xz"))
        self.ui.radio_yz_sym.clicked.connect(lambda: self.change_sym("yz"))
        self.ui.radio_xyz_sym.clicked.connect(lambda: self.change_sym("xyz"))



        self.ui.line_edit_grid_size.setText("31")
        self.ui.line_edit_grid_size.editingFinished.connect(lambda: self.get_grid())

        self.ui.line_edit_grid_step.setText("0.5")
        self.ui.line_edit_grid_step.editingFinished.connect(lambda: self.get_step())

        self.ui.checkbox_axis.clicked.connect(lambda: self.check_axis())
        self.ui.hmodel_check.clicked.connect(lambda: self.check_hmodel())

        self.ui.radio_2d.clicked.connect(lambda: self.change_dimension("2d"))
        self.ui.radio_2d.setChecked(True)
        self.ui.radio_3d.clicked.connect(lambda: self.change_dimension("3d"))

        self.ui.edit_max_ghosts.setText("300")
        self.ui.edit_method.setText("PBE")
        self.ui.edit_basis_set.setText("DZP")
        self.ui.edit_charge.setText("0")
        self.ui.edit_criteria.setText("0.001")
        self.ui.edit_memory.setText("1500MB")
        self.ui.edit_nproc.setText("4")

        self.ui.button_gaussian.clicked.connect(lambda: self.gaussian())
        self.ui.button_adf.clicked.connect(lambda: self.adf())
        self.ui.button_adf.clicked.connect(lambda: self.dalton())

        self.ui.radio_nbo.setChecked(True)
        self.ui.radio_xy2d.setChecked(True)
        self.ui.radio_full2d_sym.setChecked(True)

        self.ui.button_home.clicked.connect(lambda: self.Home())

    def Home(self):
        Geo.Atom.atoms=[]
        Geo.Cylinder.cylinders=[]

    
    def adf(self):

        both_flag=False

        if self.ui.radio_cmo.isChecked():
            analysis="cmo"
        elif self.ui.radio_both.isChecked():
            analysis="nbo"
            both_flag=True
        # elif self.ui.radio_no_analysis.isChecked():
        #     analysis="none"
        else:
            if self.ui.radio_none.isChecked():
                self.ui.textBrowser.append("Not ADF. Creating NBO runs instead")
            analysis="nbo"

        dim=self.ui.openGLWidget.dim

        max_ghosts=int(self.ui.edit_max_ghosts.text())
        method=self.ui.edit_method.text()
        basis_set=self.ui.edit_basis_set.text()
        charge=self.ui.edit_charge.text()
        criteria=self.ui.edit_criteria.text()
        memory=self.ui.edit_memory.text()
        nproc=self.ui.edit_nproc.text()

        size="_"+str(self.ui.openGLWidget.grid_size)+"_"
        step=str(self.ui.openGLWidget.grid_step).replace(".","")+"_"

        if not os.path.exists(self.fname+'_'+analysis+'_'+dim+'_'+method+'_'+basis_set+size+step+"inputs"):
            os.makedirs(self.fname+'_'+analysis+'_'+dim+'_'+method+'_'+basis_set+size+step+"inputs")
        os.chdir(self.path +"/"+self.fname+'_'+analysis+'_'+dim+'_'+method+'_'+basis_set+size+step+"inputs")



        Adf.runs(self.fname,Geo.Atom.atoms,self.ui.openGLWidget.grid_size,self.ui.openGLWidget.grid_step,
        self.ui.openGLWidget.sym,dim,self.ui.openGLWidget.plane,max_ghosts,method,basis_set,
        charge,criteria,memory,nproc,self.ui.textBrowser,both_flag).adf_run(analysis)

        ###after creating runs return to geometry dir (for hmodel to work)
        os.chdir(self.path)

    def dalton(self):

        both_flag=False
        analysis="none"
        dim=self.ui.openGLWidget.dim
        max_ghosts=int(self.ui.edit_max_ghosts.text())
        method=self.ui.edit_method.text()
        basis_set=self.ui.edit_basis_set.text()
        charge=self.ui.edit_charge.text()
        criteria=self.ui.edit_criteria.text()
        memory=self.ui.edit_memory.text()
        nproc=self.ui.edit_nproc.text()

        size="_"+str(self.ui.openGLWidget.grid_size)+"_"
        step=str(self.ui.openGLWidget.grid_step).replace(".","")+"_"

        if not os.path.exists('dalton'+self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs"):
            os.makedirs('dalton'+self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs")
        os.chdir(self.path +"/"+'dalton'+self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs")


        
        Adf.runs(self.fname,Geo.Atom.atoms,self.ui.openGLWidget.grid_size,self.ui.openGLWidget.grid_step,
        self.ui.openGLWidget.sym,dim,self.ui.openGLWidget.plane,max_ghosts,method,basis_set,
        charge,criteria,memory,nproc,self.ui.textBrowser,both_flag).dalton_run()

        ###after creating runs return to geometry dir (for hmodel to work)
        os.chdir(self.path)

    def gaussian(self):

        both_flag=False

        if self.ui.radio_cmo.isChecked():
            analysis="cmo"
        elif self.ui.radio_none.isChecked():
            analysis="none"
        elif self.ui.radio_both.isChecked():
            analysis="nbo"
            both_flag=True
            # self.ui.textBrowser.append("Not for Gaussian. Creating NBO runs instead")
        else:
            analysis="nbo"

        dim=self.ui.openGLWidget.dim
        max_ghosts=int(self.ui.edit_max_ghosts.text())
        method=self.ui.edit_method.text()
        basis_set=self.ui.edit_basis_set.text()
        charge=self.ui.edit_charge.text()
        criteria=self.ui.edit_criteria.text()
        memory=self.ui.edit_memory.text()
        nproc=self.ui.edit_nproc.text()

        size="_"+str(self.ui.openGLWidget.grid_size)+"_"
        step=str(self.ui.openGLWidget.grid_step).replace(".","")+"_"

        if not os.path.exists(self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs"):
            os.makedirs(self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs")
        os.chdir(self.path +"/"+self.fname+'_'+analysis+dim+'_'+method+'_'+basis_set+size+step+"inputs")


        
        Adf.runs(self.fname,Geo.Atom.atoms,self.ui.openGLWidget.grid_size,self.ui.openGLWidget.grid_step,
        self.ui.openGLWidget.sym,dim,self.ui.openGLWidget.plane,max_ghosts,method,basis_set,
        charge,criteria,memory,nproc,self.ui.textBrowser,both_flag).gaussian_run(analysis)

        ###after creating runs return to geometry dir (for hmodel to work)
        os.chdir(self.path)

    def change_dimension(self,a):
        if a=="2d":
            self.ui.stacked_dims.setCurrentIndex(0)
            self.ui.openGLWidget.dim="2d"
        elif a=="3d":
            self.ui.stacked_dims.setCurrentIndex(1)
            self.ui.openGLWidget.dim="3d"
        self.ui.openGLWidget.update()

    def check_hmodel(self):
        a=self.ui.hmodel_check.checkState()
        ## 0 for False , 2 for True
        self.ui.openGLWidget.hmodel=a
        Geo.Atom.atoms=[]
        Geo.Cylinder.cylinders=[]
        if self.ui.openGLWidget.mol_name!="":
            Geo.Get_Geom(self.ui.openGLWidget.mol_name,self.ui.openGLWidget.hmodel)
            try:
                Geo.Cylinder.Calculate_Cylinders(Geo.Atom.atoms)
            except ValueError:
                pass
            self.ui.openGLWidget.update()

    def check_axis(self):
        a=self.ui.checkbox_axis.checkState()
        ## 0 for False , 2 for True
        self.ui.openGLWidget.axis_state=a
        self.ui.openGLWidget.update()
        
    def get_step(self):
        step=0
        try:
            step=float(self.ui.line_edit_grid_step.text())
        except ValueError:
            pass


        self.ui.line_edit_grid_step.setText(str(step))
        self.ui.openGLWidget.grid_step=float(step)
        self.ui.openGLWidget.update()

    def get_grid(self):
        grid=0
        try:
            grid=int(self.ui.line_edit_grid_size.text())
        except ValueError:
            pass

        if (grid % 2) == 0:
            grid+=1

        self.ui.line_edit_grid_size.setText(str(grid))
        self.ui.openGLWidget.grid_size=int(grid)
        self.ui.openGLWidget.update()

    def change_plane(self,plane):
        self.ui.openGLWidget.plane=plane
        self.ui.openGLWidget.update()

    def change_sym(self,sym):
        self.ui.openGLWidget.sym=sym
        self.ui.openGLWidget.update()

    def pick_molecule(self):
        dialog = QtWidgets.QFileDialog()
        try:
            folder_path=dialog.getOpenFileName(None,"Select molecule")
            cut_path=folder_path[0].rfind("/")

            self.fname=folder_path[0][(cut_path+1):]#.replace('/','')
            self.path=folder_path[0][:cut_path]
            self.ui.openGLWidget.mol_name=self.fname

            cut_path=self.fname.rfind(".")
            self.fname=self.fname[:cut_path]


            # self.path=("F:\\workspace\\test_dir\\geom")
            # self.fname="m_8CPP_Dianion"
            # self.ui.openGLWidget.mol_name="10cpp_5cpp_dic_tzvp-align.xyz"

            ##self.path=path
            os.chdir(self.path)

            dirs=os.listdir(self.path)


            ### Empty classes so they dont stack
            Geo.Atom.atoms=[]
            Geo.Cylinder.cylinders=[]
            ###


            Geo.Get_Geom(self.ui.openGLWidget.mol_name,self.ui.openGLWidget.hmodel)


            Geo.Cylinder.Calculate_Cylinders(Geo.Atom.atoms)

            #Geo.Plane.two_d_xy(31,0.5)
            self.ui.openGLWidget.update()
        except OSError:
            pass








class GLWidget(QOpenGLWidget):

    yRotationChanged = pyqtSignal(int)

    distance_from=0
    dx=0
    dy=0
    plane="xy"
    sym="Full"
    grid_size=int(31)
    grid_step=0.5
    axis_state="0"
    hmodel=0
    mol_name=""
    dim="2d"
    display_0=0
    display_1=0


    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)


    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(self.display_0, self.display_1)
        ### this is probably a temporary solution


    def initializeGL(self):
        # version_profile = QOpenGLVersionProfile()
        # version_profile.setVersion(2, 0)
        # self.gl = self.context().versionFunctions(version_profile)
        # self.gl.initializeOpenGLFunctions()

        

        ####setup the projection matrix on the separated projection matrix stack
        glMatrixMode(GL_PROJECTION)
        gluPerspective(70, (self.display_0/self.display_1), 0.1, 500.0)

        
        #glClearColor(1.0, 1.0, 1.0, 0.0);
        ###create a model matrix
        self.a = (GLfloat * 16)()
        self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)

        glLight(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1)) # point light from the left, top, front
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

        glEnable(GL_DEPTH_TEST)


        glClearColor(16.0/255.0, 26.0/255.0, 38.0/255.0, 1.0)

        




    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(16.0/255.0, 26.0/255.0, 38.0/255.0, 1.0)


        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )
        

        glRotatef(1*self.dx,0.0,1.0,0.0)
        glRotatef(1*self.dy,1.0,0.0,0.0)
        self.dx=0
        self.dy=0
        
        glMultMatrixf( self.modelMat )
        self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
        glLoadIdentity()

        glTranslatef(0,0,-20+self.distance_from)
        glMultMatrixf( self.modelMat )


        for item in Geo.Atom.atoms:
           item.draw()

        for item in Geo.Cylinder.cylinders:
           item.draw()


        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
        
        

        if self.dim=="2d":
            Geo.Plane(self.grid_size,self.grid_step).two_d(self.plane,self.sym)
        if self.dim=="3d":
            Geo.Plane(self.grid_size,self.grid_step).three_d(self.sym)


        Geo.axis(self.axis_state)
        # glDisable(GL_LIGHT0)
        # glDisable(GL_LIGHTING)
        # glDisable(GL_COLOR_MATERIAL)

        



    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return


        #glViewport((width - side) // 2, (height - side) // 2, side, side)
        #glViewport(0, 0, self.display_0, self.display_1)
        #glViewport(0,0,0,0)

        
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #gluPerspective(70, (width/height), 0.1, 500.0)

        # self.a = (GLfloat * 16)()
        # self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)




    def mousePressEvent(self, event):
        self.lastPos = event.pos()
    
    def wheelEvent(self,event):
        self.wheel=event.angleDelta().y()
        if event.angleDelta().y()>0:
            self.distance_from+=5
        else:
            self.distance_from-=5

        self.update()
        

    def mouseMoveEvent(self, event):
        self.dx = event.x() - self.lastPos.x()
        self.dy = event.y() - self.lastPos.y()


        if Qt.LeftButton:
            # glRotatef(1*dx,0.0,1.0,0.0)
            # glRotatef(1*dy,1.0,0.0,0.0)
            self.update()

        self.lastPos = event.pos()
        #self.update()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()
    mimaf_in_window=Mimaf_In_Window()
    widget.addWidget(mimaf_in_window)

    #widget.setFixedWidth(1200)
    #widget.setFixedHeight(1200)
    widget.show()

    sys.exit(app.exec_())