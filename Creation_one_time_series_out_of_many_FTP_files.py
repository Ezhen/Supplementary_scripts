import numpy as np; from netCDF4 import Dataset; import os; import datetime

path='FTP_Verification/' #dn = lambda x: datetime.datetime(1981,1,1,0,0,0) + datetime.timedelta(seconds=x); 

rr = Dataset('FTP_Verification/20040101000000-IFR-L4_GHRSST-SST-ODYSSEA-NWS_004-v2.0-fv1.0.nc', 'r', format='NETCDF4')
x = rr.variables['lat'][301:348]	# 253-406 - bigger area (48.5-54.9); 301-348 - smaller area (50.5-52.5);
y = rr.variables['lon'][445:521]	# 330-593 - bigger area (-4.3-6.7); 445-542 - smaller area (0.5-3.7);
rr.close()

ftp = Dataset('Validation_FTP.nc', 'w', format='NETCDF4')
ftp.createDimension('lat', len(x)); ftp.createDimension('lon', len(y))
time = ftp.createDimension('time', 3288) # a number of iles inside of the folder

ftp.createVariable('time','f',('time',))
ftp.createVariable('lat','f',('lat',)); ftp.createVariable('lon','f',('lon',))
ftp.createVariable('sst','f',('time','lat','lon'))
ftp.variables['lat'][:] = x; ftp.variables['lon'][:] = y

j=0
for file in sorted(os.listdir(path)):
	rr = Dataset(path+file, 'r', format='NETCDF4')
	ftp.variables['time'][j] = rr.variables['time'][:]
	ftp.variables['sst'][j] = rr.variables['analysed_sst'][:,301:348,445:521]; j=j+1
	print j, 'file', file, 'is proceeded'
	rr.close()

ftp.close()



