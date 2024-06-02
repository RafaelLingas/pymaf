##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
import numpy as np


path=input("paste path here:")
os.chdir(path)

dirs=os.listdir(path)

###Get a file for geometry and orbitals
for data_file in dirs:
    if data_file.endswith(".out"):
        file_name=data_file
        break

###Get Geometry
geometry_array=[]
geometry_flag=False
first_atom_flag=False
end_geometry=False

with open(file_name,'r') as input_data:
    for line in input_data:
        if first_atom_flag==True:
            geometry_array.append(line)
        if 'Charge =' in line:
            first_atom_flag=True
        if 'Bq' in line:
            end_geometry=True
        if end_geometry==True:
            break

del geometry_array[-1]
geom = list(zip(*(row.split() for row in geometry_array)))
atoms=list(geom[0])
atoms_x=list(geom[1])
atoms_y=list(geom[2])
atoms_z=list(geom[3])
atoms_N=[]

for k in range(0,len(atoms)):
    if atoms[k]=='C':
        atom='6'
    if atoms[k]=='H':
        atom='1'
    atoms_N.append(atom)



magnetic_tensor_flag=False
ghost_flag=False
ghost_finish_flag=False
isotropic=[]
anisotropy=[]
xx=[]
yx=[]
zx=[]
xy=[]
yy=[]
zy=[]
xz=[]
yz=[]
zz=[]

for data_file in dirs:
    if data_file.endswith(".out"):
        with open(data_file,'r') as input_data:
            print("Working on: "+data_file)

            magnetic_tensor_flag = False
            ghost_flag = False
            ghost_finish_flag = False

            for line in input_data:
                if 'Magnetic shielding tensor' in line:
                    magnetic_tensor_flag=True
                if magnetic_tensor_flag==True and 'Bq' in line:
                    ghost_flag=True

                if ghost_flag==True and 'Population analysis' in line:
                    ghost_finish_flag=True

                if ghost_flag==True and ghost_finish_flag==False:
                    if 'Bq' in line:
                        iso_aniso=line.split()
                        isotropic.append(iso_aniso[4])
                        anisotropy.append(iso_aniso[7])

                    if 'XX=' in line:
                        comp=line.split()
                        xx.append(comp[1])
                        yx.append(comp[3])
                        zx.append(comp[5])

                    if 'XY=' in line:
                        comp=line.split()
                        xy.append(comp[1])
                        yy.append(comp[3])
                        zy.append(comp[5])

                    if 'XZ=' in line:
                        comp=line.split()
                        xz.append(comp[1])
                        yz.append(comp[3])
                        zz.append(comp[5])





### Create folders, files, changes path
components=["xx","yy","zz","Isotropic","Anisotropy","xy","xz","yx","yz","zx","zy"]

if not os.path.exists("gaussian_run"):
    os.makedirs("gaussian_run")
os.chdir(path+"/gaussian_run")

output=open("geometry.txt","w+")

for i in range(0,len(atoms)):
    output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

output.close()


os.chdir(path+"/gaussian_run")
if not os.path.exists('comps'):
    os.makedirs('comps')
os.chdir(path+"/gaussian_run/"+'comps')

for n in range(0, len(components)):
        output = open(components[n] + ".txt", "w+")
        if n == 0:
            for k in range(0,len(xx)):
                output.write(str(-1*float(xx[k])) + "\n")
        if n == 1:
            for k in range(0, len(xx)):
                output.write(str(-1*float(yy[k])) + "\n")
        if n == 2:
            for k in range(0, len(xx)):
                output.write(str(-1*float(zz[k])) + "\n")
        if n == 3:
            for k in range(0, len(xx)):
                output.write(str(-1*float(isotropic[k])) + "\n")
        if n == 4:
            for k in range(0, len(xx)):
                output.write(str(-1*float(anisotropy[k])) + "\n")
        if n == 5:
            for k in range(0, len(xx)):
                output.write(str(-1*float(xy[k])) + "\n")
        if n == 6:
            for k in range(0, len(xx)):
                output.write(str(-1*float(xz[k])) + "\n")
        if n == 7:
            for k in range(0, len(xx)):
                output.write(str(-1*float(yx[k])) + "\n")
        if n == 8:
            for k in range(0, len(xx)):
                output.write(str(-1*float(yz[k])) + "\n")
        if n == 9:
            for k in range(0, len(xx)):
                output.write(str(-1*float(zx[k])) + "\n")
        if n == 10:
            for k in range(0, len(xx)):
                output.write(str(-1*float(zy[k])) + "\n")


            output.close()