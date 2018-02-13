import pyroms; import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from numpy import ma

dstgrd = pyroms.grid.get_ROMS_grid('GRIDDIS7310'); eta=60

a=dstgrd.hgrid.lon_rho[:,eta]
hh = dstgrd.vgrid.h[:,eta]

theta_b,theta_s,Tcline,N,w=dstgrd.vgrid.theta_b,dstgrd.vgrid.theta_s,dstgrd.vgrid.Tcline,dstgrd.vgrid.N,dstgrd.vgrid.Cs_w

def Plot(N,Tcline,b,s):
	
	print 'Tcline:', dstgrd.vgrid.Tcline, 'Theta_s:', dstgrd.vgrid.theta_s, 'Theta_b:', dstgrd.vgrid.theta_b, 'Cs_w:', dstgrd.vgrid.Cs_w
	d=np.zeros((len(hh),len(w)))
	for i in range(len(hh)):
		for j in range(len(w)):
			d[i,j]=hh[i]*w[j]
	#d=np.zeros((len(hh),len(w)))
	#for i in range(len(hh)):
	#	for j in range(len(w)):
	#		d[i,j]=max(hh)*w[j]
	print d
	dd=d.copy()
	fig = plt.figure()
	ax = fig.add_subplot(111,axisbg='lightsage')
	ax.set_title(r'N = %s; Tcline = %s; $\theta_s$ = %s; $\theta_b$ = %s.' %(N,int(Tcline),int(s),int(b)), fontsize=16)
	ax.set_xlim([min(a),max(a)])
	ax.set_xlim(1,3)
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
	print d
	d_m=ma.masked_where(d=='NaN',d) 
	for k in range(len(w)):
		ax.plot(a, d_m[:,k], color='royalblue')
		#ax.plot(a, dd[:,k], color='royalblue')
	ax.plot(a, -hh, color='saddlebrown', linewidth=2)
	for i in range(len(a)):
		plt.plot((a[i], a[i]), (1, -hh[i]), 'royalblue')
		#plt.plot((a[i], a[i]), (1, -max(hh)), 'royalblue')
	plt.savefig('N%s_Tc%s_S%s_B%s_eta60.png' %(N,int(Tcline),int(s),int(b)))

Plot(N,Tcline,theta_b,theta_s)
"""
for i in range(len(theta_b)):
	for j in range(len(theta_s)):
		for k in range(len(Tcline)):
			Plot(Tcline[k],theta_b[i],theta_s[j])
			#print Tcline[k],theta_b[i],theta_s[j]
"""
