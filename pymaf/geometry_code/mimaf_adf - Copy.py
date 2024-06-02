import os











class runs:
    def __init__(self,name,atoms,size,step,sym,dim,plane,
    max_ghosts,method,basis_set,charge,criteria,memory,nproc,text_log):
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

    def adf_run(self,analysis):
        self.gridspecs()

        file_number=1
        output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
        self.text_log.append("Created "+str(file_number)+" files")
        output.write("#!/bin/sh\n\n")
        output.write("\"$ADFBIN/adf\" <<eor\n")
        output.write("\t" +"Atoms\n")

        self.adfgeom()
        
        for item in self.geom:
            output.write(item)
        
        ghost_iter=1
        
        output.write("END\n\n")
        output.write("CHARGE\t"+self.charge+"\n")
        output.write("SYMMETRY NOSYM\n\n")
        output.write("type "+self.basis_set+"\n")
        output.write("core NONE\n")
        output.write("CreateOutput None\n")
        output.write("END\n")
        output.write("XC\n")
        #### NEED TO CHANGE THE GGA THING
        output.write("GGA "+self.method+"\n") ### WORK WITH GGA?!?!?
        output.write("END\n\n")
        output.write("Save TAPE10 TAPE15\n")
        output.write("NoPrint LOGFILE\n")
        output.write("FullFock Yes\n")
        output.write("AOMat2File Yes\n")
        output.write("Relativistic Scalar ZORA\n\n")

        output.write("PointCharges\n")

        self.get_ghost_geom()

        if self.dim=="3d":
            #3d
            self.ghost_matrix=[]
            for x in range(0,self.size-self.x_sym):
                for y in range(0, self.size-self.y_sym):
                    for z in range(0, self.size-self.z_sym):
                        ghost=str(float(self.pos[y, z, x])) +"\t"+str(float(self.pos[x, z, y]))+"\t"+str(float(self.pos[x, y, z]))
                        self.ghost_matrix.append(ghost)
                        output.write(ghost+"\t0.0\n")
                        ghost_iter+=1
                        if ghost_iter==self.max_ghosts:
                            output.write('End\n\n\n\n')
                            output.write("eor\n\n")
                            output.write("###### end scalar, run gennbo ##########\n\n\n")
                            output.write("#  gennbo run\n")
                            output.write("#  ==========\n\n")
                            output.write("\"$ADFBIN/adfnbo\" <<eor")
                            output.write(" write\n")
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
                            output.write("\tprint\t"+self.criteria+"\n")
                            output.write("  nbo\n")
                            output.write("  components\n")
                            output.write("end\n")
                            output.write("FAKESO\n")
                            output.write("eor\n\n")

                            output.write("mv TAPE21 tapes 2>/dev/null\n")
                            output.write("rm -f TAPE*\n")
                            output.write("mv tapes/* . 2>/dev/null\n")
                            output.write("rm -r tapes\n\n")
                            output.write("#########################################################\n\n")

                            output.close()

                            file_number+=1
                            if file_number<10:
                                output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                            if file_number>9 and file_number<100:
                                output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                            if file_number>99:
                                output=open(self.name+"_"+"00"+str(file_number)+".run",'w+')
                            
                            self.text_log.append("Created "+str(file_number)+" files")


                            
                            output.write("#!/bin/sh\n\n")
                            output.write("\"$ADFBIN/adf\" <<eor\n")
                            output.write("\t" +"Atoms\n")

                            self.adfgeom()
                            
                            for item in self.geom:
                                output.write(item)
                            
                            ghost_iter=1
                            self.ghost_matrix=[]
                            
                            output.write("END\n\n")
                            output.write("CHARGE\t"+self.charge+"\n")
                            output.write("SYMMETRY NOSYM\n\n")
                            output.write("type "+self.basis_set+"\n")
                            output.write("core NONE\n")
                            output.write("CreateOutput None\n")
                            output.write("END\n")
                            output.write("XC\n")
                            #### NEED TO CHANGE THE GGA THING
                            output.write("GGA "+self.method+"\n") ### WORK WITH GGA?!?!?
                            output.write("END\n\n")
                            output.write("Save TAPE10 TAPE15\n")
                            output.write("NoPrint LOGFILE\n")
                            output.write("FullFock Yes\n")
                            output.write("AOMat2File Yes\n")
                            output.write("Relativistic Scalar ZORA\n\n")

                            output.write("PointCharges\n")

            #if ghost_iter!=840:
            output.write('End\n\n\n\n')
            output.write("eor\n\n")
            output.write("###### end scalar, run gennbo ##########\n\n\n")
            output.write("#  gennbo run\n")
            output.write("#  ==========\n\n")
            output.write("\"$ADFBIN/adfnbo\" <<eor")
            output.write(" write\n")
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
            output.write("\tprint\t"+self.criteria+"\n")
            output.write("  nbo\n")
            output.write("  components\n")
            output.write("end\n")
            output.write("FAKESO\n")
            output.write("eor\n\n")

            output.write("mv TAPE21 tapes 2>/dev/null\n")
            output.write("rm -f TAPE*\n")
            output.write("mv tapes/* . 2>/dev/null\n")
            output.write("rm -r tapes\n\n")
            output.write("#########################################################\n\n")

            output.close()







    def gaussian_run(self,analysis):
        self.gridspecs()

        if analysis=="cmo":
           nbo7="$nbo cmo ncs=xyz,mo,"+self.criteria+" $end"
        else:
           nbo7="$nbo ncs=xyz,"+self.criteria+" $end"

        file_number=1
        output=open(self.name+"_"+"00"+str(file_number)+".gjf",'w+')
        self.text_log.append("Created "+str(file_number)+" files")
        output.write("%chk=CHK."+self.name+".chk\n")
        output.write("%mem="+self.memory+"\n")
        output.write("%nprocshared="+self.nproc+"\n")
        output.write("#p nmr=giao "+self.basis_set+" "+self.method+" pop=nbo7read geom=connectivity\n")
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
                            output.write("Bq\t"+str(float(self.pos[y, z, x])) + "\t" + 
                            str(float(self.pos[x, z, y])) + "\t" + str(float(self.pos[x, y, z]))+"\n")
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
                                
                                output.write("%chk=CHK."+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" pop=nbo7read geom=connectivity\n")
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
                            output.write("Bq\t"+str(float(self.pos[y, z, x])) + "\t" +
                            str(float(self.pos[x, z, y])) + "\t" + str(float(self.pos[x, y, z]))+"\n")
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

                                output.write("%chk=CHK."+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" pop=nbo7read geom=connectivity\n")
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
                            output.write("Bq\t"+str(float(self.pos[y, z, x])) + "\t" +
                            str(float(self.pos[x, z, y])) + "\t" + str(float(self.pos[x, y, z]))+"\n")
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
                                
                                output.write("%chk=CHK."+self.name+".chk\n")
                                output.write("%mem="+self.memory+"\n")
                                output.write("%nprocshared="+self.nproc+"\n")
                                output.write("#p nmr=giao "+self.basis_set+" "+
                                self.method+" pop=nbo7read geom=connectivity\n")
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
                                output=open(self.name+"_"+"00"+str(file_number)+".gjf",'w+')
                            if file_number>99:
                                output=open(self.name+"_"+"00"+str(file_number)+".gjf",'w+')
                            
                            self.text_log.append("Created "+str(file_number)+" files")
                            
                            output.write("%chk=CHK."+self.name+".chk\n")
                            output.write("%mem="+self.memory+"\n")
                            output.write("%nprocshared="+self.nproc+"\n")
                            output.write("#p nmr=giao "+self.basis_set+" "+
                            self.method+" pop=nbo7read geom=connectivity\n")
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



    def gridspecs(self):
        output=open("gridspecs"+".txt",'w+')
        output.write(str(self.size)+'\n')
        output.write(str(self.step)+'\n')
        output.write('0.00'+'\t'+'0.00'+'\t'+'0.00'+'\n')
        output.write(self.sym)

        output.close()

    def fgeom(self):
        self.geom=[]
        for item in self.atoms:
            self.geom.append(item.id+"\t"+str(item.xyz[0])+"\t"+str(item.xyz[1])+"\t"+str(item.xyz[2])+"\n")
        
    def adfgeom(self):
        self.geom=[]
        incr=1
        for item in self.atoms:
            self.geom.append(str(incr)+"\t"+item.id+"\t"+
            str(item.xyz[0])+"\t"+str(item.xyz[1])+"\t"+str(item.xyz[2])+"\n")
            incr+=1
        

    
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
                        self.pos[x,y,z]=starting_pos+z*self.step

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
                self.pos[x,0,0]=starting_pos+x*self.step
                for y in range(0,self.size):
                    self.pos[x,y,0]=starting_pos+y*self.step
                    for z in range(0,self.size):
                        self.pos[x,y,z]=starting_pos+z*self.step



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


    def asdasd(self,output):
        output.write('End\n\n\n\n')
        output.write("eor\n\n")
        output.write("###### end scalar, run gennbo ##########\n\n\n")
        output.write("#  gennbo run\n")
        output.write("#  ==========\n\n")
        output.write("\"$ADFBIN/adfnbo\" <<eor")
        output.write(" write\n")
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
        output.write("\tprint\t"+self.criteria+"\n")
        output.write("  nbo\n")
        output.write("  components\n")
        output.write("end\n")
        output.write("FAKESO\n")
        output.write("eor\n\n")

        output.write("mv TAPE21 tapes 2>/dev/null\n")
        output.write("rm -f TAPE*\n")
        output.write("mv tapes/* . 2>/dev/null\n")
        output.write("rm -r tapes\n\n")
        output.write("#########################################################\n\n")

        output.close()
