from pylab import *
from netCDF4 import Dataset
import pyroms
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.mlab import griddata
import scipy
import pyroms
import pyroms_toolbox
from bathy_smoother import *
import netCDF4
from shapely.geometry import Polygon


grd=pyroms.grid.get_ROMS_grid('BCZ')

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

def Area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

def Angle(corners):			
	lb=(((corners[1][0]-corners[0][0])**2)+((corners[1][1]-corners[0][1])**2))**0.5
	ub=(((corners[2][0]-corners[1][0])**2)+((corners[2][1]-corners[1][1])**2))**0.5
	cb=(((corners[2][0]-corners[0][0])**2)+((corners[2][1]-corners[0][1])**2))**0.5
	frac_up=cb*cb-lb*lb-ub*ub
	frac_down=2*lb*ub
	alpha1=np.math.acos(-frac_up/frac_down)
	alpha1=np.math.fabs(90-np.math.degrees(alpha1))
	lb=(((corners[2][0]-corners[1][0])**2)+((corners[2][1]-corners[1][1])**2))**0.5
	ub=(((corners[3][0]-corners[2][0])**2)+((corners[3][1]-corners[2][1])**2))**0.5
	cb=(((corners[3][0]-corners[1][0])**2)+((corners[3][1]-corners[1][1])**2))**0.5
	frac_up=cb*cb-lb*lb-ub*ub
	frac_down=2*lb*ub
	alpha2=np.math.acos(-frac_up/frac_down)
	alpha2=np.math.fabs(90-np.math.degrees(alpha2))
	lb=(((corners[3][0]-corners[2][0])**2)+((corners[3][1]-corners[2][1])**2))**0.5
	ub=(((corners[0][0]-corners[3][0])**2)+((corners[0][1]-corners[3][1])**2))**0.5
	cb=(((corners[0][0]-corners[2][0])**2)+((corners[0][1]-corners[2][1])**2))**0.5
	frac_up=cb*cb-lb*lb-ub*ub
	frac_down=2*lb*ub
	alpha3=np.math.acos(-frac_up/frac_down)
	alpha3=np.math.fabs(90-np.math.degrees(alpha3))
	lb=(((corners[0][0]-corners[3][0])**2)+((corners[0][1]-corners[3][1])**2))**0.5
	ub=(((corners[1][0]-corners[0][0])**2)+((corners[1][1]-corners[0][1])**2))**0.5
	cb=(((corners[1][0]-corners[3][0])**2)+((corners[1][1]-corners[3][1])**2))**0.5
	frac_up=cb*cb-lb*lb-ub*ub
	frac_down=2*lb*ub
	alpha4=np.math.acos(-frac_up/frac_down)
	alpha4=np.math.fabs(90-np.math.degrees(alpha4))
	alpha=(alpha1+alpha2+alpha3+alpha4)/4.
	return alpha

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
	
	
count_p=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
depth=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
aspect=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
angle=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
area=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
area_sq=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
width1=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))
height1=np.zeros((len(grd.hgrid.lat_vert)-1,len(grd.hgrid.lon_vert.T)-1))

for i in range(len(grd.hgrid.lat_vert)-1):
	for j in range(len(grd.hgrid.lon_vert.T)-1):
		poly=[(grd.hgrid.lat_vert[i,j],grd.hgrid.lon_vert[i,j]),(grd.hgrid.lat_vert[i,j+1],grd.hgrid.lon_vert[i,j+1]),(grd.hgrid.lat_vert[i+1,j+1],grd.hgrid.lon_vert[i+1,j+1]),(grd.hgrid.lat_vert[i+1,j],grd.hgrid.lon_vert[i+1,j])]
		poly_cartesian=[(grd.hgrid.y_vert[i,j],grd.hgrid.x_vert[i,j]),(grd.hgrid.y_vert[i,j+1],grd.hgrid.x_vert[i,j+1]),(grd.hgrid.y_vert[i+1,j+1],grd.hgrid.x_vert[i+1,j+1]),(grd.hgrid.y_vert[i+1,j],grd.hgrid.x_vert[i+1,j])]
		width1[i,j]=Width(poly_cartesian)/1000
		height1[i,j]=Height(poly_cartesian)/1000
		aspect[i,j]=round((width1[i,j]/height1[i,j]),2)
		#angle[i,j]=round((Angle(poly_cartesian)),2)
		#area[i,j]=round(Area(poly_cartesian)/1000000,0)

def in_circle(center_x, center_y, radius, x, y):		#	verification if the topo point is inside a sphere
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2





fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))

plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, wspace=0.1)
plt.suptitle('Depth',family='Courier New, monospace',fontsize=20, y=0.88)
ax1 = plt.subplot2grid((1,2), (0,0))
ax2 = plt.subplot2grid((1,2), (0,1))
m1 = Basemap(projection='merc',llcrnrlat=50,urcrnrlat=53.0,llcrnrlon=0,urcrnrlon=5,lat_ts=51.5,resolution='h', ax=ax1)

y_bcz=array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361])
x_bcz=array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])

m2 = Basemap(projection='merc', llcrnrlat=51,urcrnrlat=51.9,llcrnrlon=2.0,urcrnrlon=3.5,lat_ts=51.45, resolution='f', ax=ax2)

m1.drawparallels(arange(50,53,1),labels=[1,0,0,1],fontsize=10)
m1.drawmeridians(arange(0,5,1),labels=[1,0,1,0,1,0],fontsize=10)
#m1.drawmapboundary()
m1.drawcountries()
m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
m2.drawparallels(arange(51.0,51.9,0.3),labels=[1,0,0,0],fontsize=10)
m2.drawmeridians(arange(2,3.5,0.5),labels=[1,0,0,1],fontsize=10)
#m2.drawmapboundary()
m2.drawcountries()
m2.fillcontinents(color='#ddaa66',lake_color='#9999FF')

x3, y3 = m1(x_bcz, y_bcz)

x4, y4 = m2(x_bcz, y_bcz)



#m1.drawmapboundary(fill_color='#9999FF')
#m2.drawmapboundary(fill_color='#9999FF')



"""
lon1, lat1 = m1(grd.hgrid.lon_vert, grd.hgrid.lat_vert)

lon2, lat2 = m2(grd.hgrid.lon_vert, grd.hgrid.lat_vert)

ax1.plot(lon1,lat1, '-k')
ax1.plot(lon1.T,lat1.T, '-k')

ax2.plot(lon2,lat2, '-k')
ax2.plot(lon2.T,lat2.T, '-k')

"""

m1.drawmapboundary(fill_color='aqua')
m1.fillcontinents(color='coral',lake_color='aqua')
m1.drawcountries(linewidth=0.25)
m2.drawmapboundary(fill_color='aqua')
m2.fillcontinents(color='coral',lake_color='aqua')
m2.drawcountries(linewidth=0.25)

def g(b,mini,maxi):
	if b<mini:
		c=0.001
	elif b>maxi:
		c=0.999
	else:
		c=(b-mini)/(maxi-mini)
	return c


Blues = plt.get_cmap('Blues')


for i in range(len(grd.hgrid.x)-1):
	for j in range(len(grd.hgrid.x.T)-1):
		#t=g(area[i,j],10,13000)
		#t=g(width1[i,j],0.1,0.9)
		#t=g(aspect[i,j],0.8,1.2)		
		#t=g(count_p[i,j],1,100)		
		#t=g(angle[i,j], 0.01, 10)
		#t=g(depth[i,j]-hraw[i,j],0.0,0.2)
		if grd.hgrid.mask_rho[i,j]==1:
			t=g(grd.vgrid.h[i,j],0,55)
			#xy=np.array([[grd.hgrid.x[i,j],grd.hgrid.y[i,j]], [grd.hgrid.x[i,j+1],grd.hgrid.y[i,j+1]], [grd.hgrid.x[i+1,j+1],grd.hgrid.y[i+1,j+1]], [grd.hgrid.x[i+1,j],grd.hgrid.y[i+1,j]],[grd.hgrid.x[i,j],grd.hgrid.y[i,j]]])
			xy=np.array([[grd.hgrid.lon[i,j],grd.hgrid.lat[i,j]], [grd.hgrid.lon[i,j+1],grd.hgrid.lat[i,j+1]], [grd.hgrid.lon[i+1,j+1],grd.hgrid.lat[i+1,j+1]], [grd.hgrid.lon[i+1,j],grd.hgrid.lat[i+1,j]],[grd.hgrid.lon[i,j],grd.hgrid.lat[i,j]]])
			x1,y1=m1(xy[:,0],xy[:,1])
			x2,y2=m2(xy[:,0],xy[:,1])
			xy=np.array((x1,y1)).T
			xy2=np.array((x2,y2)).T
			poly = mpl.patches.Polygon(xy,  closed=True, facecolor=Blues(t), edgecolor='none') #, edgecolor='none'
			poly2 = mpl.patches.Polygon(xy2,  closed=True, facecolor=Blues(t), edgecolor='none')
			ax1.add_patch(poly)
			ax2.add_patch(poly2)

cs33 = m1.plot(x3,y3,color='black',linewidth=1.0)
cs43 = m2.plot(x4,y4,color='black',linewidth=1.0)

norm = mpl.colors.Normalize(vmin=0, vmax=55)
cax = fig.add_axes([0.37, 0.05, 0.3, 0.02])
cbb = mpl.colorbar.ColorbarBase(cax, cmap=Blues, norm=norm, orientation='horizontal')
cbb.set_label('m')

show()
