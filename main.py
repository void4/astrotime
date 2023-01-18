from PIL import Image, ImageDraw
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
from astropy.time import Time
import astropy.units as u
import numpy as np

LAT_DEGREES = -30.52630901637761
LON_DEGREES = -70.85329602458852

STARTTIME = "2023-1-19 22:30:00"
UTC_OFFSET_HOURS = -3

scale = 0.05

# longer total -> more computation required
MINUTES_TOTAL = 7*60
# shorter intervals -> more computation required
MINUTE_INTERVAL = 60

w = int(360*scale)
h = int(180*scale)

img = Image.new("RGB", (w,h))
draw = ImageDraw.Draw(img)

location = EarthLocation(lat=LAT_DEGREES*u.deg, lon=LON_DEGREES*u.deg, height=1710*u.m)

grid = [[0 for x in range(w)] for y in range(h)]

for y in range(h):
	print(y)
	for x in range(w):
		ra = x/scale
		dec = y/scale-90
		
		coord = SkyCoord(ra, dec, unit=u.deg)
		
		obstime = Time(STARTTIME) - UTC_OFFSET_HOURS * u.hour
		
		steps = 0
		
		for minute in range(0, MINUTES_TOTAL, MINUTE_INTERVAL):
			t = obstime + minute * u.min
		
			altaz = AltAz(obstime=t, location=location)
			attime = coord.transform_to(altaz)
			grid[y][x] += 1/attime.secz
			steps += 1
			
		grid[y][x] /= steps
		print(y, x, attime.secz)

grid = np.array(grid)

import matplotlib as mpl
from matplotlib import pyplot

fig, ax = pyplot.subplots()
fig.set_size_inches(18.5, 10.5)
cmap2 = mpl.colors.LinearSegmentedColormap.from_list("my_colormap", ["blue", "black", "red"], 256)
img2 = pyplot.imshow(grid, interpolation="nearest", cmap=cmap2, origin="lower", extent=[0,360,-90,90])
pyplot.colorbar(img2, cmap=cmap2)
ax.set_xticks(np.arange(0,361,15))
ax.set_yticks(np.arange(-90,91,10))
ax.set_xticklabels(np.arange(0,25,1))
ax.set_yticklabels(np.arange(-90,91,10))
fig.savefig("airmass.png")

pyplot.show()
