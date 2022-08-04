import numpy as np
import os
#---------------
#FUNCTIONS
#---------------
def unique(x):
    uniq=[]
    metals=['Co','Fe','Ni'] #matals
    hal=['Cl','Br']         #halogens
    for i in metals:
        if i in x:
           uniq.append(i)
    for i in hal:
        if i in x:
            uniq.append(i)
    #uniq+=['O','N','C','H']
    for i in x:
        if i not in uniq:
            uniq.append(i)
    return uniq
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
def round_up(x,d=0):
    m=10**d
    return np.ceil(x*m) / m
#---------------------------------------------
pp='_vampire_blocks.txt'
NAMES=[]

for i in os.listdir('.'):
    if i.endswith('xyz'):
        NAMES.append(i)
for NAME in NAMES:
    #NAME='CoCl_no_ligands.txt'
    #os.mkdir('./%s'%(NAME[0:4]))
    atm=np.loadtxt(NAME,usecols=[0],dtype=str,skiprows=2)
    x,y,z=np.loadtxt(NAME, usecols=(1,2,3),skiprows=2,unpack=True)
    #r[:,0]
    uniq=unique(atm)
    #output= open('./%s/'%(NAME[0:4])+NAME+'result.txt','w') #folder for each one
    output= open(NAME[0:-4]+pp,'w')
	
    iatm=pr() 
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
        #print block
        output.write(block)
    output.close()
#input('done')

