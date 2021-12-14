#! /usr/bin/env python
import string
import sys
import math
#from copy import deepcopy


argc = len(sys.argv)
if argc != 5:
    print "This program takes a coordinate file in reduced coordinates (POSCAR format) and creates a polaron distortion around a chosen site. "
    print "It requires a file name, percentage to increase the bond, atom number for the polaron site, and number of neigbors to that polaron site."
    print "Run as: BDM-polaron-vasp.py [filename] [perc increase] [atom number] [number nearest neighbors]"
    print "e.g. BDM-polaron-vasp.py POSCAR-TiO2 4 23 6"
    print "which takes file POSCAR-TiO2 and increases bond lengths by 4% around atom 23 for the 6-nearest neighbors."
    sys.exit(0)

# Several functions are defined below 

# Reads coordinates from xyz file into list
def read_vasp(file_name):
    coords_xyz = []
    lattice_vectors = []
    line_number = 0
    multiplier = 1.0
    num_atoms = 0
    coord_type = "Direct"
    selective = ""
    atom_start = 8
    atom_end = 0
    file_xyz = open(file_name,'r')
    for line in file_xyz :
        #remove any 'bad' characters
        line = line.strip()
        #split line up
        line_split = line.split()
        line_number = line_number + 1
	#Get multiplier
        if line_number == 2:
	    multiplier = float(line_split[0])
	    #print multiplier
	#Get lattice vectors
	if (line_number > 2) & (line_number < 6):
	    lattice_vectors.append(line_split)
	#print lattice_vectors
	#Get number of atoms
        if (line_number == 7 ):
            for i in range(len(line_split)): 
                num_atoms = num_atoms + int(line_split[i])
            atom_end = num_atoms
	    #print num_atoms
	#Check whether selective
	if (line_number == 8 ):
	    if line_split[0] == "Selective":
	        selective = "Selective"  	
		line_number = line_number - 1
		atom_end = atom_end + 1

		#atom_start = atom_start -1

	#Check whether coords in reduced or cartesian
	if (line_number == 8 ):
	    #print line_split[0]
	    if line_split[0] == "Cartesian":
	        coord_type = "Cartesian"
            else:
	        coord_type = "Direct"
        #Read coordinates
        #if (line_number > atom_start) & (line_number < (num_atoms + atom_start)) :
        if (line_number > atom_start) & (line_number < (atom_end + atom_start)) :
	    if coord_type == "Direct":
	        #print line_split
	        x_reduced = float(line_split[0])
	        y_reduced = float(line_split[1])
	        z_reduced = float(line_split[2])
	        x_coord = float(lattice_vectors[0][0])*x_reduced*multiplier + float(lattice_vectors[1][0])*x_reduced*multiplier + float(lattice_vectors[2][0])*x_reduced*multiplier  
	        y_coord = float(lattice_vectors[0][1])*y_reduced*multiplier + float(lattice_vectors[1][1])*y_reduced*multiplier + float(lattice_vectors[2][1])*y_reduced*multiplier  
	        z_coord = float(lattice_vectors[0][2])*z_reduced*multiplier + float(lattice_vectors[1][2])*z_reduced*multiplier + float(lattice_vectors[2][2])*z_reduced*multiplier  
                atom_coords = []
                atom_coords.append(x_coord)
                atom_coords.append(y_coord)
                atom_coords.append(z_coord)
                coords_xyz.append(atom_coords)
		if selective == "Selective":
		    atom_coords.append(line_split[3])    
		    atom_coords.append(line_split[4])    
		    atom_coords.append(line_split[5])    
		    #print atom_coords
	    if coord_type == "Cartesian":
	        x_cart = float(line_split[0])
	        y_cart = float(line_split[1])
	        z_cart = float(line_split[2])
                atom_coords = []
                atom_coords.append(x_cart)
                atom_coords.append(y_cart)
                atom_coords.append(z_cart)
                coords_xyz.append(atom_coords)
		if selective == "Selective":
		    atom_coords.append(line_split[3])    
		    atom_coords.append(line_split[4])    
		    atom_coords.append(line_split[5])    
    file_xyz.close()
    #print len(coords_xyz)
    #print coords_xyz
    return coords_xyz 

# Calculate distance between two atoms
def calc_distance(atom1_coords,atom2_coords):
    dist_x = float(atom1_coords[0])-float(atom2_coords[0])
    dist_y = float(atom1_coords[1])-float(atom2_coords[1])
    dist_z = float(atom1_coords[2])-float(atom2_coords[2])
    distance = math.sqrt(dist_x*dist_x+dist_y*dist_y+dist_z*dist_z)
    return distance

# Creates list with indices of n nearest neighbors to polaron atom 
def find_nearest_neighbors(atom_coords, atom_number, number_neighbors):
    distances = []
    nearest_neighbors = []
    #Find all distances from polaron atom
    for i in range(len(atom_coords)):
        dist = calc_distance(atom_coords[atom_number],atom_coords[i])
	distances.append(dist) 
    #now get indices of nearest neighbors, get indices of sorted list
    index_neighbors = sorted(range(len(distances)), key=lambda k: distances[k])
    nearest_neighbors = index_neighbors[1:number_neighbors+1]
    #print index_neighbors
	
    return nearest_neighbors

#Create 
def create_polaron(atom_coords,neighbors_list,polaron_number,perc_increase):
    #Loop over all the nearest neighbors to create new positions for each nearest neighbor 
    for i in range(len(neighbors_list)):    
        #index of nearest neighbors
        index_atom = neighbors_list[i]
	#Determine vector between polaron atom and neighbor, just subtracting neighbor - polaron positions
	distance_vector = list(atom_coords[index_atom])
	distance_vector[0] = float(distance_vector[0]) - float(atom_coords[polaron_number][0])
	distance_vector[1] = float(distance_vector[1]) - float(atom_coords[polaron_number][1])
	distance_vector[2] = float(distance_vector[2]) - float(atom_coords[polaron_number][2])
        #Increase vector length
	distance_vector[0] = distance_vector[0]*(1+perc_increase)
	distance_vector[1] = distance_vector[1]*(1+perc_increase)
	distance_vector[2] = distance_vector[2]*(1+perc_increase)
        #Recenter around central polaron atom to get correct neighbor positions
	distance_vector[0] = float(distance_vector[0]) + float(atom_coords[polaron_number][0])
	distance_vector[1] = float(distance_vector[1]) + float(atom_coords[polaron_number][1])
	distance_vector[2] = float(distance_vector[2]) + float(atom_coords[polaron_number][2])
        #Now replace old coords with new coords
	new_coords = atom_coords
        new_coords[index_atom][0] = distance_vector[0]  
        new_coords[index_atom][1] = distance_vector[1]  
        new_coords[index_atom][2] = distance_vector[2]  
        #print distance_vector	
        #print atom_coords[index_atom]
	#new_coords = list(atom_coords)
    #print new_coords
    #print atom_coords
    return new_coords 

def vasp_output(atom_coords,file_name):
    file_header = open(file_name,'r')
    file_vasp = open("BDM-polaron-"+file_name,'w')
    line_number = 0
    for line in file_header :
        line_number = line_number + 1
	if line_number == 8 :
	    #print line
            line_split = line.split()
	    if line_split[0] == "Selective":
	        file_vasp.write("Selective dynamics"+"\n")
        if line_number < 8:
	    file_vasp.write(line)
    file_header.close() 
    #    file_vasp.write("Selective dynamics"+"\n")
    file_vasp.write("Cartesian"+"\n")
    
    #file_vasp.write(str(len(new_coords))+"\n")
    #file_vasp.write(str(len(new_coords))+"\n")
    #print len(new_coords)
    #print len(new_coords)

    #need to add more decimal points when making file
    for i in range(len(new_coords)):
	x_formatted = '{:f}'.format(new_coords[i][0])
	y_formatted = '{:f}'.format(new_coords[i][1])
	z_formatted = '{:f}'.format(new_coords[i][2])
	#Need check whether selective dynamics or not
	if len(atom_coords[i]) == 6:
            line_print = x_formatted+" "+ y_formatted+" "+z_formatted+" "+atom_coords[i][3]+" "+atom_coords[i][4]+" "+atom_coords[i][5]+"\n" 
        #line_print = str(new_coords[i][0]) + " " + str(new_coords[i][1]) + " " + str(new_coords[i][2]) + "\n" 
	else:
            line_print = x_formatted + " " + y_formatted + " " + z_formatted + "\n" 
        file_vasp.write(line_print)
    file_vasp.close()
    
    #return 1

#### Parameters from command line
#File name
file_name = sys.argv[1]
#How much to increase bond distances
perc_increase = float(sys.argv[2])/100
#Which atom has polaron
atom_polaron = int(sys.argv[3])-1
#Number nearest neighbors
num_neighbors = int(sys.argv[4])


#Step 1: Read in file
atom_coords = read_vasp(file_name)
#print atom_coords
#Step 2: Determine n nearest neighbors to central polaron atom
neighbors_list = find_nearest_neighbors(atom_coords,atom_polaron,num_neighbors)

#Step 3: Calculate and replace new positions of nearest neighbors to central polaron atom
new_coords = create_polaron(atom_coords,neighbors_list,atom_polaron,perc_increase)

#Step 4: Output new coords
vasp_output(new_coords,file_name)
