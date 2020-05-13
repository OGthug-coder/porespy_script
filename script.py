import porespy as ps
import matplotlib.pyplot as plt
import matplotlib
import tifffile as tif
import scipy as sp
import pytrax as pt

matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20)

from datetime import datetime 
from mogutda import SimplicialComplex

im = ps.generators.blobs(shape=[100, 100, 100], porosity=0.6, blobiness=2)

# TODO: dimension
resolution = 1e-6 #m

# metrics:
porosity = False
region_interface_areas = False
porosity_profile = False
two_point_correlation = False
linear_density = True
tortuosity = False

# For 2d images!
betti_numbers = False

# filters
local_thickness = False
porosimetry = False


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


if two_point_correlation: 
    
    start_time = datetime.now().replace(microsecond=0)
    
    result_fft = ps.metrics.two_point_correlation_fft(im)
    plt.figure(figsize=(16, 9))
    plt.title('Two-point correlation', fontsize=20)
    plt.xlabel('XLABEL', fontsize=20)
    plt.ylabel('YLABEL', fontsize=20)
    plt.grid()
    plt.plot(*result_fft, 'b.', linewidth=3)
    
    current_time = datetime.now().replace(microsecond=0)
    time = str(current_time - start_time)
               
    print('Two-point correlation test time:', time)
    
    
if linear_density: 
    
    pass

if tortuosity: 
    
    rw = pt.RandomWalk(im)
    rw.run(nt=1e4, nw=1e2, same_start=False, stride=100, num_proc=1)
    rw.plot_msd()
        

if betti_numbers: 
    
    im_c = SimplicialComplex(simplices=im)
 
    print(im_c.betti_number(0))
    print(im_c.betti_number(1)) 
    print(im_c.betti_number(2))
    
    
if local_thickness:
    
    poreSizeImage = ps.filters.local_thickness(im)
    # отрисовка изображения
    tif.imshow(poreSizeImage)
     
    # получаем данные о распределении пор
    poreSizeDist=ps.metrics.pore_size_distribution(poreSizeImage,bins=10,log=False,voxel_size=resolution)
     
    # отрисовка диаграммы
    plt.figure(figsize=(16, 9))
    plt.title('Распределение размеров пор', fontsize=16)
    plt.bar(poreSizeDist.R*2*1e6, poreSizeDist.satn,width=poreSizeDist.bin_widths*2*1e6, edgecolor='k')
    plt.xlabel('Диаметр поры (мкм)', fontsize=16)
        
        
if porosimetry: 
    
    porosimetryImage = ps.filters.porosimetry(im)
    # отрисовка изображение
    tif.imshow(porosimetryImage)
     
    # получаем данные о распределении пор
    MICP=ps.metrics.pore_size_distribution(porosimetryImage,bins=10,log=False,voxel_size=resolution)
     
    # отрисовка диаграммы
    plt.figure(figsize=(16, 9))
    plt.title('Распределение размеров пор', fontsize=16)
    plt.bar(MICP.R*2*1e6, MICP.satn,width=MICP.bin_widths*2*1e6, edgecolor='k')
    plt.xlabel('Диаметр поры (мкм)', fontsize=16)
     
    # отрисовка кривой интрузии
    plt.figure(figsize=(16, 9))
    plt.title('Кривая интрузии', fontsize=16)
    plt.plot(MICP.R*1e6, MICP.cdf, 'bo-')
    plt.xlabel('R (мкм)', fontsize=16)
    plt.ylabel('объёмная доля', fontsize=16)
