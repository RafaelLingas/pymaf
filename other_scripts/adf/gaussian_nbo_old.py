##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
#from typing import Counter
import numpy as np

#path = 'D:\\phd\\charistos\\nbo\\nbo_tests\\1'
path=input("paste path here:")
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
for i in range(0,len(atoms)):
    if atoms[i]=="C":
        atoms_N.append("6")
    if atoms[i]=="H":
        atoms_N.append("1")
    if atoms[i]=="I":
        atoms_N.append("53")

        
if not os.path.exists("nbo_run"):
    os.makedirs("nbo_run")
os.chdir(path+"/nbo_run")

output=open("geometry.txt","w+")

for i in range(0,len(atoms)):
    output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

output.close()

###

###
""" 
###NCS
ghost_num=0

###new matrices
#l_nl_total=[]

l_only={}
nl_only={}
total={}
core={}
pi={}
sigma={}
pi_alone={}
len_pi_orb = 0 """



#def file_search(fname, ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone):
def file_search(fname):
    ###NCS
    ghost_num=0

    ###new matrices
    #l_nl_total=[]

    l_only={}
    nl_only={}
    total={}
    core={}
    pi={}
    sigma={}
    pi_alone={}
    len_pi_orb = 0
    ## Orbital flags and variables##
    check_orbs_flag=True
    finding_orbs_flag=False
    found_orbs_flag=False
    check_if_pi=False
    ncs_flag=False
    ghost_flag=False
    nbo_matrix_flag=False
    cartesian_ncs=[]
    nbo=[]

    core_orb=[]
    sigma_orb=[]
    pi_orb=[]
    next_pi=0
    first_pi_alone_ghost_flag=True
    first_core_ghost_flag=True
    first_pi_ghost_flag=True
    first_sigma_ghost_flag=True
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
                        #print(line)
                    
                    if 'LP' in line or 'LV' in line:
                        #check_if_pi=True ### Will check in the same line
                        uncut_BD=line.split()
                        #print(uncut_BD)
                        n_bd=int(uncut_BD[0][:-1])


                        if 'd' in line:
                            lp_perc=uncut_BD[10][:-3]
                            if float(lp_perc)>97.0:
                                pi_orb.append(n_bd)
                            else:
                                sigma_orb.append(n_bd)
                        else:
                            
                            lp_perc=uncut_BD[len(uncut_BD)-1][:-2]
                            if '(' in lp_perc:
                                lp_perc=uncut_BD[len(uncut_BD)-1][:-2].split('(',1)
                            #lp_perc=uncut_BD[len(uncut_BD)][:-2].split('(',1)
                            if float(lp_perc[1])>97.0:
                                pi_orb.append(n_bd)
                            else: sigma_orb.append(n_bd)

                    ### Check if pi orbital needs a bit work with numbers
                    if check_if_pi==True:
                        if '%' in line:
                            check_if_big=line.split()
                            #print(check_if_big)
                            
                            #print(check_if_big)
                            orb_perc=check_if_big[1][:-2]
                            if float(orb_perc)>30.0:
                                if 'd' in line:
                                    d_in=next(s for s in check_if_big if 'd' in s)


                                    if float(d_in[:-3])>97.0:
                                        pi_orb.append(n_bd)
                                        #print(uncut_BD)
                                    else:
                                        sigma_orb.append(n_bd)
                                else:
                                    if '(' in check_if_big[7][:-3]:
                                        cut_1=check_if_big[7][:-3].split('(',1)
                                        if float(cut_1[1])>97.0:
                                            pi_orb.append(n_bd)
                                        else: sigma_orb.append(n_bd)
                                        sigma_orb.append(n_bd)
                                    elif float(check_if_big[7][:-3])>97.0:
                                        pi_orb.append(n_bd)
                                    else:
                                        sigma_orb.append(n_bd)
                            check_if_pi=False
            
            if nbo_matrix_flag==True:
                cartesian_ncs.append(line)
                if '=' not in line and '--' not in line and 'XX' not in line:
                    cut_ncs=line.split()
                    #print(line)
                    #l_nl_total.append(line)

                    if 'L' == cut_ncs[0]:
                        for i in range(1,10):
                            l_only[ghost_num,i-1]=cut_ncs[i]
                    elif 'NL' == cut_ncs[0]:
                        for i in range(1,10):
                            nl_only[ghost_num,i-1]=cut_ncs[i]
                    elif 'Total' == cut_ncs[0]:
                        for i in range(1,10):
                            total[ghost_num,i-1]=cut_ncs[i]
                    else:
                        which_nbo=int(cut_ncs[0][:-1])
                        if which_nbo<=n_lewis:
                            values_of_which=cut_ncs

                            ##Fix checking which orbital
                            ar_core=np.array(core_orb)
                            ar_sigma=np.array(sigma_orb)
                            ar_pi=np.array(pi_orb)

                            is_it_core=np.where(ar_core==which_nbo)
                            is_it_sigma=np.where(ar_sigma==which_nbo)
                            is_it_pi=np.where(ar_pi==which_nbo)

                            if ar_core[is_it_core].size >0:
                                for k in range(1,10):
                                    if first_core_ghost_flag==True:
                                        core[ghost_num,k-1]=values_of_which[k]
                                    if first_core_ghost_flag==False:
                                        core[ghost_num,k-1]=float(core[ghost_num,k-1])+float(values_of_which[k])

                                first_core_ghost_flag=False

                            if ar_sigma[is_it_sigma].size >0:
                                for k in range(1,10):
                                    if first_sigma_ghost_flag==True:
                                        sigma[ghost_num,k-1]=values_of_which[k]
                                    else:
                                        sigma[ghost_num,k-1]=float(sigma[ghost_num,k-1])+float(values_of_which[k])

                                first_sigma_ghost_flag=False

                            if ar_pi[is_it_pi].size >0:
                                #print(which_nbo)
                                for k in range(1,10):
                                    if first_pi_ghost_flag==True:
                                        pi[ghost_num,k-1]=values_of_which[k]
                                    if first_pi_ghost_flag==False:
                                        pi[ghost_num,k-1]=float(pi[ghost_num,k-1])+float(values_of_which[k])

                                    try:
                                        pi_alone[ghost_num,k-1,pi_orb.index(which_nbo)]=float(values_of_which[k])+float(pi_alone[ghost_num,k-1,pi_orb.index(which_nbo)])
                                    except KeyError:
                                        pi_alone[ghost_num,k-1,pi_orb.index(which_nbo)]=values_of_which[k]
                                        

                                first_pi_ghost_flag=False

                
                if 'Total' in line:
                    nbo_matrix_flag=False
                    ghost_flag=False


                    first_core_ghost_flag=True
                    first_pi_ghost_flag=True
                    first_sigma_ghost_flag=True
                    ###experiment
                    #next_pi=0

                    #print(ncs_only)


                    ##clean matrix from ----
                    # cartesian_ncs.pop(0)
                    # cartesian_ncs.pop(0)
                    # cartesian_ncs.pop(len(cartesian_ncs)-5)
                    # cartesian_ncs.pop(len(cartesian_ncs)-2)
                    #n_nbos=(len(cartesian_ncs)-3) ##how many MOs are
                    #print(cartesian_ncs)

                    #for i in range(0,len(cartesian_ncs)):

                     #   nbo.append(cartesian_ncs[i].split())


                    #arr=np.array(nbo)
                    #nbo=[]
                    cartesian_ncs=[]
                    #print(arr)
                    #print(n_nbos)

                    # for k in range(0,n_nbos+1):   ###instead of n_mos+1
                    #     #for j in range(0,10):
                    #         ##hotfix
                    #         #if ghost_num<2000:
                    #         j=0
                    #         t=9
                    #         all_nbos[ghost_num,k,j]=arr[k,j]
                    #         all_nbos[ghost_num,k,t]=arr[k,t]
                    #         #if ghost_num>1999:
                    #         #    all_nbos_2[ghost_num,k,j]=arr[k,j]
                
                    ghost_num+=1

            if 'NATURAL CHEMICAL SHIELDING ANALYSIS:' in line:
                ncs_flag=True
            
            if ncs_flag==True and 'Full Cartesian' in line and 'gh(' in line:
                ghost_flag=True

            if ghost_flag==True and 'NBO' in line:
                nbo_matrix_flag=True
    
    

    components=["xx","xy","xz","yx","yy","yz","zx","zy","zz"]
    file_types=["core","sigma","pi","L","NL","Total"]
    for m in range(0,9):
        os.chdir(path+"/nbo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/nbo_run/"+components[m])
        for n in range(0,6):
            output=open(file_types[n]+".txt","a")
            for k in range(0,ghost_num):
                if n==0:
                    output.write(str((-1)*float(core[k,m]))+"\n")
                if n==1:
                    output.write(str((-1)*float(sigma[k,m]))+"\n")
                if n==2:
                    output.write(str((-1)*float(pi[k,m]))+"\n")
                if n==3:
                    output.write(str((-1)*float(l_only[k,m]))+"\n")
                if n==4:
                    output.write(str((-1)*float(nl_only[k,m]))+"\n")
                if n==5:
                    output.write(str((-1)*float(total[k,m]))+"\n")

                
            output.close()

        for g in range(0,len(pi_orb)):
            output=open("_pi_"+str(pi_orb[g])+"_"+".txt","a")
            for k in range(0,ghost_num):
                output.write(str((-1)*float(pi_alone[k,m,g]))+"\n")
            output.close()
    #return ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone, len(pi_orb)

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        #ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone,len_pi_orb = file_search(data_file, ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone)
        file_search(data_file)



#print(core)

                    