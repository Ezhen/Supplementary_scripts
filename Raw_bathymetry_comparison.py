from netCDF4 import Dataset; import numpy as np; import shapely.geometry as g; import matplotlib.pyplot as plt; import matplotlib.gridspec as gridspec

rr = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Coarsest_improved.nc', 'r', format='NETCDF3')
hr=rr.variables['hraw'][0]; h=rr.variables['h'][:]; xv=rr.variables['x_vert'][:]; yv=rr.variables['y_vert'][:];

mr=rr.variables['mask_rho'][:]; mu=rr.variables['mask_u'][:]; mv=rr.variables['mask_v'][:]; mp=rr.variables['mask_psi'][:]; 

#nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Coarsest_TPXO.nc', 'a', format='NETCDF3')
#nc.variables['mask_rho'][:]=mr; nc.variables['mask_u'][:]=mu; nc.variables['mask_v'][:]=mv; nc.variables['mask_psi'][:]=mp; nc.close()

nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Coarsest_TPXO.nc', 'r', format='NETCDF3')
h_raw=nc.variables['h'][:]; ho=np.zeros((len(h),len(h.T)))

area=np.zeros((len(h),len(h.T))); vol=np.zeros((len(h),len(h.T))); vol_raw=np.zeros((len(h),len(h.T)))
for i in range(len(h)):
	for j in range(len(h.T)):
		pointList=[g.Point(yv[i,j],xv[i,j]), g.Point(yv[i,j+1],xv[i,j+1]), g.Point(yv[i+1,j+1],xv[i+1,j+1]), g.Point(yv[i+1,j],xv[i+1,j])]
		v= g.Polygon([[p.x, p.y] for p in pointList])
		area[i,j]=round(v.area/1000000,3)
		if mr[i,j]==1:
			vol[i,j]=area[i,j]*h[i,j]
			vol_raw[i,j]=area[i,j]*h_raw[i,j]
		else:
			vol[i,j]=0
			vol_raw[i,j]=0

for i in range(len(h)):
	for j in range(len(h.T)):
		if mr[i,j]==1:
			ho[i,j]=(h[i,j]/h_raw[i,j])*100
		else:
			ho[i,j]=0

vol_diff=np.zeros((len(h))); voll=np.zeros((len(h))); vollr=np.zeros((len(h)))
for i in range(len(h)):
	vol_diff[i]=(sum(vol[i])/sum(vol_raw[i]))*100
	voll[i]=sum(vol[i]); vollr[i]=sum(vol_raw[i])

fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(3, 3)
ax1 = plt.subplot(gs[:, 0])
ax2 = plt.subplot(gs[:, 1:])
ax1.plot(vol_diff,np.arange(0,112),linewidth=3)
ax1.set_xlabel('Volume ROMS / Volume TPXO',fontsize=18)
ax1.set_ylabel('Eta_rho [units]',fontsize=18)
#ax1.set_xlim(99,109)
ax1.set_ylim(0,111)
ax1.set_ylim(ax1.get_ylim()[::-1])

uu=ax2.imshow(ho, interpolation="nearest", vmin=0, vmax =200)
cb=plt.colorbar(uu)
cb.set_label('H ROMS / H TPXO [%]',fontsize=18)
fig.savefig('Bathy_comparison_TPXO_ROMS.png', dpi=200)
#plt.show()

