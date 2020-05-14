import porespy as ps
import matplotlib.pyplot as plt
import matplotlib
import tifffile as tif
import scipy as sp
import pytrax as pt
import trimesh

matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20)

from datetime import datetime 

im = ps.generators.blobs(shape=[100, 100, 100], porosity=0.5, blobiness=2)

# TODO: dimension
resolution = 1e-6 #m

remove_blind_pores = False

# metrics:
porosity = False
surface_area = True
porosity_profile = False
two_point_correlation = False

# filters
local_thickness = False
local_thickness_Points=25 # standard value 25
porosimetry = False
porosimetry_Points=25 # standard value 25


if remove_blind_pores:
    
    im=ps.filters.fill_blind_pores(im)


if porosity: 
    
    res = ps.metrics.porosity(im)
    
    print('porosity: ' + str(res))
    
    
if surface_area:
    
    inv_im = ~im
    tmp = ps.tools.mesh_region(inv_im)
    vertices = tmp.verts
    faces = tmp.faces
    
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    print('Площадь поверхности:', str(mesh.area), 'мкм^2')

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
    plt.title('Двухточечная корреляция', fontsize=20)
    plt.xlabel('мкм', fontsize=20)
    plt.ylabel('Вероятность', fontsize=20)
    plt.grid()
    plt.plot(*result_fft, 'b.', linewidth=3)
    
    current_time = datetime.now().replace(microsecond=0)
    time = str(current_time - start_time)
               
    print('Two-point correlation test time:', time)
    

    
    
if local_thickness:
    
    poreSizeImage = ps.filters.local_thickness(im,sizes=local_thickness_Points)
    # отрисовка изображения
    tif.imshow(poreSizeImage)
     
    # получаем данные о распределении пор
    poreSizeDist=ps.metrics.pore_size_distribution(poreSizeImage,bins=local_thickness_Points,log=False,voxel_size=resolution)
     
    # отрисовка диаграммы
    plt.figure(figsize=(16, 9))
    plt.title('Распределение размеров пор', fontsize=16)
    plt.bar(poreSizeDist.R*2*1e6, poreSizeDist.satn,width=poreSizeDist.bin_widths*2*1e6, edgecolor='k')
    plt.xlabel('Диаметр поры (мкм)', fontsize=16)
    plt.grid()
        
        
if porosimetry: 
    
    porosimetryImage = ps.filters.porosimetry(im,sizes=porosimetry_Points)
    # отрисовка изображение
    tif.imshow(porosimetryImage)
     
    # получаем данные о распределении пор
    MICP=ps.metrics.pore_size_distribution(porosimetryImage,bins=porosimetry_Points,log=False,voxel_size=resolution)
     
    # отрисовка диаграммы
    plt.figure(figsize=(16, 9))
    plt.title('Распределение размеров пор', fontsize=16)
    plt.bar(MICP.R*2*1e6, MICP.satn,width=MICP.bin_widths*2*1e6, edgecolor='k')
    plt.xlabel('Диаметр поры (мкм)', fontsize=16)
    plt.grid()
    
    # отрисовка кривой интрузии
    plt.figure(figsize=(16, 9))
    plt.title('Кривая интрузии', fontsize=16)
    plt.plot(MICP.R*1e6, MICP.cdf, 'bo-')
    plt.xlabel('R (мкм)', fontsize=16)
    plt.ylabel('объёмная доля', fontsize=16)
    plt.grid()
