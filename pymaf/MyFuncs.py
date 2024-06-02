import numpy as np
import os#,sys


def Principal_To_Cartesian(E1,E1_inv,type,z1):
    for i in range(0,3):
        D=np.array([[type[0,i,z1],0,0],[0,type[1,i,z1],0],[0,0,type[2,i,z1]]])
        D.reshape((3,3))
        C=E1@D@E1_inv
        type[0,i,z1]=str(-1*C[0,0])
        type[1,i,z1]=str(-1*C[1,1])
        type[2,i,z1]=str(-1*C[2,2])
        ##iso and aniso are 3,4
        type[3,i,z1]=str(-1*type[3,i,z1])
        type[4,i,z1]=str(-1*type[4,i,z1])
        
        type[5,i,z1]=str(-1*C[0,1])
        type[6,i,z1]=str(-1*C[0,2])
        type[7,i,z1]=str(-1*C[1,0])
        type[8,i,z1]=str(-1*C[1,2])
        type[9,i,z1]=str(-1*C[2,0])
        type[10,i,z1]=str(-1*C[2,1])


def Get_Adf_Geom(path,dirs,which_run):
    ###Get a file for geometry
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


    if not os.path.exists(which_run):
        os.makedirs(which_run)
    os.chdir(path+"/"+which_run)

    output=open("geometry.txt","w+")

    for i in range(0,len(atoms)):
        output.write(str(int(float(atoms_N[i])))+"\t"+atoms[i]+"\t"+atoms_x[i]+"\t"+atoms_y[i]+"\t"+atoms_z[i]+"\n")

    output.close()
    
    os.chdir(path)
    
    for data_file in dirs:
        if "grid" in data_file:
            a=[]
            file_name=data_file
            with open(file_name,'r') as input_data:
                for line in input_data:
                    a.append(line)
            os.chdir(path+"/"+which_run)
            output=open("gridspecs.txt","w+")
            for item in a:
                output.write(item)
            output.close()
            os.chdir(path)
            break




def Create_Files_Adf(path,z,what,which_run):

    components=["xx","yy","zz","Isotropic","Anisotropy","xy","xz","yx","yz","zx","zy"]
    para_dia=["Paramagnetic_SO","Diamagnetic","Sum_Para_SO_Diamagnetic"]
    for m in range(0,11):
        os.chdir(path+"/"+which_run)
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/"+which_run+"/"+components[m])
        for n in range(0,3):
            for item in what:
                output=open(para_dia[n]+'_'+item.name+".txt","a")
                for k in range(0,z):
                    output.write(item.values[m,n,k]+"\n")
                output.close()

def Create_Files_CMO_Adf(path,z,orbitals,homo,totals):
    components=["xx","yy","zz","Isotropic"]
    para_dia=["occ_vir","total"]
    for m in range(0,4):
        os.chdir(path+"/cmo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path+"/cmo_run/"+components[m])
        for n in range(0,2):
            for i in range(homo-10,homo+1):
                output=open(para_dia[n]+'_'+str(i)+".txt","a")
                for k in range(0,z):
                    output.write(str(-1*orbitals[i,m,n,k])+"\n")
                output.close()

            #for c in range(0,2):
            output=open(para_dia[n]+"_all.txt","a")
            for k in range(0,z):
                output.write(str(-1*totals[n,m,k])+"\n")
            output.close()

def Which_Orbital(diff_types,nbo,value,x,y,z):
    for item in diff_types:
        if nbo in item.orbs:
            try:
                item.values[x,y,z]=item.values[x,y,z]+value
            except KeyError:
                item.values[x,y,z]=value

class Orbital:
    orbitals=[]
    def __init__(self,name):
        self.name=name
        self.orbs=[]
        self.values={}
        Orbital.orbitals.append(self)


class Cmos:
    def __init__(self,hm):
        self.comp=[]
        self.homo=hm

    #def 

    def Occ_vir(self,orbitals,x,z):
        new_comp=[]
        for item in self.comp:
            if 'Total for' in item:
                new_comp.append(item)
        
        columns=list(zip(*(row.split() for row in new_comp)))
        which=list(columns[4])
        which=[int(x) for x in which]
        value=list(columns[5])

        if len(new_comp)<2*self.homo:
            for i in range(0,2*self.homo):
                if int(i+1) not in which:
                    which.insert(i,int(i+1))
                    value.insert(i,0.0)

        incr=1
        for i in range(0,2*self.homo):
            try:
                orbitals[incr,x,0,z]+=float(value[i])
                orbitals[incr,x,1,z]+=float(value[i])
            except KeyError:
                orbitals[incr,x,0,z]=float(value[i])
                orbitals[incr,x,1,z]=float(value[i])
            
            if (i+1)%2==0:
                incr+=1


                

    def Occ_occ(self,orbitals,x,z):
        new_comp=[]
        for item in self.comp:
            if 'Total for' in item:
                new_comp.append(item)
        
        columns=list(zip(*(row.split() for row in new_comp)))
        which=list(columns[4])
        which=[int(x) for x in which]
        value=list(columns[5])

        if len(new_comp)<2*self.homo:
            for i in range(0,2*self.homo):
                if int(i+1) not in which:
                    which.insert(i,int(i+1))
                    value.insert(i,0.0)

        incr=1
        for i in range(0,2*self.homo):
            try:
                orbitals[incr,x,1,z]+=float(value[i])
            except KeyError:
                orbitals[incr,x,1,z]=float(value[i])
            
            if (i+1)%2==0:
                incr+=1


    def Diamagnetic(self,orbitals,x,z):
        del self.comp[-1]
        columns=list(zip(*(row.split() for row in self.comp)))
        which=list(columns[0])
        which=[int(x) for x in which]
        value=list(columns[1])


        if len(self.comp)<2*self.homo:
            for i in range(0,2*self.homo):
                if int(i+1) not in which:
                    which.insert(i,int(i+1))
                    value.insert(i,0.0)
        
        incr=1
        for i in range(0,2*self.homo):
            try:
                orbitals[incr,x,1,z]+=float(value[i])
            except KeyError:
                orbitals[incr,x,1,z]=float(value[i])
            
            if (i+1)%2==0:
                incr+=1

    
