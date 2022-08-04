import numpy as np
#--------------------
#   File Prameters
#--------------------
fname='FeCl_full_Exp' # name of ucf
l_skip=223 # num. of lines to skip in ucf
JF=[fname[:4]+'_J_nonop.txt',fname[:4]+'_J_op.txt']
    
#--------------------
#   Functions
#--------------------
#Function call for non-optimized: J_creator(fname,l_skip,JF[0]) 
#Function call for optimized: J_creator(fname,l_skip,JF[1])

def J_creator(fname,l_skip,R):
    #the exchange is as following: c0,x,y,c3,c4,c5,J and all int. except for J(float)
    #read the following: i, j, and J_ij
    x,y,J=np.loadtxt(fname+'.ucf', usecols=(1,2,6),skiprows=l_skip,unpack=True)
    c0,c3,c4,c5=np.loadtxt(fname+'.ucf', usecols=(0,3,4,5),skiprows=l_skip,unpack=True)
    a,s,d=np.loadtxt(R,unpack=True)
    
    
    for i in range(len(J)):
        L=[x[i]+1,y[i]+1]
        for j in range(len(a)):
            if a[j] in L and s[j] in L: J[i]=d[j]
    
    for i in range(len(J)):
        if J[i] == 4.98277e-22 or J[i] == 2.2e-25 :
            J[i]=2.2e-27
    
    #-------------------------------------
    #            exporting data
    #-------------------------------------
    #np.savetxt('data.csv', np.c_[x,y,J],fmt='%i \t %i \t %0.6e')#delimiter='\t' 
    #%i \t %i \t %i \t %i \t %i \t %i \t %0.6e
            
    fm='%i \t %i \t %i \t %i \t %i \t %i \t %0.6e'
    np.savetxt(R[:-4]+'_data.csv', np.c_[c0,x,y,c3,c4,c5,J],fmt=fm)#delimiter='\t'
    print R[:-4]+ '... Done'
    return
#--------------------
J_creator(fname,l_skip,JF[0])
J_creator(fname,l_skip,JF[1])
      