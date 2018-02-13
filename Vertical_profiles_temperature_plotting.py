from netCDF4 import Dataset
from pylab import *
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['axes.unicode_minus']=False

mpl.rc('font',family='Times New Roman')

dn = lambda x: datetime.datetime(1950,1,1,0,0,0) + datetime.timedelta(days=x)

source = Dataset('/media/sf_Swap-between-windows-linux/Vessel/Within_the _domain/Temperature_comparison_my_vision.nc', 'r', format='NETCDF3')
#temp_model = source.variables['temperature_model'][:]
#temp_obs = source.variables['temperature_obs'][:]
octi = source.variables['time'][:]
latitude = source.variables['latitude'][:]
longitude = source.variables['longitude'][:]

source1 = Dataset('/home/eivanov/coawst_data_prrocessing/VERIFICATION_PROFILES/Mooring/Temperature_comparison.nc', 'r', format='NETCDF3')
octi1 = source1.variables['time'][:]
latitude1 = source1.variables['latitude'][:]
longitude1 = source1.variables['longitude'][:]


print "divide time into years, months, days and hours"
time=zeros((4,len(octi)))
for c in range(len(octi)):
	time[0,c]=dn(float(octi[c])).year
	time[1,c]=dn(float(octi[c])).month
	time[2,c]=dn(float(octi[c])).day
	time[3,c]=dn(float(octi[c])).hour


def index(ye,mo,da,ho):
	yy = where(time[0,:]==ye)
	mm = where(time[1,yy[0][0]:yy[0][-1]]==mo)
	dd = where(time[2,mm[0][0]:mm[0][-1]]==da)
	hh = where(time[3,dd[0][0]:dd[0][-1]]==ho)
	moment = yy[0][0]+mm[0][0]+dd[0][0]+hh[0][0]
	return moment


fig = plt.figure()
#title('August', fontsize=16)
ax = plt.subplot(111)
xlim(9,20)
ylim(-50,0)
xticks(linspace(9,20,12),fontsize=16)
yticks(linspace(-50,0,11),fontsize=16)

kk=[]
for i in range(len(octi)):
	if dn(float(octi[i])).month==8 and latitude[i]>52 and source.variables['temperature_obs'][i,2]<30 and source.variables['temperature_model'][i,2]<30:
			tm = source.variables['temperature_model'][i,:]
			dz = source.variables['depth_GEBCO_z'][i,:]
			to = source.variables['temperature_obs'][i,:]
			do = source.variables['depth'][i,:]
			j=[]
			j=where(do<60)[0][:]
			plt.plot(tm,dz,'g', linestyle='-', linewidth=2)
			plt.plot(to[j],-do[j],'b', linestyle='-', linewidth=2)
			pp=j
			kk.append(i)
			print tm, dz


for i in range(len(octi1)):
	if dn(float(octi1[i])).month==8 and latitude1[i]>52 and source1.variables['temperature_obs'][i,2]<30 and source1.variables['temperature_model'][i,2]<30:
			tm1 = source1.variables['temperature_model'][i,:]
			dz1 = source1.variables['depth_GEBCO_z'][i,:]
			to1 = source1.variables['temperature_obs'][i,:]
			do1 = source1.variables['depth'][i,:]
			j=[]
			j=where(do1<60)[0][:]
			plt.plot(tm1,dz1,'g', linestyle='-', linewidth=2)
			plt.plot(to1[j],-do1[j],'b', linestyle='--', linewidth=2)
			tt=j
			ll.append(i)
			print tm1, dz1

#ll=[], mm=[]
#for m in range(len(kk)):
#    ll.append(latitude[kk[m]])
#    mm.append(longitude[kk[m]])

plt.xlabel("Temperature [C]", fontsize=18)
plt.ylabel("Depth [m]", fontsize=18)
plt.plot(tm,dz,'g', linestyle='-', linewidth=2,  label='Model calculations')
plt.plot(to[pp],-do[pp],'b', linestyle='-',linewidth=2,label='Vessel observations')
#plt.plot(to1[tt],-do1[tt],'b', linestyle='--',linewidth=2,label='Mooring observations')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),fancybox=True, shadow=True, ncol=2, fontsize=18)

show()




				
