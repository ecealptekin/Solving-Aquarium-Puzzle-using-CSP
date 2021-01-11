#!/usr/bin/env python
# coding: utf-8

# In[2]:


from __future__ import print_function
from ortools.linear_solver import pywraplp
from ortools.constraint_solver import pywrapcp
import sys
import numpy as np
from ortools.sat.python import cp_model

class board(object):

    def __init__(self, f):
        self.file = f
        self.matrix = []
        self.xSize = 0
        self.ySize = 0
        self.column = []
        self.row = []
        self.solution = []

    def setBoard(self):

        fileName = self.file

        with open(fileName, 'r') as fObj:
            lines = fObj.readlines()
            self.xSize = len(lines)
            for line in lines:
                row = line.replace("\n", "").split(" ")
                self.ySize = len(row)

                t = []
                for x in row:
                    for y in x:
                        t.append(y)
                self.matrix.append(t)

        # initialize column and row numbers
        self.column = self.matrix[0]
        self.row = self.matrix[1]

        # delete column and row numbers from matrix
        del self.matrix[0:2]
   
        for i in range(0, len(self.column)): 
            self.column[i] = int(self.column[i])
            
        for i in range(0, len(self.row)): 
            self.row[i] = int(self.row[i]) 
            
        for i in range(0, len(self.row)):
            for j in range(0, len(self.column)):
                self.matrix[i][j] = int(self.matrix[i][j]) 
                
                
    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column
    
    def getAquarium(self,i,j):
        return self.matrix[i][j]


# Create board
filename = "hard.txt"
Board = board(filename)
Board.setBoard()


# Create the solver
model = cp_model.CpModel()

# Creates the variables.
size = len(Board.getRow())
     
# Variables
water = {}
for i in range(size):
    for j in range(size):
        water[i, j] = model.NewBoolVar('%ij%i' % (i,j))        
    
# Creates the constraints.

# for each row, the sum of the columns should be equal to the row constraint
# Constraint for each row
rowb = Board.getRow()
for i in range(size):
    row_constraint = rowb[i]
    model.Add(sum(water[i, j] for j in range(size)) == row_constraint)
    

# for each column, the sum of the rows should be equal to the column constraint
# Constraint for each column
columnb = Board.getColumn()
for j in range(size):
    column_constraint = columnb[j]
    model.Add(sum(water[i, j] for i in range(size)) == column_constraint)

    
#If the aquarium level is the same with the up, water[i-1,j] implies water[i,j]
for i in range(1, size):
    for j in range (size):   
        
        thisaquarium = Board.getAquarium(i,j)     
        upperaquarium = Board.getAquarium(i-1,j)  
        
        if(thisaquarium == upperaquarium):
            model.AddImplication(water[i-1,j], water[i,j])
            
            
#If the aquarium level is the same with the left, the value should be same.
for i in range (size):
    for j in range(1, size):
        
        thisaquarium = Board.getAquarium(i,j) 
        leftaquarium = Board.getAquarium(i,j-1) 
        
        if(thisaquarium == leftaquarium): 
            
            # Declare our intermediate boolean variable.
            b = model.NewBoolVar('b')
            
            
            model.Add(water[i,j] == 1).OnlyEnforceIf(b)
            model.Add(water[i,j] == 0).OnlyEnforceIf(b.Not())
            
            
            model.Add(water[i, j-1] == 1).OnlyEnforceIf(b)
            model.Add(water[i, j-1] == 0).OnlyEnforceIf(b.Not())
                        
                
#If the aquarium level is the same with the right, the value should be same.
for i in range (size):
    for j in range (size-1):
        
        thisaquarium = Board.getAquarium(i,j) 
        rightaquarium = Board.getAquarium(i,j+1) 
        
        if(thisaquarium == rightaquarium): 
            
            # Declare our intermediate boolean variable.
            b = model.NewBoolVar('b')
            

            model.Add(water[i,j] == 1).OnlyEnforceIf(b)
            model.Add(water[i,j] == 0).OnlyEnforceIf(b.Not())
            
            
            model.Add(water[i, j+1] == 1).OnlyEnforceIf(b)
            model.Add(water[i, j+1] == 0).OnlyEnforceIf(b.Not())
            
            

solver = cp_model.CpSolver()
status = solver.Solve(model)


for i in range(size):
    for j in range (size):
        if solver.Value(water[i, j]) == 1:
            print("W", end=" ")
        elif solver.Value(water[i, j]) == 0:
            print("_", end=" ")
    print()
print()


            
        
        
        
        
        
        
        
        
        
        




# In[ ]:





# In[ ]:





# In[ ]:




