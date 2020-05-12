import porespy as ps
import matplotlib.pyplot as plt
import tifffile as tif

from datetime import datetime 

im = ps.generators.blobs(shape=[400, 400], porosity=0.6, blobiness=2)

tif.imshow(im)
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
    
    start_time = datetime.now()
    res = ps.metrics.porosity(im)
    current_time = datetime.now()
    time = str(current_time - start_time)
    
    print('porosity: ' + str(res))
    print('porosity test time: ' + time)
    
    
if region_interface_areas:
    
   pass


if porosity_profile: 
   
    # TODO: что возвращать? 
    
    # Ось 
    axis = 0
    
    start_time = datetime.now()
    
    res = ps.metrics.porosity_profile(im, axis)
    
    
    current_time = datetime.now()
    time = str(current_time - start_time)
    
    print('\n' + 'porosity profile test time: ' + time)