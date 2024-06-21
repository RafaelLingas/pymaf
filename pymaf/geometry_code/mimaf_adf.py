import os
import math





class runs:
    def __init__(self,name,atoms,size,step,sym,dim,plane,
    max_ghosts,method,basis_set,charge,criteria,memory,nproc,text_log,both_flag):
        self.name=name
        self.atoms=atoms
        self.size=size
        self.step=step
        self.sym=sym
        self.dim=dim
        self.plane=plane
        self.max_ghosts=max_ghosts
        self.method=method
        self.basis_set=basis_set
        self.charge=charge
        self.criteria=criteria
        self.memory=memory
        self.nproc=nproc
        self.text_log=text_log
        self.both_flag=both_flag

    def adf_run(self,analysis):
        self.analysis=analysis
        self.gridspecs()

        file_number=1
        output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
        self.text_log.append("Created "+str(file_number)+" files")

        self.adfgeom()

        self.adf_geom_plus(output)
        
        self.get_ghost_geom()

        ghost_iter=1
        self.ghost_matrix=[]

        if self.dim=="2d":
            if self.plane=='xy':
                z=self.cut
                ###hotfix
                side=0
                if self.sym=="z":
                    side=self.cut
                ###end hotfix
                for x in range(0,self.size-self.x_sym):
                        for y in range(0, self.size-self.y_sym-side):
                            self.dist(x,y,z) ### if atom close to ghost move ghost_z
                            ghost=self.pos[y, z, x] +"\t"+self.pos[x, z, y]+"\t"+self.pos[x, y, z]
                            self.ghost_matrix.append(ghost)
                            output.write(ghost+"\t0.0\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                self.adf_2nd_ghost_to_end(output)

                                file_number+=1
                                if file_number<10:
                                    output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+"0"+str(file_number)+".run",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".run",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")


                                ghost_iter=1
                                self.ghost_matrix=[]

                                self.adf_geom_plus(output)                                    

            if self.plane=='xz':
                y=self.cut
                for x in range(0,self.size-self.x_sym):
                        for z in range(0, self.size-self.z_sym):
                            self.dist(x,y,z) ### if atom close to ghost move ghost_z
                            ghost=self.pos[y, z, x] +"\t"+self.pos[x, z, y]+"\t"+self.pos[x, y, z]
                            self.ghost_matrix.append(ghost)
                            output.write(ghost+"\t0.0\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                self.adf_2nd_ghost_to_end(output)

                                file_number+=1
                                if file_number<10:
                                    output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+"0"+str(file_number)+".run",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".run",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")


                                ghost_iter=1
                                self.ghost_matrix=[]

                                self.adf_geom_plus(output)                                    

            if self.plane=='yz':
                x=self.cut
                ### HotFix
                side=0
                if self.sym=="x":
                    side=x
                ### end hotfix
                for y in range(0, self.size-self.y_sym-side):
                        for z in range(0, self.size-self.z_sym):
                            self.dist(x,y,z) ### if atom close to ghost move ghost_z
                            ghost=self.pos[y, z, x] +"\t"+self.pos[x, z, y]+"\t"+self.pos[x, y, z]
                            self.ghost_matrix.append(ghost)
                            output.write(ghost+"\t0.0\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                self.adf_2nd_ghost_to_end(output)

                                file_number+=1
                                if file_number<10:
                                    output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+"0"+str(file_number)+".run",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".run",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")


                                ghost_iter=1
                                self.ghost_matrix=[]

                                self.adf_geom_plus(output)                                    

        else:
            #3d
            for x in range(0,self.size-self.x_sym):
                for y in range(0, self.size-self.y_sym):
                    for z in range(0, self.size-self.z_sym):
                        self.dist(x,y,z) ### if atom close to ghost move ghost_z
                        ghost=self.pos[y, z, x] +"\t"+self.pos[x, z, y]+"\t"+self.pos[x, y, z]


                        self.ghost_matrix.append(ghost)
                        output.write(ghost+"\t0.0\n")
                        ghost_iter+=1
                        if ghost_iter==(self.max_ghosts+1):
                            self.adf_2nd_ghost_to_end(output)

                            file_number+=1
                            if file_number<10:
                                output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                            if file_number>9 and file_number<100:
                                output=open(self.name+"_"+"0"+str(file_number)+".run",'w+')
                            if file_number>99:
                                output=open(self.name+"_"+str(file_number)+".run",'w+')
                            
                            self.text_log.append("Created "+str(file_number)+" files")


                            ghost_iter=1
                            self.ghost_matrix=[]

                            self.adf_geom_plus(output)                                                       

        #if ghost_iter!=840:
        self.adf_2nd_ghost_to_end(output)


    def dalton_run(self):

        self.get_ghost_geom()
        self.gridspecs()

        base_file=[]

        ### put the ghost in specific sized lists to then be used
        ghost_geom=[]
        for x in range(0,self.size-self.x_sym):
                for y in range(0, self.size-self.y_sym):
                    for z in range(0, self.size-self.z_sym):
                        ghost_geom.append("X "+str(float(self.pos[y, z, x])) + " " + 
                        str(float(self.pos[x, z, y])) + " " + str(float(self.pos[x, y, z]))+"\n")
                        # ghost_iter+=1

        #### BASE FILE

        base_file.append("ATOMBASIS\n")
        base_file.append("fc\n")
        base_file.append("Generated by Rafael\n")

        #### THIS OF COURSE NEED TO BE MADE PROPERLY... BUT NOT NOW   ###############
        #####
        base_file.append("AtomTypes=3"+" Charge="+self.charge+" NoSymmetry Angstrom\n")

        self.geom=[]
        # atom_types=1 ### because of Bq
        incr_type=0
        for item in self.atoms:
            if item.id=="C":
                incr_type+=1
                a=float(item.xyz[0])
                b=float(item.xyz[1])
                c=float(item.xyz[2])

                text=f"{item.id:<10s} {a:15.10f} {b:15.10f} {c:15.10f}"

                self.geom.append(text+"\n")

        base_file.append("Charge=6.0 Atoms="+str(incr_type)+" Basis="+self.basis_set+"\n")
        for item in self.geom:
            base_file.append(item)

        self.geom=[]
        incr_type=0
        for item in self.atoms:
            if item.id=="H":
                incr_type+=1
                a=float(item.xyz[0])
                b=float(item.xyz[1])
                c=float(item.xyz[2])

                text=f"{item.id:<10s} {a:15.10f} {b:15.10f} {c:15.10f}"

                self.geom.append(text+"\n")

        base_file.append("Charge=1.0 Atoms="+str(incr_type)+" Basis="+self.basis_set+"\n")
        for item in self.geom:
            base_file.append(item)

        ######### done with the bad geometry implementation ######

        file_number=1
        new_file_flag=True
        temp_ghost=[]
        for item in ghost_geom:

            if new_file_flag:
                new_file_flag=False
                output=open(self.name+"_"+"00"+str(file_number)+".mol",'w+')
                self.text_log.append("Created "+str(file_number)+" files")
                for line in base_file:
                    output.write(line)

            if len(temp_ghost)<150:
                temp_ghost.append(item)
            
            else:
                temp_ghost.append(item)
                output.write("Charge=0.0 Atoms="+str(len(temp_ghost))+" Basis=pointcharge\n")
                for line in temp_ghost:
                    output.write(line)
                
                output.close()
                new_file_flag=True
                temp_ghost=[]
                file_number+=1

            ### last ghost
            if item ==ghost_geom[-1]:

                output.write("Charge=0.0 Atoms="+str(len(temp_ghost))+" Basis=pointcharge\n")
                for line in temp_ghost:
                    output.write(line)
                
                output.close()

        ##### STARTING BAD IMPLEMENTATION OF GHOST ATOMS. JUST TEST RUN #######
        

        

        output.close

    def gaussian_run(self,analysis):
        self.gridspecs()
        self.bash_file()
        if analysis=="cmo" or self.both_flag:
           nbo7="$nbo cmo ncs=xyz,mo,"+self.criteria+" $end"
           pop="pop=nbo7read "
        elif analysis=="none":
           nbo7=""
           pop=""
        else:
           nbo7="$nbo ncs=xyz,"+self.criteria+" $end" ## MEMORY=50GB
           pop="pop=nbo7read "

        file_number=1
        output=open(self.name+"_"+"00"+str(file_number)+".gjf",'w+')
        self.text_log.append("Created "+str(file_number)+" files")
        output.write("%chk=CHK_"+self.name+".chk\n")
        output.write("%mem="+self.memory+"\n")
        output.write("%nprocshared="+self.nproc+"\n")
        output.write("#p nmr=giao "+self.basis_set+" "+self.method+" "+pop+"geom=connectivity\n")
        output.write("\n")
        output.write("Title Card"+"\n")
        output.write("\n")
        output.write(self.charge+" 1"+"\n")

        self.fgeom()

        for item in self.geom:
            output.write(item)

        ghost_iter=len(self.geom)

        self.get_ghost_geom()

        if self.dim=="2d":
            if self.plane=='xy':
                z=self.cut
                ###hotfix
                side=0
                if self.sym=="z":
                    side=self.cut
                ###end hotfix
                for x in range(0,self.size-self.x_sym):
                        for y in range(0, self.size-self.y_sym-side):
                            output.write("Bq\t"+self.pos[y, z, x] + "\t" + 
                            self.pos[x, z, y] + "\t" + self.pos[x, y, z]+"\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                output.write('\n')  ### cant use connectivity yet
                                for k in range(1,ghost_iter+1):
                                    output.write(str(k)+'\n')
                                output.write("\n"+nbo7+"\n\n")
                                output.close()
                                file_number+=1
                                ghost_iter=len(self.geom)
                                if file_number<10:
                                    output=open(self.name+"_"+'00'+str(file_number)+".gjf",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+'0'+str(file_number)+".gjf",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".gjf",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")
                                
                                output.write("%chk=CHK_"+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" "+pop+"geom=connectivity guess=read\n")
                                output.write("\n")
                                output.write("Title Card"+"\n")
                                output.write("\n")
                                output.write(self.charge+" 1"+"\n")

                                for item in self.geom:
                                    output.write(item)

            if self.plane=='xz':
                y=self.cut
                for x in range(0,self.size-self.x_sym):
                        for z in range(0, self.size-self.z_sym):
                            output.write("Bq\t"+self.pos[y, z, x] + "\t" +
                            self.pos[x, z, y] + "\t" + self.pos[x, y, z]+"\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                output.write('\n')  ### cant use connectivity yet
                                for k in range(1,ghost_iter+1):
                                    output.write(str(k)+'\n')
                                output.write("\n"+nbo7+"\n\n")
                                output.close()
                                file_number+=1
                                ghost_iter=len(self.geom)
                                if file_number<10:
                                    output=open(self.name+"_"+'00'+str(file_number)+".gjf",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+'0'+str(file_number)+".gjf",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".gjf",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")

                                output.write("%chk=CHK_"+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" "+pop+"geom=connectivity guess=read\n")
                                output.write("\n")
                                output.write("Title Card"+"\n")
                                output.write("\n")
                                output.write(self.charge+" 1"+"\n")

                                for item in self.geom:
                                    output.write(item)

            if self.plane=='yz':
                x=self.cut
                ### HotFix
                side=0
                if self.sym=="x":
                    side=x
                ### end hotfix
                for y in range(0, self.size-self.y_sym-side):
                        for z in range(0, self.size-self.z_sym):
                            output.write("Bq\t"+self.pos[y, z, x] + "\t" +
                            self.pos[x, z, y] + "\t" + self.pos[x, y, z]+"\n")
                            ghost_iter+=1
                            if ghost_iter==self.max_ghosts:
                                output.write('\n')  ### cant use connectivity yet
                                for k in range(1,ghost_iter+1):
                                    output.write(str(k)+'\n')
                                output.write("\n"+nbo7+"\n\n")
                                output.close()
                                file_number+=1
                                ghost_iter=len(self.geom)
                                if file_number<10:
                                    output=open(self.name+"_"+'00'+str(file_number)+".gjf",'w+')
                                if file_number>9 and file_number<100:
                                    output=open(self.name+"_"+'0'+str(file_number)+".gjf",'w+')
                                if file_number>99:
                                    output=open(self.name+"_"+str(file_number)+".gjf",'w+')
                                
                                self.text_log.append("Created "+str(file_number)+" files")
                                
                                output.write("%chk=CHK_"+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" "+pop+"geom=connectivity guess=read\n")
                                output.write("\n")
                                output.write("Title Card"+"\n")
                                output.write("\n")
                                output.write(self.charge+" 1"+"\n")

                                for item in self.geom:
                                    output.write(item)
                                

            # if ghost_iter!=840:
            #         output.write('\n')
            #         for k in range(1,ghost_iter+1):
            #             output.write(str(k)+'\n')
            #         output.write("\n" + nbo7 + "\n\n")
            #         output.close()






        else:
            #3d
            for x in range(0,self.size-self.x_sym):
                for y in range(0, self.size-self.y_sym):
                    for z in range(0, self.size-self.z_sym):
                        output.write("Bq\t"+str(float(self.pos[y, z, x])) + "\t" + 
                        str(float(self.pos[x, z, y])) + "\t" + str(float(self.pos[x, y, z]))+"\n")
                        ghost_iter+=1
                        if ghost_iter==self.max_ghosts:
                            output.write('\n')
                            for k in range(1,ghost_iter+1):
                                output.write(str(k)+'\n')
                            output.write("\n"+nbo7+"\n\n")
                            output.close()
                            file_number+=1
                            ghost_iter=len(self.geom)
                            if file_number<10:
                                output=open(self.name+"_"+"00"+str(file_number)+".gjf",'w+')
                            if file_number>9 and file_number<100:
                                output=open(self.name+"_"+"0"+str(file_number)+".gjf",'w+')
                            if file_number>99:
                                output=open(self.name+"_"+str(file_number)+".gjf",'w+')
                            
                            self.text_log.append("Created "+str(file_number)+" files")
                            
                            output.write("%chk=CHK_"+self.name+".chk\n")
                            output.write("%mem="+self.memory+"\n")
                            output.write("%nprocshared="+self.nproc+"\n")
                            output.write("#p nmr=giao "+self.basis_set+" "+
                            self.method+" "+pop+"geom=connectivity guess=read\n")
                            output.write("\n")
                            output.write("Title Card"+"\n")
                            output.write("\n")
                            output.write(self.charge+" 1"+"\n")

                            for item in self.geom:
                                output.write(item)

        if ghost_iter!=840:
            output.write('\n')
            for k in range(1,ghost_iter+1):
                output.write(str(k)+'\n')
            output.write("\n" + nbo7 + "\n\n")
            output.close()

        self.windows_gaussian_run_file(file_number)

        self.text_log.append("bash file needs to be given proper permissions to run (chmod +rwx)")



    def gridspecs(self):
        output=open("gridspecs"+".txt",'w+')
        if self.dim=='2d':
            output.write('GRID\n')
            output.write(self.plane+'\n')
        output.write(str(self.size)+'\n')
        output.write(str(self.step)+'\n')
        output.write('0.00'+'\t'+'0.00'+'\t'+'0.00'+'\n')
        output.write(self.sym)

        output.close()

    def bash_file(self):
        output=open("gaussian_batch.bash",'w+')
        output.write('#!/bin/bash\n')
        output.write('echo "Start date: `date +%d" "%b" "%y" "%H":"%M`"\n')
        output.write('SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"\n')
        output.write('FILES="$SCRIPT_DIR/*.gjf"\n')
        output.write('\n')
        output.write('for FILE in $FILES\n')
        output.write('do\n')
        output.write('   \n')
        output.write('    BASENAME="`basename $FILE .gjf`"\n')
        output.write('   # echo " filename is $FILE"\n')
        output.write('   OUTFILE="$SCRIPT_DIR/$BASENAME.out"\n')
        output.write(' #  echo "$OUTFILE"\n')
        output.write('   if ! [ -e $OUTFILE ]\n')
        output.write('    then\n')
        output.write('        echo "Started job $BASENAME at `date +%T`"\n')
        output.write('        g16 < $FILE > $OUTFILE\n')
        output.write('   fi\n')
        output.write('done\n')
        output.write('echo "End date: `date +%d" "%b" "%y" "%H":"%M`"\n')
        output.close()
        
    def windows_gaussian_run_file(self,file_number):
        output=open("DROPLIST.BCF",'w+')
        output.write('!\n')
        output.write('!Drag and drop batch file\n')
        output.write('!\n')
        output.write('!\n')

        path=os.getcwd()

        for i in range(1,file_number+1):
            if i<10:
                num="_"+"00"+str(i)
            if i>9 and i<100:
                num="_"+"0"+str(i)
            if i>99:
                num="_"+str(i)

            output.write(path+"\\"+self.name+num+".gjf , "+self.name+num+'.out\n')

        output.write('\n')


    def fgeom(self):
        self.geom=[]
        for item in self.atoms:
            a=str(format(float(item.xyz[0]),'.7f'))
            b=str(format(float(item.xyz[1]),'.7f'))
            c=str(format(float(item.xyz[2]),'.7f'))
            self.geom.append(item.id+"\t"+a+"\t"+b+"\t"+c+"\n")
            # self.geom.append(item.id+"\t"+str(item.xyz[0])+"\t"+str(item.xyz[1])+"\t"+str(item.xyz[2])+"\n")
        
    def adfgeom(self):
        self.geom=[]
        incr=1
        for item in self.atoms:
            a=str(format(float(item.xyz[0]),'.7f'))
            b=str(format(float(item.xyz[1]),'.7f'))
            c=str(format(float(item.xyz[2]),'.7f'))
            self.geom.append(str(incr)+"\t"+item.id+"\t"+
            a+"\t"+b+"\t"+c+"\n")
            incr+=1


    def dist(self,x,y,z):
        for item in self.atoms:
            distance=math.sqrt((item.xyz[0]-float(self.pos[y, z, x]))**2+
            (item.xyz[1]-float(self.pos[x, z, y]))**2+(item.xyz[2]-float(self.pos[x, y, z]))**2)
            if distance<0.1:
                self.pos[x, y, z]=str(float(self.pos[x, y, z])+0.2500)
        

    
    def get_ghost_geom(self):

        starting_pos=-(self.size-1)*self.step/2
        self.pos={}

        if self.dim=="2d":
            #if self.plane=='xz':
            for x in range(0,self.size):
                #self.pos[x,0,0]=starting_pos+x*self.step
                for y in range(0,self.size):
                    #self.pos[x,y,0]=0
                    for z in range(0,self.size):
                        self.pos[x,y,z]=f"{starting_pos+z*self.step:{'.4f'}}"

            # elif self.plane=='xy':
            #     for x in range(0,self.size):
            #         self.pos[x,0,0]=starting_pos+x*self.step
            #         for y in range(0,self.size):
            #             self.pos[x,y,0]=starting_pos+y*self.step
            #             for z in range(0,self.size):
            #                 self.pos[x,y,z]=starting_pos+z*self.step

            # else:
            #     self.plane='yz'
            #     for x in range(0,self.size):
            #         self.pos[x,0,0]=0
            #         for y in range(0,self.size):
            #             self.pos[x,y,0]=starting_pos+y*self.step
            #             for z in range(0,self.size):
            #                 self.pos[x,y,z]=starting_pos+z*self.step
        
        else:
            self.dim="3d"
            for x in range(0,self.size):
                #self.pos[x,0,0]=f"{starting_pos+x*self.step:{'.4f'}}"
                for y in range(0,self.size):
                    #self.pos[x,y,0]=f"{starting_pos+y*self.step:{'.4f'}}"
                    for z in range(0,self.size):
                        self.pos[x,y,z]=f"{starting_pos+z*self.step:{'.4f'}}"



        slices=int((self.size+1)/2)
        cut=int((self.size-1)/2)
        self.cut=cut

        self.x_sym,self.y_sym,self.z_sym=0,0,0

        if self.sym=="x":
            self.x_sym=cut
        if self.sym=="y":
            self. y_sym=cut
        if self.sym=="z":
            self.z_sym=cut
        if self.sym=="yz":
            self.y_sym=cut
            self.z_sym=cut
        if self.sym=="xy":
            self.x_sym=cut
            self.y_sym=cut
        if self.sym=="xz":
            self.x_sym=cut
            self.z_sym=cut
        if self.sym=="xyz":
            self.x_sym=cut
            self.y_sym=cut
            self.z_sym=cut


    def adf_2nd_ghost_to_end(self,output):
        output.write('End\n\n\n\n')
        if self.analysis=="cmo":
            output.write("SAVE  TAPE10 TAPE13\n")
        output.write("eor\n\n")
        if self.analysis=="nbo":
            output.write("###### end scalar, run gennbo ##########\n\n\n")
            output.write("#  gennbo run\n")
            output.write("#  ==========\n\n")
            output.write("\"$ADFBIN/adfnbo\" <<eor\n")
            output.write(" write\n")
            output.write(" spherical\n")
            output.write(" fock\n")
            output.write("eor\n\n")

            output.write("rm -f adfnbo.37 adfnbo.39 adfnbo.49 adfnbo.48\n")

            output.write("\"$ADFBIN/gennbo6\" FILE47\n")

            output.write("\"$ADFBIN/adfnbo\" <<eor\n")
            output.write(" copy\n")
            output.write(" spherical\n")
            output.write(" fock\n")
            output.write("eor\n\n")

            output.write("\"$ADFBIN/adfnbo\" <<eor\n")
            output.write(" read\n")
            output.write(" spherical\n")
            output.write(" fock\n")
            output.write("eor\n\n")
            
            output.write("rm -f adfnbo.37 adfnbo.39 adfnbo.49 adfnbo.48\n")
            output.write("# ===\n")
            output.write("# NMR\n")
            output.write("# ===\n\n")

        output.write("mkdir tapes\n")
        output.write("mv TAPE* tapes 2>/dev/null\n")
        output.write("mv tapes/TAPE21 TAPE21 2>/dev/null\n")
        output.write("cp -f tapes/TAPE10 TAPE10\n\n")
        output.write("$ADFBIN/nmr <<eor\n\n")
        output.write("NMR\n")
        output.write(" u1k best\n")
        output.write(" out iso tens\n")
        output.write(" NUC\n")
        output.write("  GHOSTS\n")

        for item in self.ghost_matrix:
            output.write(item+"\n")
        
        output.write("subend\n")
        output.write("end\n")
        output.write("ANALYSIS\n")
        output.write("  print  "+self.criteria+"\n")
        if self.analysis=="nbo":
            output.write("  nbo\n")
            if self.both_flag:
                output.write("  canonical\n")
        elif self.analysis=="cmo":
            output.write("  canonical\n")
        output.write("  components\n")
        output.write("end\n")
        output.write("FAKESO\n")
        if self.analysis=="cmo":
            output.write(" END INPUT\n")
        output.write("eor\n\n")

        output.write("mv TAPE21 tapes 2>/dev/null\n")
        output.write("rm -f TAPE*\n")
        output.write("mv tapes/* . 2>/dev/null\n")
        output.write("rm -r tapes\n\n")
        output.write("#########################################################\n\n")

        output.close()


    def adf_geom_plus(self,output):
        output.write("#!/bin/sh\n\n")
        output.write("\"$ADFBIN/adf\" <<eor\n")
        output.write("  Atoms\n")

        
        for item in self.geom:
            output.write(item)
        
        
        output.write("END\n\n")
        output.write("CHARGE\t"+self.charge+"\n")
        output.write("SYMMETRY NOSYM\n\n")
        output.write("BASIS\n")
        output.write("type "+self.basis_set+"\n")
        output.write("core NONE\n")
        if self.analysis=="nbo":
            output.write("CreateOutput None\n")
        output.write("END\n")
        output.write("XC\n")
        #### NEED TO CHANGE THE GGA THING
        output.write("GGA "+self.method+"\n") ### WORK WITH GGA?!?!?
        output.write("END\n\n")
        if self.analysis=="nbo":
            output.write("Save TAPE10 TAPE15\n")
            output.write("NoPrint LOGFILE\n")
            output.write("FullFock Yes\n")
            output.write("AOMat2File Yes\n")
        elif self.analysis=="cmo":
            output.write("allow  closeatoms\n\n")

        output.write("Relativistic Scalar ZORA\n\n")

        output.write("PointCharges\n")
