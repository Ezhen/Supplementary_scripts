import matplotlib.pyplot as plt
from numpy import ma
from math import isnan
import ftplib
import urllib

plat=[]
lat1=[]
lat2=[]
lon1=[]
lon2=[]

for line in open('/media/sf_Swap-between-windows-linux/FTP_DATA/Table_6.txt', 'r'):	
	plat.append(str(line.split("\t")[0]))
	lat1.append(float(line.split("\t")[1]))
	lat2.append(float(line.split("\t")[2]))
	lon1.append(float(line.split("\t")[3]))
	lon2.append(float(line.split("\t")[4]))


num=[]
for i in range(len(plat)):
	if lat1[i]>48.5 and lat2[i]<54.9:
		if lon1[i]>-4.3 and lon1[i]<6.7:
			num.append(i)


path = 'Core/INSITU_GLO_NRT_OBSERVATIONS_013_030/monthly/'
ftp = ftplib.FTP("134.246.142.20") 
ftp.login("eivanov", "Evgeny@CMEMS2016") 
ftp.cwd(path)


for i in range(len(num)):
	b=plat[num[i]].split('/')
	ftp.cwd(b[0])
	ftp.cwd(b[1])
	filename = b[2]
	try:
		ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
		print 'file'+filename+'stored'	
		ftp.cwd('..')
		ftp.cwd('..')
	except:
		pass

ftp.quit()

