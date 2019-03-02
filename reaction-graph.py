#! /usr/bin/env python
import string
import sys
# Takes a txt file with reaction energies and creates data
# to make common reaction plot
# run:  python reaction-graph.py INPUTFILE bar-length reaction-spacing
# Date: 3-2-19

file_in=open(sys.argv[1],'r')
file_out=open('reaction-data.txt','w')
bar_length = sys.argv[2]
rxn_space = sys.argv[3]
it=0

while 1:
    line = file_in.readline()
    line = line.strip()
    if not line:
        break
    for i in range(int(bar_length)):
        it+=1
	t = str(it)+" "+str(line)+"\n"
        file_out.write(t)
    for i in range(int(rxn_space)):
	it+=1


file_in.close()
file_out.close()
