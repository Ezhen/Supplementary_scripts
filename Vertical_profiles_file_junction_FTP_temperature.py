import os
import subprocess
import commands
import _iso
from netCDF4 import Dataset
from nco import Nco
import datetime
import numpy as np
from numpy import *
from functools import partial

dnsdatetime2py = lambda x: datetime.datetime(1950,1,1,0,0,0) + datetime.timedelta(days=x)
dn = lambda x: datetime.datetime(2013,1,1,0,0,0) + datetime.timedelta(seconds=x)

source = Dataset('/media/sf_Swap-between-windows-linux/ocean_his_2013.nc', 'r', format='NETCDF3')
lat_rho = source.variables['lat_rho'][:]
lon_rho = source.variables['lon_rho'][:]
octi = source.variables['ocean_time'][:]
s_rho = source.variables['s_rho'][:]
h = source.variables['h'][:]

time=np.zeros((4,len(octi)))
for c in range(len(octi)):
	time[0,c]=dn(octi[c]).year
	time[1,c]=dn(octi[c]).month
	time[2,c]=dn(octi[c]).day
	time[3,c]=dn(octi[c]).hour

a=[]
for d in range(len(np.hstack(lat_rho))):
	a.append((np.hstack(lat_rho)[d],np.hstack(lon_rho)[d]))
a=np.array(a)

def find_closest_coordinate_source(la,lo,a):
	dist=lambda s,d: (s[0]-d[0])**2+(s[1]-d[1])**2
	coord=(la,lo)
	return(min(a, key=partial(dist, coord)))


def make_analysis_1(la,lo,ye,mo,da,ho):
	lat,lon=find_closest_coordinate_source(la,lo,a)
	bb,cc=where(lat_rho==lat)
	lat=bb[0];lon=cc[0]
	yy = where(time[0,:]==ye)
	mm = where(time[1,yy[0][0]:yy[0][-1]]==mo)
	dd = where(time[2,mm[0][0]:mm[0][-1]]==da)
	hh = where(time[3,dd[0][0]:dd[0][-1]]==ho)
	if not sum(hh)==0:
		moment = yy[0][0]+mm[0][0]+dd[0][0]+hh[0][0]
	elif not sum(dd)==0:
		moment = yy[0][0]+mm[0][0]+dd[0][0]
	else:
		moment = yy[0][0]+mm[0][0]
	print 'Observation time: %g-%g-%g %g:00:00. Model:' %(ye,mo,da,ho), dn(octi[moment])
	print 'Observation lat-lon: (%g, %g). Model lat-lon: (%g, %g).' %(la,lo,lat_rho[lat,lon],lon_rho[lat,lon])
	temperature = source.variables['temp'][moment,:,lat,lon]
	return temperature

def make_analysis_2(la,lo):
	lat,lon=find_closest_coordinate_source(la,lo,a)
	bb,cc=where(lat_rho==lat)
	lat=bb[0];lon=cc[0]
	h = source.variables['h'][lat,lon]
	return h

def read_netcdf(name,j):
	ncdata = Dataset(name, 'r', format='NETCDF3')
	lat = ncdata.variables['LATITUDE'][:]
	lon = ncdata.variables['LONGITUDE'][:]
	print 'lat:', min(lat), '-', max(lat), 'lon:', min(lon), '-', max(lon)
	t = ncdata.variables['TIME'][:]
	try:
		z = ncdata.variables['DEPH'][:,:]
	except:
		z = ncdata.variables['PRES'][:,:]
	m=0
	print 'data was appended',j, 'shape depth', np.shape(z)
	try:
		temp = ncdata.variables['TEMP'][:,:]
	except:
		ncdata.close()
		print ' No data within the choosen domain'
		return(j)
	for i in range(len(t)):
		if lat[i]>50 and lat[i]<53:
			if lon[i]>0 and lon[i]<6:
				nc.variables['temperature_model'][j+m] = make_analysis_1(lat[i],lon[i],dnsdatetime2py(t[i]).year,dnsdatetime2py(t[i]).month,dnsdatetime2py(t[i]).day,dnsdatetime2py(t[i]).hour)
				nc.variables['depth_GEBCO_interp'][j+m] = make_analysis_2(lat[i],lon[i])
				nc.variables['depth_GEBCO_z'][j+m] = make_analysis_2(lat[i],lon[i])*s_rho
				nc.variables['year'][j+m] = dnsdatetime2py(t[i]).year
				nc.variables['month'][j+m] = dnsdatetime2py(t[i]).month
				nc.variables['day'][j+m] = dnsdatetime2py(t[i]).day
				nc.variables['hour'][j+m] = dnsdatetime2py(t[i]).hour
				nc.variables['minute'][j+m] = dnsdatetime2py(t[i]).minute
				nc.variables['second'][j+m] = dnsdatetime2py(t[i]).second
				nc.variables['latitude'][j+m] = lat[i]
				nc.variables['longitude'][j+m] = lon[i]
				for k in range(len(z.T)):
					if not type(z[i,k])==np.ma.core.MaskedConstant:
						if not type(temp[i,k])==np.ma.core.MaskedConstant:
							nc.variables['depth'][j+m,k] = z[i,k]
							nc.variables['temperature_obs'][j+m,k] = temp[i,k]
				nc.variables['time'][j+m] = t[i]
				m=m+1
	print 'data has been appended at this moment', j+m
	ncdata.close()
	return(j+m)
		
			
				
nc = Dataset('Temperature_comparison_my_vision.nc', 'w', format='NETCDF3_64BIT')
nc.createDimension('record', None)
nc.createDimension('depth', 15)
nc.createDimension('depth_obs', 10000)

nc.createVariable('year', 'f4', ('record'))
nc.variables['year'].long_name = 'year'
nc.variables['year'].units = 'year'

nc.createVariable('month', 'f4', ('record'))
nc.variables['month'].long_name = 'month'
nc.variables['month'].units = 'month'

nc.createVariable('day', 'f4', ('record'))
nc.variables['day'].long_name = 'day'
nc.variables['day'].units = 'day'

nc.createVariable('hour', 'f4', ('record'))
nc.variables['hour'].long_name = 'hour'
nc.variables['hour'].units = 'hour'

nc.createVariable('minute', 'f4', ('record'))
nc.variables['minute'].long_name = 'minute'
nc.variables['minute'].units = 'minute'

nc.createVariable('second', 'f4', ('record'))
nc.variables['second'].long_name = 'second'
nc.variables['second'].units = 'second'

nc.createVariable('latitude', 'f4', ('record'))
nc.variables['latitude'].long_name = 'latitude'
nc.variables['latitude'].units = 'degrees north'

nc.createVariable('longitude', 'f4', ('record'))
nc.variables['longitude'].long_name = 'longitude'
nc.variables['longitude'].units = 'degrees east'
    
nc.createVariable('depth', 'f4', ('record', 'depth_obs'))
nc.variables['depth'].long_name = 'depth'
nc.variables['depth'].units = 'meters'

nc.createVariable('temperature_obs', 'f4', ('record', 'depth_obs'))
nc.variables['temperature_obs'].long_name = 'temperature observed from a vessel'
nc.variables['temperature_obs'].units = 'celcius'

nc.createVariable('time', 'f4', ('record'))
nc.variables['time'].long_name = 'time'
nc.variables['time'].units = 'days'

nc.createVariable('temperature_model', 'f4', ('record', 'depth'))
nc.variables['temperature_model'].long_name = 'temperature modelled'
nc.variables['temperature_model'].units = 'celcius'

nc.createVariable('depth_GEBCO_z', 'f4', ('record', 'depth'))
nc.variables['depth_GEBCO_z'].long_name = 'depth from GEBCO for temperature'
nc.variables['depth_GEBCO_z'].units = 'meters'

nc.createVariable('depth_GEBCO_interp', 'f4', ('record'))
nc.variables['depth_GEBCO_interp'].long_name = 'depth from GEBCO interpolated'
nc.variables['depth_GEBCO_interp'].units = 'meters'



path='/home/eivanov/coawst_data_prrocessing/VERIFICATION_PROFILES/Vessel/'
m=0; jj=0
for file in os.listdir(path):
	current_file = os.path.join(path, file)
	print '%g) Processing:' %(jj+1), current_file
	mm=read_netcdf(current_file,m)
	m=mm; jj=jj+1

nc.close()
