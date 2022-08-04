import numpy as np
old=np.loadtxt('old.txt', usecols=(0),skiprows=0,unpack=True)
new=np.loadtxt('new.txt', usecols=(0),skiprows=0,unpack=True)
C1,C2=np.loadtxt('ij.txt', usecols=(0,1),skiprows=0,unpack=True)
nc1=np.array([])
nc2=np.array([])

for i in C2:
    if i not in old: print i 
for i in range(len(C1)):
    for j in range(len(old)):
        if C1[i] == old[j] : 
            nc1=np.append(nc1,new[j])

for i in range(len(C2)):
    for j in range(len(old)):
        if C2[i] == old[j] : 
            nc2=np.append(nc2,new[j])
fm="%i \t %i"        
np.savetxt('ij_new.txt', np.c_[nc1,nc2],fmt=fm)#delimiter='\t'
