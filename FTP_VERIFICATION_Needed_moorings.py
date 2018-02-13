import matplotlib.pyplot as plt
from numpy import ma
from math import isnan
import ftplib
import urllib

path = 'Core/SST_NWS_SST_L4_REP_OBSERVATIONS_010_023/IFREMER-NWS-SST-L4-REP-OBS_FULL_TIME_SERIE/'
ftp = ftplib.FTP("130.186.13.101") 
ftp.login("eivanov", "Evgeny@CMEMS2016") 
ftp.cwd(path)

for i in ftp.nlst():
	if int(i)>2003 and int(i)<2014:
		ftp.cwd(i)
		for j in ftp.nlst():
			ftp.cwd(j)
			for k in ftp.nlst():
				ftp.retrbinary("RETR " + k ,open(k, 'wb').write)
				print k
			ftp.cwd('..')
		ftp.cwd('..')

ftp.quit()

