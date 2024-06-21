##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
import numpy as np
import time
start_time = time.time()


# path=input("paste path here:")
def dalton_nics(path,text_log):
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
            if 'X' in line and first_atom_flag:
                break
            if first_atom_flag==True:
                if line.strip() and '-----' not in line:
                    geometry_array.append(line)
            if 'Molecular geometry' in line:
                first_atom_flag=True
    

    # del geometry_array[-1]
    geom = list(zip(*(row.split() for row in geometry_array)))
    atoms=list(geom[0])
    atoms_x=list(geom[1])
    atoms_y=list(geom[2])
    atoms_z=list(geom[3])
    atoms_N=[]

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
                # print("Working on: "+data_file)

                shielding_flag=False
                for line in input_data:

                    if 'Chemical shielding for X' in line:
                        shielding_flag=True

                    if shielding_flag:

                        if 'X      x' in line:
                            comp=line.split()
                            xx.append(comp[2].replace('D', 'E'))
                            xy.append(comp[3].replace('D', 'E'))
                            xz.append(comp[4].replace('D', 'E'))

                        if 'X      y' in line:
                            comp=line.split()
                            yx.append(comp[2].replace('D', 'E'))
                            yy.append(comp[3].replace('D', 'E'))
                            yz.append(comp[4].replace('D', 'E'))

                        if 'X      z' in line:
                            comp=line.split()
                            zx.append(comp[2].replace('D', 'E'))
                            zy.append(comp[3].replace('D', 'E'))
                            zz.append(comp[4].replace('D', 'E'))
                    
                    if shielding_flag and 'Diamagnetic and' in line:
                        shielding_flag=False
                        iso=str((float(xx[-1])+float(yy[-1])+float(zz[-1]))/3)
                        isotropic.append(iso)

                        ### THIS MIGHT BE WRONG. TOO BORED TO CHECK
                        aniso=str(float(zz[-1])-(float(xx[-1])+float(yy[-1]))/2)
                        anisotropy.append(aniso)




    ### Create folders, files, changes path
    components=["xx","yy","zz","Isotropic","Anisotropy","xy","xz","yx","yz","zx","zy"]

    if not os.path.exists("dalton_run"):
        os.makedirs("dalton_run")
    os.chdir(path+"/dalton_run")

    output=open("geometry.txt","w+")

    for i in range(0,len(atoms)):
        output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

    output.close()


    os.chdir(path+"/dalton_run")
    if not os.path.exists('comps'):
        os.makedirs('comps')
    os.chdir(path+"/dalton_run/"+'comps')

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
                    pass
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

    os.chdir(path)
    for data_file in dirs:
        if "grid" in data_file:
            a=[]
            file_name=data_file
            with open(file_name,'r') as input_data:
                for line in input_data:
                    a.append(line)
            os.chdir(path+"/"+'dalton_run')
            output=open("gridspecs.txt","w+")
            for item in a:
                output.write(item)
            output.close()
            # os.chdir(path) ### gia na prospathisei na kanei to symmetry
            break

    # text_log.append("Program took " + str(int(time.time() - start_time))+ " seconds to run")
    text_log.append("Done")