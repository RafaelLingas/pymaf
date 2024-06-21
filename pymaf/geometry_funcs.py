#import pygame
#import numpy as np
#import os
#import glm
#from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math



class Atom:
    atoms=[]
    def __init__(self,id,x,y,z):
        self.id=id
        self.xyz=[x,y,z]
        hydro=0.3
        if self.id=="1" or self.id=="H":
            self.id="H"
            self.charge=1
            self.radius=hydro
            self.color=[220,223,232]
        elif self.id=="2" or self.id=="He":
            self.id='He'
            self.radius=hydro
            self.color=[217,255,255]
        elif self.id=="3" or self.id=="Li":
            self.id='Li'
            self.radius=hydro
            self.color=[204,128,255]
        elif self.id=="4" or self.id=="Be":
            self.id='Be'
            self.radius=hydro
            self.color=[194,255,0]
        elif self.id=="5" or self.id=="B":
            self.id='B'
            self.radius=hydro*1.31
            self.color=[255,181,181]
        elif self.id=="6" or self.id=="C":
            self.id='C'
            self.charge=6
            self.radius=hydro*1.41
            self.color=[144,144,144]
        elif self.id=="7" or self.id=="N":
            self.id="N"
            self.charge=7
            self.radius=hydro
            self.color=[48,80,248]
        elif self.id=="8" or self.id=="O":
            self.id="O"
            self.charge=8
            self.radius=hydro
            self.color=[255,13,13]
        elif self.id=="9" or self.id=="F":
            self.id="F"
            self.charge=9
            self.radius=hydro
            self.color=[144,224,80]
        elif self.id=="10" or self.id=="Ne":
            self.id="Ne"
            self.radius=hydro
            self.color=[179,227,245]
        elif self.id=="11" or self.id=="Na":
            self.id="Na"
            self.radius=hydro
            self.color=[171,92,242]
        elif self.id=="12" or self.id=="Mg":
            self.id="Mg"
            self.radius=hydro
            self.color=[138,255,0]
        elif self.id=="17" or self.id=="Cl":
            self.id="Cl"
            self.radius=hydro*1.65
            self.color=[31,240,31]
        elif self.id=="20" or self.id=="Ca":
            self.id="Ca"
            self.radius=hydro*1.62
            self.color=[61,255,0]
        elif self.id=="53" or self.id=="I":
            self.id="I"
            self.radius=hydro*1.65
            self.color=[148,0,148]
        else:
            # self.id="H"
            self.radius=hydro
            self.color=[220,223,232]
        Atom.atoms.append(self)

    def draw(self):

        glPushMatrix()
        sphere = gluNewQuadric()
        glColor3f(self.color[0]/255.0,self.color[1]/255.0,self.color[2]/255.0)
        
        
        glTranslatef(self.xyz[0],self.xyz[1],self.xyz[2])
        gluSphere(sphere, self.radius, 32, 16) #Draw sphere
        gluDeleteQuadric(sphere)
        glPopMatrix()

class Cylinder:
    cylinders=[]
    def __init__(self,xyz,dista,vx,vy,vz,angle):
        Cylinder.cylinders.append(self)
        self.xyz=xyz
        self.distance=dista
        self.vx=vx
        self.vy=vy
        self.vz=vz
        self.theta=angle

    def dist(atom1,atom2):
        distance=math.sqrt((atom2.xyz[0]-atom1.xyz[0])**2+(atom2.xyz[1]-atom1.xyz[1])**2+(atom2.xyz[2]-atom1.xyz[2])**2)
        # if atom1.id==6 and atom2.id==6:
        #     if distance>3:
        #         distance=0
        # else:
        #     distance=0

        return distance

    def Calculate_Cylinders(atoms_):
        dist_list=[]
        for atom1 in atoms_:
            for atom2 in atoms_:
                dist_list.append(Cylinder.dist(atom1,atom2))
            #break
        dist_list=[i for i in dist_list if i !=0]
        min_dist=min(dist_list)
        for atom1 in atoms_:
            for atom2 in atoms_:
                dista=Cylinder.dist(atom1,atom2)
                if dista<(min_dist+min_dist/1.57) and dista!=0:
                    vx=(atom2.xyz[0]-atom1.xyz[0])
                    vy=(atom2.xyz[1]-atom1.xyz[1])
                    vz=(atom2.xyz[2]-atom1.xyz[2])
                    ax=0.0
                    if abs(vz)<0.001:   #### this is stupid but ill change some other time.   nothing works yet other than this problem in draw() when self.vz<0.001
                        vz=0.001

                    if abs(vz)<0.0001:
                        ax=(180/math.pi)*math.acos(vx/dista)
                        if vx<=0.0:
                            ax=-ax
                    
                    else:
                        ax=(180/math.pi)*math.acos(vz/dista)
                        if vz<=0.0:
                            ax=-ax

                    Cylinder(atom1.xyz,dista,vx,vy,vz,ax)

    def draw(self):
        #for item in Cylinder.cylinders:
        glPushMatrix()
        glColor3f(1, 1, 1)
        cylinder_ = gluNewQuadric()
        glTranslatef(self.xyz[0],self.xyz[1],self.xyz[2])

        if abs(self.vz)<0.001:
            glRotatef(90.0,0,1,0) ##Rotate & align with x axis    original
            glRotatef(self.theta,-1.0,0.0,0.0) ##Rotate to point 2 in x-y plane  original
            
        else:
            glRotatef(self.theta,-self.vy*self.vz,self.vx*self.vz,0) ##Rotate about rotation vector

        gluCylinder(cylinder_,0.1,0.1,self.distance/2,32,16)
        gluDeleteQuadric(cylinder_)
        glPopMatrix()

class Get_Geom:
    
    def __init__(self,name,hmodel):
        self.name=name
        self.cube_info=[]
        self.hmodel=hmodel

        with open(name,'r') as input_data:
            for line in input_data:
                self.cube_info.append(line)
        
        if name.endswith('.cube') or name.endswith('.cub'):
            Get_Geom.cube(self)
        elif name.endswith('.txt'):
            Get_Geom.txt(self)
        elif name.endswith('.xyz'):
            Get_Geom.xyz(self)
        elif name.endswith('.gjf'):
            Get_Geom.gjf(self)

    # def gjf(self):
    #     for i in range(8,len(self.cube_info)):
    #         coor=self.cube_info[i].split()
    #         if len(coor)<3:
    #             continue
    #         if 'Bq' in coor:
    #             break
    #         if self.hmodel==2:
    #             if 'H' in coor[0]:
    #                 continue
    #             coor[0]='H'
    #         Atom(coor[0],float(coor[1]),float(coor[2]),float(coor[3]))

    def gjf(self):
        start_flag=False
        for i in range(0,len(self.cube_info)):
            coor=self.cube_info[i].split()
            try:
                if coor:
                    check=int(coor[0])
                    check=int(coor[1])
                    start_flag=True
            except ValueError:
                pass

            if start_flag and not coor:
                break

            if len(coor)<3:
                continue
            if start_flag:
                if 'Bq' in coor:
                    break
                if self.hmodel==2:
                    if 'H' in coor[0]:
                        continue
                    coor[0]='H'
                Atom(coor[0],float(coor[1]),float(coor[2]),float(coor[3]))

    def cube(self):
        atom_num=self.cube_info[2].split()
        atom_num=int(atom_num[0])
        geom_end=6+atom_num
        for i in range(6,geom_end):
            coor=self.cube_info[i].split()
            if self.hmodel==2:
                if 'H' in coor[0] or coor[0]=="1":
                    continue
                coor[0]='H'
            Atom(coor[0],float(coor[2])/1.889725989,float(coor[3])/1.889725989,float(coor[4])/1.889725989)
    
    def txt(self):
        for item in self.cube_info:
            if "MOs" in item:
                break
            coor=item.split()

            if self.hmodel==2:
                if 'H' in item or coor[0]=="1":
                    continue
                coor[1]='H'
            Atom(coor[1],float(coor[2]),float(coor[3]),float(coor[4]))
    
    def xyz(self):
        for item in self.cube_info:

            coor=item.split()
            if len(coor)<3:
                continue

            if self.hmodel==2:
                if 'H' in item:
                    continue
                coor[0]='H'
                
            Atom(coor[0],float(coor[1]),float(coor[2]),float(coor[3]))


class Plane:
    def __init__(self,grid_size,step):
        self.step=step
        self.grid_size=grid_size
        self.edge=self.step*(self.grid_size-1)/2
        # self.x=self.edge
        # self.y=self.edge
        # self.z=self.edge
        self.top_sym=0
        self.side_sym=0

    def three_d(self,sym):

        
        a=self.edge
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
        glDisable(GL_DEPTH_TEST)
        glPushMatrix()
        glColor4f(255.0/255.0, 51/255.0, 95.0/255.0, 0.3)
        #glColor4f(97.0/255.0, 242.0/255.0, 242.0/255.0,0.3)
        glBegin(GL_QUADS)
        ###
        glVertex3f(-a,-a,-a)
        glVertex3f(-a,+a,-a)
        glVertex3f(+a,+a,-a)
        glVertex3f(+a,-a,-a)

        glVertex3f(-a,-a,+a)
        glVertex3f(-a,+a,+a)
        glVertex3f(+a,+a,+a)
        glVertex3f(+a,-a,+a)
        ###
        glVertex3f(-a,-a,-a)
        glVertex3f(-a,-a,+a)
        glVertex3f(-a,+a,+a)
        glVertex3f(-a,+a,-a)

        glVertex3f(+a,-a,-a)
        glVertex3f(+a,-a,+a)
        glVertex3f(+a,+a,+a)
        glVertex3f(+a,+a,-a)
        ###
        glVertex3f(-a,-a,-a)
        glVertex3f(-a,-a,+a)
        glVertex3f(+a,-a,+a)
        glVertex3f(+a,-a,-a)

        glVertex3f(-a,+a,-a)
        glVertex3f(-a,+a,+a)
        glVertex3f(+a,+a,+a)
        glVertex3f(+a,+a,-a)
        ###

        glEnd()
        glPopMatrix()
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

        #### Symmetry Cubes
        
        if sym!='Full':
            z_a=0
            y_a=0
            x_a=0
            if sym=="z":
                z_a=a
            if sym=="y":
                y_a=a
            if sym=="x":
                x_a=a
            if sym=="xy":
                x_a=a
                y_a=a
            if sym=="xz":
                x_a=a
                z_a=a
            if sym=="yz":
                y_a=a
                z_a=a
            if sym=="xyz":
                x_a=a
                y_a=a
                z_a=a

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
            glDisable(GL_DEPTH_TEST)
            glPushMatrix()
            #glColor4f(230.0/255.0, 50.0/255.0, 50.0/255.0, 0.3)
            glColor4f(237.0/255.0, 194.0/255.0, 21.0/255.0,0.3)
            glBegin(GL_QUADS)
            ###
            glVertex3f(-a,-a,-a)
            glVertex3f(-a,+a-y_a,-a)
            glVertex3f(+a-x_a,+a-y_a,-a)
            glVertex3f(+a-x_a,-a,-a)

            glVertex3f(-a,-a,a-z_a)
            glVertex3f(-a,+a-y_a,a-z_a)
            glVertex3f(+a-x_a,+a-y_a,a-z_a)
            glVertex3f(+a-x_a,-a,a-z_a)
            ###
            glVertex3f(-a,-a,-a)
            glVertex3f(-a,-a,a-z_a)
            glVertex3f(-a,+a-y_a,a-z_a)
            glVertex3f(-a,+a-y_a,-a)

            glVertex3f(+a-x_a,-a,-a)
            glVertex3f(+a-x_a,-a,a-z_a)
            glVertex3f(+a-x_a,+a-y_a,a-z_a)
            glVertex3f(+a-x_a,+a-y_a,-a)
            ###
            glVertex3f(-a,-a,-a)
            glVertex3f(-a,-a,a-z_a)
            glVertex3f(+a-x_a,-a,a-z_a)
            glVertex3f(+a-x_a,-a,-a)

            glVertex3f(-a,+a-y_a,-a)
            glVertex3f(-a,+a-y_a,a-z_a)
            glVertex3f(+a-x_a,+a-y_a,a-z_a)
            glVertex3f(+a-x_a,+a-y_a,-a)
            ###

            glEnd()
            glPopMatrix()
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)

    def two_d(self,plane,sym):

        if sym=="z": ###top sym
            self.top_sym=self.edge
        if sym=="x":
            self.side_sym=self.edge
        if sym=="xyz":
            self.top_sym=self.edge
            self.side_sym=self.edge

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
        glPushMatrix()
        glColor4f(255.0/255.0, 51/255.0, 95.0/255.0, 0.3)
        glBegin(GL_POLYGON)
        if plane=="xy":
            glVertex3f(-self.edge,-self.edge,0)
            glVertex3f(-self.edge,self.edge-self.top_sym,0)
            glVertex3f(self.edge-self.side_sym,self.edge-self.top_sym,0)
            glVertex3f(self.edge-self.side_sym,-self.edge,0)
        elif plane=="xz":
            glVertex3f(-self.edge,0,-self.edge)
            glVertex3f(-self.edge,0,self.edge-self.top_sym)
            glVertex3f(self.edge-self.side_sym,0,self.edge-self.top_sym)
            glVertex3f(self.edge-self.side_sym,0,-self.edge)
        elif plane=="yz":
            glVertex3f(0,-self.edge,-self.edge)
            glVertex3f(0,-self.edge,self.edge-self.top_sym)
            glVertex3f(0,self.edge-self.side_sym,self.edge-self.top_sym)
            glVertex3f(0,self.edge-self.side_sym,-self.edge)

        glEnd()
        glPopMatrix()
        glDisable(GL_BLEND)

def axis(state):

    if state==2:
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glBegin(GL_LINES)
        ### X axis
        glColor3f(1.0,0.0,0.0)
        glVertex3f(0,0,0)
        glVertex3f(15,0,0)

        ### Y axis
        glColor3f(0.0,1.0,0.0)
        glVertex3f(0,0,0)
        glVertex3f(0,15,0)

        ### Z axis
        glColor3f(0.0,0.0,1.0)
        glVertex3f(0,0,0)
        glVertex3f(0,0,15)
        
        glEnd()
        glPopMatrix()
        glEnable(GL_LIGHTING)


class extract:
    # def __init__(self,names,plane,grid,step,subtract):
    def __init__(self,grid,step,dimensions,plane):
        self.rez=30
        self.step=step
        self.grid=grid
        self.cols=self.grid
        self.rows=self.grid
        
        self.plane=plane
        # self.subtract=subtract
        self.edge=(grid-1)*step/2
        self.dimensions=dimensions

    
    def draw(self,which_dots):


        if '-' in which_dots:
            try:
                start=int(which_dots[:which_dots.find('-')])
                finish=which_dots[which_dots.find('-'):]
                finish=int(finish.replace('-',''))
            except ValueError:
                start=1
                finish=int(self.grid*self.grid)
        else:
            try:
                start=int(which_dots)
                finish=int(which_dots)
            except ValueError:
                start=1
                finish=int(self.grid*self.grid)

        self.start=start
        self.finish=finish

        if self.dimensions=='3d':

            iter=1
            for i in range(0,self.cols-1):
                for j in range(0,self.rows-1):
                    for k in range(0,self.rows-1):
                        x=-(self.cols-1)*self.step/2+i*self.step
                        y=-(self.cols-1)*self.step/2+j*self.step
                        z=-(self.cols-1)*self.step/2+k*self.step
                

                        if iter>=start and iter<=finish:
                            glColor3f(220/255.0,223/255.0,232/255.0)
                            glPushMatrix()
                            sphere = gluNewQuadric()
                            
                            
                            glTranslatef(x,y,z)
                            gluSphere(sphere, 0.1, 32, 16) #Draw sphere
                            gluDeleteQuadric(sphere)
                            glPopMatrix()
                        else:
                            pass
                            # glColor3f(120/255.0,123/255.0,132/255.0)
                        
                        iter+=1


        else:

            
                
            iter=1
            for i in range(0,self.cols):
                for j in range(0,self.rows):
                    x=-(self.cols-1)*self.step/2+i*self.step
                    y=-(self.cols-1)*self.step/2+j*self.step
                    # z=-(self.cols-1)*self.step/2+k*self.step

                    glPushMatrix()
                    sphere = gluNewQuadric()

                    if iter>=start and iter<=finish:
                        glColor3f(220/255.0,223/255.0,232/255.0)
                    else:
                        glColor3f(120/255.0,123/255.0,132/255.0)
                    
                    
                    if self.plane=='xy':
                        glTranslatef(x,y,0)
                    elif self.plane=='xz':
                        glTranslatef(x,0,y)
                    else:
                        glTranslatef(0,x,y)
                    gluSphere(sphere, 0.1, 32, 16) #Draw sphere
                    gluDeleteQuadric(sphere)
                    glPopMatrix()
                    iter+=1

    def isolate(self,info):
        output=open('isolated.txt',"w+")

        for i in range(1,len(info)+1):
            if i>=self.start and i<=self.finish:
                output.write(str(info[i-1])+"\n")
            else:
                output.write("0\n")

        output.close()

    def get_values(self,info):
        
        output=open('nics.txt',"w+")

        for i in range(1,len(info)+1):
            if i>=self.start and i<=self.finish:
                output.write(str(info[i-1])+"\n")

        output.close()
