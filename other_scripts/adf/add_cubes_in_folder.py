import os,sys,numpy

path = input("paste path here:")
os.chdir(path)

dirs = os.listdir(path)
values=[]
first_file_flag=True

for data_file in dirs:
    cube=open(data_file)
    lines=cube.readlines()
    cube.close()
    how_many_atoms=lines[2].split()

    if first_file_flag==True:
        first_file_flag=False
        for i in range(0, int(how_many_atoms[0]) + 6):
            values.append(lines[i])

    for i in range(int(how_many_atoms[0]) + 6, len(lines)):
        try:
            values[i]=float(lines[i])+float(values[i])
        except IndexError:
            values.append(lines[i])

output = open("added_cubes.cube", 'w+')

for i in range(0, int(how_many_atoms[0]) + 6):
    output.write(lines[i])
for i in range(int(how_many_atoms[0]) + 6, len(lines)):
    output.write(str(float(values[i])) + "\n")
output.close()
