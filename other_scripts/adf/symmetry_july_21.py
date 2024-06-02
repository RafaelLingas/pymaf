##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys,numpy
array=[]
file=[]
folder=[]
gridSpecs=[]
atoms=[]
slides=0
cut=0

## Try for no symmetry
def symmetry_full():
    output = open(file.replace("txt", "") + "cube", "w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms)) + "\t" + str(coor) + "\t" + str(coor) + "\t" + str(coor) + "\n")

    output.write(str(slices) + "\t" + str(step_bohr) + "\t0\t0\n")
    output.write(str(slices) + "\t0\t" + str(step_bohr) + "\t0\n")
    output.write(str(slices) + "\t0\t0\t" + str(step_bohr) + "\n")

    for height in range(0, len(atoms)):
        output.write(str(int(col_0[height])) + "\t")
        output.write("0\t")
        output.write(str(col_2[height] * 1.889725989) + "\t")
        output.write(str(col_3[height] * 1.889725989) + "\t")
        output.write(str(col_4[height] * 1.889725989))
        output.write("\n")

    for x in array:
        output.write(x + "\n")

    output.close()

def symmetry_x():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    for x in array:
        output.write(x+"\n")

    for j in range(2,cut+1):
        for t in range(0,slices*slices):
            output.write(array[len(array)-j*slices*slices+t]+"\n")

    output.close()

def symmetry_y():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1

    for x in array:
        output.write(x+"\n")

        if j%(cut*slices)==0:
            for t in range(2,cut+1):
                for k in range(1,slices+1):  ##could be(0,slices)
                    output.write(array[j-1-t*slices+k]+"\n")
        j+=1

    output.close()

def symmetry_z():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1

    for x in array:
        output.write(x+"\n")

        if j%cut==0:
            for k in range(1,cut):
                output.write(array[j-1-k]+"\n")

        j+=1
    output.close()

def symmetry_xy():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1
    j_1=0
    array_1=[]

    for x in array:
        output.write(x+"\n")
        array_1.append(x)
        j_1+=1


        if j%(cut*slices)==0:
            for t in range(2,cut+1):
                for k in range(1,slices+1):
                    output.write(array[j-1-t*slices+k]+"\n")
                    array_1.append(array[j-1-t*slices+k])
                    j_1+=1

        j+=1

    for t_1 in range(2,cut+1):
        for t_2 in range(0,slices*slices):
            output.write(array_1[j_1-t_1*slices*slices+t_2]+"\n")

    output.close()

def symmetry_yz():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1
    incr=0
    array_1=[]

    for x in array:
        output.write(x+"\n")
        array_1.append(x)
        incr+=1

        if j%cut==0:
            for k in range(1,cut):
                output.write(array[j-1-k]+"\n")
                array_1.append(array[j-1-k])
                incr+=1

        if j%(cut*cut)==0:
            for t in range(2,cut+1):
                for t_1 in range(0,slices):
                    output.write(array_1[incr-t*slices+t_1]+"\n")
        j+=1

    output.close()

def symmetry_xz():
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##comment\n")
    output.write("##comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1
    incr=0
    array_1=[]

    for x in array:
        output.write(x+"\n")
        array_1.append(x)
        incr+=1

        if j%cut==0:
            for k in range(1,cut):
                output.write(array[j-1-k]+"\n")
                array_1.append(array[j-1-k])
                incr+=1
        j+=1

    for t in range(2,cut+1):
        for t_1 in range(0,slices*slices):
            output.write(array_1[incr-t*slices*slices+t_1]+"\n")
    

    output.close()

def symmetry_xyz():
    
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")

    j=1
    incr=1
    array_1=[]

    for x in array:
        array_1.append(x)
        incr+=1

        if j%cut==0:
            for k in range(1,cut):
                array_1.append(array[j-1-k])
                incr+=1
        j+=1

    j=1
    i=1
    k=1
    array_2=[]

    for j in range(1,incr):
        output.write(array_1[j-1]+"\n")
        array_2.append(array_1[j-1])
        i+=1

        if j%(cut*slices)==0:
            for t in range(2,cut+1):
                for k in range(1,slices+1):
                    output.write(array_1[j-1-t*slices+k]+"\n")
                    array_2.append(array_1[j-1-t*slices+k])
                    i+=1

    j=2
    t=0

    for j in range(2,cut+1):
        for t in range(0,slices*slices):
            output.write(array_2[i-1-j*slices*slices+t]+"\n")

    output.close()

def symmetry_xzix():

    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")
    

    j=1
    incr=0
    array_1=[]

    for x in array:
        output.write(x+"\n")
        array_1.append(x)
        incr+=1

        if j%cut==0:
            for k in range(1,cut):
                output.write(array[j-1-k]+"\n")
                array_1.append(array[j-1-k])
                incr+=1
        j+=1

    for t in range(2,cut+1):
        for t_1 in range(0,slices*slices):
            output.write(array_1[incr-1-(t-1)*slices*slices-t_1]+"\n")
    

    output.close()

def symmetry_xyz_d2d():
    
    output=open(file.replace("txt","")+"cube","w+")

    if folder!="xx" and folder!="yy":

        output.write("##Comment\n")
        output.write("##Comment\n")

        output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

        output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
        output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
        output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

        for height in range(0,len(atoms)):
            output.write(str(int(col_0[height]))+"\t")
            output.write("0\t")
            output.write(str(col_2[height]*1.889725989)+"\t")
            output.write(str(col_3[height]*1.889725989)+"\t")
            output.write(str(col_4[height]*1.889725989))
            output.write("\n")


    matrix={}
   
    x=0
    y=0
    z=0
    i=0

    for m in array:     #1/8 dld xyz

        matrix[x,y,z]=m
        i+=1
        z+=1

        if i%(cut)==0:
            y+=1
            z=0
        
        if i%(cut*cut)==0:
            x+=1
            y=0

    x=0
    y=0
    z=0
    i_2=i
    for k in range(1,i+1-(cut*cut)):    #1/4 dld xz

        matrix[x,cut+y,z]=matrix[x,cut-y-2,z]
        z+=1
        i_2+=1

        if k%(cut)==0:
            y+=1
            z=0

        if k%(cut*(cut-1))==0:
            x+=1
            y=0

    x=0
    y=0
    z=0
    i_3=i_2

    for k in range(1,i_2+1-(cut*slices)):   #1/2 dld z

        matrix[cut+x,y,z]=matrix[cut-x-2,y,z]
        z+=1
        i_3+=1

        if k%cut==0:
            y+=1
            z=0

        if k%(cut*slices)==0:
            x+=1
            y=0
            
    
    x=0
    y=0
    z=0
    i_4=i_3
    for k in range(1,i_3+1-(slices*slices)):

        matrix[x,y,cut+z]=matrix[y,slices-x-1,cut-z-2]
        z+=1
        i_4+=1

        if k%(cut-1)==0:
            y+=1
            z=0

        if k%((cut-1)*slices)==0:
            x+=1
            y=0

    x=0
    y=0
    z=0

    for k in range(1,i_4+1):
        output.write(matrix[x,y,z]+"\n")
        z+=1

        if k%slices==0:
            z=0
            y+=1
        if k%(slices*slices)==0:
            x+=1
            y=0
            
    
    output.close()



def symmetry_iz():
    
    output=open(file.replace("txt","")+"cube","w+")

    output.write("##Comment\n")
    output.write("##Comment\n")

    output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

    output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
    output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
    output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

    for height in range(0,len(atoms)):
        output.write(str(int(col_0[height]))+"\t")
        output.write("0\t")
        output.write(str(col_2[height]*1.889725989)+"\t")
        output.write(str(col_3[height]*1.889725989)+"\t")
        output.write(str(col_4[height]*1.889725989))
        output.write("\n")


    matrix={}
   
    x=0
    y=0
    z=0
    i=0

    for m in array:
        matrix[x,y,z]=m
        i+=1
        z+=1

        if i%(cut)==0:
            y+=1
            z=0

        if i%(cut*slices)==0:
            x+=1
            y=0
    x=0
    y=0
    z=0
    i_2=i
    for k in range(1,i+1-slices*slices): #
        matrix[slices-x-1,slices-y-1,slices-z-1]=matrix[x,y,z]
        z+=1
        i_2+=1

        if k%(cut-1)==0:
            y+=1
            z=0

        if k%((cut-1)*slices)==0:
            x+=1
            y=0
    
    x=0
    y=0
    z=0
    for k in range(1,i_2+1):
        output.write(matrix[x,y,z]+"\n")
        z+=1

        if k%slices==0:
            z=0
            y+=1
        if k%(slices*slices)==0:
            x+=1
            y=0

    output.close()



path=input("paste path here:")
os.chdir(path)

dirs=os.listdir(path)

for item in dirs:
     if item.endswith(".txt") ==True:
         if "grid" in item:
             item_object=open("./"+item,'r')
             gridSpecs=item_object.read().split()
             item_object.close()
             slices=int(float(gridSpecs[0])) ## have to make it float first
             step=float(gridSpecs[1])
             symmetry=gridSpecs[5]

         if "geometry" in item:
            with open(item,'r') as input_data:
                output=open("geo_cut.txt",'w+')
                for line in input_data:
                    if 'MOs' in line:
                        break
                    atoms.append(line)
                    output.write(line)
                output.close()
                
col_0=numpy.loadtxt("geo_cut.txt",usecols=(0))
## col_1 would be 0
col_2=numpy.loadtxt("geo_cut.txt",usecols=(2))
col_3=numpy.loadtxt("geo_cut.txt",usecols=(3))
col_4=numpy.loadtxt("geo_cut.txt",usecols=(4))


## compute -x , -y , -z (bohr)
coor=-((slices-1)/2)*step*1.889725989
##step in bohr
step_bohr=step*1.889725989


cut=(slices-1)/2+1
cut=int(cut)

for folder in dirs:
    if "." not in folder:
       sub_dirs=os.listdir(path+'/'+folder)
       for file in sub_dirs:
           if file.endswith(".txt")==True:
               if "_c_" not in file:
                    os.chdir(path+'/'+folder)
                    file_object=open(path+'/'+folder+'/'+file,'r')
                    array=file_object.read().split()
                    file_object.close()
                    if symmetry=="x":
                        symmetry_x()
                    if symmetry=="y":
                        symmetry_y()
                    if symmetry=="z":
                        symmetry_z()
                    if symmetry=="xy":
                        symmetry_xy()
                    if symmetry=="yz":
                        symmetry_yz()
                    if symmetry=="xz":
                        symmetry_xz()
                    if symmetry=="xyz":
                        symmetry_xyz()
                    if symmetry=="xzix":
                        symmetry_xzix()
                    if symmetry=="xyz_d2d":
                        symmetry_xyz_d2d()
                    if symmetry=="iz":
                        symmetry_iz()
                    if symmetry=="Full":
                        symmetry_full()
    print("calculating...")

if symmetry=="xyz_d2d":

    for folder in dirs:
        if "xx" in folder:
            sub_dirs=os.listdir(path+'/'+folder)
            for file in sub_dirs:
               if file.endswith(".cube")==True:
                   file_object=open(path+'/'+folder+'/'+file,'r')
                   array=file_object.read().split()
                   file_object.close()

                   matrix_xx={}
   
                   x=0
                   y=0
                   z=0
                   i=0

                   for m in array:
                       matrix_xx[x,y,z]=m
                       i+=1
                       z+=1

                       if i%slices==0:
                           z=0
                           y+=1

                       if i%(slices*slices)==0:
                           y=0
                           x+=1

                   
                   os.chdir(path+'/'+'yy')
                   file_object=open(path+'/'+'yy'+'/'+file.replace("xx","yy"),'r')
                   array=file_object.read().split()
                   file_object.close()

                   matrix_yy={}
   
                   x=0
                   y=0
                   z=0
                   i=0

                   for m in array:
                       matrix_yy[x,y,z]=m
                       i+=1
                       z+=1

                       if i%slices==0:
                           z=0
                           y+=1

                       if i%(slices*slices)==0:
                           y=0
                           x+=1
                    
                   output=open(file.replace("xx","yy"),"w+")

                   output.write("##Comment\n")
                   output.write("##Comment\n")

                   output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

                   output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
                   output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
                   output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

                   for height in range(0,len(atoms)):
                       output.write(str(int(col_0[height]))+"\t")
                       output.write("0\t")
                       output.write(str(col_2[height]*1.889725989)+"\t")
                       output.write(str(col_3[height]*1.889725989)+"\t")
                       output.write(str(col_4[height]*1.889725989))
                       output.write("\n")

                   x=0
                   y=0
                   z=0

                   for k in range(1,cut*slices*slices+1):
                       output.write(matrix_yy[x,y,z]+"\n")
                       z+=1

                       if k%cut==0:
                          
                          for j in range(0,cut-1):
                              output.write(matrix_xx[x,y,z+j]+"\n")
                          y+=1
                          z=0

                       if k%(cut*slices)==0:
                          x+=1
                          y=0

                   output.close()
                   
                   os.chdir(path+'/'+'xx')

                   output=open(file,"w+")

                   output.write("##Comment\n")
                   output.write("##Comment\n")

                   output.write(str(len(atoms))+"\t"+str(coor)+"\t"+str(coor)+"\t"+str(coor)+"\n")

                   output.write(str(slices)+"\t"+str(step_bohr)+"\t0\t0\n")
                   output.write(str(slices)+"\t0\t"+str(step_bohr)+"\t0\n")
                   output.write(str(slices)+"\t0\t0\t"+str(step_bohr)+"\n")

                   for height in range(0,len(atoms)):
                       output.write(str(int(col_0[height]))+"\t")
                       output.write("0\t")
                       output.write(str(col_2[height]*1.889725989)+"\t")
                       output.write(str(col_3[height]*1.889725989)+"\t")
                       output.write(str(col_4[height]*1.889725989))
                       output.write("\n")

                   x=0
                   y=0
                   z=0

                   for k in range(1,cut*slices*slices+1):
                       output.write(matrix_xx[x,y,z]+"\n")
                       z+=1

                       if k%cut==0:
                          
                          for j in range(0,cut-1):
                              output.write(matrix_yy[x,y,z+j]+"\n")
                          y+=1
                          z=0

                       if k%(cut*slices)==0:
                          x+=1
                          y=0
                   
                   output.close()



print("Done")