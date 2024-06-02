#from asyncio.windows_events import NULL
#from colorsys import hls_to_rgb
#from PIL import ImageColor
#from pygame import *
#import os
from EasyDraw.Vector import Vector
from colour import Color
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glm
from PIL import Image
import numpy as np
import pygame
from collections import defaultdict

class marching_squares():
    def __init__(self,names,plane,grid,step,subtract,from_iso,to_iso,step_color,draw_lines):
        self.field={}
        self.rez=30
        self.step=step
        self.iso=0
        self.grid=grid
        self.cols=self.grid
        self.rows=self.grid
        self.names=names
        self.plane=plane
        self.subtract=subtract
        self.edge=(grid-1)*step/2

        self.from_iso=from_iso
        self.to_iso=to_iso
        self.step_color=step_color
        self.draw_lines=draw_lines

        self.Read_file()
        self.Colors()
        self.Calc_Field()
        self.Create_texture()


        #self.read_texture()



    def Draw_texture(self):
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        
        if self.plane=="yz":

            glPushMatrix()
            glBegin(GL_QUADS)
            glTexCoord2f(0,0)
            #glTexCoord2f(-1.0,-1.0)
            glVertex3f(0,-self.edge,-self.edge)
            glTexCoord2f(0,1)
            #glTexCoord2f(-1.0,1.0)
            glVertex3f(0,-self.edge,self.edge)
            #glTexCoord2f(1.0,1.0)
            glTexCoord2f(1.0,1.0)
            glVertex3f(0,self.edge,self.edge)
            #glTexCoord2f(1.0,-1.0)
            glTexCoord2f(1,0)
            glVertex3f(0,self.edge,-self.edge)
            glEnd()
            glPopMatrix()

        elif self.plane=="xz":

            glPushMatrix()
            glBegin(GL_QUADS)
            glTexCoord2f(0,0)
            #glTexCoord2f(-1.0,-1.0)
            glVertex3f(-self.edge,0,-self.edge)
            glTexCoord2f(0,1)
            #glTexCoord2f(-1.0,1.0)
            glVertex3f(-self.edge,0,self.edge)
            #glTexCoord2f(1.0,1.0)
            glTexCoord2f(1.0,1.0)
            glVertex3f(self.edge,0,self.edge)
            #glTexCoord2f(1.0,-1.0)
            glTexCoord2f(1,0)
            glVertex3f(self.edge,0,-self.edge)
            glEnd()
            glPopMatrix()

        elif self.plane=="xy":

            glPushMatrix()
            glBegin(GL_QUADS)
            glTexCoord2f(0,0)
            #glTexCoord2f(-1.0,-1.0)
            glVertex3f(-self.edge,-self.edge,0)
            glTexCoord2f(0,1)
            #glTexCoord2f(-1.0,1.0)
            glVertex3f(-self.edge,self.edge,0)
            #glTexCoord2f(1.0,1.0)
            glTexCoord2f(1.0,1.0)
            glVertex3f(self.edge,self.edge,0)
            #glTexCoord2f(1.0,-1.0)
            glTexCoord2f(1,0)
            glVertex3f(self.edge,-self.edge,0)
            glEnd()
            glPopMatrix()

        # glColor3f(0.4,0.4,0.4)
        # glPushMatrix()
        # glTranslatef(0,-5,0)
        # sphere=gluNewQuadric()
        # gluSphere(sphere, 2, 16, 8) #Draw sphere
        # gluDeleteQuadric(sphere)
        # glPopMatrix()

        glDisable(GL_TEXTURE_2D)
                   


    def Colors(self):
        
        red=Color("#ff0000")
        self.red_color=list(red.range_to(Color("#c6fc03"),abs(int(self.to_iso/self.step_color))))
        blue=Color("Blue")
        self.blue_color=list(blue.range_to(Color("#03fcb5"),abs(int(self.from_iso/self.step_color))))

        self.red_rgb=[]
        for item in self.red_color:
            self.red_rgb.append(item.rgb)
        
        self.blue_rgb=[]
        for item in self.blue_color:
            self.blue_rgb.append(item.rgb)


        # height=200
        # width=30
        # incr_red=(height/2)/len(self.red_color)
        # incr_blue=(height/2)/len(self.blue_color)
        # color_palette = pygame.Surface((width,height))
        # color_palette.fill("Green")
        # i=0
        # for item in self.red_color:
        #     pygame.draw.polygon(color_palette,item.hex_l,((0,i*incr_red),(width,i*incr_red),
        #     (width,(i+1)*incr_red),(0,(i+1)*incr_red)),width=0)
        #     i+=1
        
        # i=0
        # for item in self.blue_color:
        #     pygame.draw.polygon(color_palette,item.hex_l,((0,height-i*incr_blue),
        #     (width,height-i*incr_blue),(width,height-(i+1)*incr_blue),(0,height-(i+1)*incr_blue)),width=0)
        #     i+=1
        #self.red_color[len(self.red_color)-k].hex_l


        #pygame.image.save(color_palette, "color_palette"+".png")

        #self.read_texture("color_palette.png")

    def Draw_color_palette(self):
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.texture_color)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        glPushMatrix()
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(0,0,0)
        glTexCoord2f(0,1)
        glVertex3f(0,50,0)
        glTexCoord2f(1.0,1.0)
        glVertex3f(700,50,0)
        glTexCoord2f(1,0)
        glVertex3f(700,0,0)
        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def Calc_Field(self):
        k=0
        for i in range(0,self.cols):
            for j in range(0,self.rows):
                self.field[i,j]=float(self.cubes[k])

                k+=1

    def Merge_files(names,subtract):
        cube_info=[]
        cubes={}

        for item in names:
            i=0
            with open(item,'r') as input_data:
                for line in input_data:
                    try:
                        if subtract:
                            cubes[i]-=float(line)
                        else:
                            cubes[i]+=float(line)
                    except KeyError:
                        cubes[i]=float(line)
                    i+=1

        new_name=''
        for item in names:
            new_name+=item.replace('.txt','_')

        output=open(new_name+'.txt',"w+")
        for i in range(0,len(cubes)):
            output.write(str(cubes[i])+"\n")
        output.close()


    def Read_file(self):
        self.cube_info=[]
        self.cubes={}

        for item in self.names:
            i=0
            with open(item,'r') as input_data:
                for line in input_data:
                    #self.cube_info.append(line)
                    try:
                        if self.subtract:
                            self.cubes[i]-=float(line)
                        else:
                            self.cubes[i]+=float(line)
                    except KeyError:
                        self.cubes[i]=float(line)
                    i+=1

        


    def getState(self, num_1, num_2, num_3, num_4,iso) -> int:

        if num_4>=iso:
            num_4=1
        else:
            num_4=0

        if num_3>=iso:
            num_3=1
        else:
            num_3=0

        if num_2>=iso:
            num_2=1
        else:
            num_2=0

        if num_1>=iso:
            num_1=1
        else:
            num_1=0


        return num_1*8 + num_2*4 + num_3*2 + num_4*1


    def generate_vector(self,x_pos, y_pos,iso_1,iso_2,iso_3,iso_4,iso):

        global half_a
        global half_b
        global half_c
        global half_d

        try:
            half_a = Vector(x_pos + (iso-iso_1)*self.rez/(iso_2-iso_1),y_pos)
        except ZeroDivisionError:
            half_a = Vector(x_pos + self.rez*0.5,y_pos)
        try:
            half_b = Vector(x_pos + self.rez,y_pos+(iso-iso_2)*self.rez/(iso_3-iso_2))
        except ZeroDivisionError:    
            half_b = Vector(x_pos + self.rez,y_pos+self.rez*0.5)
        try:
            half_c = Vector(x_pos + (iso-iso_4)*self.rez/(iso_3-iso_4), y_pos+self.rez)
        except ZeroDivisionError:
            half_c = Vector(x_pos + self.rez*0.5, y_pos+self.rez)
        try:
            #half_d = Vector(x_pos, y_pos +(iso-iso_4)*rez/(iso_1-iso_4))
            half_d = Vector(x_pos, y_pos +(iso-iso_1)*self.rez/(iso_4-iso_1))
        except ZeroDivisionError:
            half_d = Vector(x_pos, y_pos +self.rez*0.5)
        return half_a, half_b, half_c, half_d


    def generate_case(self,x_pos, y_pos,iso_1,iso_2,iso_3,iso_4,iso):

        half_a, half_b, half_c, half_d = self.generate_vector(
            x_pos, y_pos,iso_1,iso_2,iso_3,iso_4,iso)


        case = {
            0: (),
            1: (half_c, half_d),
            2: (half_b, half_c),
            3: (half_b, half_d),
            4: (half_a, half_b),
            5: [(half_a, half_d),
                (half_b, half_c)],
            6: (half_a, half_c),
            7: (half_a, half_d),
            8: (half_a, half_d),
            9: (half_a, half_c),
            10: [(half_a, half_b),
                (half_d, half_c)],
            11: (half_a, half_b),
            12: (half_b, half_d),
            13: (half_b, half_c),
            14: (half_d, half_c),
            15: ()
        }
        return case


    def fill_squares(self,state_,a,b,c,d,color_,x_,y_,screen):
        one=Vector(x_,y_)
        two=Vector(x_+self.rez,y_)
        three=Vector(x_+self.rez,y_+self.rez)
        four=Vector(x_,y_+self.rez)

        if self.draw_lines==True:
            line_width=1
        else:
            line_width=0


        if state_==0:
            pass
        elif state_==1:
            pygame.draw.polygon(screen,color_,((d.x,d.y),(c.x,c.y),(four.x,four.y)),width=0)
            pygame.draw.line(screen,("Black"),(d.x,d.y),(c.x,c.y),width=line_width)
        elif state_==2:
            pygame.draw.polygon(screen,color_,((b.x,b.y),(c.x,c.y),(three.x,three.y)),width=0)
            pygame.draw.line(screen,("Black"),(b.x,b.y),(c.x,c.y),width=line_width)
        elif state_==3:
            pygame.draw.polygon(screen,color_,((d.x,d.y),(b.x,b.y),(three.x,three.y),(four.x,four.y)),width=0)
            pygame.draw.line(screen,("Black"),(d.x,d.y),(b.x,b.y),width=line_width)
        elif state_==4:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(b.x,b.y),(two.x,two.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(b.x,b.y),width=line_width)
        elif state_==5:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(two.x,two.y),(b.x,b.y),(c.x,c.y),(three.x,three.y),(d.x,d.y)),width=0)
            pygame.draw.lines(screen,("Black"),True,((a.x,a.y),(two.x,two.y),(b.x,b.y),(c.x,c.y),(three.x,three.y),(d.x,d.y)),width=line_width)
        elif state_==6:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(c.x,c.y),(three.x,three.y),(two.x,two.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(c.x,c.y),width=line_width)
        elif state_==7:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(two.x,two.y),(three.x,three.y),(four.x,four.y),(d.x,d.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(d.x,d.y),width=line_width)
        elif state_==8:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(d.x,d.y),(one.x,one.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(d.x,d.y),width=line_width)
        elif state_==9:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(c.x,c.y),(four.x,four.y),(one.x,one.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(c.x,c.y),width=line_width)
        elif state_==10:

            pygame.draw.polygon(screen,color_,((one.x,one.y),(a.x,a.y),(b.x,b.y),(three.x,three.y),(c.x,c.y),(d.x,d.y)),width=0)
            pygame.draw.lines(screen,("Black"),True,((one.x,one.y),(a.x,a.y),(b.x,b.y),(three.x,three.y),(c.x,c.y),(d.x,d.y)),width=line_width)
        elif state_==11:
            pygame.draw.polygon(screen,color_,((a.x,a.y),(b.x,b.y),(three.x,three.y),(four.x,four.y),(one.x,one.y)),width=0)
            pygame.draw.line(screen,("Black"),(a.x,a.y),(b.x,b.y),width=line_width)
        elif state_==12:
            pygame.draw.polygon(screen,color_,((d.x,d.y),(b.x,b.y),(two.x,two.y),(one.x,one.y)),width=0)
            pygame.draw.line(screen,("Black"),(d.x,d.y),(b.x,b.y),width=line_width)
        elif state_==13:
            pygame.draw.polygon(screen,color_,((b.x,b.y),(c.x,c.y),(four.x,four.y),(one.x,one.y),(two.x,two.y)),width=0)
            pygame.draw.line(screen,("Black"),(b.x,b.y),(c.x,c.y),width=line_width)
        elif state_==14:
            pygame.draw.polygon(screen,color_,((d.x,d.y),(c.x,c.y),(three.x,three.y),(two.x,two.y),(one.x,one.y)),width=0)
            pygame.draw.line(screen,("Black"),(d.x,d.y),(c.x,c.y),width=line_width)
        elif state_==15:
            pygame.draw.polygon(screen,color_,((one.x,one.y),(two.x,two.y),(three.x,three.y),(four.x,four.y)),width=0)
    

    def read_texture(self,pic):

        img = Image.open(pic)   ### I could also convert it to not have an alpha channel:     img = img.convert("RGB")
        if img.mode=="RGB":
            format=GL_RGB
        else: 
            format=GL_RGBA

        img_data = np.array(img, dtype=np.int8)
        ### THIS IS WHAT I HAD BEFORE AND WAS LAGGING IN THE LATEST VERSION
        # img_data = np.array(list(img.getdata()), np.int8) 

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0,
                    format, GL_UNSIGNED_BYTE, img_data)     ########               GL_RGB for tga files, GL_RGBA for png files
        
        
        if pic=="temp.png":
            self.texture_id=texture_id
        elif pic=="color_palette.png":
            self.texture_color=texture_id



    def Create_texture(self):
        screen = pygame.Surface(((self.grid-1)*self.rez,(self.grid-1)*self.rez))
        screen.fill("Green")
        for i in range(0,self.cols-1):
            for j in range(0,self.rows-1):
                x=i*self.rez
                y=j*self.rez
               
                incr=self.step_color
                k=1
                while incr<self.to_iso:

                    
                    state=self.getState(self.field[i,j],self.field[i+1,j],
                    self.field[i+1,j+1],self.field[i,j+1],incr)
                    case_dict=self.generate_case(x,y,self.field[i,j],self.field[i+1,j],
                    self.field[i+1,j+1],self.field[i,j+1],incr)
                    #case_line_points = case_dict[state]


                    self.fill_squares(state,half_a,half_b,half_c,half_d,self.red_color[len(self.red_color)-k].hex_l,x,y,screen)
                    k+=1
                    incr+=self.step_color


                incr=-self.step_color
                k=1
                while incr>=self.from_iso:

                    
                    state=self.getState(self.field[i,j],self.field[i+1,j],
                    self.field[i+1,j+1],self.field[i,j+1],incr)
                    case_dict=self.generate_case(x,y,self.field[i,j],self.field[i+1,j],
                    self.field[i+1,j+1],self.field[i,j+1],incr)
                    #case_line_points = case_dict[state]


                    self.fill_squares(15-state,half_a,half_b,half_c,half_d,self.blue_color[len(self.blue_color)-k].hex_l,x,y,screen)
                    k+=1
                    incr-=self.step_color


        pygame.image.save(screen, "temp"+".png")



triangulationTable = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 8, 3, 9, 8, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 2, 10, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 8, 3, 2, 10, 8, 10, 9, 8, -1, -1, -1, -1, -1, -1, -1],
    [3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 11, 2, 8, 11, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 11, 2, 1, 9, 11, 9, 8, 11, -1, -1, -1, -1, -1, -1, -1],
    [3, 10, 1, 11, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 10, 1, 0, 8, 10, 8, 11, 10, -1, -1, -1, -1, -1, -1, -1],
    [3, 9, 0, 3, 11, 9, 11, 10, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 4, 7, 3, 0, 4, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1],
    [9, 2, 10, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
    [2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, -1],
    [8, 4, 7, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 4, 7, 11, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 1, 8, 4, 7, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
    [4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1, -1, -1, -1, -1],
    [3, 10, 1, 3, 11, 10, 7, 8, 4, -1, -1, -1, -1, -1, -1, -1],
    [1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4, -1, -1, -1, -1],
    [4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3, -1, -1, -1, -1],
    [4, 7, 11, 4, 11, 9, 9, 11, 10, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 5, 4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 1, 2, 10, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
    [5, 2, 10, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, -1],
    [2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, -1],
    [9, 5, 4, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 11, 2, 0, 8, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1],
    [0, 5, 4, 0, 1, 5, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1],
    [2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5, -1, -1, -1, -1],
    [10, 3, 11, 10, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10, -1, -1, -1, -1],
    [5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3, -1, -1, -1, -1],
    [5, 4, 8, 5, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1],
    [9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 3, 0, 9, 5, 3, 5, 7, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, -1],
    [1, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 7, 8, 9, 5, 7, 10, 1, 2, -1, -1, -1, -1, -1, -1, -1],
    [10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3, -1, -1, -1, -1],
    [8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2, -1, -1, -1, -1],
    [2, 10, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1],
    [7, 9, 5, 7, 8, 9, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11, -1, -1, -1, -1],
    [2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, -1],
    [11, 2, 1, 11, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11, -1, -1, -1, -1],
    [5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0, -1],
    [11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0, -1],
    [11, 10, 5, 7, 11, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 1, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 8, 3, 1, 9, 8, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 5, 2, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, -1],
    [9, 6, 5, 9, 0, 6, 0, 2, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, -1],
    [2, 3, 11, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 0, 8, 11, 2, 0, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11, -1, -1, -1, -1],
    [6, 3, 11, 6, 5, 3, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6, -1, -1, -1, -1],
    [3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9, -1, -1, -1, -1],
    [6, 5, 9, 6, 9, 11, 11, 9, 8, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 3, 0, 4, 7, 3, 6, 5, 10, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 5, 10, 6, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1],
    [10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, -1],
    [6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, -1],
    [8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, -1],
    [7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, -1],
    [3, 11, 2, 7, 8, 4, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1],
    [5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11, -1, -1, -1, -1],
    [0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1],
    [9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6, -1],
    [8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6, -1, -1, -1, -1],
    [5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11, -1],
    [0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7, -1],
    [6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9, -1, -1, -1, -1],
    [10, 4, 9, 6, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 10, 6, 4, 9, 10, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1],
    [10, 0, 1, 10, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, -1],
    [8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10, -1, -1, -1, -1],
    [1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, -1],
    [0, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1],
    [10, 4, 9, 10, 6, 4, 11, 2, 3, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6, -1, -1, -1, -1],
    [3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10, -1, -1, -1, -1],
    [6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1, -1],
    [9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3, -1, -1, -1, -1],
    [8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1, -1],
    [3, 11, 6, 3, 6, 0, 0, 6, 4, -1, -1, -1, -1, -1, -1, -1],
    [6, 4, 8, 11, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 10, 6, 7, 8, 10, 8, 9, 10, -1, -1, -1, -1, -1, -1, -1],
    [0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10, -1, -1, -1, -1],
    [10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0, -1, -1, -1, -1],
    [10, 6, 7, 10, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1, -1],
    [2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, -1],
    [7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, -1],
    [7, 3, 2, 6, 7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7, -1, -1, -1, -1],
    [2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7, -1],
    [1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11, -1],
    [11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1, -1, -1, -1, -1],
    [8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6, -1],
    [0, 9, 1, 11, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0, -1, -1, -1, -1],
    [7, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 8, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 9, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 1, 9, 8, 3, 1, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
    [10, 1, 2, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 3, 0, 8, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
    [2, 9, 0, 2, 10, 9, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1],
    [6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8, -1, -1, -1, -1],
    [7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1, -1, -1, -1, -1, -1],
    [2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1],
    [1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1, -1, -1, -1],
    [10, 7, 6, 10, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, -1],
    [10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8, -1, -1, -1, -1],
    [0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7, -1, -1, -1, -1],
    [7, 6, 10, 7, 10, 8, 8, 10, 9, -1, -1, -1, -1, -1, -1, -1],
    [6, 8, 4, 11, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 6, 11, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1, -1],
    [8, 6, 11, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, -1],
    [9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6, -1, -1, -1, -1],
    [6, 8, 4, 6, 11, 8, 2, 10, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6, -1, -1, -1, -1],
    [4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9, -1, -1, -1, -1],
    [10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3, -1],
    [8, 2, 3, 8, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1],
    [0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8, -1, -1, -1, -1],
    [1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, -1],
    [8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1, -1, -1, -1, -1],
    [10, 1, 0, 10, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, -1],
    [4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3, -1],
    [10, 9, 4, 6, 10, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 5, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 4, 9, 5, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1],
    [5, 0, 1, 5, 4, 0, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
    [11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, -1],
    [9, 5, 4, 10, 1, 2, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1],
    [6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5, -1, -1, -1, -1],
    [7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2, -1, -1, -1, -1],
    [3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6, -1],
    [7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, -1],
    [3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, -1],
    [6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8, -1],
    [9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, -1],
    [1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4, -1],
    [4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10, -1],
    [7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10, -1, -1, -1, -1],
    [6, 9, 5, 6, 11, 9, 11, 8, 9, -1, -1, -1, -1, -1, -1, -1],
    [3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, -1],
    [0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11, -1, -1, -1, -1],
    [6, 11, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6, -1, -1, -1, -1],
    [0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10, -1],
    [11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5, -1],
    [6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3, -1, -1, -1, -1],
    [5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2, -1, -1, -1, -1],
    [9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, -1],
    [1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8, -1],
    [1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6, -1],
    [10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, -1],
    [0, 3, 8, 5, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [10, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 5, 10, 7, 5, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [11, 5, 10, 11, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, -1],
    [5, 11, 7, 5, 10, 11, 1, 9, 0, -1, -1, -1, -1, -1, -1, -1],
    [10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, -1],
    [11, 1, 2, 11, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11, -1, -1, -1, -1],
    [9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7, -1, -1, -1, -1],
    [7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2, -1],
    [2, 5, 10, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1],
    [8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5, -1, -1, -1, -1],
    [9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2, -1, -1, -1, -1],
    [9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2, -1],
    [1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 7, 0, 7, 1, 1, 7, 5, -1, -1, -1, -1, -1, -1, -1],
    [9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, -1],
    [9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [5, 8, 4, 5, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1],
    [5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0, -1, -1, -1, -1],
    [0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5, -1, -1, -1, -1],
    [10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4, -1],
    [2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8, -1, -1, -1, -1],
    [0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11, -1],
    [0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5, -1],
    [9, 4, 5, 2, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, -1],
    [5, 10, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, -1],
    [3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9, -1],
    [5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, -1],
    [8, 4, 5, 8, 5, 3, 3, 5, 1, -1, -1, -1, -1, -1, -1, -1],
    [0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5, -1, -1, -1, -1],
    [9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 11, 7, 4, 9, 11, 9, 10, 11, -1, -1, -1, -1, -1, -1, -1],
    [0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11, -1, -1, -1, -1],
    [1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11, -1, -1, -1, -1],
    [3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4, -1],
    [4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2, -1, -1, -1, -1],
    [9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3, -1],
    [11, 7, 4, 11, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1, -1, -1],
    [11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, -1],
    [2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, -1],
    [9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7, -1],
    [3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10, -1],
    [1, 10, 2, 8, 7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, -1],
    [4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1, -1, -1, -1, -1],
    [4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [4, 8, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [9, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 9, 3, 9, 11, 11, 9, 10, -1, -1, -1, -1, -1, -1, -1],
    [0, 1, 10, 0, 10, 8, 8, 10, 11, -1, -1, -1, -1, -1, -1, -1],
    [3, 1, 10, 11, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 2, 11, 1, 11, 9, 9, 11, 8, -1, -1, -1, -1, -1, -1, -1],
    [3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9, -1, -1, -1, -1],
    [0, 2, 11, 8, 0, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [3, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 8, 2, 8, 10, 10, 8, 9, -1, -1, -1, -1, -1, -1, -1],
    [9, 10, 2, 0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8, -1, -1, -1, -1],
    [1, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 9, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]

class marching_cubes():
    def __init__(self,names,grid,step,iso,subtract,color_pos,color_neg,smooth,clip_axis):
        self.field={}
        #self.rez=30
        self.names=names
        self.step=step
        self.cols=grid
        self.rows=grid
        self.iso=iso
        self.subtract=subtract
        self.pos_vertices=[]
        self.neg_vertices=[]
        self.color_pos=color_pos
        self.color_neg=color_neg
        self.smooth=smooth

        self.clip_axis=clip_axis

        self.Read_file()
        self.Calc_Field()
        self.Get_Vertices()
        self.Get_Normals()

    def Get_Normals(self):
        self.vertices=[]
        self.colors= []
        self.normals=[]
        #self.normals2=[]#other direction
        converted=[]
        self.angles=[]

        ###new triangles
        # self.vertices2=[]
        # self.colors2=[]
        # self.normals2=[]
        # converted2=[]
        ###

        for item in self.pos_vertices:
            if item[0]==-0.0 or item[0]==0:
                item[0]=0.0
            elif item[1]==-0.0 or item[1]==0:
                item[1]=0.0
            elif item[2]==-0.0 or item[2]==0:
                item[2]=0.0

            self.vertices.append(item)
            self.colors.append(self.color_pos)
            converted.append(str(item))

        for item in self.neg_vertices:
            if item[0]==-0.0 or item[0]==0:
                item[0]=0.0
            elif item[1]==-0.0 or item[1]==0:
                item[1]=0.0
            elif item[2]==-0.0 or item[2]==0:
                item[2]=0.0

            self.vertices.append(item)
            self.colors.append(self.color_neg)
            converted.append(str(item))


        shared = defaultdict(list)
        for i,item in enumerate(converted):
            shared[item].append(i)
        shared = {k:v for k,v in shared.items()} #if len(v)>0}


        if self.smooth:
            for vertex in converted:
                average_pos=glm.vec3(0,0,0)
                for i in range(0,len(shared[vertex])):
                    if shared[vertex][i]%3==0:
                        average_pos+=glm.vec3(self.vertices[shared[vertex][i]+1])+glm.vec3(self.vertices[shared[vertex][i]+2])
                    if shared[vertex][i]%3==1:
                        average_pos+=glm.vec3(self.vertices[shared[vertex][i]-1])+glm.vec3(self.vertices[shared[vertex][i]+1])
                    if shared[vertex][i]%3==2:
                        average_pos+=glm.vec3(self.vertices[shared[vertex][i]-2])+glm.vec3(self.vertices[shared[vertex][i]-1])
                average_pos=average_pos/(2*len(shared[vertex]))
                for i in range(0,len(shared[vertex])):
                    pass
                    # self.vertices[shared[vertex][i]][0]=(self.vertices[shared[vertex][i]][0]+average_pos.x)/2
                    # self.vertices[shared[vertex][i]][1]=(self.vertices[shared[vertex][i]][1]+average_pos.y)/2
                    # self.vertices[shared[vertex][i]][2]=(self.vertices[shared[vertex][i]][2]+average_pos.z)/2

                    self.vertices[shared[vertex][i]][0]=(4*self.vertices[shared[vertex][i]][0]+average_pos.x)/5
                    self.vertices[shared[vertex][i]][1]=(4*self.vertices[shared[vertex][i]][1]+average_pos.y)/5
                    self.vertices[shared[vertex][i]][2]=(4*self.vertices[shared[vertex][i]][2]+average_pos.z)/5



        ###get normals
        for i in range(0,len(self.vertices),3):

            v1=glm.vec3(self.vertices[i])
            v2=glm.vec3(self.vertices[i+1])
            v3=glm.vec3(self.vertices[i+2])
            
            edge1=v2-v1
            edge2=v3-v1
            edge3=v3-v2

            # try:
            #     angle_1=glm.degrees(glm.acos((edge1.x*edge2.x+edge1.y*edge2.y+edge1.z*edge2.z)/
            #     (glm.length(edge1)*glm.length(edge2))))
            #     angle_2=glm.degrees(glm.acos((edge1.x*edge3.x+edge1.y*edge3.y+edge1.z*edge3.z)/
            #     (glm.length(edge1)*glm.length(edge3))))
            #     angle_3=glm.degrees(glm.acos((edge3.x*edge2.x+edge3.y*edge2.y+edge3.z*edge2.z)/
            #     (glm.length(edge3)*glm.length(edge2))))
            # except ZeroDivisionError:
            #     angle_1=0.0
            #     angle_2=0.0
            #     angle_3=0.0


            normal=np.cross(edge1,edge2)/2

            self.normals.append(normal)
            self.normals.append(normal)
            self.normals.append(normal)

            # self.angles.append(angle_1)
            # self.angles.append(angle_2)
            # self.angles.append(angle_3)


        ###average normals
        for vertex in converted:
            temp=0
            #angle_sum=0
            #temp2=0
            #norm_temp=[]
            #angle_temp=[]
            #flag=False
            for i in range(0,len(shared[vertex])):
                temp+=self.normals[shared[vertex][i]]#*self.angles[shared[vertex][i]]/360
                #angle_sum+=self.angles[shared[vertex][i]]
                #norm_temp.append(self.normals[shared[vertex][i]])
                #angle_temp.append(self.angles[shared[vertex][i]])

            # for item in norm_temp:
            #     for other_item in norm_temp:
            #         theta=glm.degrees(glm.acos((item[0]*other_item[0]+item[1]*other_item[1]+item[2]*other_item[2])/
            #     (glm.length(item)*glm.length(other_item))))
            #         if theta>39.0:
            #             flag=True
            #             for i in range(0,len(shared[vertex])):
            #                 #self.vertices2.append(self.vertices[shared[vertex][i]])
            #                 #self.normals2.append(glm.normalize(temp))
            #                 #self.colors[shared[vertex][i]]=[255,0,0,0]
            #                 pass

            # for i in range(0,len(norm_temp)):
            #     temp+=norm_temp[i]*angle_temp[i]/angle_sum
            #     self.normals[shared[vertex][i]]=glm.normalize(norm_temp[i]*angle_temp[i]/angle_sum)

            #temp=temp/angle_sum
            temp=glm.normalize(temp)
            #if flag==False:
            for i in range(0,len(shared[vertex])):
                self.normals[shared[vertex][i]]=temp
        

        self.vertices=np.array(self.vertices,dtype=np.float32)
        self.colors=np.array(self.colors,dtype=np.float32)
        self.normals=np.array(self.normals,dtype=np.float32)




    def Get_Vertices(self):

        if self.clip_axis==0:
            clip_x=0
            clip_y=0
            clip_z=0
        elif self.clip_axis=='x':
            clip_x=int((self.cols-1)/2)
            clip_y=0
            clip_z=0
        elif self.clip_axis=='y':
            clip_x=0
            clip_y=int((self.cols-1)/2)
            clip_z=0
        elif self.clip_axis=='z':
            clip_x=0
            clip_y=0
            clip_z=int((self.cols-1)/2)

        for i in range(0,self.cols-1-clip_x):
            for j in range(0,self.rows-1-clip_y):
                for k in range(0,self.rows-1-clip_z):
        # for i in range(int((self.cols-1)/2)-1,int((self.cols-1)/2)+1): ###get half like vmd
        #     for j in range(15,self.rows-17):
        #         for k in range(0,int((self.rows-1)/2)):
                    x=-(self.cols-1)*self.step/2+i*self.step
                    y=-(self.cols-1)*self.step/2+j*self.step
                    z=-(self.cols-1)*self.step/2+k*self.step

                    state=self.getState(self.field[i,j,k],self.field[i+1,j,k],
                    self.field[i+1,j,k+1],self.field[i,j,k+1],self.field[i,j+1,k],
                    self.field[i+1,j+1,k],self.field[i+1,j+1,k+1],self.field[i,j+1,k+1],self.iso)

                    self.generate_vector(x,y,z,self.field[i,j,k],self.field[i+1,j,k],
                    self.field[i+1,j,k+1],self.field[i,j,k+1],self.field[i,j+1,k],
                    self.field[i+1,j+1,k],self.field[i+1,j+1,k+1],self.field[i,j+1,k+1],self.iso)

                    for edgeIndex in triangulationTable[state]:
                        if (edgeIndex != -1):
                            pass
                            self.pos_vertices.append([round(self.edges[edgeIndex].x,12),round(self.edges[edgeIndex].y,12),round(self.edges[edgeIndex].z,12)])
                    
                    ###negative
                    state=self.getState(self.field[i,j,k],self.field[i+1,j,k],
                    self.field[i+1,j,k+1],self.field[i,j,k+1],self.field[i,j+1,k],
                    self.field[i+1,j+1,k],self.field[i+1,j+1,k+1],self.field[i,j+1,k+1],-self.iso)

                    self.generate_vector(x,y,z,self.field[i,j,k],self.field[i+1,j,k],
                    self.field[i+1,j,k+1],self.field[i,j,k+1],self.field[i,j+1,k],
                    self.field[i+1,j+1,k],self.field[i+1,j+1,k+1],self.field[i,j+1,k+1],-self.iso)

                    for edgeIndex in triangulationTable[state]:
                        if (edgeIndex != -1):
                            pass
                            self.neg_vertices.append([round(self.edges[edgeIndex].x,12),round(self.edges[edgeIndex].y,12),round(self.edges[edgeIndex].z,12)])

    def generate_vector(self,x_pos, y_pos,z_pos,iso_0,iso_1,iso_2,
    iso_3,iso_4,iso_5,iso_6,iso_7,iso):

        self.edges=[0,0,0,0,0,0,0,0,0,0,0,0]

        try:
            self.edges[0]=glm.vec3(x_pos + (iso-iso_0)*self.step/(iso_1-iso_0),y_pos,z_pos)
        except ZeroDivisionError:
            self.edges[0]=glm.vec3(x_pos + self.step/2,y_pos,z_pos)

        try:
            self.edges[1]=glm.vec3(x_pos + self.step,y_pos,z_pos + (iso-iso_1)*self.step/(iso_2-iso_1))
        except ZeroDivisionError:
            self.edges[1]=glm.vec3(x_pos + self.step,y_pos,z_pos + self.step/2)

        try:
            self.edges[2]=glm.vec3(x_pos+ (iso-iso_3)*self.step/(iso_2-iso_3) ,y_pos,z_pos+ self.step)
        except ZeroDivisionError:
            self.edges[2]=glm.vec3(x_pos+self.step/2 ,y_pos,z_pos+ self.step)

        try:
            self.edges[3]=glm.vec3(x_pos ,y_pos,z_pos+ (iso-iso_0)*self.step/(iso_3-iso_0))
        except ZeroDivisionError:
            self.edges[3]=glm.vec3(x_pos ,y_pos,z_pos+ self.step/2)

        try:
            self.edges[4]=glm.vec3(x_pos+ (iso-iso_4)*self.step/(iso_5-iso_4) ,y_pos+self.step,z_pos)
        except ZeroDivisionError:
            self.edges[4]=glm.vec3(x_pos+self.step/2 ,y_pos+self.step,z_pos)

        try:
            self.edges[5]=glm.vec3(x_pos+self.step ,y_pos+self.step,z_pos+ (iso-iso_5)*self.step/(iso_6-iso_5))
        except ZeroDivisionError:
            self.edges[5]=glm.vec3(x_pos+self.step ,y_pos+self.step,z_pos+ self.step/2)

        try:
            self.edges[6]=glm.vec3(x_pos+ (iso-iso_7)*self.step/(iso_6-iso_7) ,y_pos+self.step,z_pos+self.step)
        except ZeroDivisionError:
            self.edges[6]=glm.vec3(x_pos+self.step/2 ,y_pos+self.step,z_pos+self.step)

        try:
            self.edges[7]=glm.vec3(x_pos,y_pos+self.step,z_pos+ (iso-iso_4)*self.step/(iso_7-iso_4))
        except ZeroDivisionError:
            self.edges[7]=glm.vec3(x_pos,y_pos+self.step,z_pos+ self.step/2)

        try:
            self.edges[8]=glm.vec3(x_pos,y_pos+ (iso-iso_0)*self.step/(iso_4-iso_0),z_pos)
        except ZeroDivisionError:
            self.edges[8]=glm.vec3(x_pos,y_pos+self.step/2,z_pos)

        try:
            self.edges[9]=glm.vec3(x_pos+self.step,y_pos+ (iso-iso_1)*self.step/(iso_5-iso_1),z_pos)
        except ZeroDivisionError:
            self.edges[9]=glm.vec3(x_pos+self.step,y_pos+self.step/2,z_pos)

        try:
            self.edges[10]=glm.vec3(x_pos+self.step,y_pos+ (iso-iso_2)*self.step/(iso_6-iso_2),z_pos+self.step)
        except ZeroDivisionError:
            self.edges[10]=glm.vec3(x_pos+self.step,y_pos+self.step/2,z_pos+self.step)

        try:
            self.edges[11]=glm.vec3(x_pos,y_pos+ (iso-iso_3)*self.step/(iso_7-iso_3),z_pos+self.step)
        except ZeroDivisionError:
            self.edges[11]=glm.vec3(x_pos,y_pos+self.step/2,z_pos+self.step)



    def getState(self, vertex_0, vertex_1, vertex_2, vertex_3,vertex_4,
    vertex_5,vertex_6,vertex_7,iso) -> int:

        if vertex_0>=iso:
            vertex_0=1
        else:
            vertex_0=0

        if vertex_1>=iso:
            vertex_1=1
        else:
            vertex_1=0

        if vertex_2>=iso:
            vertex_2=1
        else:
            vertex_2=0

        if vertex_3>=iso:
            vertex_3=1
        else:
            vertex_3=0

        if vertex_4>=iso:
            vertex_4=1
        else:
            vertex_4=0
        
        if vertex_5>=iso:
            vertex_5=1
        else:
            vertex_5=0
        
        if vertex_6>=iso:
            vertex_6=1
        else:
            vertex_6=0

        if vertex_7>=iso:
            vertex_7=1
        else:
            vertex_7=0

        return vertex_7*128 + vertex_6*64 + vertex_5*32 +vertex_4*16+vertex_3*8 + vertex_2*4 + vertex_1*2 + vertex_0*1

    def Merge_files(names,subtract):
        cube_info=[]
        cubes={}

        for item in names:
            cube_info=[]
            with open(item,'r') as input_data:
                for line in input_data:
                    cube_info.append(line)

            atom_num=cube_info[2].split()
            iso_start=int(atom_num[0])+6
            for i in range(iso_start,len(cube_info)):
                try:
                    if subtract:
                        cubes[i-iso_start]-=float(cube_info[i])
                    else:
                        cubes[i-iso_start]+=float(cube_info[i])
                except KeyError:
                    try:
                        cubes[i-iso_start]=float(cube_info[i])
                    except ValueError:
                        pass

        cube_geo=[]
        for item in names:
            cube_info=[]
            with open(item,'r') as input_data:
                for line in input_data:
                    cube_info.append(line)

            atom_num=cube_info[2].split()
            iso_start=int(atom_num[0])+6
            for i in range(0,iso_start):
                cube_geo.append(cube_info[i])

            break

        new_name=''
        for item in names:
            new_name+=item.replace('.cube','_')

        output=open(new_name+'.cube',"w+")
        for item in cube_geo:
            output.write(str(item))
        for i in range(0,len(cubes)):
            output.write(str(cubes[i])+"\n")
        output.close()

    def Read_file(self):
        self.cubes={}
        for item in self.names:
            i=0
            cube_info=[]
            with open(item,'r') as input_data:
                for line in input_data:
                    cube_info.append(line)

            atom_num=cube_info[2].split()
            iso_start=int(atom_num[0])+6
            for i in range(iso_start,len(cube_info)):
                try:
                    if self.subtract:
                        self.cubes[i-iso_start]-=float(cube_info[i])
                    else:
                        self.cubes[i-iso_start]+=float(cube_info[i])
                except KeyError:
                    try:
                        self.cubes[i-iso_start]=float(cube_info[i])
                    except ValueError:
                        pass
            i+=1


    def Calc_Field(self):
        k=0
        for i in range(0,self.cols):
            for j in range(0,self.rows):
                for m in range(0,self.rows):
                    self.field[i,j,m]=float(self.cubes[k])

                    k+=1


def myglCreateBuffers(width, height):

    fbo = glGenFramebuffers(1)
    color_buf = glGenRenderbuffers(1)
    depth_buf = glGenRenderbuffers(1)

    # binds created FBO to context both for read and draw
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)

    # bind color render buffer
    glBindRenderbuffer(GL_RENDERBUFFER, color_buf)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA8, width, height)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_buf)

    # bind depth render buffer - no need for 2D, but necessary for real 3D rendering
    glBindRenderbuffer(GL_RENDERBUFFER, depth_buf)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buf)

    return fbo, color_buf, depth_buf, width, height

def myglDeleteBuffers(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glDeleteRenderbuffers(1, color_buf)
    glDeleteRenderbuffers(1, depth_buf)
    glDeleteFramebuffers(1, fbo)

def myglReadColorBuffer(buffers):
    fbo, color_buf, depth_buf, width, height = buffers
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(GL_COLOR_ATTACHMENT0)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    return data, width, height


