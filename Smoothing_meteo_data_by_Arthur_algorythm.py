"""
Script averages data over dataset to make "climatological forcing file".
Created by Evgeny Ivanov on 11/04/2016
"""

import datetime # Python standard library datetime  module
from numpy import *
from netCDF4 import Dataset


# Good function to import variables and dimensions from netcdf file
def ncdump(nc_fid, verb=True):
    '''
    ncdump outputs dimensions, variables and their attribute information.
    The information is similar to that of NCAR's ncdump utility.
    ncdump requires a valid instance of Dataset.

    Parameters
    ----------
    nc_fid : netCDF4.Dataset
        A netCDF4 dateset object
    verb : Boolean
        whether or not nc_attrs, nc_dims, and nc_vars are printed

    Returns
    -------
    nc_attrs : list
        A Python list of the NetCDF file global attributes
    nc_dims : list
        A Python list of the NetCDF file dimensions
    nc_vars : list
        A Python list of the NetCDF file variables
    '''
    def print_ncattr(key):
        """
        Prints the NetCDF file attributes for a given key

        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print "\t\ttype:", repr(nc_fid.variables[key].dtype)
            for ncattr in nc_fid.variables[key].ncattrs():
                print '\t\t%s:' % ncattr,\
                      repr(nc_fid.variables[key].getncattr(ncattr))
        except KeyError:
            print "\t\tWARNING: %s does not contain variable attributes" % key

    # NetCDF global attributes
    nc_attrs = nc_fid.ncattrs()
    if verb:
        print "NetCDF Global Attributes:"
        for nc_attr in nc_attrs:
            print '\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr))
    nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
    # Dimension shape information.
    if verb:
        print "NetCDF dimension information:"
        for dim in nc_dims:
            print "\tName:", dim 
            print "\t\tsize:", len(nc_fid.dimensions[dim])
            print_ncattr(dim)
    # Variable information.
    nc_vars = [var for var in nc_fid.variables]  # list of nc variables
    if verb:
        print "NetCDF variable information:"
        for var in nc_vars:
            if var not in nc_dims:
                print '\tName:', var
                print "\t\tdimensions:", nc_fid.variables[var].dimensions
                print "\t\tsize:", nc_fid.variables[var].size
                print_ncattr(var)
    return nc_attrs, nc_dims, nc_vars

nc_f = './Meteo_2000_2010.nc'  	# Your filename
nc_fid = Dataset(nc_f, 'r')  	# Dataset is the class behavior to open the file
                             	# and create an instance of the ncCDF4 class
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)


# import of latitude, longitude, time and some f physical parameter of the particular interest

x = nc_fid.variables['latitude'][:] 	 # extract/copy the data
y = nc_fid.variables['longitude'][:]
t = nc_fid.variables['time'][:]
#sst = nc_fid.variables['sst'][:]	# for simplification of the script, any of physical parameters has to be imported as "sst" variables
#sst = nc_fid.variables['sp'][:]
#tcc = nc_fid.variables['tcc'][:]
#u10 = nc_fid.variables['u10'][:]
sst = nc_fid.variables['v10'][:]
#sst = nc_fid.variables['t2m'][:]
#sst = nc_fid.variables['d2m'][:]

#var=['sst','sp','tcc','u10','v10','t2m','d2m']
#desc=['Sea surface temperature','Air pressure', 'Total cLoud clover', 'Wind u-component', 'Wind v-component', 'Air temperature', 'Dew temperature']
#dim=['K','Pa','0-1','m*s-1','m*s-1','K','K']

dnsdatetime2py = lambda x: datetime.datetime(1900,1,1,0,0,0) + datetime.timedelta(hours=x)	# conversion of ESMWF time int normal time

sst_av = array([[[0.001]*int(len(y))]*int(len(x))]*int(len(t))) 	# creation of an array for averaged sea-surface temperature
sst_diff = array([[[0.001]*int(len(y))]*int(len(x))]*int(len(t)))	# and some additional arrays which will be needed during the processing
sst_clim = array([[[0.001]*int(len(y))]*int(len(x))]*1461)
sst_forc = array([[[0.001]*int(len(y))]*int(len(x))]*1461)


# LOWFREQ: moving average. Smoothes data through the time by thier averaging. The size of moving window is 15 time steps (4 days)
def lowfreq():
	for j in range(len(x)):
		for k in range(len(y)):
			for i in range(len(t)):
				if i<len(t)-15:
					sst_av[i,j,k]=sum(sst[i:i+15,j,k])/15.
				else:
					sst_av[i,j,k]=sst_av[i-1,j,k]
				#print "lat:", x[j], "  lon:", y[k], "  time:", dnsdatetime2py(int(t[i])), " sst:", round(sst[i,j,k]-273.15,2), "  smothed sst:", round(sst_av[i,j,k]-273.15,2)
	print "done!"
	return sst_av

# HIGHFREQ: getting of the difference between LOWFREQ and real data at the each time moment

def highfreq():
	for j in range(len(x)):
		for k in range(len(y)):
			for i in range(len(t)-15):
				sst_diff[i+7,j,k]=sst[i+7,j,k]-sst_av[i,j,k]
			for i in range(0,7):
				sst_diff[i,j,k]=sst_diff[10,j,k]
			for i in range(len(t)-8,len(t)):
				sst_diff[i,j,k]=sst_diff[-10,j,k]
			#print "lat:", x[j], "  lon:", y[k], "  time:", dnsdatetime2py(int(t[i])), "  smothed sst:", round(sst_av[i,j,k]-273.15,2), " diff:", round(sst_diff[i,j,k],2)
	print "done!"
	return sst_diff
		

# LOWFREQ_CLIM: averaging of LOWFREQ through years
def lowfreq_clim():
	m=0
	for j in range(len(x)):
		for k in range(len(y)):
			for i in range(len(t)):
				if dnsdatetime2py(int(t[i])).month==2 and dnsdatetime2py(int(t[i])).day==29:
					pass
				else:
					if m<1460:
						sst_clim[m,j,k]=(sst_clim[m,j,k]+sst_av[i,j,k])
						m=m+1
						#print "lat:",x[j], "  lon:", y[k],  "  time:", dnsdatetime2py(int(t[i])), "  sst_clim:", round(sst_clim[m,j,k]), "  m:", m 
					else:
						m=0
	print "done!"
	return sst_clim

				

# FORCING: adding of HIGHFREQ to LOWFREQ_CLIM  for getting some fluctuations. Then - duplication of this year  throgh the dataset. After that, forcing time series is created
def forcing():
	for j in range(len(x)):
		for k in range(len(y)):
			for i in range(len(sst_clim)):
				sst_forc[i,j,k]=sst_clim[i,j,k]/11.+sst_diff[7300+i,j,k]
				#print "lat:",x[j], "  lon:", y[k],  "  time:", dnsdatetime2py(int(t[i])), "  sst_forc:", round(sst_forc[i,j,k],2)
	sst_f = array([[[0.001]*int(len(y))]*int(len(x))]*int(len(t)))
	mmm=0				
	for j in range(len(x)):
		for k in range(len(y)):
			for i in range(len(t)):
				if dnsdatetime2py(int(t[i])).year==2000 and dnsdatetime2py(int(t[i])).month==2 and dnsdatetime2py(int(t[i])).day==29 or dnsdatetime2py(int(t[i])).year==2004 and dnsdatetime2py(int(t[i])).month==2 and dnsdatetime2py(int(t[i])).day==29 or dnsdatetime2py(int(t[i])).year==2008 and dnsdatetime2py(int(t[i])).month==2 and dnsdatetime2py(int(t[i])).day==29:
					sst_f[i,j,k]=sst_forc[mmm-1,j,k]
					#print "lat:",x[j], "  lon:", y[k],  "  time:", dnsdatetime2py(int(t[i])), "  sst_f:", round(sst_f[i,j,k],2), "  m:", mmm
				else: 
					sst_f[i,j,k]=sst_forc[mmm,j,k]
					mmm=mmm+1
					#print "lat:",x[j], "  lon:", y[k],  "  time:", dnsdatetime2py(int(t[i])), "  sst_f:", round(sst_f[i,j,k],2), "  m:", mmm
					if mmm==1460:
						mmm=0
	print "done!"
	return sst_f


# Calling of functions we needed
"""
sst_av = lowfreq()
sst_diff = highfreq()
sst_clim = lowfreq_clim()
sst_f = forcing()
sst_av=sst_f
sst_av=lowfreq()
sst_f = sst_av
	

#nc_fid.close()


# Writing of netcdf file with coordinates, time and averaged parameter.

test = Dataset('v10.nc', 'w', format='NETCDF4')
time = test.createDimension('time', len(t))
lat = test.createDimension('lat', len(x))
lon = test.createDimension('lon', len(y))
times = test.createVariable('time','i4',('time',))
lats = test.createVariable('latitude','f4',('lat',))
lons = test.createVariable('longitude','f4',('lon',))
v10 = test.createVariable('v10','f8',('time','lat','lon',))
times[:] = t
lats[:] = x
lons[:] = y
v10[:,:,:] = sst_f
test.close()
"""
