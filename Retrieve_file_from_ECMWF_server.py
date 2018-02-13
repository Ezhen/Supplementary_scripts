#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
    
server = ECMWFDataServer()
    
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "sfc",
    'param'     : "151.128/164.128/165.128/166.128/167.128/168.128/176.128/177.128/228.128",
    'dataset'   : "interim",
    'step'      : "3/6/9/12",
    'grid'      : "0.125/0.125",
    'time'      : "00:00:00/12:00:00",
    'date'      : "2006-01-01/to/2009-01-01",
    'type'      : "fc",
    'class'     : "ei",
    'area'      : "55/-4.5/48.375/6.875",
    'format'    : "netcdf",
    'target'    : "Bulk_2006_2009.nc"
 })

# surface net solar radiation (shortwave) - ssr - 176
# surface net thermal radiation (longwave) - str - 177
# total cloud cover - tcc - 164
# total precipitation - tp - 228
# mean sea level pressure - msl - 151
# 10 metre U wind component - u10 - 165
# 10 metre V wind component - v10 - 166
# 2 metre temperature - t2m - 167
# 2 metre dewpoint temperature - d2m - 168
# 

# 'type'      : "an", - instantenious
# 'type'      : "fc", - accumulated

