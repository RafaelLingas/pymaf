##(Occupancy)   Bond orbital / Coefficients / Hybrids

##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments


import os,sys
from xml.etree.ElementTree import TreeBuilder
import numpy as np
import MyFuncs as adf
import time
start_time = time.time()


#path=input("path:")
path=("F:\\workspace\\test_dir\\cmo")
os.chdir(path)

dirs=os.listdir(path)
dirs.sort()

class Cmos:
    orbitals=[]
    def __init__(self,name):
        self.name=name
        self.orbs=[]
        self.values={}
        #Orbital.orbitals.append(self)


def file_search_cmo(fname):

    #ghost_flag=False
    homo_flag=False
    comp_flag=False
    x=0
    y=0
    z=0
    orbitals={}
    which_comp_counter=1
    total = adf.Orbital("total")
    occ_vir = adf.Orbital("occ_vir")

    types=(total,occ_vir)


    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)

        for line in input_data:

            if 'HOMO :' in line:
                if homo_flag==True:
                    homo_num=line.split()
                    homo_num=int(homo_num[2])
                    break
                homo_flag=True

        for line in input_data:


            # if 'G H O S T' in line:
            #     ghost_flag=True

            if 'i (occ)' in line:
                comp_flag=True

                comp=adf.Cmos(homo_num)

            if comp_flag==True and 'total printed' not in line and 'i (occ)' not in line and '----' not in line:

                comp.comp.append(line)


            if 'total printed' in line:
                comp_flag=False

                if which_comp_counter==1:
                    comp.Occ_vir(orbitals,x,z)
                elif which_comp_counter==2:
                    comp.Occ_occ(orbitals,x,z)
                else:
                    comp.Diamagnetic(orbitals,x,z)
                
                if which_comp_counter==3:
                    which_comp_counter=1
                else:
                    which_comp_counter+=1


                #update
                y+=1
                if y==3:
                    y=0
                    x+=1
                if x==4:
                    x=0
                    z+=1










    adf.Create_Files_CMO_Adf(path,z,orbitals,homo_num)

###Execute
adf.Get_Adf_Geom(path,dirs)

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        file_search_cmo(data_file)

print("My program took" + str(time.time() - start_time)+ " to run")