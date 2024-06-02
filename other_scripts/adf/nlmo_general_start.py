##(Occupancy)   Bond orbital / Coefficients / Hybrids

##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
import numpy as np
import MyFuncs as adf
import time
start_time = time.time()


#path=input("path:")
path=("D:\\phd\\charistos\\nbo\\russian_dolls\\adf_tests\\rydberg_for_pi_types")
os.chdir(path)

dirs=os.listdir(path)
dirs.sort()


def file_search(fname):
    check_orbs_flag=True
    finding_orbs_flag=False
    found_orbs_flag=False
    check_if_pi=False
    ghost_flag=False

    eigenvectors_flag=False
    eigenvector_array=[]

    x=0
    y=0
    z=0
    comp_flag=False
    comp_start_flag=False


    core= adf.Orbital("core")
    sigma= adf.Orbital("sigma")
    total= adf.Orbital("total")
    pi= adf.Orbital("pi")
    type_1= adf.Orbital("type_1")

    #print(adf.Orbital.orbitals[0].name)

    types=(core,sigma,total,pi,type_1)

    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)
        for line in input_data:
            if check_orbs_flag==True:
                if found_orbs_flag==True and 'Individual LMO' in line:
                    n_lewis=int(uncut_BD[0][:-1])
                    check_orbs_flag=False
                    found_orbs_flag=False
                    finding_orbs_flag=False


                if '(NLMO) ANALYSIS:' in line:
                    finding_orbs_flag=True
                if finding_orbs_flag==True and '-----------' in line:
                    found_orbs_flag=True

                if found_orbs_flag ==True:
                    if 'CR' in line:
                        uncut_ncores=line.split()
                        n_cores=int(uncut_ncores[0][:-1])
                        core.orbs.append(n_cores)
                        

                    if check_if_pi==True and 'BD' not in line and 'LP' not in line and '3C' not in line and check_orbs_flag==True:
                        a=line[:line.find('%')] ### atom contribution to orbital
                        orb_contr.append(a)                      

                        a=line[line.find('p'):]
                        b=a[:a.find('%')]
                        c=b[b.find('('):]
                        try:
                            p_perc=float(c.replace('(',''))
                        except ValueError:
                            p_perc=0.0
                        p_contr.append(p_perc)

                    elif check_if_pi==True and ('BD' in line or 'LP' in line or '3C' in line or check_orbs_flag==False):
                        check_if_pi=False
                        a=max(orb_contr)
                        max_contr=orb_contr.index(a)
                        if p_contr[max_contr]>90.0:
                            pi.orbs.append(n_bd)

                            if int(uncut_BD[len(uncut_BD)-1])>60:
                                type_1.orbs.append(n_bd)

                        else:
                            sigma.orbs.append(n_bd)

                    
                    if 'BD' in line or 'LP' in line or '3C' in line:
                        check_if_pi=True
                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])

                        orb_contr=[]
                        p_contr=[]
                    
            if 'G H O S T' in line:
                ghost_flag=True
                eigenvector_array=[]
            if ghost_flag==True:
                
                if eigenvectors_flag==True:
                    if 'xxx' in line:

                        eigenvectors_flag=False
                        ghost_flag=False
                        del eigenvector_array[0]
                        eigenvector_array = [w.replace('D','e') for w in eigenvector_array]
                        columns_eigen = list(zip(*(row.split() for row in eigenvector_array)))

                if eigenvectors_flag==True:
                    eigenvector_array.append(line)

                if 'eigenvectors' in line:
                    eigenvectors_flag=True

            if 'NLMO #' in line:
                comp_flag=True
                comp_start_flag=True
                ### Give a value to all Pi_alone
                # for p_orb in range(0,len(pi.orbs)-1):
                #     pi_alone[x,y,z,p_orb]=0
                core.values[x,y,z]=0
                
            if comp_flag==True:

                if comp_start_flag==True and '----------' not in line and 'sum' not in line and 'NBO' not in line:
                    cut_ncs=line.split()
                    which_nbo=int(cut_ncs[0][:-1])
                    if which_nbo<=n_lewis:
                        values_of_which=float(cut_ncs[3])

                        adf.Which_Orbital(types,which_nbo,values_of_which,x,y,z)

                if 'sum' in line:
                    comp_start_flag=False
                    comp_flag=False

                    ###total.values
                    sum_uncut=line.split()
                    total.values[x,y,z]=float(sum_uncut[3])

                    #update
                    y+=1
                    if y==3:
                        y=0
                        x+=1
                    if x==5:

                        E=np.array(columns_eigen)
                        E.reshape((3,3))
                        E=E.transpose()
                        E=E.astype(np.float64)
                        E_inv=np.linalg.inv(E)

                        for item in types:
                            adf.Principal_To_Cartesian(E,E_inv,item.values,z)

                        x=0
                        z+=1

    adf.Create_Files_Adf(path,z,types)


adf.Get_Adf_Geom(path,dirs)

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        file_search(data_file)

print("My program took" + str(time.time() - start_time)+ " to run")
