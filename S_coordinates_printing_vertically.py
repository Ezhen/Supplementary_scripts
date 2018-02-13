import pyroms
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from numpy import ma
import gc

dstgrd = pyroms.grid.get_ROMS_grid('GRIDRECT')

eta=60; a=dstgrd.hgrid.lon_rho[:,eta]
hh = dstgrd.vgrid.h[:,eta]

theta_b=[1.0]
theta_s=[2.0]
Tcline=[10.0]

def Plot(Tcline,b,s):
	vgrd = pyroms.vgrid.s_coordinate_4(dstgrd.vgrid.h, theta_b=b, theta_s=s, Tcline=Tcline, N=10, hraw=dstgrd.vgrid.hraw)
	grd = pyroms.grid.ROMS_Grid('GRIDRECT', dstgrd.hgrid, vgrd)
	w=grd.vgrid.Cs_w
	print 'Tcline:', grd.vgrid.Tcline, 'Theta_s:', grd.vgrid.theta_s, 'Theta_b:', grd.vgrid.theta_b
	print 'Cs_w:', grd.vgrid.Cs_w
	#d=np.zeros((len(hh),len(w)))
	#for i in range(len(hh)):
	#	for j in range(len(w)):
	#		d[i,j]=hh[i]*w[j]
	d=np.zeros((len(hh),len(w)))
	for i in range(len(hh)):
		for j in range(len(w)):
			d[i,j]=max(hh)*w[j]
	print d
	dd=d.copy()
	fig = plt.figure()
	ax = fig.add_subplot(111,axisbg='lightsage')
	ax.set_title(r'Tcline = %s; $\theta_s$ = %s; $\theta_b$ = %s.' %(Tcline,s,b), fontsize=16)
	ax.set_xlim([min(a),max(a)])
	#ax.set_ylim([d.min(),1])
	ax.set_ylim([min(-hh),1])
	#for k in range(len(w)):
	#	ax.plot(a, d[:,k], color='royalblue')
	#ax.plot(a, d[:,0], color='saddlebrown', linewidth=2)
	#plt.fill_between(a, np.ones((len(hh))), -hh)
	g=np.array((len(a),len(w)))
	for i in range(len(a)):
		for j in range(len(w)):
			if d[i,j]<-hh[i]:
				d[i,j]='NaN'
	d_m=ma.masked_where(d=='NaN',d) 
	for k in range(len(w)):
		ax.plot(a, d_m[:,k], color='royalblue')
		#ax.plot(a, dd[:,k], color='royalblue')
	ax.plot(a, -hh, color='saddlebrown', linewidth=2)
	for i in range(len(a)):
		plt.plot((a[i], a[i]), (1, -hh[i]), 'royalblue')
		#plt.plot((a[i], a[i]), (1, -max(hh)), 'royalblue')
	plt.savefig('111Tcline%sS%sB%seta.png' %(Tcline,s,b))


for i in range(len(theta_b)):
	for j in range(len(theta_s)):
		for k in range(len(Tcline)):
			Plot(Tcline[k],theta_b[i],theta_s[j])
			#print Tcline[k],theta_b[i],theta_s[j]
