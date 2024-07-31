from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.uic import loadUi
import sys

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor#, QOpenGLVersionProfile
from PyQt5.QtWidgets import QOpenGLWidget,QListWidgetItem# (QApplication, QHBoxLayout, , QSlider,
       # QWidget)

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import geometry_funcs as Geo
#import geometry_code.mimaf_adf as Adf
import view_funcs
import math
from PIL import Image
from PIL import ImageOps
import os


class Mimaf_View_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mimaf_View_Window, self).__init__()
        self.ui=loadUi("mimaf_view.ui",self)


        ### thats kind of stupid probably
        # display_0=self.ui.openGLWidget.width()
        # display_1=self.ui.openGLWidget.height()
        display_0=self.ui.frame_7.width()
        display_1=self.ui.frame_7.height()
        # ### stupid
        

        self.ui.openGLWidget = GLWidget_view(self.ui.openGLWidget)
        #self.ui.openGLWidget = GLWidget_view()

        # #  ### thats kind of stupid probably
        # self.ui.openGLWidget.display_0=display_0
        # self.ui.openGLWidget.display_1=display_1
        self.ui.openGLWidget.display_0=self.ui.frame_7.width()
        self.ui.openGLWidget.display_1=self.ui.frame_7.height()
         ### stupid


        #self.setCentralWidget(self.ui.centralwidget)

        self.ui.button_import_molecule.clicked.connect(lambda: self.pick_molecule())


        self.ui.listdir.itemClicked.connect(lambda: self.Change_Dir())
        #self.ui.listfile.itemClicked.connect(lambda: self.View())
        self.ui.listfile.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        #self.ui.listfile.itemSelectionChanged.connect(lambda: self.View())
        self.ui.listfile.itemClicked.connect(lambda: self.View())

        self.ui.line_edit_from.setText("-15")
        self.ui.line_edit_from.editingFinished.connect(lambda: self.View())
        self.ui.line_edit_to.setText("15")
        self.ui.line_edit_to.editingFinished.connect(lambda: self.View())
        self.ui.line_edit_step.setText("1.0")
        self.ui.line_edit_step.editingFinished.connect(lambda: self.View())

        self.ui.line_edit_iso.setText("15")
        self.ui.line_edit_iso.editingFinished.connect(lambda: self.View())

        self.ui.line_edit_iso2.setText("5")
        self.ui.line_edit_iso2.editingFinished.connect(lambda: self.View())
        self.ui.check_iso2.clicked.connect(lambda: self.View())

        self.ui.button_reset.clicked.connect(lambda: self.Reset())
        self.ui.button_turn.clicked.connect(lambda: self.Turn())

        self.ui.check_palette.clicked.connect(lambda: self.Show_palette())

        self.ui.button_background.clicked.connect(lambda: self.Background())

        self.ui.button_save_image.clicked.connect(lambda: self.Save_Image())

        self.ui.button_home.clicked.connect(lambda: self.Home())

        self.ui.check_ortho.clicked.connect(lambda: self.Ortho())

        self.ui.check_lines.clicked.connect(lambda: self.View())

        self.ui.check_smooth.clicked.connect(lambda: self.View())

        self.ui.button_merge.clicked.connect(lambda: self.Merge())

        self.ui.button_delete.clicked.connect(lambda: self.Delete_b())

        self.ui.button_rotation.clicked.connect(lambda: self.Rotation())
        self.ui.line_edit_degrees.setText("30")

        self.ui.checkbox_axis.clicked.connect(lambda: self.check_axis())

        self.ui.checkbox_enable_extract.clicked.connect(lambda: self.check_enable_extract())

        self.ui.line_edit_which_dots.textChanged.connect(lambda: self.check_dots())

        self.ui.button_isolate.clicked.connect(lambda: self.Isolate())

        self.ui.button_get_values.clicked.connect(lambda: self.Get_values())

        self.ui.check_clip.clicked.connect(lambda: self.Clip())

        self.ui.combobox_clip.currentIndexChanged.connect(lambda: self.Clip())

    def Clip(self):
        try:
            self.View()
        except AttributeError:
            pass

    def Isolate(self):
        try:
            extract_instance.isolate(self.ui.openGLWidget.squares.cubes)
        except NameError:
            pass

    def Get_values(self):
        try:
            extract_instance.get_values(self.ui.openGLWidget.squares.cubes)
        except NameError:
            pass
    
    def check_dots(self):
        self.ui.openGLWidget.which_dots=self.ui.line_edit_which_dots.text()
        self.ui.openGLWidget.update()

    def check_enable_extract(self):
        a=self.ui.checkbox_enable_extract.checkState()
        ## 0 for False , 2 for True

        try:
            self.plane
        except AttributeError:
            self.plane=0

        try:
            # self.ui.openGLWidget.dots=Geo.extract(self.grid,self.step,self.ui.openGLWidget.dim,self.plane)
            # self.dots=Geo.extract(self.grid,self.step,self.ui.openGLWidget.dim,self.plane)
            global extract_instance
            extract_instance=Geo.extract(self.grid,self.step,self.ui.openGLWidget.dim,self.plane)

            self.ui.openGLWidget.check_enable_extract=a
            self.ui.openGLWidget.update()

        except AttributeError:
            pass
    
    def check_axis(self):
        a=self.ui.checkbox_axis.checkState()
        ## 0 for False , 2 for True
        self.ui.openGLWidget.axis_state=a
        self.ui.openGLWidget.update()

    def Rotation(self):
        self.ui.openGLWidget.rotation_axis=self.ui.combobox_axis.currentText()
        self.ui.openGLWidget.rotation_degrees=int(float(self.ui.line_edit_degrees.text()))
        self.ui.openGLWidget.rotation=True
        self.ui.openGLWidget.update()

    def Delete_b(self):

        try:

            dirs=[]
            for i in range(0,self.ui.listdir.count()):
                dirs.append(self.ui.listdir.item(i).text())

            files=[]
            for item in self.ui.listfile.selectedItems():
                files.append(item.text())

            for dir in dirs:
                os.chdir(self.path+"/"+dir)
                for file in files:
                    if os.path.exists(file):
                        os.remove(file)
                os.chdir(self.path)

            self.keep_selected_flag=False
            self.Change_Dir()

        except AttributeError:
            pass

    def Merge(self):
        
        try:

            subtract=self.ui.check_subtract.isChecked()
            dirs=[]
            for i in range(0,self.ui.listdir.count()):
                dirs.append(self.ui.listdir.item(i).text())

            files=[]
            for item in self.ui.listfile.selectedItems():
                files.append(item.text())

            for dir in dirs:
                os.chdir(self.path+"/"+dir)
                if self.ui.openGLWidget.dim=="2d":
                    view_funcs.marching_squares.Merge_files(files,subtract)
                else:
                    view_funcs.marching_cubes.Merge_files(files,subtract)
                os.chdir(self.path)
            
            self.Change_Dir()
        
        except AttributeError:
            pass


    def Save_Image(self):

        try:

            if not os.path.exists("Images"):
                os.makedirs("Images")
            os.chdir(self.path+"/Images")

            try:
                name=self.ui.listdir.currentItem().text()+"_"
            except AttributeError:
                name=""

            for item in self.ui.listfile.selectedItems():
                a=item.text()[item.text().find('.'):]
                b=item.text().replace(a,"_")
                name+=b

            if name=="":
                name=self.full_name
            self.ui.openGLWidget.image_name=name
            self.ui.openGLWidget.save_image=True
            self.ui.openGLWidget.update()

        except AttributeError:
            pass

    def Ortho(self):

        try:

            a=self.ui.check_ortho.checkState()
            ## 0 for False , 2 for True
            self.ui.openGLWidget.ortho=a

            Geo.Atom.atoms=[]
            Geo.Cylinder.cylinders=[]
            ###
            Geo.Get_Geom(self.ui.openGLWidget.mol_name,self.ui.openGLWidget.hmodel)
            Geo.Cylinder.Calculate_Cylinders(Geo.Atom.atoms)

            #self.ui.openGLWidget.display_0=self.ui.frame_7.width()
            #self.ui.openGLWidget.display_1=self.ui.frame_7.height()
            

            self.ui.openGLWidget.update()
            self.Reset()

        except FileNotFoundError:
            pass

    def Home(self):
        Geo.Atom.atoms=[]
        Geo.Cylinder.cylinders=[]
        self.ui.listfile.clear()
        self.ui.listdir.clear()
        self.ui.openGLWidget.marching_squares=False
        self.ui.openGLWidget.marching_cubes=False

    def Background(self):
        if self.ui.openGLWidget.background==True:
            self.ui.openGLWidget.background=False
        else:
            self.ui.openGLWidget.background=True
        self.ui.openGLWidget.update()

    def Show_palette(self):
        a=self.ui.check_palette.checkState()
        ## 0 for False , 2 for True
        self.ui.openGLWidget.palette_state=a
        self.ui.openGLWidget.update()

    def Turn(self):
        self.ui.openGLWidget.turn=True
        self.ui.openGLWidget.update()

    def Reset(self):
        self.ui.openGLWidget.reset=True
        self.ui.openGLWidget.update()


    def View(self):
        try:
            if not self.individual:
                # self.file_name=self.ui.listfile.currentItem().text()
                #a=self.ui.listfile.selectedItems()
                #print([item.text() for item in self.ui.listfile.selectedItems()])
                all_files=[]
                for item in self.ui.listfile.selectedItems():
                    join_item=os.path.join(self.dir_name,item.text())
                    all_files.append(os.path.join(self.path, join_item))
            else:
                all_files=[]
                all_files.append(os.path.join(self.path,self.full_name))
                # all_files.append(self.path+ '\\'+self.full_name)


            subtract=self.ui.check_subtract.isChecked()

            if self.ui.openGLWidget.dim=="2d":

                draw_lines=self.ui.check_lines.isChecked()

                #colors=int(self.ui.line_edit_colors.text())

                from_=int(float(self.ui.line_edit_from.text()))
                to_=int(float(self.ui.line_edit_to.text())+1)
                step_color=float(self.ui.line_edit_step.text())
                if step_color==0.0:
                    self.ui.line_edit_step.setText("1.0")
                    step_color=0.1


                #file_name=os.path.join(self.path, self.dir_name+'\\'+self.file_name)

                self.ui.openGLWidget.squares=view_funcs.marching_squares(all_files,
                self.plane,self.grid,self.step,subtract,from_,to_,step_color,draw_lines)


                self.ui.openGLWidget.marching_squares=True

                self.ui.openGLWidget.squares.read_texture("temp.png")

            elif self.ui.openGLWidget.dim=="3d":

                check_if_clip=self.ui.check_clip.checkState()
                if check_if_clip==2:
                    clip_axis=self.ui.combobox_clip.currentText()
                else:
                    clip_axis=0
                
                isovalue=float(self.ui.line_edit_iso.text())
                # subtract=self.ui.check_subtract_3d.isChecked()
                smooth=self.ui.check_smooth.isChecked()

                color1_pos=[1.0,0.0,0.0,1]
                color1_neg=[0.0,0.0,1.0,1]
                #color1_neg=[42.0/255.0, 171.0/255.0, 191.0/255.0,1]
                #color1_pos=[96.0/255.0, 76.0/255.0, 199.0/255.0,1]

                self.ui.openGLWidget.cubes=view_funcs.marching_cubes(all_files,
                self.grid,self.step,isovalue,subtract,color1_pos,color1_neg,smooth,clip_axis)
                self.ui.openGLWidget.marching_cubes=True

                if self.ui.check_iso2.isChecked():
                    isovalue2=float(self.ui.line_edit_iso2.text())
                    # subtract=self.ui.check_subtract_3d.isChecked()

                    if check_if_clip==2:
                        alpha=1
                        self.ui.openGLWidget.no_trans_because_clip=True
                    else:
                        alpha=0.4
                        self.ui.openGLWidget.no_trans_because_clip=False

                    clip_axis=0

                    color1_pos=[227.0/255.0, 203/255.0, 150.0/255.0,alpha]
                    color1_neg=[2.0/255.0, 117.0/255.0, 240.0/255.0,alpha]

                    self.ui.openGLWidget.cubes2=view_funcs.marching_cubes(all_files,
                    self.grid,self.step,isovalue2,subtract,color1_pos,color1_neg,smooth,clip_axis)
                    self.ui.openGLWidget.marching_cubes2=True
                else:
                    self.ui.openGLWidget.marching_cubes2=False


            self.keep_selected_flag=True
            self.ui.openGLWidget.update()

        except KeyError:
            pass


    def Change_Dir(self):
        self.dir_name=self.ui.listdir.currentItem().text()

        files=os.listdir(os.path.join(self.path,self.dir_name))
        # files=os.listdir(self.path+'\\'+self.dir_name)  ### old for windows

        def custom_sort(value):
            try:
                # try to extract a numerical value from the filename
                numerical_value = int(value.split('.')[0])
                return (True, numerical_value)
            except ValueError:
                # if the filename is not numerical, return it as-is
                return (False, value)

        # sort the list of files using the numerical sorting function
        files.sort(key=custom_sort)

        try:
            if self.keep_selected_flag:
                self.View()
        except FileNotFoundError:
            pass
        
        save_selected=[]
        for item in self.ui.listfile.selectedItems():
            save_selected.append(item.text())


        self.ui.listfile.clear()
        for item in files:
            if self.ui.openGLWidget.dim=="3d" and '.txt' in item:
                continue
            if '.' in item:
                self.ui.listfile.addItem(item)
        

        for i in save_selected:
            matching_items = self.ui.listfile.findItems(i, Qt.MatchExactly)
            for item in matching_items:
                item.setSelected(True)



    def pick_molecule(self):

        self.ui.openGLWidget.display_0=self.ui.frame_7.width()
        self.ui.openGLWidget.display_1=self.ui.frame_7.height()

        self.ui.listfile.clear()


        dialog = QtWidgets.QFileDialog()
        try:
            folder_path=dialog.getOpenFileName(None,"Select molecule")
            cut_path=folder_path[0].rfind("/")

            self.fname=folder_path[0][(cut_path+1):]#.replace('/','')
            self.path=folder_path[0][:cut_path]
            self.ui.openGLWidget.mol_name=self.fname

            cut_path=self.fname.rfind(".")
            self.full_name=self.fname
            self.fname=self.fname[:cut_path]

            ##3d example
            # self.path=("F:\\workspace\\test_dir\\3d\\problematic\\zz")
            # ##2d example
            # #self.path=("F:\\workspace\\test_dir\\test_for_view")
            # self.fname="Sum_Para_SO_Diamagnetic_total.cube"
            # self.full_name="Sum_Para_SO_Diamagnetic_total.cube"
            # self.ui.openGLWidget.mol_name="Sum_Para_SO_Diamagnetic_total.cube"

            ##self.path=path
            os.chdir(self.path)

            dirs=os.listdir(self.path)

            ### Let path be known to opengl widget as well
            self.ui.openGLWidget.path=self.path


            ### Empty classes so they dont stack
            Geo.Atom.atoms=[]
            Geo.Cylinder.cylinders=[]
            ###


            Geo.Get_Geom(self.ui.openGLWidget.mol_name,self.ui.openGLWidget.hmodel)


            Geo.Cylinder.Calculate_Cylinders(Geo.Atom.atoms)

            #Geo.Plane.two_d_xy(31,0.5)
            self.ui.listdir.clear()
            if not self.full_name.endswith(".cube"):
                for item in dirs:
                    if '.' not in item and item!='Images':
                        self.ui.listdir.addItem(item)
                    if 'gridSpecs' in item or 'gridspecs' in item:
                        gridspecs=[]
                        with open(item,'r') as input_data:
                            for line in input_data:
                                gridspecs.append(line)
                        if "GRID" in gridspecs[0] or "Grid" in gridspecs[0]:
                            self.plane=gridspecs[1].replace('\n','')
                            self.ui.openGLWidget.plane=self.plane
                            self.grid=int(float(gridspecs[2].replace('\n','')))
                            self.step=float(gridspecs[3].replace('\n',''))
                            self.ui.openGLWidget.dim="2d"
                            self.ui.openGLWidget.marching_cubes=False
                            self.ui.openGLWidget.marching_squares=False
                            self.ui.stacked_dim.setCurrentIndex(1)
                            self.individual=False
                        else:
                            self.grid=int(float(gridspecs[0].replace('\n','')))
                            self.step=float(gridspecs[1].replace('\n',''))
                            self.ui.openGLWidget.dim="3d"
                            self.ui.openGLWidget.marching_squares=False
                            self.ui.openGLWidget.marching_cubes=False
                            self.ui.stacked_dim.setCurrentIndex(2)
                            self.individual=False
                            # self.ui.openGLWidget.ortho=0
            else:
                #self.grid=int(float(gridspecs[0].replace('\n','')))
                #self.step=float(gridspecs[1].replace('\n',''))
                gridspecs=[]
                i=0
                with open(self.full_name,'r') as input_data:
                        for line in input_data:
                            #gridspecs.append(line)
                            if i==2:
                                a=line.split()
                                start_pos=0.529177249*float(a[1])
                                

                            if i==3:
                                a=line.split()
                                a=0.529177249*float(a[1]) ### from Bohr to angstrom
                                self.step=a
                                self.grid=int(float(-start_pos*2/self.step+1))
                                break
                            i+=1

                self.ui.openGLWidget.dim="3d"
                self.ui.openGLWidget.marching_squares=False
                self.ui.openGLWidget.marching_cubes=False
                self.ui.stacked_dim.setCurrentIndex(2)
                self.individual=True
                self.ui.openGLWidget.ortho=0
                self.View()

            try:
                self.ui.line_edit_which_dots.setText("1-"+str(self.grid*self.grid))
                self.ui.openGLWidget.which_dots=self.ui.line_edit_which_dots.text()
            except AttributeError:
                self.ui.line_edit_which_dots.setText("")

            self.ui.openGLWidget.reset=True
            self.ui.openGLWidget.update()
            self.keep_selected_flag=False
        except OSError:
            pass


class GLWidget_view(QOpenGLWidget):

    yRotationChanged = pyqtSignal(int)

    distance_from=0
    dx=0
    dy=0
    plane="xy"
    sym="Full"
    grid_size=int(31)
    grid_step=0.5
    hmodel=0
    mol_name=""
    dim="2d"
    display_0=0
    display_1=0
    marching_squares=False
    marching_cubes=False
    marching_cubes2=False
    reset=False
    first_time=True ### probably should implement in init but..
    turn=False
    palette_state=0
    background=False
    ortho=3 
    save_image=False
    axis_state="0"
    check_enable_extract="0"
    which_dots=0
    

    rotation=False
    store_rotations=[]

    def __init__(self, parent=None):
        super(GLWidget_view, self).__init__(parent)

    def minimumSizeHint(self):
        return QSize(50, 50)
        #return QSize(self.display_0, self.display_1)

    # def adjustSize(self):
    #     print("wwww")
    #     return super().adjustSize()

    # def changeEvent(self, a0: QtCore.QEvent):
    #     print("change")
    #     return super().changeEvent(a0)

    def sizeHint(self):
        return QSize(self.display_0, self.display_1)
        ### this is probably a temporary solution


    def initializeGL(self):


        ####setup the projection matrix on the separated projection matrix stack
        glMatrixMode(GL_PROJECTION)
        gluPerspective(70, (self.display_0/self.display_1), 0.1, 200.0)

        ###create a model matrix
        self.a = (GLfloat * 16)()
        self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)

        glEnable(GL_DEPTH_TEST)

        glClearColor(16.0/255.0, 26.0/255.0, 38.0/255.0, 1.0)


        glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 0, 1))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        # glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        # glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
        # glEnable(GL_MULTISAMPLE)
        # glEnable(GL_LINE_SMOOTH)
        # glEnable(GL_POLYGON_SMOOTH)
        # glEnable(GL_POINT_SMOOTH)



    def paintGL(self):
     

        if self.save_image==True:
            width, height = 4000, 4000
            buffers = view_funcs.myglCreateBuffers(width, height)
            glViewport(0, 0, width, height)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.ortho==2:
            self.ortho=1 ### different for ortho
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            #gluPerspective(70, (self.display_0/self.display_1), 0.1, 200.0)
            glOrtho(-15,15,-15,15,-100,100)
            # glOrtho(-1,1,-1,1,-100,100)    #### this is kinda weird self.distance=0 generally alla...
            # #self.a = (GLfloat * 16)()
            self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
            # self.distance_from=95    #### this should be 0 but want to take pictures for 3d now
            self.distance_from=0


        elif self.ortho==0:
            self.ortho=3
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(70, (self.display_0/self.display_1), 0.1, 200.0)
            ###create a model matrix
            #self.a = (GLfloat * 16)()
            self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
            self.distance_from=0
            

        if self.background:      
            glClearColor(255.0, 255.0, 255.0,1)
            
        else:
            glClearColor(16.0/255.0, 26.0/255.0, 38.0/255.0, 1)
            pass
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE )

        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()


        if self.reset:
            glLoadIdentity()
            if self.plane=="yz":
                glRotatef(90,0,1,0)
                glRotatef(90,0,0,1)
            elif self.plane=="xz":
                glRotatef(90,0,1,1)
            elif self.plane=="xy": 
                pass

            self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
            self.reset=False
            self.store_rotations=[]

        if self.turn:
            glRotatef(90,0,0,1)
            self.turn=False
        
        if self.rotation:
            ax=0
            ay=0
            az=0
            # glLoadIdentity()
            

            if self.rotation_axis=='x':
                ax=1
                glRotatef(self.rotation_degrees,1,0,0)
            elif self.rotation_axis=='y':
                ay=1
                glRotatef(self.rotation_degrees,0,1,0)
            else:
                az=1
                glRotatef(self.rotation_degrees,0,0,1)
            
            # self.store_rotations.append([self.rotation_degrees,ax,ay,az])
            # for i in range(0,len(self.store_rotations)):
            #     #incr=len(self.store_rotations)-1-i
                
            #     incr=i
            #     glRotatef(self.store_rotations[incr][0],self.store_rotations[incr][1],self.store_rotations[incr][2],self.store_rotations[incr][3])
            #     #print(self.store_rotations[len(self.store_rotations)-1-i])
            
            # glRotatef(ax*self.rotation_degrees,0,1,0)
            # glRotatef(ay*self.rotation_degrees,1,0,0)
            # glRotatef(az*self.rotation_degrees,0,0,1)
            #self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
            # for item in self.modelMat:
            #     print(item)
            # glMultMatrixf( (self.rotation_degrees,ax,ay,az) )
            # glTranslatef(0,0,-20+self.distance_from)
            # self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
            self.rotation=False


        


        glRotatef(1*self.dx,0.0,1.0,0.0)
        glRotatef(1*self.dy,1.0,0.0,0.0)
        self.dx=0
        self.dy=0

        

        glMultMatrixf( self.modelMat )
        
        self.modelMat = glGetFloatv(GL_MODELVIEW_MATRIX, self.a)
        glLoadIdentity()

        if self.ortho==3:
            glTranslatef(0,0,-20+self.distance_from)
        elif self.ortho==1:
            glTranslatef(0,0,-20)
            glEnable (GL_NORMALIZE)
            glScalef(1*(1-0.01*self.distance_from),1*(1-0.01*self.distance_from),1*(1-0.01*self.distance_from))

        glMultMatrixf( self.modelMat )

        for item in Geo.Atom.atoms:
           item.draw()

        for item in Geo.Cylinder.cylinders:
           item.draw()

       

        # Geo.axis(self.axis_state) this used to be here originally

        #glDisable(GL_LIGHT0)
        # glDisable(GL_LIGHTING)
        # glDisable(GL_COLOR_MATERIAL)

        if self.check_enable_extract==2:
                # # self.dots.draw(self.which_dots)
                # mimaf_view_window.dots.draw(self.which_dots)
                extract_instance.draw(self.which_dots)

        if self.marching_squares==True:
            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)

            self.squares.Draw_texture()

            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)

        elif self.marching_cubes==True:

            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)

            # mat_specular = ( 0.1, 0.1, 0.1, 1.0 )
            # mat_shininess = ( 50.0 )
            # mat_ambient=(0.2, 0.2, 0.2, 1.0)

            #glEnable(GL_LIGHT1)

            mat_specular = ( 0.1, 0.1, 0.1, 1.0 )
            mat_shininess = ( 50 )
            mat_ambient=(0.2, 0.2, 0.2, 1.0)
            # mat_diffuse=(1, 1, 1, 1.0)
            # mat_emission=(0.1, 0.1, 0.1, 1.0)

            # glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
            # glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
            # glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
            # glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emission)
            #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)

            glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

            glShadeModel(GL_SMOOTH)
            glDisable(GL_CULL_FACE)
            #glEnable(GL_BLEND)

            #glEnable(GL_BLEND)
            #glBlendFunc(GL_ONE, GL_ZERO)

            #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

            # glEnable(GL_CULL_FACE)
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT,0,self.cubes.normals)

            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3,GL_FLOAT,0,self.cubes.vertices)

            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4,GL_FLOAT,0,self.cubes.colors)
            glDrawArrays(GL_TRIANGLES,0,len(self.cubes.vertices))


            # ##draw normals to see whats happening
            # glBegin(GL_LINES)
            # i=0
            # for item in self.cubes.vertices2:
            #     glVertex3f(item[0],item[1],item[2])
            #     glVertex3f(item[0]-self.cubes.normals2[i][0],item[1]-self.cubes.normals2[i][1],item[2]-self.cubes.normals2[i][2])
            #     i+=1
            # glEnd()
            


            if self.marching_cubes2==True:

                if not self.no_trans_because_clip:
                    glEnable(GL_BLEND)
                    glDepthMask(GL_FALSE)
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

                #glBlendFunc(GL_SRC_ALPHA, GL_ONE)
                #glBlendEquation(GL_FUNC_ADD)
                #glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ZERO)

                glEnableClientState(GL_NORMAL_ARRAY)
                glNormalPointer(GL_FLOAT,0,self.cubes2.normals)

                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(3,GL_FLOAT,0,self.cubes2.vertices)

                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(4,GL_FLOAT,0,self.cubes2.colors)
                glDrawArrays(GL_TRIANGLES,0,len(self.cubes2.vertices))
                glEnable(GL_DEPTH_TEST)
                #glDisable(GL_DEPTH_TEST)
                glDepthMask (GL_TRUE)
                glDisable(GL_BLEND)
                
        if self.marching_squares==True and self.palette_state==2:
            
            width_color=400
            #glViewport(0,0,width_color,50)
            #glClearColor(255.0, 255.0, 255.0, 1.0)
            glScissor(0,0,width_color+30,50)
            glEnable(GL_SCISSOR_TEST)
            glClearColor(255.0, 255.0, 255.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            
            #print(self.squares.red_rgb[0])
            incr_red=( width_color/2)/len(self.squares.red_rgb)
            i=0
            for item in self.squares.red_rgb:
                glScissor(10+i*int(incr_red),10,int(incr_red),30)
                glEnable(GL_SCISSOR_TEST)
                glClearColor(item[0], item[1], item[2], 1.0)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                i+=1

            glScissor(200,10,25,30)
            glEnable(GL_SCISSOR_TEST)
            glClearColor(0, 255.0, 0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            incr_blue=( width_color/2)/len(self.squares.blue_rgb)
            i=0
            for item in self.squares.blue_rgb:
                glScissor(width_color+20-(i+1)*int(incr_blue),10,int(incr_blue),30)
                glEnable(GL_SCISSOR_TEST)
                glClearColor(item[0], item[1], item[2], 1.0)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                i+=1


            #self.squares.Draw_color_palette()
            glDisable(GL_SCISSOR_TEST)

        Geo.axis(self.axis_state)


        if self.save_image==True:
            self.save_image=False

            data, width, height = view_funcs.myglReadColorBuffer(buffers)
            image = Image.frombytes("RGBA", (width, height), data)
            image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason
            image = image.resize((int(width), int(height)), Image.LANCZOS)
            #image.save('Image.png', 'PNG')
            image.save(self.image_name+".png", 'PNG')
            os.chdir(self.path)
            self.update()


    # def myglReadColorBuffer(self,buffers):
    #     fbo, color_buf, depth_buf, width, height = buffers
    #     glPixelStorei(GL_PACK_ALIGNMENT, 1)
    #     glReadBuffer(GL_COLOR_ATTACHMENT0)
    #     data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    #     return data, width, height

    # def myglCreateBuffers(self,width, height):

    #     fbo = glGenFramebuffers(1)
    #     color_buf = glGenRenderbuffers(1)
    #     depth_buf = glGenRenderbuffers(1)

    #     # binds created FBO to context both for read and draw
    #     glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    #     # bind color render buffer
    #     glBindRenderbuffer(GL_RENDERBUFFER, color_buf)
    #     glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, width, height)
    #     glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_buf)

    #     # bind depth render buffer - no need for 2D, but necessary for real 3D rendering
    #     glBindRenderbuffer(GL_RENDERBUFFER, depth_buf)
    #     glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
    #     glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buf)

    #     return fbo, color_buf, depth_buf, width, height

    def resizeGL(self, width, height):
        side = min(width, height)
        #side=min(self.display_0,self.display_1)
        #glViewport(0, 0, self.display_0,self.display_1)
        #print("resize")
        if side < 0:
            return


        #glViewport((width - side) // 2, (height - side) // 2, side, side)
        #glViewport(0, 0, self.display_0, self.display_1)


    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    
    def wheelEvent(self,event):
        self.wheel=event.angleDelta().y()
        if event.angleDelta().y()>0:
            self.distance_from+=3
        else:
            self.distance_from-=3

        self.update()
        

    def mouseMoveEvent(self, event):

        self.dx = event.x() - self.lastPos.x()
        self.dy = event.y() - self.lastPos.y()


        if Qt.LeftButton:
            self.update()

        
        self.lastPos = event.pos()
        
        #self.update()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()
    mimaf_view_window=Mimaf_View_Window()
    widget.addWidget(mimaf_view_window)

    # widget.setFixedWidth(1033)
    # widget.setFixedHeight(728)
    widget.show()

    sys.exit(app.exec_())