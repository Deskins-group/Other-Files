# OtherFiles
Here are scripts to help form polarons using the Bond Distortion Method (BDM) discussed in our recent paper XYZ. Several files exist, one that processes VASP POSCAR files, and one that processes cartesian xyz files. Currently neither script considers periodic boundary conditions, so be sure to place the polaron near the center of the simulation cell. 

The scripts work by picking a central atom, finding the n-nearest neighbors (specified by the user and usually determined by the crystal structure), and then increasing the bond distances between the central atom and the n-nearest neighbors by a specified percentage. Thus, the user needs to provide the following: filename of the undistorted structure, atom for the polaron site (e.g. 135), percentage bond increase (e.g. 4 would be a 4% bond increase), number of nearest neighbors around the central atom (e.g. 6). 

Also provided is an example of how to use ASE with the bond distortion method.

If you use these scripts or the BDM, please cite our recent paper. 



- **BDM-polaron-vasp.pyy** A script to create a polaronic distortion around a specified atomic site. Works with VASP POSCAR files. Usage is: "BDM-polaron-vasp.py [filename] [perc increase] [atom number] [number nearest neighbors]".
- **BDM-polaron-xyz.py** A script to create a polaronic distortion around a specified atomic site. Works with xyz files. Usage is: "BDM-polaron-xyz.py [filename] [perc increase] [atom number] [number nearest neighbors]".
- **BDM-ASE.py** An example script to create a polaronic distortion around a specified atomic site use the Atomic Simulation Environment (ASE). 

