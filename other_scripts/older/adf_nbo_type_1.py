##(Occupancy)   Bond orbital / Coefficients / Hybrids

##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
import numpy as np

#path = 'D:\\phd\\charistos\\nbo\\nbo_tests\\1'
#path=input("path:")
path=("D:\\phd\\charistos\\nbo\\russian_dolls\\adf_tests")
os.chdir(path)

dirs=os.listdir(path)
dirs.sort()
# actualdirs = [a for a in dirs]

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
        if 'G E O M E T R Y' in line:
            geometry_flag=True
        if geometry_flag==True:
            if '1' in line:
                first_atom_flag=True
            if 'FRAGMENTS' in line:
                end_geometry=True
        if end_geometry==True:
            break
        if first_atom_flag==True:
            geometry_array.append(line)

del geometry_array[-1]
del geometry_array[-1]
geom = list(zip(*(row.split() for row in geometry_array)))
atoms=list(geom[1])
atoms_x=list(geom[2])
atoms_y=list(geom[3])
atoms_z=list(geom[4])
atoms_N=list(geom[5])

if not os.path.exists("nbo_run"):
    os.makedirs("nbo_run")
os.chdir(path+"/nbo_run")

output=open("geometry.txt","w+")

for i in range(0,len(atoms)):
    output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

output.close()

def file_search(fname):
    check_orbs_flag=True
    finding_orbs_flag=False
    found_orbs_flag=False
    check_if_pi=False
    ncs_flag=False
    ghost_flag=False
    nbo_matrix_flag=False
    #cartesian_ncs=[]
    nbo=[]

    core_orb=[]
    sigma_orb=[]
    pi_orb=[]

    ### GHOSTS and choosing components
    ghost_flag=False
    eigenvectors_flag=False
    eigenvector_array=[]
    ###eigen

    x=0
    y=0
    z=0
    total={}
    core={}
    sigma={}
    pi={}
    pi_alone={}
    comp_flag=False
    comp_start_flag=False
    #comp_end_flag=False
    #comp_array=[]

    ### Pi types test
    was_it_pi_flag=False
    type_1_orb=[]
    type_1={}


    ### End Pi types test


    os.chdir(path)
    with open(data_file,'r') as input_data:
        print("Working on: "+data_file)
        for line in input_data:
            if check_orbs_flag==True:
                if found_orbs_flag==True and ('RY' in line or 'NHO DIRECTIONALITY' in line):
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
                        core_orb.append(n_cores)
                    
                    if 'BD' in line:
                        check_if_pi=True
                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])
                    
                    if 'LP' in line or 'LV' in line:

                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])

                        a=line[line.find('p'):]
                        b=a[:a.find(')')]
                        if '1.00' in b or '99.' in b or '98.' in b:
                            pi_orb.append(n_bd)
                            was_it_pi_flag=True
                        else:
                            sigma_orb.append(n_bd)


                        ###Pi type
                        if was_it_pi_flag==True:
                            was_it_pi_flag=False
                            if int(uncut_BD[6])>60:
                                type_1_orb.append(n_bd)



                    ### Check if pi orbital needs a bit of work with numbers
                    if check_if_pi==True:
                        if '%' in line:

                            a=line[line.find('p'):]
                            b=a[:a.find(')')]
                            if '1.00' in b or '99.' in b or '98.' in b:
                                pi_orb.append(n_bd)
                                was_it_pi_flag=True
                            else:
                                sigma_orb.append(n_bd)

                            check_if_pi=False

                            ###Pi type
                            if was_it_pi_flag==True:
                                was_it_pi_flag=False
                                #print(uncut_BD[len(uncut_BD)-1])
                                if int(uncut_BD[len(uncut_BD)-1])>60:
                                    type_1_orb.append(n_bd)
                
            #for line in input_data:
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
                        #eigen_1=list(columns_eigen[0])
                        #eigen_2=list(columns_eigen[1])
                        #eigen_3=list(columns_eigen[2])

                if eigenvectors_flag==True:
                    eigenvector_array.append(line)

                if 'eigenvectors' in line:
                    eigenvectors_flag=True

            if 'NBO #' in line:
                comp_flag=True
                comp_start_flag=True
                ### Give a value to all Pi_alone
                for p_orb in range(0,len(pi_orb)-1):
                    pi_alone[x,y,z,p_orb]=0
                core[x,y,z]=0
                
            if comp_flag==True:
                #print(line)
                # if '1:' in line:
                #     comp_start_flag=True



                if comp_start_flag==True and '----------' not in line and 'RY' not in line and 'sum' not in line and 'NBO' not in line:
                    cut_ncs=line.split()
                    #print(line)
                    which_nbo=int(cut_ncs[0][:-1])
                    if which_nbo<=n_lewis:
                        values_of_which=cut_ncs[1]

                        ##Fix checking which orbital
                        ar_core=np.array(core_orb)
                        ar_sigma=np.array(sigma_orb)
                        ar_pi=np.array(pi_orb)

                        is_it_core=np.where(ar_core==which_nbo)
                        is_it_sigma=np.where(ar_sigma==which_nbo)
                        is_it_pi=np.where(ar_pi==which_nbo)

                        ###pi type test
                        ar_type_1=np.array(type_1_orb)
                        is_it_type_1=np.where(ar_type_1==which_nbo)

                        if ar_type_1[is_it_type_1].size >0:
                            try:
                                type_1[x,y,z]=float(type_1[x,y,z])+float(values_of_which)
                            except KeyError:
                                type_1[x,y,z]=values_of_which

                        ### end pi type test

                        if ar_core[is_it_core].size >0:
                            try:
                                core[x,y,z]=float(core[x,y,z])+float(values_of_which)
                            except KeyError:
                                core[x,y,z]=values_of_which

                        if ar_sigma[is_it_sigma].size >0:
                            try:
                                sigma[x,y,z]=float(sigma[x,y,z])+float(values_of_which)
                            except KeyError:
                                sigma[x,y,z]=values_of_which

                        if ar_pi[is_it_pi].size >0:
                            try:
                                pi[x,y,z]=float(pi[x,y,z])+float(values_of_which)
                            except KeyError:
                                pi[x,y,z]=values_of_which

                            try:
                                pi_alone[x,y,z,pi_orb.index(which_nbo)]=float(values_of_which)+float(pi_alone[x,y,z,pi_orb.index(which_nbo)])
                            except KeyError:
                                pi_alone[x,y,z,pi_orb.index(which_nbo)]=values_of_which
                                
                        #next_pi+=1

                        first_pi_ghost_flag=False



                if 'sum' in line:
                    comp_start_flag=False
                    comp_flag=False
                    #comp_array.append(line)

                    ###total
                    sum_uncut=line.split()
                    total[x,y,z]=sum_uncut[1]


                    
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


                        ### pi type test

                        for i in range(0,3):
                            D=np.array([[type_1[0,i,z],0,0],[0,type_1[1,i,z],0],[0,0,type_1[2,i,z]]])
                            D.reshape((3,3))
                            C=E@D@E_inv
                            type_1[0,i,z]=C[0,0]
                            type_1[1,i,z]=C[1,1]
                            type_1[2,i,z]=C[2,2]
                            
                            type_1[5,i,z]=C[0,1]
                            type_1[6,i,z]=C[0,2]
                            type_1[7,i,z]=C[1,0]
                            type_1[8,i,z]=C[1,2]
                            type_1[9,i,z]=C[2,0]
                            type_1[10,i,z]=C[2,1]


                        # end pi type test

                        ##core
                        for i in range(0,3):
                            D=np.array([[core[0,i,z],0,0],[0,core[1,i,z],0],[0,0,core[2,i,z]]])
                            D.reshape((3,3))
                            C=E@D@E_inv
                            core[0,i,z]=C[0,0]
                            core[1,i,z]=C[1,1]
                            core[2,i,z]=C[2,2]
                            
                            core[5,i,z]=C[0,1]
                            core[6,i,z]=C[0,2]
                            core[7,i,z]=C[1,0]
                            core[8,i,z]=C[1,2]
                            core[9,i,z]=C[2,0]
                            core[10,i,z]=C[2,1]


                        ##sigma
                        for i in range(0,3):
                            D=np.array([[sigma[0,i,z],0,0],[0,sigma[1,i,z],0],[0,0,sigma[2,i,z]]])
                            D.reshape((3,3))
                            C=E@D@E_inv
                            sigma[0,i,z]=C[0,0]
                            sigma[1,i,z]=C[1,1]
                            sigma[2,i,z]=C[2,2]
                            
                            sigma[5,i,z]=C[0,1]
                            sigma[6,i,z]=C[0,2]
                            sigma[7,i,z]=C[1,0]
                            sigma[8,i,z]=C[1,2]
                            sigma[9,i,z]=C[2,0]
                            sigma[10,i,z]=C[2,1]


                        ##pi
                        for i in range(0,3):
                            D=np.array([[pi[0,i,z],0,0],[0,pi[1,i,z],0],[0,0,pi[2,i,z]]])
                            D.reshape((3,3))
                            D=D.astype(np.float64)
                            C=E@D@E_inv
                            C=C.astype(np.float64)
                            pi[0,i,z]=C[0,0]
                            pi[1,i,z]=C[1,1]
                            pi[2,i,z]=C[2,2]
                            
                            pi[5,i,z]=C[0,1]
                            pi[6,i,z]=C[0,2]
                            pi[7,i,z]=C[1,0]
                            pi[8,i,z]=C[1,2]
                            pi[9,i,z]=C[2,0]
                            pi[10,i,z]=C[2,1]


                        for k in range(0,len(pi_orb)-1):
                            for i in range(0,3):
                                D=np.array([[pi_alone[0,i,z,k],0,0],[0,pi_alone[1,i,z,k],0],[0,0,pi_alone[2,i,z,k]]])
                                D.reshape((3,3))
                                D=D.astype(np.float64)
                                C=E@D@E_inv
                                C=C.astype(np.float64)
                                pi_alone[0,i,z,k]=C[0,0]
                                pi_alone[1,i,z,k]=C[1,1]
                                pi_alone[2,i,z,k]=C[2,2]
                                
                                pi_alone[5,i,z,k]=C[0,1]
                                pi_alone[6,i,z,k]=C[0,2]
                                pi_alone[7,i,z,k]=C[1,0]
                                pi_alone[8,i,z,k]=C[1,2]
                                pi_alone[9,i,z,k]=C[2,0]
                                pi_alone[10,i,z,k]=C[2,1]


                        ##total
                        for i in range(0,3):
                            D=np.array([[total[0,i,z],0,0],[0,total[1,i,z],0],[0,0,total[2,i,z]]])
                            D=D.astype(float)
                            D.reshape((3,3))
                            C=E@D@E_inv
                            total[0,i,z]=C[0,0]
                            total[1,i,z]=C[1,1]
                            total[2,i,z]=C[2,2]
                            
                            total[5,i,z]=C[0,1]
                            total[6,i,z]=C[0,2]
                            total[7,i,z]=C[1,0]
                            total[8,i,z]=C[1,2]
                            total[9,i,z]=C[2,0]
                            total[10,i,z]=C[2,1]

                        
                        x=0
                        z+=1
            
                    #comp_array=[]

            if comp_start_flag==True:
                #comp_array.append(line)
                pass

    components=["xx","yy","zz","Isotropic","Anisotropy","xy","xz","yx","yz","zx","zy"]
    para_dia=["Paramagnetic_SO","Diamagnetic","Sum_Para_SO_Diamagnetic"]
    create_files=["total","pi","sigma","core"]
    for m in range(0,11):
        os.chdir(path+"/nbo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/nbo_run/"+components[m])
        for n in range(0,3):
            for file in range(0,4):
                output=open(para_dia[n]+"_"+create_files[file]+".txt","a")
                for k in range(0,z):
                    if file==0:
                        output.write(str((-1)*float(total[m,n,k]))+"\n")
                    if file==1:
                        output.write(str(np.float64((-1)*pi[m,n,k]))+"\n")
                    if file==2:
                        output.write(str((-1)*sigma[m,n,k])+"\n")
                    if file==3:
                        output.write(str((-1)*core[m,n,k])+"\n")
                    
                output.close()

            # for g in range(0,len(pi_orb)-1):
            #     output=open(para_dia[n]+"_pi_"+str(pi_orb[g])+"_"+".txt","a")
            #     for k in range(0,z):
            #         output.write(str((-1)*float(pi_alone[m,n,k,g]))+"\n")
            #     output.close()

            ##pi_type
            output=open(para_dia[n]+"_pi_type_1"+".txt","a")
            for k in range(0,z):
                output.write(str((-1)*float(type_1[m,n,k]))+"\n")
            output.close()
        
        # for g in range(0,len(sigma_orb)):
        #     output=open("_sigma_"+str(sigma_orb[g])+"_"+".txt","a")
        #     for k in range(0,ghost_num):
        #         output.write(str((-1)*float(sigma_alone[k,m,g]))+"\n")
        #     output.close()
    #return ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone, len(pi_orb)



##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        #ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone,len_pi_orb = file_search(data_file, ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone)
        file_search(data_file)