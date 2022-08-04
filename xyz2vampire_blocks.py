import numpy as np
import os
#---------------------------------------------
#FUNCTIONS
#---------------------------------------------
#Func.1: Identify system's atoms
def unique(x):
    uniq=[]
    metals=['Co','Fe','Ni'] #metal atoms
    hal=['Cl','Br']         #halogen atoms
    for i in metals:
        if i in x:
           uniq.append(i)
    for i in hal:
        if i in x:
            uniq.append(i)
    for i in x:
        if i not in uniq:
            uniq.append(i)
    return uniq
#Func.2: indexer, change atom's symbol to number based Func.1
def pr():
    k=0
    for m in uniq:
        i='%s=%i'%(m,k)
        exec (i)
        if m != uniq[-1]:
            i+='    '
        else:
            i+='\n'
        output.write(i)
        print i
        k+=1
    output.write(str(uniq)+'\n')
    iatm=[]
    for i in atm:
        exec ('a0=%s'%(i))
        iatm.append(a0)
    output.write('%i\n'%(len(iatm)))
    return iatm
#Func.3: Rounding function
def round_up(x,d=0):
    m=10**d
    return np.ceil(x*m) / m
#---------------------------------------------
pp='_vampire_blocks.txt'
NAMES=[]

for i in os.listdir('.'):
    if i.endswith('xyz'):
        NAMES.append(i)
# for-loop on all ".xyz" files to output vampire blocks
for NAME in NAMES:
    l_s=2
    atm=np.loadtxt(NAME,usecols=[0],dtype=str,skiprows=l_s)
    x,y,z=np.loadtxt(NAME, usecols=(1,2,3),skiprows=l_s,unpack=True)
    uniq=unique(atm)
    output= open(NAME[0:-4]+pp,'w')
    iatm=pr() #change atoms sympol to indix based on "uniq"
    #--------------------------------------   
    #prepare some notes in the output file
    #--------------------------------------
    xm=round_up(max(x),1)
    ym=round_up(max(y),1)
    zm=round_up(max(z),1)
    print 'xm',max(x)
    print 'ym',max(y)
    print 'zm',max(z)
    output.write('Xm=%f\n'%(max(x)))
    output.write('Ym=%f\n'%(max(y)))
    output.write('Zm=%f\n'%(max(z)))
    output.write('{%f,%f,%f}\n'%(xm,ym,zm))
    output.write('mat_num=%i\t #num_materials\n\n'%(len(uniq)))
    xr=x/xm
    yr=y/ym
    zr=z/zm
	#-------------
    for i in range(len(iatm)):
        block='''  unit_cell.at(%i).cx=%f;
  unit_cell.at(%i).cy=%f;
  unit_cell.at(%i).cz=%f;
  unit_cell.at(%i).material=%i;
  unit_cell.at(%i).hc=%i;
  unit_cell.at(%i).lc=0;'''%(i,xr[i],i,yr[i],i,zr[i],i,iatm[i],i,iatm[i],i)
        if i !=len(iatm)-1:
            block+='\n\n'
        output.write(block)
    output.close()
    
