import matplotlib.pyplot as plt
from numpy import ma
from math import isnan
import ftplib
import urllib

plat=[]; lat1=[]; lat2=[]; lon1=[]; lon2=[]

for line in open('/media/sf_Swap-between-windows-linux/FTP_DATA/BCZ_monthly.txt', 'r'):	
	plat.append(str(line.split("\t")[0]))
	lat1.append(float(line.split("\t")[1]))
	lat2.append(float(line.split("\t")[2]))
	lon1.append(float(line.split("\t")[3]))
	lon2.append(float(line.split("\t")[4]))


path = 'Core/INSITU_GLO_NRT_OBSERVATIONS_013_030/monthly/'
ftp = ftplib.FTP("134.246.142.20") 
ftp.login("eivanov", "Evgeny@CMEMS2016") 
ftp.cwd(path)


for i in range(len(plat)):
	b=plat[i].split('/')
	if not b[1][0:4]=='2011':
		if not ftp.pwd().split('/')[-1]=='monthly':
			ftp.cwd('..')
			ftp.cwd('..')
		else:
			print i
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

