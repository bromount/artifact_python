'''
Created on 01-Aug-2015

@author: bromount
'''
from __builtin__ import isinstance

#this is about the list input

movies = ['Jeans','roja','Alaipauthey']

print movies

movies.append(2000)

print movies

movies.insert(1, 1998)

print movies

movies.insert(3, 1992)

print movies

for item in movies:
    print item
    
count = 0

while count < len(movies):
    print (movies[count])
    count = count + 1


