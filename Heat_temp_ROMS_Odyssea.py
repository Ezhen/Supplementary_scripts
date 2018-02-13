from pylab import *; import numpy as np; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; from mpl_toolkits.basemap import Basemap; import sys,os,shutil; import matplotlib.gridspec as gridspec; import re; from scipy import spatial; lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(days=x)#; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman')
lo2 = lambda x: datetime(2004,1,1,0,0,0) + timedelta(seconds=x); mintemp=-50; maxtemp=50; folder = os.path.abspath("Heat"); from mpl_toolkits.axes_grid1 import make_axes_locatable

nc1 = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/ROMS_REPLOTTED_METEO.nc', 'r', format='NETCDF4')
lats = nc1.variables['lat'][::-1]; lons = nc1.variables['lon'][:]; lons_p,lats_p=np.meshgrid(lons,lats); msk2 = flipud(nc1.variables['sst'][0,:,:]);maska=np.zeros((np.shape(msk2)[0],np.shape(msk2)[1]))
ncdata2 = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo_Climatology/Meteo_2004_all_improved.nc', 'r', format='NETCDF4')
ff = Dataset('/media/sf_Swap-between-windows-linux/Climatology_Meteo.nc', 'r', format='NETCDF3'); msk = flipud(ff.variables['sst'][0,:,:]); ff.close()
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) == np.ma.core.MaskedConstant or msk2[i,j] < 0.001 or j<11:
			maska[i,j]=1

#for i in range(365):
#		w2=flipud(ncdata2.variables['sst'][i,:,:])-273.15; w1=flipud(nc1.variables['sst'][i,:,:]); a=w1-w2;a=np.ma.masked_where(maska==1, a); print i,a.min(),a.max()

def PRINT(a1,a2):
	fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 16));plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, wspace=0.1) 
	ax1 = plt.subplot2grid((1,2), (0,0))
	ax2 = plt.subplot2grid((1,2), (0,1))
	m1 = Basemap(projection='merc',llcrnrlat=49,urcrnrlat=55,llcrnrlon=-3,urcrnrlon=6,lat_ts=51.5,resolution='i', ax=ax1)
	m2 = Basemap(projection='merc',llcrnrlat=49,urcrnrlat=55,llcrnrlon=-3,urcrnrlon=6,lat_ts=51.5,resolution='i', ax=ax2)
	y_bcz=array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361]); x_bcz=array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
	m1.drawparallels(arange(49,55,0.5),labels=[1,0,0,1],fontsize=10); m1.drawmeridians(arange(-3,6,0.5),labels=[1,1,1,0],fontsize=10); m1.drawcoastlines(); m1.drawmapboundary(fill_color='#9999FF')
	m2.drawparallels(arange(49,55,0.5),labels=[1,0,0,1],fontsize=10); m2.drawmeridians(arange(-3,6,0.5),labels=[1,1,1,0],fontsize=10); m2.drawcoastlines(); m2.drawmapboundary(fill_color='#9999FF')
	x4, y4 = m1(x_bcz, y_bcz); cs43 = m1.plot(x4,y4,color='black',linewidth=1.0); x5, y5 = m2(x_bcz, y_bcz); cs45 = m2.plot(x5,y5,color='black',linewidth=1.0)
	x1, y1 = m1(lons_p, lats_p); cax = make_axes_locatable(ax1).append_axes("bottom", size=0.4, pad=0.15); norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp); mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.RdBu_r, norm=norm, orientation='horizontal'); nx2 = int((m1.xmax-m1.xmin)/3000.)+1; ny2 = int((m1.ymax-m1.ymin)/3000.)+1
	for n in range(a1,a2):
		w2=np.matrix(np.sum(ncdata2.variables['str'][n*8:n*8+8,:,:],axis=0))/8; w1=np.matrix(np.sum(nc1.variables['lwr'][n*24:n*24+24,:,:],axis=0))/24
		print np.shape(w2), np.shape(w1)
		a=w1-w2; a=flipud(a);a=np.ma.masked_where(maska==1, a)
		tempo2 = m1.transform_scalar(a,lons,lats,nx2,ny2);CS3 = m1.imshow(tempo2,mpl.cm.RdBu_r,vmin=mintemp,vmax=maxtemp); clevs = np.arange(mintemp,maxtemp,0.1)
		m1.drawcountries(); m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
		b=np.matrix(np.sum(ncdata2.variables['t2m'][n*8:n*8+8,:,:],axis=0))/8; b=flipud(b); print np.shape(b)
		tempo3 = m2.transform_scalar(b,lons,lats,nx2,ny2);CS3 = m2.imshow(tempo3,mpl.cm.RdBu_r,vmin=0,vmax=20); clevs = np.arange(0,20,0.5)
		lol=ax2.annotate('%s' %(str(lo2(int(n*60*60*24)))[0:10]), xy=(0,0),  xycoords='data',xytext=(x1[10,60], y1[10,60]), family='Courier New, monospace',textcoords='data',fontsize=20, bbox=dict(facecolor='none', edgecolor='none', pad=5.0)); print n
		file_name = os.path.abspath(folder + "/tmp%s" %(n)+".png"); fig.savefig(file_name, dpi=200); lol.remove()

for i in range(0,1):
	PRINT(10*i,10*i+10)
#PRINT(360,365)


