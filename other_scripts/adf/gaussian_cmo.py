##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

##need to make it create missing values or we have to put very small print

import os,sys
from typing import Counter
import numpy as np
import time
start_time = time.time()

#path = 'D:\\phd\\charistos\\nbo\\nbo_tests\\cmo_tests\\1'
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
        if 'Bq' in line and geometry_flag==True:
                break
        if geometry_flag==True:
            geometry_array.append(line)
        if 'Charge =' in line:
            geometry_flag=True


geom = list(zip(*(row.split() for row in geometry_array)))
atoms=list(geom[0])
atoms_x=list(geom[1])
atoms_y=list(geom[2])
atoms_z=list(geom[3])
atoms_N=[]
###Get atomic number. have to add atoms later
elements=["H","He","Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti",
    "V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se",
    "Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd",
    "Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce",
    "Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb",
    "Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi",
    "Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm",
    "Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt"]

ar_elements=np.array(elements)

for i in range(0,len(atoms)):
    which_atom=np.where(ar_elements==atoms[i])
    atoms_N.append(which_atom[0]+1)
###

class Orbital:
    orbitals=[]
    def __init__(self,name):
        self.name=name
        self.orbs=[]
        self.values={}
        Orbital.orbitals.append(self)


def file_search(fname):

    ghost_flag=False
    cmo_matrix_flag=False
    cmo_uncut=[]
    cmo=[]

    ghost_num=0
    all_cmos={}

    ### orbital_flags##
    check_orbs_flag=True
    finding_orbs_flag=False
    check_comp=False



    core = Orbital("core")
    sigma = Orbital("sigma")
    pi = Orbital("pi")
    total= Orbital("total")

    types=(core,sigma,pi)


    ##starting main loop
    # for data_file in dirs:
    #     if data_file.endswith(".out"):
    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)

        for line in input_data:



            ### check orbitals ####
            if check_orbs_flag==True:
                if finding_orbs_flag==True and 'vir' in line:
                    check_orbs_flag=False
                    #found_orbs_flag=False
                    finding_orbs_flag=False
                    uncut_ncores=line.split()
                    n_orb=int(uncut_ncores[1])-1

                if 'CMO: NBO Analysis of Cano' in line:
                    finding_orbs_flag=True

                if "MO" and "orbital energy" in line:
                    uncut_mo=line.split()
                    mo=uncut_mo[1]
                    check_comp=True
                
                if check_comp and 'CR' in line:
                    core.orbs.append(mo)
                    check_comp=False
                
                if check_comp and ('BD ( 1)' in line or '3C ( 1)' in line or 'LV ( 1)' in line):
                    sigma.orbs.append(mo)
                    check_comp=False
                
                if check_comp and ('BD ( 2)' in line or '3C ( 2)' in line or '3Cn( 2)' in line):
                    pi.orbs.append(mo)
                    check_comp=False
                #if finding_orbs_flag==True and 'MO' in line and 'occ' in line:
                    #asd=1

            if cmo_matrix_flag==True:
                cmo_uncut.append(line)

            if cmo_matrix_flag==True and 'Total' in line:
                cmo_uncut.pop(0)
                cmo_uncut.pop(0)
                cmo_uncut.pop(0)
                cmo_uncut.pop(len(cmo_uncut)-2)
                n_mos=(len(cmo_uncut)-1) ##how many MOs are

                for i in range(0,len(cmo_uncut)):

                    #if i>(len(cmo_uncut)-10): ### to get highest energies only + total
                    cmo.append(cmo_uncut[i].split())
                    orb_comp=cmo_uncut[i].split()
                    orb_num=orb_comp[0].replace('.','')


                    for item in types:
                        if orb_num in item.orbs:
                            for k in range(0,9):
                                try:
                                    item.values[k,ghost_num]=item.values[k,ghost_num]+float(orb_comp[k+1])
                                except KeyError:
                                    item.values[k,ghost_num]=float(orb_comp[k+1])
                        
                        # if orb_num =="Total":
                        #     for k in range(0,9):
                        #         try:
                        #             item.values[k,ghost_num]=item.values[k,ghost_num]+float(orb_comp[k+1])
                        #         except KeyError:
                        #             item.values[k,ghost_num]=float(orb_comp[k+1])
                


                ### remake matrix for missing cmos
                for k in range(0,n_orb+1):
                    # if start_flag
                    if '.' in cmo[k][0]:
                        cmo[k][0]=cmo[k][0].replace('.','')
                    if cmo[k][0]=='Total':
                        if len(cmo)!=n_orb+1:
                            missing=n_orb+1-len(cmo)
                            for i in range (0,missing):
                                cmo.insert(k+i,[k+i+1,0,0,0,0,0,0,0,0,0])
                        break
                    if int(cmo[k][0]) != (k+1):
                        cmo.insert(k,[k+1,0,0,0,0,0,0,0,0,0])

                arr=np.array(cmo)
                cmo=[]
                cmo_uncut=[]

                for k in range(0,n_orb+1):   ###instead of n_mos+1
                    for j in range(0,10):
                        all_cmos[ghost_num,k,j]=arr[k,j]
                
                ghost_num+=1


                cmo=[]



                ghost_flag=False
                cmo_matrix_flag=False


            if 'Full Cartesian' in line and 'gh(' in line:
                ghost_flag=True
            
            if ghost_flag==True and 'Canonical MO' in line:
                cmo_matrix_flag=True

                ### try to give it a value so its not empty
                for item in types:
                    for k in range(0,9):
                        item.values[k,ghost_num]=0





    if not os.path.exists("cmo_run"):
        os.makedirs("cmo_run")
    os.chdir(path+"/cmo_run")

    output=open("geometry.txt","w+")

    for i in range(0,len(atoms)):
        output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

    output.close()


    components=["xx","xy","xz","yx","yy","yz","zx","zy","zz"]


    for m in range(0,9):
        os.chdir(path+"/cmo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/cmo_run/"+components[m])
        for n in range(0,n_mos+1):   #### for the last ten: range(n_mos-10,n_mos+1)
            output=open(str(all_cmos[0,n,0]).replace('.','')+".txt","a+")
            for k in range(0,ghost_num):
                output.write(str((-1)*float(all_cmos[k,n,m+1]))+"\n")
            output.close()
        
        for item in types:
            output=open(item.name+".txt","a")
            for k in range(0,ghost_num):
                output.write(str((-1)*item.values[m,k])+"\n")
            output.close()

for data_file in dirs:
        if data_file.endswith(".out"):
            file_search(data_file)
                