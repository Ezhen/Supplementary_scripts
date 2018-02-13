from pylab import *; import numpy as np; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; from mpl_toolkits.basemap import Basemap; import sys,os,shutil; import matplotlib.gridspec as gridspec; import re; from scipy import spatial; lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(days=x)#; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman')
lo2 = lambda x: datetime(2004,1,1,0,0,0) + timedelta(seconds=x); from mpl_toolkits.axes_grid1 import make_axes_locatable; from shiftedColorMap import shiftedColorMap

vv=[['swrad','ssr'],['lwr','str'],['sensible','sshf'],['latent','slhf']]; d1=[56,191,328]; temprange=[[-5,5],[-30,20],[-70,30],[-70,50]]

nc1 = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/CLOUDS_Fluxes_Replotted.nc', 'r', format='NETCDF4')
lats = nc1.variables['lat'][::-1]; lons = nc1.variables['lon'][:]; lons_p,lats_p=np.meshgrid(lons,lats); msk2 = flipud(nc1.variables['swrad'][0,:,:]);maska=np.zeros((np.shape(msk2)[0],np.shape(msk2)[1]))
ncdata2 = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo_Climatology/Meteo_2004_all_improved.nc', 'r', format='NETCDF4')
ff = Dataset('/media/sf_Swap-between-windows-linux/Climatology_Meteo.nc', 'r', format='NETCDF3'); msk = flipud(ff.variables['sst'][0,:,:]);  ff.close()
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) == np.ma.core.MaskedConstant or msk2[i,j] == 0 :
			maska[i,j]=1

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10)); m1 = Basemap(projection='merc',llcrnrlat=49,urcrnrlat=55,llcrnrlon=-3,urcrnrlon=6,lat_ts=51.5,resolution='i', ax=ax)
y_bcz=array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361]); x_bcz=array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
m1.drawparallels(arange(49,55,0.5),labels=[1,0,0,1],fontsize=10); m1.drawmeridians(arange(-3,6,0.5),labels=[1,1,1,0],fontsize=10); m1.drawcoastlines(); m1.drawmapboundary(fill_color='#9999FF')
x4, y4 = m1(x_bcz, y_bcz); cs43 = m1.plot(x4,y4,color='black',linewidth=1.0); a=np.zeros((np.shape(msk2)[0],np.shape(msk2)[1])); x1, y1 = m1(lons_p, lats_p); cax = make_axes_locatable(ax).append_axes("bottom", size=0.4, pad=0.15); 

number=1	# choose a pair of fluxes ROMS - ECMWF
for k in range(0,2):
	w1=np.zeros((np.shape(msk2)[0],np.shape(msk2)[1])); w2=np.zeros((np.shape(msk2)[0],np.shape(msk2)[1]))
	for i in range(len(msk)):
		print i
		for j in range(len(msk.T)):
			w2[i,j]=np.sum(ncdata2.variables[vv[number][1]][d1[0+k]*8:d1[1+k]*8,i,j])/len(range(d1[0+k]*8,d1[1+k]*8))	#Odyssea time range 1
			w1[i,j]=np.sum(nc1.variables[vv[number][0]][d1[0+k]:d1[1+k],i,j])/len(range(d1[0+k],d1[1+k]));			#ROMS time range 1
	w=w1-w2; w=flipud(w); w=np.ma.masked_where(maska==1, w)
	#mintemp=np.round(w.min(),-1); maxtemp=np.round(w.max(),-1); 
	mintemp=temprange[number][0];maxtemp=temprange[number][1]
	midpt=1-maxtemp/(float(maxtemp)+abs(mintemp))
	v = range(mintemp,maxtemp+10,10)
	shifted_cmap=shiftedColorMap(cmap=mpl.cm.RdBu_r, midpoint=midpt, name='shifted')
	#norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp); 
	nx2 = int((m1.xmax-m1.xmin)/3000.)+1; ny2 = int((m1.ymax-m1.ymin)/3000.)+1
	tempo2 = m1.transform_scalar(w,lons,lats,nx2,ny2);CS3 = m1.imshow(tempo2,cmap=shifted_cmap, vmin=mintemp,vmax=maxtemp);
	plt.colorbar(CS3, cax, ticks=v, orientation='horizontal')
	m1.drawcountries(); m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	file_name = os.path.abspath("Time_period_%s_%s.png" %(vv[number][0],str(k))); fig.savefig(file_name, dpi=200)



