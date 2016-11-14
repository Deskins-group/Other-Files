#! /usr/bin/env python
import string
import sys


argc = len(sys.argv)
if argc != 2:
    print "This program takes a text file with a series of TODOs and pairs them up for comparison to generate a sorted priority list."
    print "syntax: pair-sort-todo.py todo-file.txt" 
    sys.exit(0)

todos = []
#Read in todos from a text file
todo_file = open(sys.argv[1],'r')
while 1:
    line = todo_file.readline()
    line = line.strip()
    if not line:
        break
    todos.append([0,line])
todo_file.close()

#Now compare each todo item and prompt which has higher priority
num = len(todos)
for i in range(num):
    for j in range(i+1,num):
        print "########"
        print "(1) ",todos[i][1]
        print "or"
        print "(2) ",todos[j][1]
        priority = raw_input("Which has higher priority: (1) or (2)?")
        if priority == "1":
            todos[i][0]+=1
        elif priority == "2":
            todos[j][0]+=1

#Sort results
todos.sort(key=lambda x: int(x[0]), reverse=True)

#Print results
print " "
print "---------------------------------------------"
print "Final ranking (number is relative importance)"
print "---------------------------------------------"
for i in range(num):
    print todos[i][0], todos[i][1]

#Save to file
file_name = sys.argv[1]
if file_name[-4:] == ".txt":
    file_name = file_name[:-4]
todo_file_sorted = open(file_name+"-sorted.txt",'w')
for i in range(num):
    todo_file_sorted.write(str(todos[i][0])+" "+todos[i][1]+"\n")
todo_file_sorted.close()
