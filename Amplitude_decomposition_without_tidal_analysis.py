from netCDF4 import Dataset; import numpy as np

rr = Dataset('M2_tide.nc', 'r', format='NETCDF4')
lats = rr.variables['lat_rho'][:]; lons = rr.variables['lon_rho'][:]; z=np.copy(rr.variables['zeta'][1,:,:])
for i in range(len(rr.variables['zeta'][0,:,0])):
	for j in range(len(rr.variables['zeta'][0,0,:].T)):
		mx=[];mn=[]
		for k in range(len(rr.variables['zeta'][0])-2):
			if rr.variables['zeta'][k+1,i,j]>rr.variables['zeta'][k,i,j] and rr.variables['zeta'][k+1,i,j]>rr.variables['zeta'][k+2,i,j]:
				mx.append(rr.variables['zeta'][k+1,i,j])
			elif rr.variables['zeta'][k+1,i,j]<rr.variables['zeta'][k,i,j] and rr.variables['zeta'][k+1,i,j]<rr.variables['zeta'][k+2,i,j]:
				mn.append(rr.variables['zeta'][k+1,i,j])
		z[i,j]=(np.mean(mx)-np.mean(mn))/2.; print i,j,z[i,j]

nc = Dataset('M2.nc', 'w', format='NETCDF4')
nc.createDimension('eta', len(lats));nc.createDimension('xi',len(lats.T));nc.createVariable('lat', 'f4', ( 'eta','xi'));nc.createVariable('lon', 'f4', ( 'eta', 'xi'));nc.createVariable('M2', 'f4', ( 'eta', 'xi'))
nc.variables['lat'][:]=lats; nc.variables['lon'][:]=lons
nc.variables['M2'][:]=z
nc.close()

