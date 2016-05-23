#!/usr/bin/python


import os, sys


import time
import random
import math
import urllib.request
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)
  
def latlon2px(z,lat,lon):



	x = 2**z*(lon+180)/360*256
	y = -(.5*math.log((1+math.sin(math.radians(lat)))/(1-math.sin(math.radians(lat))))/math.pi-1)*256*2**(z-1)
	return x,y

def latlon2xy(z,lat,lon):
	x,y = latlon2px(z,lat,lon)
	x = int(x/256)#,int(x%256)
	y = int(y/256)#,int(y%256)
	return x,y

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

	start_x, start_y = deg2num(lat_start, lon_start, zoom)
	stop_x, stop_y = deg2num(lat_stop, lon_stop, zoom)
	
	print ("x range", start_x, stop_x)
	print ("y range", start_y, stop_y)
	
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
	headers = { 'User-Agent' : user_agent }
	
	directory=None
	if satellite:		
		directory = "s/%d" % (zoom)
	else:
		directory = "r/%d" % (zoom)
	if not os.path.exists(directory):
		os.makedirs(directory)
	for x in range(start_x, stop_x+1):
		print (".")

		directory=None
		if satellite:		
			directory = "s/%d/%d" % (zoom, x)
		else:
			directory = "r/%d/%d" % (zoom, x)
		if not os.path.exists(directory):
			os.makedirs(directory)
		for y in range(start_y, stop_y+1):
			
			url = None
			filename = None
			
			if satellite:		
				url = "http://khm1.google.com/kh?v=87&hl=en&x=%d&y=%d&z=%d" % (x, y, zoom)
				filename = "s/%d/%d/%d.jpg" % (zoom, x, y)
			else:
				url = "http://mt1.google.com/vt/lyrs=m@110&hl=en&x=%d&y=%d&z=%d" % (x, y, zoom)
				filename = "r/%d/%d/%d.png" % (zoom, x, y)	
	
			if not os.path.exists(filename):
				
				bytes = None
				
				try:
					print ("--", url )
					urllib.request.urlretrieve(url, filename)
				except (Exception) as e:
					print ("--", filename, "->", e)
					sys.exit(1)
				
				
				time.sleep(1 + random.random())

if __name__ == "__main__":
	
	zoom = 21

#	lat_start, lon_start = 42.220035, -9.751003
#	lat_stop, lon_stop = 36.776286, -5.981797
	lat_start, lon_start = 38.762049, -9.248752
	lat_stop, lon_stop = 38.753093, -9.232857
	
	

		
	download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=False)