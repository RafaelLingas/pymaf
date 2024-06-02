##(Occupancy)   Bond orbital / Coefficients / Hybrids

##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments


import os,sys
import numpy as np
import MyFuncs as adf
import time
start_time = time.time()


path=input("path:")
#path=("F:\\workspace\\test_dir\\cmo")
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
    ###thats pretty dumb
    x1=0
    z1=0
    ### thats pretty dumb
    orbitals={}
    which_comp_counter=1
    total = adf.Orbital("total")
    occ_vir = adf.Orbital("occ_vir")

    totals={}

    types=(total,occ_vir)


    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)

        for line in input_data:

            if 'HOMO :' in line:
                #if homo_flag==True:
                homo_num=line.split()
                homo_num=int(homo_num[2])
                #break
                #homo_flag=True
            if 'List of all MOs,' in line:
                    break

    with open(data_file,'r') as input_data:
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
                    
                    total_occ=line.split()
                    total_occ=total_occ[len(total_occ)-1]
                    totals[0,x,z]=float(total_occ)

                elif which_comp_counter==2:
                    comp.Occ_occ(orbitals,x,z)
                else:
                    comp.Diamagnetic(orbitals,x,z)

                    # total_vir=line.split()
                    # total_vir=total_vir[len(total_vir)-1]
                    # totals[1,x,z]=float(total_vir)
                
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

            if 'total Para+SO U1 + S1 + Dia' in line:
                ## the name total_vir is not correct but whatever
                total_vir=line.split()
                total_vir=total_vir[len(total_vir)-1]
                totals[1,x1,z1]=float(total_vir)

                x1+=1
                if x1==4:
                    x1=0
                    z1+=1








    adf.Create_Files_CMO_Adf(path,z,orbitals,homo_num,totals)

###Execute
adf.Get_Adf_Geom(path,dirs,"cmo_run")

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        file_search_cmo(data_file)

print("My program took" + str(time.time() - start_time)+ " to run")