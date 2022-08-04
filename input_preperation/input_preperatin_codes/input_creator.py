import os
#---------------------------
#   Functions : benchmarking,curi temp, and H. loop simulations
#---------------------------
def bench():
    X='''
#------------------------------------------
# Simulation attributes:
#------------------------------------------
sim:minimum-temperature=0
sim:maximum-temperature=4
sim:temperature-increment=4
sim:time-steps-increment=3
sim:equilibration-time-steps=500000
sim:loop-time-steps=1000000
#------------------------------------------
# Program and integrator details
#------------------------------------------
sim:program=benchmark
sim:integrator=llg-heun
#------------------------------------------
# data output
#------------------------------------------
config:atoms
    '''
    return X

def curi():
    X='''
#------------------------------------------
# Simulation attributes:
#------------------------------------------
sim:minimum-temperature=0
sim:maximum-temperature=300
sim:temperature-increment=2
sim:time-steps-increment=4
sim:equilibration-time-steps=500000
sim:loop-time-steps=1000000

#------------------------------------------
# Program and integrator details
#------------------------------------------
sim:applied-field-strength = 0.1 
sim:program=curie-temperature
sim:integrator=monte-carlo
#------------------------------------------
# data output
#------------------------------------------
output:temperature
output:magnetisation-length
output:mean-magnetisation-length
output:mean-susceptibility
config:atoms
#screen:temperature
#screen:mean-magnetisation-length
#screen:mean-susceptibility
    '''    
    return X


#------------
names=[]    #cif files names (without the extinsion)
suf='_vampire_blocks.txt' # suffix to files that contains vampire's data block
for i in os.listdir('.'):
    if i.endswith('xyz'):
        names.append(i[0:-4])
iii=1 	#index for the file in the output screen
for name in names:
    print iii,'\t', name + '...',
    iii+=1
#-------------------------------------------------------------------------
#           reading data
#-------------------------------------------------------------------------
    r=open(name+suf,'r') #file to be read
    r.readline()    #skip first line
    exec'uatoms=%s'%(r.readline()) # unique atoms from file (2nd line )
    exec 'num_atoms=%s'%(r.readline())
    r.readline() ; r.readline() ; r.readline() # skip 4th ,5th and the 6th line of the file
    cell_size=r.readline()[0:-1]
    ucv=cell_size[1:-1].split(",")
        #----------------------
        #       mat_num
        #----------------------
    exec r.readline() # variable called mat_num
        #----------------------
    data_block=r.read()
    r.close()
#-------------------------------------------------------------------------
#           writing data
#-------------------------------------------------------------------------
    w=open(name+'.input','w') # input file to be written
    w.write('''#------------------------------------------
# Vampire input file for benchmarking
#------------------------------------------
#    %s
#------------------------------------------
# System Dimensions:
#------------------------------------------\n''' %(name))
    w.write("#"+cell_size)
    w.write('''
dimensions:system-size-x = %s !A
dimensions:system-size-y = %s !A
dimensions:system-size-z = %s !A
            \n'''%(ucv[0],ucv[1],ucv[2]) ) 
    w.write('''#------------------------------------------
# Material Files:
#------------------------------------------
material:file=%s.mat
material:unit-cell-file=%s.ucf
\n'''%(name,name))
    B=curi()
    w.write(B)
    w.close()
    print '... done :)'
print ('input files created')
#input('all done ...')