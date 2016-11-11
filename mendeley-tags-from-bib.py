#! /usr/bin/env python
#Created by N. A. Deskins 11-11-16. 
#Simple script to take a bib file that was exported from Mendeley and create a list of Mendeley tags
#Useful when you have many tags to keep track of
import string
import sys

#Stop if no input file provided
num_args = len(sys.argv)
if num_args != 2:
    print "Input required is bib file name."
    print "mendeley-tags-from-bib.py file.bib > tag.txt"
    sys.exit(0)

tags_list=[]
bib_file = open(sys.argv[1],'r')
while 1:
    #Read lines from bib file 
    line = bib_file.readline()
    line = line.strip()
    if not line:
        break 
    line_parts = line.split()
    #Process lines with mendeley-tags
    if line_parts[0]=="mendeley-tags":
        tags_current = line_parts[2] 
        #Remove brackets and split up tags
        tags_current=tags_current.replace("{","")
        tags_current=tags_current.replace("},","")
        tags_split = tags_current.split(',')
        #Add tags to tag list and remove funny underscore syntax
        for i in range(len(tags_split)):
            tag_fixed=str(tags_split[i]).replace("\_}","_")
            tags_list.append(tag_fixed)
bib_file.close()

#create and print final sorted tag list
final_list=sorted(set(tags_list), key=str.lower)
for i in range(len(final_list)):
    print final_list[i]

