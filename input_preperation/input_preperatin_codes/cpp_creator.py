import os
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
    w=open(name+'.cpp','w') # cpp file to be written
    w.write('''//-------------------------------------------------------
//
//  Unit Cell creator
//
//  Takes a primitive unit cell and replicates it, 
//  creating the neighbourlist and populating atomic 
//  properties for input into vampire
//
//  (C) R.F.L.Evans 22/04/2015
//
//
//-------------------------------------------------------
#include <string>
#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

class uc_atom_t{

public:

  double cx;
  double cy;
  double cz;

  int material;
  int hc;
  int lc;

};

class material_t{

public:

  double mu_s;
  double alpha;
  double Ku;
  double Sx;
  double Sy;
  double Sz;
  std::string name;
  std::string element;


};

class nn_t{

public:
  int i;
  int j;
  int dx;
  int dy;
  int dz;
  double Jij;
};

int main(){

  // system constants
  //unit cell sizes\n''')
  
    
    
    w.write('''  double unit_cell_size[3]=%s;\n'''%(cell_size)) #cell size
    w.write('''
  const int num_materials=%i;\n'''%(mat_num))
    w.write('''  // exchange constants
  std::vector<std::vector<double> > exchange_constants;
  exchange_constants.resize(num_materials);
  for(int m=0;m<num_materials;m++) exchange_constants.at(m).resize(num_materials);

  // material parameters
  std::vector<material_t> materials(num_materials);\n''')
    #------------------------------------------
    #   prepare mu_s and exchange constant
    #------------------------------------------
    metals=['Fe','Co','Ni']
    spin=[4.0,3.0,1.0]
    hals=['Cl','Br']
#                   exchange constant
#           FeCl2                CoCl2               NiBr2                NiCl2
    JJ=[4.08555024164e-22 , 3.14026606809e-22 , 4.98276911824e-22 , 5.14298677477e-22]
    
    for i in range(len(metals)):
        if uatoms[0]==metals[i]:
            s=spin[i]    # metal mu_s
    if uatoms[0]=='Fe':
        j=JJ[0]
    elif uatoms[0]=='Co':
        j=JJ[1]
    elif uatoms[0]=='Ni' and uatoms[1]=='Br':
        j=JJ[2]
    elif uatoms[0]=='Ni'and uatoms[1]=='Cl':
        j=JJ[3]
    
    #------------------------------------------
    #       material parameters
    #------------------------------------------
    for i in range(len(uatoms)):
        if i==0:
            w.write('''\n  materials.at(%i).mu_s=%f; // mu_B's\n'''%(i,s))
            w.write('''  materials.at(%i).alpha=0.1;\n'''%(i))
            w.write('''  materials.at(%i).Ku=1.0e-28; // J/atom\n'''%(i))
            w.write('''  materials.at(%i).name="%s";\n'''%(i,uatoms[i]))
            w.write('''  materials.at(%i).element="%s";\n'''%(i,uatoms[i]))
            w.write('''  materials.at(%i).Sx=0.0;\n'''%(i))
            w.write('''  materials.at(%i).Sy=0.0;\n'''%(i))
            w.write('''  materials.at(%i).Sz=1.0;\n\n'''%(i))
        else:
            w.write('''  materials.at(%i).mu_s=0.1; // mu_B's\n'''%(i))
            w.write('''  materials.at(%i).alpha=0.1;\n'''%(i))
            w.write('''  materials.at(%i).Ku=1.0e-28; // J/atom\n'''%(i))
            w.write('''  materials.at(%i).name="%s";\n'''%(i,uatoms[i]))
            w.write('''  materials.at(%i).element="%s";\n'''%(i,uatoms[i]))
            w.write('''  materials.at(%i).Sx=0.0;\n'''%(i))
            w.write('''  materials.at(%i).Sy=0.0;\n'''%(i))
            w.write('''  materials.at(%i).Sz=1.0;\n\n'''%(i))
        
        #w.write('''\n''')
    #------------------------------------------
    #    exchange constant
    #------------------------------------------
    n=len(uatoms) #number of unique atoms
    for i in range(n):
        for k in range(n)[i:]:
            if i == k:
                if i==0 and k==0:
                    ex='  exchange_constants.at(%i).at(%i)=%s; //%s-%s\n'%(i,k,str(j),uatoms[i],uatoms[k])
                else:
                    ex='  exchange_constants.at(%i).at(%i)=2.2e-25; //%s-%s\n'%(i,k,uatoms[i],uatoms[k])
                w.write(ex)
            else:
                ex='  exchange_constants.at(%i).at(%i)=2.2e-25; //%s-%s\n'%(i,k,uatoms[i],uatoms[k])
                ex1='  exchange_constants.at(%i).at(%i)=2.2e-25; //%s-%s\n'%(k,i,uatoms[k],uatoms[i])
                w.write(ex)
                w.write(ex1)
    #------------------------------------------ 
    w.write('\n')   
    w.write('''  // create atoms in unit cell
  std::vector<uc_atom_t> unit_cell(0);\n\n''')
    w.write('''  unit_cell.resize(%i);\n\n'''%(num_atoms))
    w.write(data_block)
    w.write('\n\n')
    w.write('''
  // store vector of unit cells
  std::vector< std::vector < std::vector < std::vector<uc_atom_t > > > >crystal;
  
  crystal.resize(3);
  for(int i=0;i<3;i++){
    crystal.at(i).resize(3);
    for(int j=0;j<3;j++){
      crystal.at(i).at(j).resize(3);
      for(int k=0;k<3;k++){
	crystal.at(i).at(j).at(k).resize(unit_cell.size());
      }
    }
  }
    
  // replicate unit cell
  for(int i=0;i<3;i++){
    for(int j=0;j<3;j++){
      for(int k=0;k<3;k++){
	for(int a=0;a<unit_cell.size();a++){
	  crystal.at(i).at(j).at(k).at(a).cx=unit_cell.at(a).cx+double(i);
          crystal.at(i).at(j).at(k).at(a).cy=unit_cell.at(a).cy+double(j);
	  crystal.at(i).at(j).at(k).at(a).cz=unit_cell.at(a).cz+double(k);
	  crystal.at(i).at(j).at(k).at(a).material=unit_cell.at(a).material;
	  crystal.at(i).at(j).at(k).at(a).hc=unit_cell.at(a).hc+2*k-2;
          crystal.at(i).at(j).at(k).at(a).lc=unit_cell.at(a).lc;	  
	}
      }
    }
  }

  // create neighbour list
  double nn_range=0.5*0.5+0.5*0.5;
  std::vector<nn_t> nn_list;

  // loop over all atoms in unit cell
  for(int ai=0;ai<unit_cell.size();ai++){
    double icx=crystal[1][1][1].at(ai).cx;
    double icy=crystal[1][1][1].at(ai).cy;
    double icz=crystal[1][1][1].at(ai).cz;
    int imat=crystal[1][1][1].at(ai).material;
    int ihc=crystal[1][1][1].at(ai).hc;
    int ilc=crystal[1][1][1].at(ai).lc;

    // loop over all other atoms
    for(int i=0;i<3;i++){
      for(int j=0;j<3;j++){
	for(int k=0;k<3;k++){
	  for(int aj=0;aj<unit_cell.size();aj++){
	    double jcx=crystal[i][j][k].at(aj).cx;
	    double jcy=crystal[i][j][k].at(aj).cy;
	    double jcz=crystal[i][j][k].at(aj).cz;
	    int jmat=crystal[i][j][k].at(aj).material;
	    int jhc=crystal[i][j][k].at(aj).hc;
	    int jlc=crystal[i][j][k].at(aj).lc;
	    double range_sq=(jcx-icx)*(jcx-icx)+(jcy-icy)*(jcy-icy)+(jcz-icz)*(jcz-icz);
	    bool same_atom=(ai==aj && i==1 && j==1 && k==1);
	    if(range_sq<=nn_range && same_atom==false){
	      nn_t temp;
	      temp.i=ai;
	      temp.j=aj;
	      temp.dx=i-1;
	      temp.dy=j-1;
	      temp.dz=k-1;
	      temp.Jij=exchange_constants.at(imat).at(jmat);
	      nn_list.push_back(temp);
	      //std::cout << ai << "\t" << aj << "\t" << i-1 << "\t" << j-1 << "\t" << k-1 << "\t" << sqrt(range_sq) << std::endl;
	    } 
	  }
	}
      }
    }

  }


  // output to files
  // declare outfile file stream
  std::ofstream ucf_file;
  // open it (file_name)
  ucf_file.open ("%s.ucf");

  ucf_file << "# Unit cell size:" << std::endl;
  ucf_file << unit_cell_size[0] << "\t" << unit_cell_size[1] << "\t" << unit_cell_size[2] << std::endl;
  ucf_file << "# Unit cell vectors: " << std::endl;
  ucf_file << "1.0 0.0 0.0 " << std::endl;
  ucf_file << "0.0 1.0 0.0 " << std::endl;
  ucf_file << "0.0 0.0 1.0 " << std::endl;
  ucf_file << "# Atoms num, id cx cy cz mat lc hc " << std::endl;
  ucf_file << unit_cell.size() << std::endl;
  // loop over all atoms
  for(int atom=0; atom<unit_cell.size(); atom++){
    ucf_file << atom << "\t";
    ucf_file << unit_cell.at(atom).cx << "\t";
    ucf_file << unit_cell.at(atom).cy << "\t";
    ucf_file << unit_cell.at(atom).cz << "\t";
    ucf_file << unit_cell.at(atom).material << "\t";
    ucf_file << unit_cell.at(atom).lc << "\t";
    ucf_file << unit_cell.at(atom).hc << std::endl;
  }
  ucf_file << "#Interactions n exctype, id i j dx dy   dz        Jij"<< std::endl;
  ucf_file << nn_list.size() << "\t" << "isotropic" << std::endl;
  // loop over all interactions
  for(unsigned int nn=0; nn < nn_list.size(); nn++){
    ucf_file << nn << "\t";
    ucf_file << nn_list[nn].i << "\t";
    ucf_file << nn_list[nn].j << "\t"; 
    ucf_file << nn_list[nn].dx << "\t";
    ucf_file << nn_list[nn].dy << "\t"; 
    ucf_file << nn_list[nn].dz << "\t"; 
    ucf_file << nn_list[nn].Jij << std::endl;
  }
  
  // material file
  std::ofstream mat_file;
  // open it (file_name)
  mat_file.open ("%s.mat");
  mat_file << "#================================================" << std::endl;
  mat_file << "# Generated material file for input into vampire" << std::endl;
  mat_file << "#================================================" << std::endl;
  mat_file << "#" << std::endl;
  mat_file << "# File timestamp: " << std::endl;
  mat_file << "#" << std::endl;
  mat_file << "#------------------------------------------------" << std::endl;
  mat_file << "# Number of Materials" << std::endl;
  mat_file << "#------------------------------------------------" << std::endl;
  mat_file << "material:num-materials=" << num_materials << std::endl;
  mat_file << "#------------------------------------------------" << std::endl;
  
  // Loop over all materials
  for(int m=0;m<materials.size();m++){
    mat_file << "# Material " << m+1 << " (" << materials.at(m).name << ")" << std::endl;
    mat_file << "#------------------------------------------------" << std::endl;
    mat_file << "material[" << m+1 << "]:material-name=" << materials.at(m).name << std::endl;
    mat_file << "material[" << m+1 << "]:damping-constant=" << materials.at(m).alpha << std::endl;
    mat_file << "material[" << m+1 << "]:atomic-spin-moment="<< materials.at(m).mu_s << " !muB" << std::endl;
    mat_file << "material[" << m+1 << "]:uniaxial-anisotropy-constant=" << materials.at(m).Ku << std::endl;
    //mat_file << "material[" << m << "]:uniaxial-anisotropy-direction=" << 0 << "," << 1 << ","<< 0 << std::endl;
    mat_file << "material[" << m+1 << "]:material-element="<< materials.at(m).element << ""<< std::endl;
    mat_file << "material[" << m+1 << "]:initial-spin-direction="<< materials.at(m).Sx << "," << materials.at(m).Sy << "," << materials.at(m).Sz << std::endl;
    mat_file << "#------------------------------------------------" << std::endl;
  }
  return 0;
}
'''%(name,name))
    w.write('\n')
    w.close()
    print j, '... done :)'
print("unit cell cpp files created")
#input('all done ...')