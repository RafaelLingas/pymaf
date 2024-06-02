import os,sys

array=[]
dimensions=[]

path=input("paste path here:")
os.chdir(path)

dirs=os.listdir(path)

cube_1=input("Name of cube(with extension): ")

f_1=open(cube_1)
lines=f_1.readlines()
f_1.close()

array=lines[2].split()   # so that array[0] is the number of atoms
dimensions=lines[3].split() #so that dimensions[0] is the number of slides


plane="xyz"
while(plane!="xy" and plane!="xz" and plane!="yz"):
    plane=input("Choose plane 'xy', 'xz' or 'yz': ")

n_slide=0
while(int(n_slide)<1 or int(n_slide)>int(dimensions[0])):
    n_slide=input("There are "+dimensions[0]+" slides here. Which one do you want? : ")

n_slide=int(n_slide)

output=open("extracted_plane.cube",'w+')

output.write("##Plane "+plane+"\n")
output.write("##Number of slide extracted: "+str(n_slide)+"\n")

for i in range(2,int(array[0])+6):

   output.write(lines[i])

if plane=="yz":
    for i in range(0,int(dimensions[0])*int(dimensions[0])):
        output.write(str(float(lines[i+(n_slide-1)*int(dimensions[0])*int(dimensions[0])+int(array[0])+6]))+"\n")

if plane=="xy":
    for i in range(0,int(dimensions[0])*int(dimensions[0])):
        output.write(str(float(lines[n_slide-1+i*int(dimensions[0])+int(array[0])+6]))+"\n")


j=0
incr=0
if plane=="xz":
    for i in range(1,int(dimensions[0])*int(dimensions[0])+1):
        output.write(str(float(lines[incr+(n_slide-1)*int(dimensions[0])+j*int(dimensions[0])*int(dimensions[0])+int(array[0])+6]))+"\n")
        incr+=1
        if i%int(dimensions[0])==0:
            j+=1
            incr=0

output.close()
