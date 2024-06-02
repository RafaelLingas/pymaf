##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

##need to make it create missing values or we have to put very small print

import os,sys
from typing import Counter
import numpy as np
import time
start_time = time.time()

#path = 'D:\\phd\\charistos\\nbo\\nbo_tests\\cmo_tests\\1'
#path=input("paste path here:")
def gaussian_cmo(path,text_log):
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
    ###Get atomic number. 

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
        # sigma = Orbital("sigma")
        # pi = Orbital("pi")
        total= Orbital("total")
        total.orbs.append('Total')

        #types=(core,sigma,pi)


        ##starting main loop
        # for data_file in dirs:
        #     if data_file.endswith(".out"):
        os.chdir(path)
        with open(data_file,'r') as input_data:
            text_log.append("Working on: "+data_file)

            for line in input_data:



                ### check orbitals ####
                if check_orbs_flag==True:
                    if finding_orbs_flag==True and 'vir' in line:
                        check_orbs_flag=False
                        #found_orbs_flag=False
                        finding_orbs_flag=False
                        uncut_ncores=line.split()
                        n_orb=int(uncut_ncores[1])-1

                        


                        types=(core,total)#,nth,nth1,nth2,nth3,nth4,nth5,nth6,nth7,nth8,nth9)

                    if 'CMO: NBO Analysis of Cano' in line:
                        finding_orbs_flag=True

                    if "MO" and "orbital energy" in line:
                        uncut_mo=line.split()
                        mo=uncut_mo[1]
                        check_comp=True
                    
                    if check_comp and 'CR' in line:
                        core.orbs.append(mo)
                        check_comp=False
                    
                    # if check_comp and 'BD ( 1)' in line:
                    #     sigma.orbs.append(mo)
                    #     check_comp=False
                    
                    # if check_comp and 'BD ( 2)' in line:
                    #     pi.orbs.append(mo)
                    #     check_comp=False
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
                                item.values[9,ghost_num]= (item.values[0,ghost_num]+item.values[4,ghost_num]+item.values[8,ghost_num])/3
                            
                            # if orb_num =="Total":
                            #     for k in range(0,9):
                            #         try:
                            #             item.values[k,ghost_num]=item.values[k,ghost_num]+float(orb_comp[k+1])
                            #         except KeyError:
                            #             item.values[k,ghost_num]=float(orb_comp[k+1])
                    
                    cmo_uncut.pop(len(cmo_uncut)-1)
                    columns=list(zip(*(row.split() for row in cmo_uncut)))
                    which=list(columns[0])
                    which=[int(x.replace('.','')) for x in which]


                    values=[]
                    for i in range(1,10):
                        values.append(list(columns[i]))



                    if len(cmo_uncut)<n_orb:
                        for i in range(0,n_orb):
                            if int(i+1) not in which:
                                which.insert(i,int(i+1))
                                for k in range(0,9):
                                    values[k].insert(i,0.0)

                    for k in range(0,n_orb):
                        for j in range(0,9):
                            all_cmos[ghost_num,k,j]= float(values[j][k])
                        ### Make isotropic
                        all_cmos[ghost_num,k,9]= (float(values[0][k])+float(values[4][k])+float(values[8][k]))/3

                    # print(which)
                    # print(values[0])
                    # print(int("total"))
                    # for item in cmo:
                    #     print(item[0])
                    # for k in range(0,n_orb):
                    #     a=int(cmo[k][0].replace('.',''))
                    #     if (k+1)!=a:
                    #         cmo.insert(k,[str(k+1)+'.','0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00', '0.00'])

                    # arr=np.array(cmo)
                    cmo_uncut=[]


                    # for k in range(0,n_orb+1):   ###instead of n_mos+1
                    #     for j in range(0,10):
                    #         all_cmos[ghost_num,k,j]=arr[k,j]
                    
                    ghost_num+=1

                    cmo=[]



                    ghost_flag=False
                    cmo_matrix_flag=False


                if 'Full Cartesian' in line and 'gh(' in line:
                    ghost_flag=True
                
                if ghost_flag==True and 'Canonical MO' in line:
                    cmo_matrix_flag=True




        if not os.path.exists("cmo_run"):
            os.makedirs("cmo_run")
        os.chdir(path+"/cmo_run")

        output=open("geometry.txt","w+")

        for i in range(0,len(atoms)):
            output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

        output.close()


        components=["xx","xy","xz","yx","yy","yz","zx","zy","zz",'isotropic']

        for m in range(0,10):
            os.chdir(path+"/cmo_run")
            if not os.path.exists(components[m]):
                os.makedirs(components[m])
            os.chdir(path+"/cmo_run/"+components[m])
            # for n in range(0,n_mos):
            #     output=open(str(all_cmos[0,n,0]).replace('.','')+".txt","a+")
            #     for k in range(0,ghost_num):
            #         output.write(str((-1)*float(all_cmos[k,n,m+1]))+"\n")
            #     output.close()
            for n in range(0,n_orb):
                output=open(str(which[n])+".txt","a+")
                for k in range(0,ghost_num):
                    output.write(str((-1)*all_cmos[k,n,m])+"\n")
                output.close()
            
            for item in types:
                output=open(item.name+".txt","a")
                for k in range(0,ghost_num):
                    try:
                        output.write(str((-1)*item.values[m,k])+"\n")
                    except KeyError:
                        print(item.values(m,k))
                output.close()

    for data_file in dirs:
            if data_file.endswith(".out"):
                file_search(data_file)
    
    os.chdir(path)
    for data_file in dirs:
        if "grid" in data_file:
            a=[]
            file_name=data_file
            with open(file_name,'r') as input_data:
                for line in input_data:
                    a.append(line)
            os.chdir(path+"/"+'cmo_run')
            output=open("gridspecs.txt","w+")
            for item in a:
                output.write(item)
            output.close()
            # os.chdir(path) ### gia na prospathisei na kanei to symmetry
            break

    # text_log.append("Program took " + str(int(time.time() - start_time))+ " seconds to run")
    text_log.append("Done")
                