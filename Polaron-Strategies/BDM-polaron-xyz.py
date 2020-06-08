#! /usr/bin/env python
import string
import sys
import math
#from copy import deepcopy


argc = len(sys.argv)
if argc != 5:
    print "This program takes a coordinate file (xyz format) and creates a polaron distortion around a chosen site. "
    print "It requires a file name, percentage to increase the bond, atom number for the polaron site, and number of neigbors to that polaron site."
    print "Run as: BDM-polaron-xyz.py [filename] [perc increase] [atom number] [number nearest neighbors]"
    print "e.g. BDM-polaron-xyz.py tio2.xyz 4 23 6"
    print "which takes file tio2.xyz and increases bond lengths by 4% around atom 23 for the 6-nearest neighbors."
    sys.exit(0)

# Several functions are defined below 

# Reads coordinates from xyz file into list
def read_xyz(file_name):
    coords_xyz = []
    line_number = 0
    file_xyz = open(file_name,'r')
    for line in file_xyz :
        #remove any 'bad' characters
        line = line.strip()
        #split line up
        line_split = line.split()
        line_number = line_number + 1
        #only read lines after file header
        if line_number > 2:
            coords_xyz.append(line_split)
    file_xyz.close()
    return coords_xyz 

# Calculate distance between two atoms
def calc_distance(atom1_coords,atom2_coords):
    dist_x = float(atom1_coords[1])-float(atom2_coords[1])
    dist_y = float(atom1_coords[2])-float(atom2_coords[2])
    dist_z = float(atom1_coords[3])-float(atom2_coords[3])
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
	distance_vector[1] = float(distance_vector[1]) - float(atom_coords[polaron_number][1])
	distance_vector[2] = float(distance_vector[2]) - float(atom_coords[polaron_number][2])
	distance_vector[3] = float(distance_vector[3]) - float(atom_coords[polaron_number][3])
        #Increase vector length
	distance_vector[1] = distance_vector[1]*(1+perc_increase)
	distance_vector[2] = distance_vector[2]*(1+perc_increase)
	distance_vector[3] = distance_vector[3]*(1+perc_increase)
        #Recenter around central polaron atom to get correct neighbor positions
	distance_vector[1] = float(distance_vector[1]) + float(atom_coords[polaron_number][1])
	distance_vector[2] = float(distance_vector[2]) + float(atom_coords[polaron_number][2])
	distance_vector[3] = float(distance_vector[3]) + float(atom_coords[polaron_number][3])
        #Now replace old coords with new coords
	new_coords = atom_coords
        new_coords[index_atom][1] = distance_vector[1]  
        new_coords[index_atom][2] = distance_vector[2]  
        new_coords[index_atom][3] = distance_vector[3]  
        #print distance_vector	
        #print atom_coords[index_atom]
	#new_coords = list(atom_coords)
    #print new_coords
    #print atom_coords
    return new_coords 

def xyz_output(atom_coords,file_name):
    file_xyz = open("BDM-polaron-"+file_name,'w')
    file_xyz.write(str(len(new_coords))+"\n")
    file_xyz.write(str(len(new_coords))+"\n")
    #print len(new_coords)
    #print len(new_coords)
    for i in range(len(new_coords)):
        line_print = str(new_coords[i][0]) + " " + str(new_coords[i][1]) + " " + str(new_coords[i][2]) + " " + str(new_coords[i][3]) + "\n" 
        file_xyz.write(line_print)
    file_xyz.close()
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
atom_coords = read_xyz(file_name)

#Step 2: Determine n nearest neighbors to central polaron atom
neighbors_list = find_nearest_neighbors(atom_coords,atom_polaron,num_neighbors)

#Step 3: Calculate and replace new positions of nearest neighbors to central polaron atom
new_coords = create_polaron(atom_coords,neighbors_list,atom_polaron,perc_increase)

#Step 4: Output new coords
xyz_output(new_coords,file_name)

