from pylab import *;  import os; from mpl_toolkits.basemap import Basemap; from Ncdump import *; import datetime; from scipy import spatial; import matplotlib.path as mplPath; from datetime import date
try:
  import netCDF4 as netCDF
except:
  import netCDF3 as netCDF

#we have 1709 files; 894836 records; unique latitudes-  43635, unique longitudes - 43694, and only 2751 within BCZ, and only 2750 PSAL, and only 2733 TEMP; but only 23674 unique values if we round until 4 digit after comma; and 4184 unique values if we round until 2 digit after comma (59 within BCZ); and 797 unique values if we round until 1 digit after comma;

path='/media/sf_Swap-between-windows-linux/FTP_DATA/FTP_2/Altogether/'

dn = lambda x: datetime.datetime(1950,1,1,0,0,0) + datetime.timedelta(days=x)

m=0; jj=0
latitude=[]; longitude=[]; variable=[]; time=[]; depth=[]; tp=[]; temperature=[]; name_mooring=[]; unique_latitude=[]; unique_longitude=[]; jjj=[]; jjj.append(0)

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

x_bcz=np.array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472]); y_bcz=np.array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361]); poly=[]
for i in range(len(y_bcz)):
    poly.append((x_bcz[i],y_bcz[i]))



def read_netcdf(name,jj):
	try:
		ncdata = netCDF.Dataset(name, 'r')
		lat = ncdata.variables['LATITUDE'][:]; lat=[round(lat[k],5) for k in range(len(lat))]
		lon = ncdata.variables['LONGITUDE'][:]; lon=[round(lon[k],5) for k in range(len(lon))]
		t = ncdata.variables['TIME'][:]
		try:
			h = ncdata.variables['DEPTH'][:]; hh=0
		except:
			try:
				h = ncdata.variables['DEPH'][:]; hh=0
			except:
				try:
					h=ncdata.variables['PRES'][:]; hh=0
				except:
					hh=-32767
		#print len(latitude)
		var = ncdump(ncdata, verb=False)
		if 'TEMP' in var[:] and not hh==-32767:			#TEMP
			temp = ncdata.variables['TEMP'][:]
			for i in range(len(t)):
				if dn(t[i]).year>2003 and dn(t[i]).year<2014 and point_inside_polygon(lon[i],lat[i],poly)==True:
					if dn(t[i]).month==6 or dn(t[i]).month==7 or dn(t[i]).month==8:
						for j in range(len(h.T)):
							if h[i,j]>4. and shape(t)==shape(lat):
								tp.append(t[i]);latitude.append(lat[i]); longitude.append(lon[i]); depth.append(h[i,j]); temperature.append(temp[i,j]);jjj.append(jj);jj=jj+1
							elif h[i,j]>4.:
								tp.append(t[i]);latitude.append(lat[0]); longitude.append(lon[0]); depth.append(h[i,j]); temperature.append(temp[i,j]);jjj.append(jj);jj=jj+1
	except:
		pass




"""
for file in os.listdir(path):
	current_file = os.path.join(path, file)
	print '%g) Processing:' %(jj+1), current_file
	mm=read_netcdf(current_file,jj)
	m=mm; jj=jj+1

"""

plat=[]; jj=0
for line in open('/media/sf_Swap-between-windows-linux/FTP_DATA/FTP_2/Needed_moorings_ONLY_TEMP_SALT.py', 'r'):	
	plat.append(str(line.split("\t")[0]))
for kk in range(len(plat)):
	current_file = os.path.join(path, plat[kk][0:-1])
	print '%g) Processing:' %(kk+1), current_file
	read_netcdf(current_file,jjj[-1])

jjj=jjj[0:-1]

a=[];b=[];tpp=[]; dpp=[]; jjjj=[]; mm=[]; mm.append(0); long=[]; lati=[]
for i in range(len(latitude)):
	a.append([longitude[i],latitude[i],tp[i]])
	mm.append(i)

for i in range(len(a)-1):
	if not a[i]==a[i+1]:
		b.append(a[i][0:2])
		tpp.append((date(dn(tp[i]).year, dn(tp[i]).month, dn(tp[i]).day)-date(dn(tp[i]).year,1,1)).days)
		dpp.append(depth[i]); jjjj.append(jjj[i])
		long.append(longitude[i]); lati.append(latitude[i])

b=array(b); jjjj.append(0)

temptemp=[[] for x in xrange(len(dpp))];depthdepth=[[] for x in xrange(len(dpp))]
for i in range(len(dpp)):
		temptemp[i].append(temperature[jjjj[i]:jjjj[i+1]])
		depthdepth[i].append(depth[jjjj[i]:jjjj[i+1]])
"""
d = [[] for x in xrange(41)]; dd=zeros((41)); ddd=np.array(np.arange(0,41,1))
for k in range(len(temperature)):
	if depth[k]>-1 and depth[k]<41 and not type(temperature[k])==np.ma.core.MaskedConstant:
		d[int(round(depth[k],0))].append(temperature[k])

for k in range(len(d)):
	dd[k]=sum(d[k])/len(d[k])
"""


ii=[]; jj=[]; hh=[]
rr = netCDF.Dataset('/media/sf_Swap-between-windows-linux/New_Grid/RESULTS/ocean_avg_tides.nc', 'r', format='NETCDF3')
lon = rr.variables['lon_rho'][:]; lat = rr.variables['lat_rho'][:]; Cs_r = rr.variables['Cs_r'][:]; h = rr.variables['h'][:]; time = rr.variables['ocean_time'][0:365]
coord_precise=np.zeros((len(hstack(lat)),2))
coord_precise[:,0]=hstack(lon)
coord_precise[:,1]=hstack(lat)
hh=[]; temp=[]; latlat=[]; lonlon=[]
for i in range(len(b)):
	depth_cool=coord_precise[spatial.KDTree(coord_precise).query(b[i])[1]]
	distance,index = spatial.KDTree(coord_precise).query(b[i])	
	print 'closest point:', depth_cool, 'distance:', distance, 'index:', index
	lonlon.append(depth_cool[0]);latlat.append(depth_cool[1])
	hh.append(h[index/82,index-(index/82)*82])
	temp.append(rr.variables['temp'][tpp[i],:,index/82,index-(index/82)*82])
	
dt=[]
for j in range(len(hh)):
	for k in range(0,15):
		dt.append(hh[j]*Cs_r[k]*(-1))
"""
for i in range(len(lon)):
	for j in range(len(lon.T)):
		if point_inside_polygon(lon[i,j],lat[i,j],poly)==True:
			ii.append(i);jj.append(j)
"""

'''			hh.append(h[i,j]); 
temp=[]; dt=[]
for i in range(len(time)):
	print i
	if time[i]/24/60/60.>140 and time[i]/24/60/60.<234:
		for j in range(len(h)):
			for k in range(0,15):
				dt.append(hh[j]*Cs_r[k])
				temp.append(rr.variables['temp'][i,k,int(ii[j]),int(jj[j])])

g = [[] for x in xrange(41)]; gg=zeros((41)); ggg=np.array(np.arange(0,41,1))
for k in range(len(temp)):
	if dt[k]>-40 and dt[k]<0:
		g[int(round(-1*dt[k],0))].append(temp[k])
for k in range(len(g)):
	gg[k]=sum(g[k])/len(g[k])
'''

#plot(dd,ddd, label='In-situ'); ylim(0,80); xlabel('Temperature, [C]'); ylabel('Depth, [m]'); gca().invert_yaxis()
#plot(gg,ggg, label='ROMS')
#legend(loc=3)

"""
scatter(temperature, depth, color='r', label='in-situ')
scatter(hstack(temp), dt, color='b', label='model')

xlim(8,18); xlabel('Temperature, [C]')
#xlim(30,38); xlabel('Salinity, [psu]')
ylabel('Depth, [m]');ylim(0,80);
gca().invert_yaxis()
show()
"""
#for i in range(len(b)):


for i in range(40,41):
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))
	plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, wspace=0.1)
	ax1 = plt.subplot2grid((1,2), (0,0))
	ax2 = plt.subplot2grid((1,2), (0,1))
	ax1.set_xlim(4,20); ax1.set_xlabel('Temperature, [C]')
	#xlim(30,38); xlabel('Salinity, [psu]')
	ax1.set_ylabel('Depth, [m]')#;ax1.set_ylim(0,80)
	ax1.set_ylim(80, 0)
	#ax1 = plt.gca()
	#ax1.set_ylim(ax1.get_ylim()[::-1])
	ax1.scatter(temptemp[i], depthdepth[i], color='r', label='in-situ')
	ax1.scatter(temp[i], dt[15*i:15*i+15], color='b', label='model')
	ax1.legend(loc=3)
	m2 = Basemap(projection='merc', llcrnrlat=51,urcrnrlat=51.9,llcrnrlon=2.0,urcrnrlon=3.5,lat_ts=51.45, resolution='i', ax=ax2)
	m2.drawparallels(arange(51.0,51.9,0.3),labels=[1,0,0,1],fontsize=10)
	m2.drawmeridians(arange(2,3.5,0.5),labels=[1,0,0,1],fontsize=10)
	m2.drawcoastlines()
	m2.drawmapboundary(fill_color='#9999FF')
	x4, y4 = m2(x_bcz, y_bcz); 	lnln, ltlt = m2(lonlon[i], latlat[i]); lg,lt=m2(long[i],lati[i]);clevs = np.arange(0.,60.0,1);cax = fig.add_axes([0.2, 0.08, 0.6, 0.04])
	x2, y2 = m2(lon, lat)
	cs43 = m2.plot(x4,y4,color='black',linewidth=1.0)
	CS4 = m2.contourf(x2,y2,h,clevs,cmap='Blues',animated=True)
	cb1 = colorbar(CS4, cax, orientation='horizontal')
	m2.drawcountries()
	m2.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	m2.scatter(lnln,ltlt,20,marker='o',color='r')
	m2.scatter(lg,lt,20,marker='o',color='b')

show()
'''
#m1 = Basemap(projection='merc',llcrnrlat=49,urcrnrlat=54.0,llcrnrlon=-1,urcrnrlon=6,lat_ts=51.5,resolution='i')
m1 = Basemap(projection='merc', llcrnrlat=51,urcrnrlat=51.9,llcrnrlon=2.0,urcrnrlon=3.5,lat_ts=51.45,resolution='h')
m1.drawparallels
m1.drawmeridians
m1.drawcoastlines()
m1.drawmapboundary(fill_color='#9999FF')
m1.drawcountries()
m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
x, y = m1(longitude, latitude)
m1.scatter(x,y,3,marker='o',color='k')

'''

