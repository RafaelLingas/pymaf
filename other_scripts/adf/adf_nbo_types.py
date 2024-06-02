##(Occupancy)   Bond orbital / Coefficients / Hybrids

##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments


import os,sys
import numpy as np
import MyFuncs as adf
import time
start_time = time.time()


path=input("path:")
#path=("D:\\phd\\charistos\\nbo\\russian_dolls\\adf_tests\\rydberg_for_pi_types")
os.chdir(path)

dirs=os.listdir(path)
dirs.sort()


def file_search(fname):
    check_orbs_flag=True
    finding_orbs_flag=False
    found_orbs_flag=False
    check_if_pi=False
    ghost_flag=False

    ### GHOSTS and choosing components
    ghost_flag=False
    eigenvectors_flag=False
    eigenvector_array=[]

    x=0
    y=0
    z=0

    comp_flag=False
    comp_start_flag=False

    core = adf.Orbital("core")
    sigma = adf.Orbital("sigma")
    total = adf.Orbital("total")
    pi = adf.Orbital("pi")
    type_1 = adf.Orbital("type_1")
    type_2 = adf.Orbital("type_2")
    # mg=adf.Orbital("Mg")

    # ry_p1=adf.Orbital("ry_p1")
    # ry_p2=adf.Orbital("ry_p2")
    # ry_d1=adf.Orbital("ry_d1")
    # ry_d2=adf.Orbital("ry_d2")

    types=(core,sigma,total,pi,type_1,type_2)#,ry_p1,ry_p2,ry_d1,ry_d2)



    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)
        for line in input_data:
            if check_orbs_flag==True:
                if found_orbs_flag==True and ('Hyperbond' in line or 'SECOND ORDER' in line):
                    n_lewis=int(uncut_BD[0][:-1])
                    check_orbs_flag=False
                    found_orbs_flag=False
                    finding_orbs_flag=False


                if '(Occupancy)   Bond orbital / Coefficients / Hybrids' in line:
                    finding_orbs_flag=True
                if finding_orbs_flag==True and '--- Lewis ----' in line:
                    found_orbs_flag=True

                if found_orbs_flag ==True:
                    if 'CR' in line:
                        uncut_ncores=line.split()
                        n_cores=int(uncut_ncores[0][:-1])
                        core.orbs.append(n_cores)
                    
                    if 'BD' in line or '3C' in line:
                        check_if_pi=True
                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])
                    
                    if 'LP' in line or 'LV' in line:

                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])

                        a=line[line.find('p'):]
                        b=a[:a.find('%')]
                        c=b[b.find('('):]
                        p_perc=float(c.replace('(',''))

                        # if 'Mg' in line:
                        #     mg.orbs.append(n_bd)

                        if p_perc>90.0:
                            pi.orbs.append(n_bd)

                            ####pi type
                            if int(uncut_BD[6])>60:
                                type_1.orbs.append(n_bd)
                            else:
                                type_2.orbs.append(n_bd)

                        else:
                            sigma.orbs.append(n_bd)


                    if 'RY' in line:

                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])

                        a=line[line.find('p'):]
                        b=a[:a.find('%')]
                        c=b[b.find('('):]
                        p_perc=float(c.replace('(',''))

                        a=line[line.find('d'):]
                        b=a[:a.find('%')]
                        c=b[b.find('('):]
                        try:
                            d_perc=float(c.replace('(',''))
                        except ValueError:
                            d_perc=0.0

                        a=line[line.find('Y'):]
                        a=a[a.find(')'):]
                        b=a[:a.find('s')]
                        #c=b[b.find('('):]
                        # which_type=(b.replace('H',''))
                        # which_type=(which_type.replace('C',''))
                        # which_type=int(which_type.replace(')',''))

                        # if p_perc>85.0:
                        #     if which_type>60:
                        #         ry_p1.orbs.append(n_bd)
                        #     else:
                        #         ry_p2.orbs.append(n_bd)
                        # elif d_perc>85.0:
                        #     if which_type>60:
                        #         ry_d1.orbs.append(n_bd)
                        #     else:
                        #         ry_d2.orbs.append(n_bd)
                        # else:
                        #     sigma.orbs.append(n_bd)

                        
                        sigma.orbs.append(n_bd)
                        #ry_orb.append(n_bd)

                        # if 'H' in line:
                        #     a=line[line.find('p'):]
                        #     b=a[:a.find('%')]
                        #     c=b[b.find('('):]
                        #     p_perc=float(c.replace('(',''))
                        #     if p_perc>92.0:
                        #         ry_hydro_p_orb.append(n_bd)
                        #     else:
                        #         ry_hydro_s_orb.append(n_bd)



                    ### Check if pi orbital needs a bit of work with numbers
                    if check_if_pi==True:
                        if '%' in line:

                            a=line[line.find('p'):]
                            b=a[:a.find('%')]
                            c=b[b.find('('):]
                            p_perc=float(c.replace('(',''))
                        
                            if p_perc>90.0:
                                pi.orbs.append(n_bd)
                                #was_it_pi_flag=True

                                ####pi type
                                if int(uncut_BD[len(uncut_BD)-1])>60:
                                    type_1.orbs.append(n_bd)
                                else:
                                    type_2.orbs.append(n_bd)


                            else:
                                sigma.orbs.append(n_bd)

                            check_if_pi=False

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

            if 'NBO #' in line:
                comp_flag=True
                comp_start_flag=True
                ### Give a value to all Pi_alone
                # for p_orb in range(0,len(pi_orb)-1):
                #     pi_alone[x,y,z,p_orb]=0
                core.values[x,y,z]=0
                # mg.values[x,y,z]=0
                
            if comp_flag==True:
                if comp_start_flag==True and '----------' not in line and 'sum' not in line and 'NBO' not in line:
                    cut_ncs=line.split()
                    #print(line)
                    which_nbo=int(cut_ncs[0][:-1])
                    if which_nbo<=n_lewis:
                        values_of_which=float(cut_ncs[1])

                        adf.Which_Orbital(types,which_nbo,values_of_which,x,y,z)
                                

                if 'sum' in line:
                    comp_start_flag=False
                    comp_flag=False
                    ###total
                    sum_uncut=line.split()
                    total.values[x,y,z]=float(sum_uncut[1])

                    #update
                    y+=1
                    if y==3:
                        y=0
                        x+=1
                        #eigen_incr+=1
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


###Execute
adf.Get_Adf_Geom(path,dirs)

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        file_search(data_file)

print("My program took" + str(time.time() - start_time)+ " to run")