# Details: This python script is used to create initial bond distortion structure for a TiO2 rutile 3x3x3 supercell.
# Requirement: ASE (Atomic Simulation Environment) installed
# File usage: POSCAR that contains supercell to be modeled
# Usage: python bond_distortion.py
from ase.io import read, write
from ase.atom import Atom

# Read POSCAR that contains the supercell
inp = read('POSCAR')

#Scale factor sf - denotes how much distortion from the original Ti-O bond that is needed. Here, 1.02 means the new Ti-O bond is 1.02 times the original Ti-O bond 
# (or the new Ti-O bonds are 2% longer than the orignal Ti-O)
sf = 1.02

# The POSCAR used here is a 3x3x3 TiO2 rutile supercell. Modifications of the atom indexes is needed for other materials.
# Get distance between Ti (134) and 6 O surrounding Ti (134), with periodic boundary conditions
# Get the atom indexes of 6 O atoms surrounding Ti (134) by visuallizing
d1=inp.get_distance(134,53,mic=True)
d2=inp.get_distance(134,52,mic=True)
d3=inp.get_distance(134,59,mic=True)
d4=inp.get_distance(134,54,mic=True)
d5=inp.get_distance(134,55,mic=True)
d6=inp.get_distance(134,58,mic=True)

#Adjust the Ti-O bonds using scale factor
d1a = sf * d1
d2a = sf * d2
d3a = sf * d3
d4a = sf * d4
d5a = sf * d5
d6a = sf * d6

#Set new O position, keeping Ti fixed, with periodic boundary conditions
inp.set_distance(134,53,d1a,fix=0,mic=True)
inp.set_distance(134,52,d2a,fix=0,mic=True)
inp.set_distance(134,59,d3a,fix=0,mic=True)
inp.set_distance(134,54,d4a,fix=0,mic=True)
inp.set_distance(134,55,d5a,fix=0,mic=True)
inp.set_distance(134,58,d6a,fix=0,mic=True)

# Write a new POSCAR after distorting the bonds using sf factor
write('%.2f.POSCAR'%sf,inp)
