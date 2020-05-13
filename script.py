import porespy as ps
import matplotlib.pyplot as plt
import matplotlib
import tifffile as tif
import scipy as sp

matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20)

from datetime import datetime 

im = ps.generators.blobs(shape=[300, 300, 300], porosity=0.6, blobiness=2)

# TODO: dimension, 

# metrics:
porosity = True
region_interface_areas = True
porosity_profile = True 
two_point_correlation = True
linear_density = True
tortuosity = True 
betti_numbers = True

# ?
radial_density = True

# filters
local_thickness = True 
porosimetry = True 


if porosity: 
    
    res = ps.metrics.porosity(im)
    
    print('porosity: ' + str(res))
    
    
if region_interface_areas:
    
   pass


if porosity_profile: 
    
    fig, axs = plt.subplots(3, sharex=True, sharey=True, figsize=(16, 16))
    fig.suptitle('Porosity profile', fontsize=20)
    
    
    phiX=ps.metrics.porosity_profile(im,0)
    axs[0].plot(phiX, linewidth=3)
    axs[0].set_xlabel('voxel', fontsize=20)
    axs[0].set_ylabel('$\phi_x$', fontsize=20)
    axs[0].grid()
    axs[0].set_title('$E(\phi_x)=$'+sp.array2string(sp.mean(phiX),precision=2)+', $\sigma=$'+\
              sp.array2string(sp.std(phiX),precision=2), fontsize=20)
        
    phiY=ps.metrics.porosity_profile(im,1)
    axs[1].plot(phiY, linewidth=3)
    axs[1].set_xlabel('voxel', fontsize=20)
    axs[1].set_ylabel('$\phi_y$', fontsize=20)
    axs[1].grid()
    axs[1].set_title('$E(\phi_y)=$'+sp.array2string(sp.mean(phiY),precision=2)+', $\sigma=$'+\
              sp.array2string(sp.std(phiY),precision=2), fontsize=20)
        
    phiZ=ps.metrics.porosity_profile(im,2)
    axs[2].plot(phiZ, linewidth=3)
    axs[2].set_xlabel('voxel', fontsize=20)
    axs[2].set_ylabel('$\phi_z$', fontsize=20)
    axs[2].grid()
    axs[2].set_title('$E(\phi_z)=$'+sp.array2string(sp.mean(phiZ),precision=2)+', $\sigma=$'+\
              sp.array2string(sp.std(phiZ),precision=2), fontsize=20)
