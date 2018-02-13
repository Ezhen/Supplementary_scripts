import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.mlab import griddata
import scipy
import pyroms
import pyroms_toolbox
from bathy_smoother import *
import netCDF4



Lp = 50 				#closeness to BCZ
Mp = 40

rr = netCDF4.Dataset('GEBCO_2014_2D_-15.0_40.0_10.0_60.0_BATHYMETRY_FILE.nc', 'r', format='NETCDF4')
lats = rr.variables['lat'][1080:1560]
lons = rr.variables['lon'][1500:2500]
topo = rr.variables['elevation'][1080:1560,1500:2500]

topo=-topo

print 'fix minimum depth'
hmin = 2
topo = pyroms_toolbox.change(topo, '<', hmin, hmin)

lon0=6.7 ; lat0=50.3
lon1=5.0 ; lat1=52.3
lon2=0 ; lat2=52.3
lon4=0 ; lat4=49.7
lon5=1.8 ; lat5=50.3
lon6=2.61 ; lat6=51.04
lon7=3.40 ; lat7=51.32
lonp = np.array([lon0, lon1, lon2,  lon4, lon5, lon6, lon7])
latp = np.array([lat0, lat1, lat2,  lat4, lon5, lat6, lat7])
beta = np.array([0, 1,  0,  1, 0, 1, 1])
map = Basemap(projection='merc', llcrnrlon=-2.5, llcrnrlat=49, urcrnrlon=6, urcrnrlat=53, lat_ts=51, resolution='h')
map.drawcoastlines()

hgrd = pyroms.grid.Gridgen(lonp, latp, beta, (Mp+3,Lp+3), proj=map)

lonv, latv = map(hgrd.x_vert, hgrd.y_vert, inverse=True)
hgrd = pyroms.grid.CGrid_geo(lonv, latv, map)

plt.plot(hgrd.x,hgrd.y, '-k') 
plt.plot(hgrd.x.T,hgrd.y.T, '-k')

def point_inside_polygon(x,y,poly):	# Ex.: a=[(0,0),(0,2),(1,1),(1,0)] if x=0.4 y=1.2 function gives "True" if x=0.8 y=1.8 function gives "False"
	n = len(poly)
	inside =False
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside

def PolygonArea(corners):		# Shoelace formula; Ex.: a=[(0,0),(0,2),(1,1),(1,0)] Function gives 1.5
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def Width(corners):			
	ls=[((corners[0][0]+corners[1][0])/2.,(corners[0][1]+corners[1][1])/2.)]
	rs=[((corners[2][0]+corners[3][0])/2.,(corners[2][1]+corners[3][1])/2.)]
	width=(((rs[0][0]-ls[0][0])**2)+((rs[0][1]-ls[0][1])**2))**0.5
	return width

def Height(corners):
	us=[((corners[1][0]+corners[2][0])/2.,(corners[1][1]+corners[2][1])/2.)]
	ds=[((corners[0][0]+corners[3][0])/2.,(corners[0][1]+corners[3][1])/2.)]
	height=(((us[0][0]-ds[0][0])**2)+((us[0][1]-ds[0][1])**2))**0.5
	return height

def Aspect(width,height):			# Calculation of aspect; Ex.: a=[(0,0),(0,2),(1,1),(1,0)] Function gives 0.7453559924999299
	aspect=width/height
	return aspect
	
	
count_p=np.zeros((len(hgrd.lat_vert)-1,len(hgrd.lon_vert.T)-1))
depth=np.zeros((len(hgrd.lat_vert)-1,len(hgrd.lon_vert.T)-1))

for i in range(len(hgrd.lat_vert)-1):
	for j in range(len(hgrd.lon_vert.T)-1):
		poly=[(hgrd.lat_vert[i,j],hgrd.lon_vert[i,j]),(hgrd.lat_vert[i+1,j],hgrd.lon_vert[i+1,j]),(hgrd.lat_vert[i,j+1],hgrd.lon_vert[i,j+1]),(hgrd.lat_vert[i+1,j+1],hgrd.lon_vert[i+1,j+1])]
		poly_cartesian=[(hgrd.y_vert[i,j],hgrd.x_vert[i,j]),(hgrd.y_vert[i+1,j],hgrd.x_vert[i+1,j]),(hgrd.y_vert[i,j+1],hgrd.x_vert[i,j+1]),(hgrd.y_vert[i+1,j+1],hgrd.x_vert[i+1,j+1])]
		for k in range(np.where(lats>min(np.array(poly)[:,0]))[0][0],np.where(lats<max(np.array(poly)[:,0]))[0][-1]):
			for l in range(np.where(lons>min(np.array(poly)[:,1]))[0][0],np.where(lons<max(np.array(poly)[:,1]))[0][-1]):
				if point_inside_polygon(lats[k],lons[l],poly)==True:
					count_p[i,j]=count_p[i,j]+1
					depth[i,j]=topo[k,l]+depth[i,j]
					#print lats[k], lons[l], 'True'
				else:
					#print lats[k], lons[l],'False'
					pass
		#print 'grid cell number i=%g,j=%g;' %(i,j),'number of depth points inside:',int(count_p[i,j]), 'polygon area', round((PolygonArea(poly_cartesian))/1000000,1), 'km', 'Width:', round((Width(poly_cartesian))/1000,1), 'Height:', round((Height(poly_cartesian))/1000,1), 'Aspect:', round((Width(poly_cartesian)/Height(poly_cartesian)),2)

for i in range(len(depth)):
	for j in range(len(depth.T)):
		if count_p[i,j]>0:
			depth[i,j]=depth[i,j]/count_p[i,j]
		else:
			pass

for i in range(len(depth)):
	for j in range(len(depth.T)):
		if count_p[i,j]==0 and j<len(depth.T)-1 and i<len(depth)-1:
			depth[i,j]=(depth[i,j-1]+depth[i,j+1]+depth[i-1,j]+depth[i+1,j])/4.
		elif count_p[i,j]==0 and j==len(depth.T)-1 and i<len(depth)-1:
			depth[i,j]=(depth[i,j-1]+depth[i-1,j]+depth[i+1,j])/3.
		elif count_p[i,j]==0 and j<len(depth.T)-1 and i==len(depth)-1:
			depth[i,j]=(depth[i,j-1]+depth[i,j+1]+depth[i-1,j])/3.
		elif count_p[i,j]==0 and j==len(depth.T)-1 and i==len(depth)-1:
			depth[i,j]=(depth[i,j-1]+depth[i-1,j])/2.
		else:
			pass
		#print 'i', i, 'j', j, 'depth', round(depth[i,j],2)

#map.scatter(hgrd.x_rho,hgrd.y_rho,count_p)


print 'insure that depth is always deeper than hmin'
depth = pyroms_toolbox.change(depth, '<', hmin, hmin)

print 'set depth to hmin where masked'
idx = np.where(hgrd.mask_rho == 0)
depth[idx] = hmin

print 'save raw bathymetry'
hraw = depth.copy()

print 'check bathymetry roughness'
RoughMat = bathy_tools.RoughnessMatrix(depth, hgrd.mask_rho)
print 'Max Roughness value is: ', RoughMat.max()

print 'smooth the raw bathy using the direct iterative method from Martinho and Batteen (2006)'
rx0_max = 0.35
depth = bathy_smoothing.smoothing_Positive_rx0(hgrd.mask_rho, depth, rx0_max)

print 'check bathymetry roughness again'
RoughMat = bathy_tools.RoughnessMatrix(depth, hgrd.mask_rho)
print 'Max Roughness value is: ', RoughMat.max()

for i in range(Mp+2):
	for j in range(Lp+2):
		if depth[i,j]==2:
			hgrd.mask_rho[i,j]=0


print 'vertical coordinate'
theta_b = 0.1
theta_s = 3
Vtransform=2
Vstretching=4
Tcline=10
N = 5
vgrd = pyroms.vgrid.s_coordinate_4(depth, theta_b, theta_s, Tcline, N, hraw=hraw)

print 'ROMS grid'
grd_name = 'EUROPE'
grd = pyroms.grid.ROMS_Grid(grd_name, hgrd, vgrd)

print 'write grid to netcdf file'
pyroms.grid.write_ROMS_grid(grd, filename='dst_grd_spherical.nc')

