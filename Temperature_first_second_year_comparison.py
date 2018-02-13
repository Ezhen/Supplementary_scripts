from pylab import *; from netCDF4 import *

def Area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

rr = Dataset('/home/eivanov/COAWST/Data/ROMS/Grid/Coarsest_improved.nc', 'r', format='NETCDF3')
y_vert = rr.variables['y_vert'][:]; x_vert = rr.variables['x_vert'][:]
Cs_w = rr.variables['Cs_w'][:]; h = rr.variables['h'][:]; 
mask = rr.variables['mask_rho'][:]
rr.close()

area=np.zeros((len(y_vert)-1,len(y_vert.T)-1)); volume=np.zeros((len(Cs_w)-1,len(y_vert)-1,len(y_vert.T)-1))
for i in range(len(y_vert)-1):
	for j in range(len(x_vert.T)-1):
		poly_cartesian=[(y_vert[i,j],x_vert[i,j]),(y_vert[i,j+1],x_vert[i,j+1]),(y_vert[i+1,j+1],x_vert[i+1,j+1]),(y_vert[i+1,j],x_vert[i+1,j])]
		area[i,j]=round(Area(poly_cartesian))
		for k in range(len(Cs_w)-1):
			volume[k,i,j]=area[i,j]*h[i,j]*(Cs_w[k+1]-Cs_w[k])

volume=volume/10**12
print 'Volume is calculated in km3'

temp_avg=np.zeros((10,364*2))
for m in range(0,2):
	ncdata = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/RESULTS/ocean_avg_tides%s.nc' %(m+1), 'r', format='NETCDF3')
	t = ncdata.variables['ocean_time'][:]
	for p in range(len(t)):
		a=0;b=0
		temp=ncdata.variables['temp'][p,:,:,:]
		for i in range(len(volume[0,:,0])):
			for j in range(len(volume[0,0,:])):
				if mask[i,j]==1:
					for k in range(len(volume[:,0,0])):
						a=a+temp[k,i,j]*volume[k,i,j]
						b=b+volume[k,i,j]
		a=a/b
		print m+1,a
		temp_avg[m,p]=a

ncdata.close()

xlim(0,364); ylim(temp_avg.min(),temp_avg.max())
for m in range(len(temp_avg[:,0])):
	plot(temp_avg[m,0:364],label='year %s' %(m+1))
	plot(temp_avg[m,364:728],label='year %s' %(m+2))
legend(loc=2)


