##Control+K then Control+C adds comments for selected lines
## Control+K then Control-U removes comments

import os,sys
#from typing import Counter
import numpy as np

#path = 'D:\\phd\\charistos\\nbo\\nbo_tests\\1'
# path=("F:\\workspace\\test_dir\\c6i6_tests\\dic\\gaussian")
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

def Which_Orbital(diff_types,nbo,value,ghost):
    for item in diff_types:
        if nbo in item.orbs:
            for k in range(1,10):
                try:
                    item.values[ghost,k-1]=item.values[ghost,k-1]+float(value[k])
                except KeyError:
                    item.values[ghost,k-1]=float(value[k])




class Orbital:
    orbitals=[]
    def __init__(self,name):
        self.name=name
        self.orbs=[]
        self.values={}
        Orbital.orbitals.append(self)



#def file_search(fname, ghost_num,l_only,nl_only,total,core,pi,sigma,pi_alone):
def file_search(fname):
    ###NCS
    ghost_num=0

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


    core=Orbital("core")
    sigma=Orbital("sigma")
    pi=Orbital("pi")
    total=Orbital("total")

    lewis=Orbital("lewis")
    non_lewis=Orbital("non_lewis")

    lp1=Orbital("lp1")
    # lp2=Orbital("lp2")
    # lp3=Orbital("lp3")
    # cc=Orbital("cc")
    # ci=Orbital("ci")
    # ii=Orbital("ii")
    lv=Orbital("lv")
    type_1=Orbital("type_1")
    type_2=Orbital("type_2")


    types=(core,sigma,pi,lp1,lv,type_1,type_2,total)#,type_1,type_2)#,ry_p1,ry_p2,ry_d1,ry_d2)


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
                        core.orbs.append(n_cores)
                    
                    if 'BD' in line:
                        check_if_pi=True
                        uncut_BD=line.split()
                        n_bd=int(uncut_BD[0][:-1])
                        aa=uncut_BD[len(uncut_BD)-1]

                        if int(aa)<=60:
                            type_1.orbs.append(n_bd)
                        else:
                            type_2.orbs.append(n_bd)

                        # if 'BD' in line and 'C' in line and 'I' in line:
                        #     ci.orbs.append(n_bd)
                        # if 'BD' in line and 'C' not in line and 'I' in line:
                        #     ii.orbs.append(n_bd)
                    
                    if 'LP' in line or 'LV' in line:
                        #check_if_pi=True ### Will check in the same line
                        uncut_BD=line.split()
                        #print(uncut_BD)
                        n_bd=int(uncut_BD[0][:-1])


                        if 'd' in line:
                            lp_perc=uncut_BD[10][:-3]
                            if float(lp_perc)>97.0:
                                pi.orbs.append(n_bd)
                            else:
                                sigma.orbs.append(n_bd)
                        else:
                            
                            lp_perc=uncut_BD[len(uncut_BD)-1][:-2]
                            if '(' in lp_perc:
                                lp_perc=uncut_BD[len(uncut_BD)-1][:-2].split('(',1)
                            #lp_perc=uncut_BD[len(uncut_BD)][:-2].split('(',1)
                                if float(lp_perc[1])>97.0:
                                    pi.orbs.append(n_bd)
                            elif float(lp_perc)>97.0:
                                #print(uncut_BD)
                                #print(lp_perc[0])
                                pi.orbs.append(n_bd)
                            else: sigma.orbs.append(n_bd)

                        if 'LP ( 1)' in line:
                            lp1.orbs.append(n_bd)
                        # if 'LP ( 2)' in line:
                        #     lp2.orbs.append(n_bd)
                        # if 'LP ( 3)' in line:
                        #     lp3.orbs.append(n_bd)
                        if 'LV' in line:
                            lv.orbs.append(n_bd)

                    ### Check if pi orbital needs a bit work with numbers
                    if check_if_pi==True:
                        if '%' in line:
                            check_if_big=line.split()

                            a=line[line.find('p'):]
                            b=a[:a.find('%')]
                            c=b[b.find('('):]
                            try:
                                p_perc=float(c.replace('(',''))
                            except ValueError:
                                    p_perc=5.0
                            
                            orb_perc=check_if_big[1][:-2]
                            if float(orb_perc)>30.0:

                                if p_perc>90.0:
                                        pi.orbs.append(n_bd)
                                    
                                    # cc.orbs.append(n_bd)

                                else:
                                    sigma.orbs.append(n_bd)

                            check_if_pi=False
            
            if nbo_matrix_flag==True:
                cartesian_ncs.append(line)

                if '=' not in line and '--' not in line and 'XX' not in line:
                    cut_ncs=line.split()
                    #print(line)
                    #l_nl_total.append(line)

                    if 'L' == cut_ncs[0]:
                        for i in range(1,10):
                            lewis.values[ghost_num,i-1]=float(cut_ncs[i])
                    elif 'NL' == cut_ncs[0]:
                        for i in range(1,10):
                            non_lewis.values[ghost_num,i-1]=float(cut_ncs[i])
                    elif 'Total' == cut_ncs[0]:
                        for i in range(1,10):
                            total.values[ghost_num,i-1]=float(cut_ncs[i])
                    else:
                        which_nbo=int(cut_ncs[0][:-1])
                        if which_nbo<=n_lewis:
                            values_of_which=cut_ncs


                            Which_Orbital(types,which_nbo,values_of_which,ghost_num)

                
                if 'Total' in line:
                    nbo_matrix_flag=False
                    ghost_flag=False

                    ##clean matrix from ----
                    cartesian_ncs.pop(0)
                    cartesian_ncs.pop(0)
                    cartesian_ncs.pop(len(cartesian_ncs)-5)
                    cartesian_ncs.pop(len(cartesian_ncs)-2)
                    #n_nbos=(len(cartesian_ncs)-3) ##how many MOs are
                    #print(cartesian_ncs)

                    for i in range(0,len(cartesian_ncs)):

                        nbo.append(cartesian_ncs[i].split())


                    arr=np.array(nbo)
                    nbo=[]
                    cartesian_ncs=[]
                
                    ghost_num+=1            


            if 'NATURAL CHEMICAL SHIELDING ANALYSIS:' in line:
                ncs_flag=True

                
            
            if ncs_flag==True and 'Full Cartesian' in line and 'gh(' in line:
                ghost_flag=True

            if ghost_flag==True and 'NBO' in line:
                nbo_matrix_flag=True
                for item in types:
                    for k in range(1,10):
                        item.values[ghost_num,k-1]=0
    
    
    #print(pi_orb)
    
    components=["xx","xy","xz","yx","yy","yz","zx","zy","zz"]
    #file_types=["core","sigma","pi","L","NL","Total"]
    for m in range(0,9):
        os.chdir(path+"/nbo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/nbo_run/"+components[m])

        for item in types:
            output=open('_'+item.name+".txt","a")
            for k in range(0,ghost_num):
                output.write(str((-1)*item.values[k,m])+"\n")
            output.close()

##starting main loop
for data_file in dirs:
    if data_file.endswith(".out"):
        file_search(data_file)



#print(core)

                    