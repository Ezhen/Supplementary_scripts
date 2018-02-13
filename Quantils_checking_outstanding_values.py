from netCDF4 import Dataset; from scipy import stats; import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl
mpl.rcParams['axes.unicode_minus']=False
var=['temp','salt']; d=3650
for m in range(len(var)):
	fig=plt.figure(figsize=(20, 12))
	plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
	rr=Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_simulation/Climatology.nc', 'r', format='netCDF4')
	#rr=Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo/t2mGRIDRECT.nc', 'r', format='netCDF4')
	mean=[]; min=[]; max=[]; q_10=[]; q_90=[]
	for i in range(d):
		p=np.ravel(rr.variables[var[m]][i,:,:,:])
		p[p == -32768] = 'nan'
   		mean_p=stats.nanmean(p); min_p=np.nanmin(p); max_p=np.nanmax(p); q_10_p=np.percentile(p[~np.isnan(p)],10); q_90_p=np.percentile(p[~np.isnan(p)],90.)
   		mean.append(mean_p); min.append(min_p); max.append(max_p); q_10.append(q_10_p); q_90.append(q_90_p)
	plt.plot(min,label='min', color='lightgray', linewidth=1.5)
	plt.plot(q_10,label='q10',color='gray', linewidth=1.5)
	plt.plot(mean, label='mean', color='black', linewidth=1.5)
	plt.plot(q_90,label='q90',color='gray', linewidth=1.5)
	plt.plot(max, label='max',color='lightgray', linewidth=1.5)
	plt.xlim(0,d); plt.legend(loc=3, ncol=5)
	fig.savefig(var[m], dpi=200)

from netCDF4 import Dataset; from scipy import stats; import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl
mpl.rcParams['axes.unicode_minus']=False
#var=['temp_north','temp_south','salt_north','salt_south','u_north','u_south','v_north','v_south','zeta_north', 'zeta_south','ubar_north','ubar_south','vbar_north','vbar_south']; d=3650
var=['ubar_south']; d=3650
for m in range(len(var)):
	fig=plt.figure(figsize=(20, 12))
	plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
	rr=Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_simulation/Boundary.nc', 'r', format='netCDF4')
	#rr=Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo/t2mGRIDRECT.nc', 'r', format='netCDF4')
	mean=[]; min=[]; max=[]; q_10=[]; q_90=[]
	for i in range(d):
		if var[m] == 'zeta_north' or var[m] == 'zeta_south' or var[m] == 'ubar_north' or var[m] == 'ubar_south' or var[m] == 'vbar_north' or var[m] == 'vbar_south':
   			p=np.ravel(rr.variables[var[m]][i,:])
		else:
   			p=np.ravel(rr.variables[var[m]][i,:,:])
		p[p == -32767] = 'nan'
   		mean_p=stats.nanmean(p); min_p=np.nanmin(p); max_p=np.nanmax(p); q_10_p=np.percentile(p[~np.isnan(p)],10); q_90_p=np.percentile(p[~np.isnan(p)],90.)
   		mean.append(mean_p); min.append(min_p); max.append(max_p); q_10.append(q_10_p); q_90.append(q_90_p)
	plt.plot(min,label='min', color='lightgray', linewidth=1.5)
	plt.plot(q_10,label='q10',color='gray', linewidth=1.5)
	plt.plot(mean, label='mean', color='black', linewidth=1.5)
	plt.plot(q_90,label='q90',color='gray', linewidth=1.5)
	plt.plot(max, label='max',color='lightgray', linewidth=1.5)
	plt.xlim(0,d); plt.legend(loc=3, ncol=5)
	fig.savefig(var[m], dpi=200)

from netCDF4 import Dataset; from scipy import stats; import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl
mpl.rcParams['axes.unicode_minus']=False
var=['sst','Pair','cloud','Tair','Qair','swrad','lwrad','rain','Uwind','Vwind']; d=3650*4
#var=['Tair']; d=3650*4
for m in range(len(var)):
	fig=plt.figure(figsize=(20, 12))
	plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
	rr=Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_simulation/Forcing.nc', 'r', format='netCDF4')
	#rr=Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo/t2mGRIDRECT.nc', 'r', format='netCDF4')
	mean=[]; min=[]; max=[]; q_10=[]; q_90=[]
	for i in range(d):
   		p=np.ravel(rr.variables[var[m]][i,:,:])
		p[p == -32767] = 'nan'
		if var[m]=='Uwind' or var[m]=='Vwind':
			p[p == 0] = 'nan'
   		mean_p=stats.nanmean(p); min_p=np.nanmin(p); max_p=np.nanmax(p); q_10_p=np.percentile(p[~np.isnan(p)],10); q_90_p=np.percentile(p[~np.isnan(p)],90.)
   		mean.append(mean_p); min.append(min_p); max.append(max_p); q_10.append(q_10_p); q_90.append(q_90_p)
	plt.plot(min,label='min', color='lightgray', linewidth=1.5)
	plt.plot(q_10,label='q10',color='gray', linewidth=1.5)
	plt.plot(mean, label='mean', color='black', linewidth=1.5)
	plt.plot(q_90,label='q90',color='gray', linewidth=1.5)
	plt.plot(max, label='max',color='lightgray', linewidth=1.5)
	plt.xlim(0,d); plt.legend(loc=3, ncol=5)
	fig.savefig(var[m], dpi=200)


