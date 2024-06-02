### Quantum Utilities GUI
### version 1.01
### it needs to be able to handle errors in tkinter window

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np

import os


def create_frame(root):

    #frame = Frame(root)

    frame = LabelFrame(root, bg="gray22", padx=200, pady=200)
    frame.pack()

    b_cube_conversion = Button(frame, text="Cube Conversion", bg="orange", fg="red", command=cube_conversion)
    b_cube_conversion.grid(column=0, row=0)

    b_cube_operations = Button(frame, text="Cube Operations", bg="orange", fg="red", command=cube_operation)
    b_cube_operations.grid(column=1, row=0)

    b_extract = Button(frame, text="Extract plane from Cube", bg="orange", fg="red", command=cube_extract)
    b_extract.grid(column=2, row=0)

    b_nbo_no_single_point = Button(frame, text="NBO without single point", bg="orange", fg="red", command=nbo_no_single_point)
    b_nbo_no_single_point.grid(column=0, row=1)

    b_clear_all = Button(frame, text='Home', command=reset_all)
    b_clear_all.grid(column=2, row=2)

    return frame


def reset_all():
    global home_frame

    cube_oper_frame.destroy()
    cube_conv_frame.destroy()
    nbo_no_single_point_frame.destroy()

    home_frame.destroy()


    home_frame = create_frame(root)
    #frame = create_different_frame(root)
    #frame.pack()


def cube_conversion():

    home_frame.destroy()
    file = filedialog.askopenfilename()
    directory = os.path.split(file)[0]

    array = []

    os.chdir(directory)

    #dirs = os.listdir(path)

    cube_1 = file

    f_1 = open(cube_1)
    lines = f_1.readlines()
    f_1.close()

    array = lines[2].split()
    coor = lines

    output = open("converted.cube", 'w+')

    for i in range(0, int(array[0]) + 6):
        output.write(lines[i])
        coor = coor[1:]

    for i in range(0, len(coor)):

        array_split = coor[i].split()
        for k in range(0, len(array_split)):
            output.write(str(array_split[k]) + "\n")

    output.close()


    #frame1 = Frame(root)
    global cube_conv_frame
    cube_conv_frame = LabelFrame(root, bg="gray22", padx=200, pady=200)
    cube_conv_frame.pack()

    b_done = Label(cube_conv_frame, text="Done", bg="orange", fg="red")
    b_done.grid(column=0, row=0)

    #b_cube_operations = Button(frame1, text="Cube Opasdsdas", bg="orange", fg="red")
    #b_cube_operations.grid(column=1, row=0)

    #b_extract = Button(frame1, text="Extasdasd", bg="orange", fg="red")
    #b_extract.grid(column=2, row=0)

    b_clear_all = Button(cube_conv_frame, text='Home', command=reset_all)
    b_clear_all.grid(column=2, row=0)


def cube_operation():
    home_frame.destroy()
    global cube_oper_frame
    cube_oper_frame = LabelFrame(root, bg="gray22", padx=200, pady=200)
    cube_oper_frame.pack()

    file = filedialog.askopenfilename(title="First cube file")
    directory = os.path.split(file)[0]

    array = []

    os.chdir(directory)

    #dirs = os.listdir(path)

    cube_1 = file

    f_1 = open(cube_1)
    lines = f_1.readlines()
    f_1.close()

    array = lines[2].split()

    output = open("added_cubes.cube", 'w+')

    for i in range(0, int(array[0]) + 6):
        output.write(lines[i])

    for i in range(int(array[0]) + 6, len(lines)):
        output.write(str(float(lines[i])) + "\n")

    output.close()

    more_cubes = "y"

    while (more_cubes == "y"):

        operation = simpledialog.askstring("Choose Operation", "'a' to add cube,'s' to subtract cube or 'm' to multiply cube with number")

        if (operation == "a"):
            cube_next = filedialog.askopenfilename(title="next cube")

            f_ = open(cube_next)
            lines_next = f_.readlines()
            f_.close()

            f_sum2 = open("added_cubes.cube")
            lines_sum2 = f_sum2.readlines()
            f_sum2.close()

            output = open("added_cubes.cube", 'w+')

            for i in range(0, int(array[0]) + 6):
                output.write(lines[i])

            for i in range(int(array[0]) + 6, len(lines)):
                output.write(str(float(lines_sum2[i]) + float(lines_next[i])) + "\n")

            output.close()

        if (operation == "s"):
            cube_next = filedialog.askopenfilename(title="Subtract cube")

            f_ = open(cube_next)
            lines_next = f_.readlines()
            f_.close()

            f_sum2 = open("added_cubes.cube")
            lines_sum2 = f_sum2.readlines()
            f_sum2.close()

            output = open("added_cubes.cube", 'w+')

            for i in range(0, int(array[0]) + 6):
                output.write(lines[i])

            for i in range(int(array[0]) + 6, len(lines)):
                output.write(str(float(lines_sum2[i]) - float(lines_next[i])) + "\n")

            output.close()

        if (operation == "m"):
            scale = simpledialog.askfloat("Multiply cube", "number with which to multiply")

            f_sum2 = open("added_cubes.cube")
            lines_sum2 = f_sum2.readlines()
            f_sum2.close()

            output = open("added_cubes.cube", 'w+')

            for i in range(0, int(array[0]) + 6):
                output.write(lines[i])

            for i in range(int(array[0]) + 6, len(lines)):
                output.write(str(float(lines_sum2[i]) * float(scale)) + "\n")

            output.close()

        more_cubes = simpledialog.askstring("More operations?", "Press 'y' to add or subtract more cubes")

        b_done = Label(cube_oper_frame, text="Done", bg="orange", fg="red")
        b_done.grid(column=0, row=0)

        b_clear_all = Button(cube_oper_frame, text='Home', command=reset_all)
        b_clear_all.grid(column=2, row=0)

def cube_extract():

    print("asd")


def nbo_no_single_point():

    ###frame details
    home_frame.destroy()
    global nbo_no_single_point_frame
    nbo_no_single_point_frame = LabelFrame(root, bg="gray22", padx=0, pady=0)
    nbo_no_single_point_frame.pack()

    text_box = Text(nbo_no_single_point_frame, bg="gray22", fg="white")
    text_box.pack(side=TOP, anchor=N)

    path = filedialog.askdirectory()
    #directory = os.path.split(file)[0]
    os.chdir(path)

    dirs = os.listdir(path)

    ###Get a file for geometry and orbitals
    for data_file in dirs:
        if data_file.endswith(".out"):
            file_name = data_file
            break

    ###Get Geometry
    geometry_array = []
    geometry_flag = False
    first_atom_flag = False
    end_geometry = False

    with open(file_name, 'r') as input_data:
        for line in input_data:
            if 'G E O M E T R Y' in line:
                geometry_flag = True
            if geometry_flag == True:
                if '1' in line:
                    first_atom_flag = True
                if 'FRAGMENTS' in line:
                    end_geometry = True
            if end_geometry == True:
                break
            if first_atom_flag == True:
                geometry_array.append(line)

    del geometry_array[-1]
    del geometry_array[-1]
    geom = list(zip(*(row.split() for row in geometry_array)))
    atoms = list(geom[1])
    atoms_x = list(geom[2])
    atoms_y = list(geom[3])
    atoms_z = list(geom[4])
    atoms_N = list(geom[5])

    ###find all tables and do total pi sigma core###
    comp_flag = False
    comp_start_flag = False
    # comp_end_flag=False
    comp_array = []

    ###[x,y,z] x:zz,xx,yy,iso,aniso     y:para,dia,sum      z:N_ghosts  Need to change X
    x = 0
    y = 0
    z = 0

    total = {}

    pi = {}
    first_pi_flag = True

    sigma = {}
    first_sigma_flag = True
    j = 0
    j_2 = 0

    core = {}
    first_core_flag = True

    ### Lewis and non Lewis code 11-2020   #########
    total_L = {}
    total_NL = {}
    pi_L = {}
    pi_NL = {}
    sigma_L = {}
    sigma_NL = {}
    core_L = {}
    core_NL = {}

    ###Test for flags and incrs
    orbitals_flag = False
    first_BD_flag = True
    next_BD_flag = False
    pi_orb_flag = False
    end_orbitals_flag = False
    incr = 0
    pi_orb = []
    # pi_occup=[]

    sigma_orb = []
    sigma_incr = 0

    ### GHOSTS and choosing components
    ghost_flag = False
    eigenvectors_flag = False
    eigenvector_array = []
    ###eigen

    ### different pi orbitals
    pi_alone = {}

    ###different types of pi orbitals
    pi_t1 = {}  ##might change that
    first_pi_t1_flag = True
    pi_t2 = {}
    first_pi_t2_flag = True
    pi_t3 = {}
    first_pi_t3_flag = True
    type_1 = 0
    type_1_pos = []
    type_2 = 0
    type_2_pos = []
    type_3 = 0
    type_3_pos = []
    new_type_flag = True
    # next_pi=0

    for data_file in dirs:
        if data_file.endswith(".out"):
            with open(data_file, 'r') as input_data:
                #print("Working on: " + data_file)
                text_box.insert(INSERT, "Working on: " + data_file+"\n")

                ###Re-initialize positions of different pi type orbitals
                type_1_pos = []
                type_2_pos = []
                type_2_pos = []

                orbitals_flag = False
                first_BD_flag = True
                next_BD_flag = False
                pi_orb_flag = False
                end_orbitals_flag = False
                incr = 0
                pi_orb = []
                pi_occup = []
                sigma_orb = []
                sigma_incr = 0
                for line in input_data:
                    if '(NLMO) ANALYSIS:' in line:
                        orbitals_flag = True
                    if orbitals_flag == True:
                        if ('BD' in line or 'LP' in line) and first_BD_flag == True:
                            first_BD_flag = False
                            uncut_ncores = line.split()
                            n_cores = int(uncut_ncores[0][:-1]) - 1  # number of core orbitals
                        if '( 2)' in line or 'LP' in line:
                            pi_orb_flag = True
                        #         if next_BD_flag==True:
                        #            if "p" in line:
                        #               checkifp1=line.split("(",2)
                        #              checkifbig=line.split("%",1)
                        #             if float(checkifbig[0])>35.0:
                        #                checkifp2=checkifp1[2].split("%",1)
                        #               if (float(checkifp2[0]))>90.0:
                        #                  pi_orb_flag=True
                        if 'BD' in line or 'LP' in line:
                            uncut_BD = line.split()
                            next_BD_flag = True
                            sigma_orb.append(uncut_BD[0][:-1])
                            sigma_incr += 1
                        if pi_orb_flag == True:

                            pi_type = float(uncut_BD[2][:-1])
                            ### Get pi_types and positions. in progress..
                            if new_type_flag == False:
                                if pi_type <= (type_1 + 0.03 * type_1) and pi_type >= (type_1 - 0.03 * type_1):
                                    type_1_pos.append(uncut_BD[0][:-1])
                                elif pi_type <= (type_2 + 0.03 * type_2) and pi_type >= (type_2 - 0.03 * type_2):
                                    type_2_pos.append(uncut_BD[0][:-1])
                                elif pi_type <= (type_3 + 0.03 * type_3) and pi_type >= (type_3 - 0.03 * type_3):
                                    type_3_pos.append(uncut_BD[0][:-1])
                                    # print(uncut_BD)
                                else:
                                    new_type_flag = True

                            if new_type_flag == True:
                                if type_3 == 0 and type_2 != 0 and uncut_BD[3] != "LP":
                                    type_3 = pi_type
                                    type_3_pos.append(uncut_BD[0][:-1])
                                if type_2 == 0 and type_1 != 0 and uncut_BD[3] != "LP":
                                    type_2 = pi_type
                                    type_2_pos.append(uncut_BD[0][:-1])
                                if type_1 == 0 and uncut_BD[3] != "LP":
                                    type_1 = pi_type
                                    type_1_pos.append(uncut_BD[0][:-1])

                                new_type_flag = False

                            pi_occup.append(float(uncut_BD[2][:-1]))
                            ###
                            pi_orb.append(uncut_BD[0][:-1])
                            del sigma_orb[-1]
                            sigma_incr -= 1
                            pi_orb_flag = False
                            next_BD_flag = False
                            incr += 1
                        if 'NBO/NLMO' in line:
                            n_orbs = (uncut_BD[0][:-1])  ## how many orbitals we have
                            end_orbitals_flag = True
                    if end_orbitals_flag == True:
                        # orbitals_flag=False
                        break

                # print(len(sigma_orb))

                for line in input_data:
                    if 'G H O S T' in line:
                        ghost_flag = True
                        eigenvector_array = []
                    if ghost_flag == True:

                        if eigenvectors_flag == True:
                            if 'xxx' in line:
                                eigenvectors_flag = False
                                ghost_flag = False
                                del eigenvector_array[0]
                                eigenvector_array = [w.replace('D', 'e') for w in eigenvector_array]
                                columns_eigen = list(zip(*(row.split() for row in eigenvector_array)))
                                # eigen_1=list(columns_eigen[0])
                                # eigen_2=list(columns_eigen[1])
                                # eigen_3=list(columns_eigen[2])

                        if eigenvectors_flag == True:
                            eigenvector_array.append(line)

                        if 'eigenvectors' in line:
                            eigenvectors_flag = True
                    if 'NLMO #' in line:
                        comp_flag = True
                    if comp_flag == True:
                        if '1:' in line:
                            comp_start_flag = True

                        if 'sum' in line:
                            comp_start_flag = False
                            comp_flag = False
                            comp_array.append(line)

                            ###total
                            sum_uncut = comp_array[len(comp_array) - 1].split()
                            total[x, y, z] = sum_uncut[3]
                            total_L[x, y, z] = sum_uncut[1]
                            total_NL[x, y, z] = sum_uncut[2]
                            del comp_array[-1]
                            del comp_array[-1]
                            columns = list(zip(*(row.split() for row in comp_array)))
                            check_orbitals = list(columns[0])
                            n_check_orbitals = len(check_orbitals)
                            col3array = list(columns[3])
                            col2array_NL = list(columns[2])
                            col1array_L = list(columns[1])

                            if len(col3array) < int(n_orbs):
                                for k in range(0, n_check_orbitals):
                                    if int(check_orbitals[k][:-1]) != int(k + 1):
                                        col3array.insert(k, '0')
                                        col1array_L.insert(k, '0')
                                        col2array_NL.insert(k, '0')
                                        check_orbitals.insert(k, str(k + 1))
                                while (len(col3array) < int(n_orbs)):
                                    col3array.append('0')
                                    col2array_NL.append('0')
                                    col1array_L.append('0')

                            # print(len(col3array))
                            ###total_manual
                            # for k in range(0,len(col3array)):
                            #    if first_total_flag==False:
                            #        total_manual[x,y,z]=float(total_manual[x,y,z])+float(col3array[k])
                            #    if first_total_flag==True:
                            #        total_manual[x,y,z]=float(col3array[k])
                            #        first_total_flag=False

                            # first_total_flag=True

                            ###everything (for the cube files)
                            # for k in range(0,len(col3array)):
                            # everything[x,y,orbitals+k]=col3array[k]

                            ###pi and pi_alone orbitals
                            for k in range(0, incr):
                                if first_pi_flag == False:
                                    pi[x, y, z] = np.float64(pi[x, y, z]) + np.float64(col3array[int(pi_orb[k]) - 1])
                                    pi_L[x, y, z] = np.float64(pi_L[x, y, z]) + np.float64(
                                        col1array_L[int(pi_orb[k]) - 1])
                                    pi_NL[x, y, z] = np.float64(pi_NL[x, y, z]) + np.float64(
                                        col2array_NL[int(pi_orb[k]) - 1])
                                    # pi_alone[x,y,z,k]=float(col3array[int(pi_orb[k])-1])
                                if first_pi_flag == True:
                                    pi[x, y, z] = np.float64(col3array[int(pi_orb[k]) - 1])
                                    pi_L[x, y, z] = np.float64(col1array_L[int(pi_orb[k]) - 1])
                                    pi_NL[x, y, z] = np.float64(col2array_NL[int(pi_orb[k]) - 1])
                                    # pi_alone[x,y,z,k]=float(col3array[int(pi_orb[k])-1])
                                    first_pi_flag = False

                            first_pi_flag = True

                            for k in range(0, sigma_incr):
                                if first_sigma_flag == False:
                                    if (int(sigma_orb[k]) - 1) < len(col3array):
                                        sigma[x, y, z] = float(sigma[x, y, z]) + float(col3array[int(sigma_orb[k]) - 1])
                                        sigma_L[x, y, z] = float(sigma_L[x, y, z]) + float(
                                            col1array_L[int(sigma_orb[k]) - 1])
                                        sigma_NL[x, y, z] = float(sigma_NL[x, y, z]) + float(
                                            col2array_NL[int(sigma_orb[k]) - 1])
                                if first_sigma_flag == True:
                                    if (int(sigma_orb[k]) - 1) < len(col3array):
                                        sigma[x, y, z] = float(col3array[int(sigma_orb[k]) - 1])
                                        sigma_L[x, y, z] = float(col1array_L[int(sigma_orb[k]) - 1])
                                        sigma_NL[x, y, z] = float(col2array_NL[int(sigma_orb[k]) - 1])
                                    else:
                                        sigma[x, y, z] = 0
                                        sigma_L[x, y, z] = 0
                                        sigma_NL[x, y, z] = 0
                                    first_sigma_flag = False

                            first_sigma_flag = True

                            ###Core orbitals
                            for k in range(0, n_cores):
                                if first_core_flag == False:
                                    if k < len(col3array):
                                        core[x, y, z] = float(core[x, y, z]) + float(col3array[k])
                                        core_L[x, y, z] = float(core_L[x, y, z]) + float(col1array_L[k])
                                        core_NL[x, y, z] = float(core_NL[x, y, z]) + float(col2array_NL[k])
                                if first_core_flag == True:
                                    if k < len(col3array):
                                        core[x, y, z] = float(col3array[k])
                                        core_L[x, y, z] = float(col1array_L[k])
                                        core_NL[x, y, z] = float(col2array_NL[k])
                                    first_core_flag = False

                            first_core_flag = True

                            # update
                            y += 1
                            if y == 3:
                                y = 0
                                x += 1
                                # eigen_incr+=1
                            if x == 5:

                                E = np.array(columns_eigen)
                                E.reshape((3, 3))
                                E = E.transpose()
                                E = E.astype(np.float64)
                                E_inv = np.linalg.inv(E)

                                ##pi
                                for i in range(0, 3):
                                    D = np.array([[pi[0, i, z], 0, 0], [0, pi[1, i, z], 0], [0, 0, pi[2, i, z]]])
                                    D.reshape((3, 3))
                                    D = D.astype(np.float64)
                                    C = E @ D @ E_inv
                                    C = C.astype(np.float64)
                                    pi[0, i, z] = C[0, 0]
                                    pi[1, i, z] = C[1, 1]
                                    pi[2, i, z] = C[2, 2]

                                    pi[5, i, z] = C[0, 1]
                                    pi[6, i, z] = C[0, 2]
                                    pi[7, i, z] = C[1, 0]
                                    pi[8, i, z] = C[1, 2]
                                    pi[9, i, z] = C[2, 0]
                                    pi[10, i, z] = C[2, 1]

                                    D_L = np.array(
                                        [[pi_L[0, i, z], 0, 0], [0, pi_L[1, i, z], 0], [0, 0, pi_L[2, i, z]]])
                                    D_L.reshape((3, 3))
                                    D_L = D_L.astype(np.float64)
                                    C_L = E @ D_L @ E_inv
                                    C_L = C_L.astype(np.float64)
                                    pi_L[0, i, z] = C_L[0, 0]
                                    pi_L[1, i, z] = C_L[1, 1]
                                    pi_L[2, i, z] = C_L[2, 2]

                                    pi_L[5, i, z] = C_L[0, 1]
                                    pi_L[6, i, z] = C_L[0, 2]
                                    pi_L[7, i, z] = C_L[1, 0]
                                    pi_L[8, i, z] = C_L[1, 2]
                                    pi_L[9, i, z] = C_L[2, 0]
                                    pi_L[10, i, z] = C_L[2, 1]

                                    D_NL = np.array(
                                        [[pi_NL[0, i, z], 0, 0], [0, pi_NL[1, i, z], 0], [0, 0, pi_NL[2, i, z]]])
                                    D_NL.reshape((3, 3))
                                    D_NL = D_NL.astype(np.float64)
                                    C_NL = E @ D_NL @ E_inv
                                    C_NL = C_NL.astype(np.float64)
                                    pi_NL[0, i, z] = C_NL[0, 0]
                                    pi_NL[1, i, z] = C_NL[1, 1]
                                    pi_NL[2, i, z] = C_NL[2, 2]

                                    pi_NL[5, i, z] = C_NL[0, 1]
                                    pi_NL[6, i, z] = C_NL[0, 2]
                                    pi_NL[7, i, z] = C_NL[1, 0]
                                    pi_NL[8, i, z] = C_NL[1, 2]
                                    pi_NL[9, i, z] = C_NL[2, 0]
                                    pi_NL[10, i, z] = C_NL[2, 1]

                                ##total
                                for i in range(0, 3):
                                    D = np.array(
                                        [[total[0, i, z], 0, 0], [0, total[1, i, z], 0], [0, 0, total[2, i, z]]])
                                    D = D.astype(float)
                                    D.reshape((3, 3))
                                    C = E @ D @ E_inv
                                    total[0, i, z] = C[0, 0]
                                    total[1, i, z] = C[1, 1]
                                    total[2, i, z] = C[2, 2]

                                    total[5, i, z] = C[0, 1]
                                    total[6, i, z] = C[0, 2]
                                    total[7, i, z] = C[1, 0]
                                    total[8, i, z] = C[1, 2]
                                    total[9, i, z] = C[2, 0]
                                    total[10, i, z] = C[2, 1]

                                    D_L = np.array(
                                        [[total_L[0, i, z], 0, 0], [0, total_L[1, i, z], 0], [0, 0, total_L[2, i, z]]])
                                    D_L.reshape((3, 3))
                                    D_L = D_L.astype(np.float64)
                                    C_L = E @ D_L @ E_inv
                                    C_L = C_L.astype(np.float64)
                                    total_L[0, i, z] = C_L[0, 0]
                                    total_L[1, i, z] = C_L[1, 1]
                                    total_L[2, i, z] = C_L[2, 2]

                                    total_L[5, i, z] = C_L[0, 1]
                                    total_L[6, i, z] = C_L[0, 2]
                                    total_L[7, i, z] = C_L[1, 0]
                                    total_L[8, i, z] = C_L[1, 2]
                                    total_L[9, i, z] = C_L[2, 0]
                                    total_L[10, i, z] = C_L[2, 1]

                                    D_NL = np.array([[total_NL[0, i, z], 0, 0], [0, total_NL[1, i, z], 0],
                                                     [0, 0, total_NL[2, i, z]]])
                                    D_NL.reshape((3, 3))
                                    D_NL = D_NL.astype(np.float64)
                                    C_NL = E @ D_NL @ E_inv
                                    C_NL = C_NL.astype(np.float64)
                                    total_NL[0, i, z] = C_NL[0, 0]
                                    total_NL[1, i, z] = C_NL[1, 1]
                                    total_NL[2, i, z] = C_NL[2, 2]

                                    total_NL[5, i, z] = C_NL[0, 1]
                                    total_NL[6, i, z] = C_NL[0, 2]
                                    total_NL[7, i, z] = C_NL[1, 0]
                                    total_NL[8, i, z] = C_NL[1, 2]
                                    total_NL[9, i, z] = C_NL[2, 0]
                                    total_NL[10, i, z] = C_NL[2, 1]

                                ##sigma
                                for i in range(0, 3):
                                    D = np.array(
                                        [[sigma[0, i, z], 0, 0], [0, sigma[1, i, z], 0], [0, 0, sigma[2, i, z]]])
                                    D.reshape((3, 3))
                                    C = E @ D @ E_inv
                                    sigma[0, i, z] = C[0, 0]
                                    sigma[1, i, z] = C[1, 1]
                                    sigma[2, i, z] = C[2, 2]

                                    sigma[5, i, z] = C[0, 1]
                                    sigma[6, i, z] = C[0, 2]
                                    sigma[7, i, z] = C[1, 0]
                                    sigma[8, i, z] = C[1, 2]
                                    sigma[9, i, z] = C[2, 0]
                                    sigma[10, i, z] = C[2, 1]

                                    D_L = np.array(
                                        [[sigma_L[0, i, z], 0, 0], [0, sigma_L[1, i, z], 0], [0, 0, sigma_L[2, i, z]]])
                                    D_L.reshape((3, 3))
                                    D_L = D_L.astype(np.float64)
                                    C_L = E @ D_L @ E_inv
                                    C_L = C_L.astype(np.float64)
                                    sigma_L[0, i, z] = C_L[0, 0]
                                    sigma_L[1, i, z] = C_L[1, 1]
                                    sigma_L[2, i, z] = C_L[2, 2]

                                    sigma_L[5, i, z] = C_L[0, 1]
                                    sigma_L[6, i, z] = C_L[0, 2]
                                    sigma_L[7, i, z] = C_L[1, 0]
                                    sigma_L[8, i, z] = C_L[1, 2]
                                    sigma_L[9, i, z] = C_L[2, 0]
                                    sigma_L[10, i, z] = C_L[2, 1]

                                    D_NL = np.array([[sigma_NL[0, i, z], 0, 0], [0, sigma_NL[1, i, z], 0],
                                                     [0, 0, sigma_NL[2, i, z]]])
                                    D_NL.reshape((3, 3))
                                    D_NL = D_NL.astype(np.float64)
                                    C_NL = E @ D_NL @ E_inv
                                    C_NL = C_NL.astype(np.float64)
                                    sigma_NL[0, i, z] = C_NL[0, 0]
                                    sigma_NL[1, i, z] = C_NL[1, 1]
                                    sigma_NL[2, i, z] = C_NL[2, 2]

                                    sigma_NL[5, i, z] = C_NL[0, 1]
                                    sigma_NL[6, i, z] = C_NL[0, 2]
                                    sigma_NL[7, i, z] = C_NL[1, 0]
                                    sigma_NL[8, i, z] = C_NL[1, 2]
                                    sigma_NL[9, i, z] = C_NL[2, 0]
                                    sigma_NL[10, i, z] = C_NL[2, 1]

                                ##core
                                for i in range(0, 3):
                                    D = np.array([[core[0, i, z], 0, 0], [0, core[1, i, z], 0], [0, 0, core[2, i, z]]])
                                    D.reshape((3, 3))
                                    C = E @ D @ E_inv
                                    core[0, i, z] = C[0, 0]
                                    core[1, i, z] = C[1, 1]
                                    core[2, i, z] = C[2, 2]

                                    core[5, i, z] = C[0, 1]
                                    core[6, i, z] = C[0, 2]
                                    core[7, i, z] = C[1, 0]
                                    core[8, i, z] = C[1, 2]
                                    core[9, i, z] = C[2, 0]
                                    core[10, i, z] = C[2, 1]

                                    D_L = np.array(
                                        [[core_L[0, i, z], 0, 0], [0, core_L[1, i, z], 0], [0, 0, core_L[2, i, z]]])
                                    D_L.reshape((3, 3))
                                    D_L = D_L.astype(np.float64)
                                    C_L = E @ D_L @ E_inv
                                    C_L = C_L.astype(np.float64)
                                    core_L[0, i, z] = C_L[0, 0]
                                    core_L[1, i, z] = C_L[1, 1]
                                    core_L[2, i, z] = C_L[2, 2]

                                    core_L[5, i, z] = C_L[0, 1]
                                    core_L[6, i, z] = C_L[0, 2]
                                    core_L[7, i, z] = C_L[1, 0]
                                    core_L[8, i, z] = C_L[1, 2]
                                    core_L[9, i, z] = C_L[2, 0]
                                    core_L[10, i, z] = C_L[2, 1]

                                    D_NL = np.array(
                                        [[core_NL[0, i, z], 0, 0], [0, core_NL[1, i, z], 0], [0, 0, core_NL[2, i, z]]])
                                    D_NL.reshape((3, 3))
                                    D_NL = D_NL.astype(np.float64)
                                    C_NL = E @ D_NL @ E_inv
                                    C_NL = C_NL.astype(np.float64)
                                    core_NL[0, i, z] = C_NL[0, 0]
                                    core_NL[1, i, z] = C_NL[1, 1]
                                    core_NL[2, i, z] = C_NL[2, 2]

                                    core_NL[5, i, z] = C_NL[0, 1]
                                    core_NL[6, i, z] = C_NL[0, 2]
                                    core_NL[7, i, z] = C_NL[1, 0]
                                    core_NL[8, i, z] = C_NL[1, 2]
                                    core_NL[9, i, z] = C_NL[2, 0]
                                    core_NL[10, i, z] = C_NL[2, 1]

                                x = 0
                                z += 1
                                # eigen_incr=1
                                # orbitals+=len(col3array)

                            comp_array = []

                    if comp_start_flag == True:
                        comp_array.append(line)

    components = ["xx", "yy", "zz", "Isotropic", "Anisotropy", "xy", "xz", "yx", "yz", "zx", "zy"]
    para_dia = ["Paramagnetic_SO", "Diamagnetic", "Sum_Para_SO_Diamagnetic"]
    create_files = ["total", "pi", "sigma", "core", "total_L", "pi_L", "sigma_L", "core_L", "total_NL", "pi_NL",
                    "sigma_NL", "core_NL"]

    if not os.path.exists("nbo_run"):
        os.makedirs("nbo_run")
    os.chdir(path + "/nbo_run")

    output = open("geometry.txt", "w+")

    for i in range(0, len(atoms)):
        output.write(
            str(int(float(atoms_N[i]))) + "\t" + atoms[i] + "\t" + atoms_x[i] + "\t" + atoms_y[i] + "\t" + atoms_z[
                i] + "\n")

    output.close()

    for m in range(0, 11):
        os.chdir(path + "/nbo_run")
        if not os.path.exists(components[m]):
            os.makedirs(components[m])
        os.chdir(path + "/nbo_run/" + components[m])
        for n in range(0, 3):
            for file in range(0, 12):
                output = open(para_dia[n] + "_" + create_files[file] + ".txt", "w+")
                for k in range(0, z):
                    if file == 0:
                        output.write(str((-1) * float(total[m, n, k])) + "\n")
                    if file == 1:
                        output.write(str(np.float64((-1) * pi[m, n, k])) + "\n")
                    if file == 2:
                        output.write(str((-1) * sigma[m, n, k]) + "\n")
                    if file == 3:
                        output.write(str((-1) * core[m, n, k]) + "\n")
                    if file == 4:
                        output.write(str((-1) * float(total_L[m, n, k])) + "\n")
                    if file == 5:
                        output.write(str(np.float64((-1) * pi_L[m, n, k])) + "\n")
                    if file == 6:
                        output.write(str((-1) * sigma_L[m, n, k]) + "\n")
                    if file == 7:
                        output.write(str((-1) * core_L[m, n, k]) + "\n")
                    if file == 8:
                        output.write(str((-1) * float(total_NL[m, n, k])) + "\n")
                    if file == 9:
                        output.write(str(np.float64((-1) * pi_NL[m, n, k])) + "\n")
                    if file == 10:
                        output.write(str((-1) * sigma_NL[m, n, k]) + "\n")
                    if file == 11:
                        output.write(str((-1) * core_NL[m, n, k]) + "\n")

                output.close()

    b_done = Label(nbo_no_single_point_frame, text="Done", bg="orange", fg="red")
    #b_done.grid(column=0, row=0)
    b_done.pack()

    b_clear_all = Button(nbo_no_single_point_frame, text='Home', command=reset_all)
    #b_clear_all.grid(column=2, row=0)
    b_clear_all.pack(side=TOP, anchor=NE)

#def removethis():
    #frame1.destroy()


root = Tk()
root.title("Quantum Utilities")
#root.geometry('450x300')
root.configure(background="gray22")
home_frame = create_frame(root)
cube_conv_frame = LabelFrame()
cube_oper_frame = LabelFrame()
nbo_no_single_point_frame = LabelFrame()
#frame.pack()


root.mainloop()
