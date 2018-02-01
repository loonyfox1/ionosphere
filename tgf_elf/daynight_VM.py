import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from datetime import datetime

# example showing how to compute the day/night terminator and shade nightime
# areas on a map.

miller projection
m = Basemap(projection='mill',lon_0=0)
# plot coastlines, draw label meridians and parallels.
m.drawcoastlines()
m.drawparallels(np.arange(-90,90,30), labels=[1,0,0,0])
m.drawmeridians(np.arange(m.lonmin, m.lonmax+30,60), labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
shade the night areas, with alpha transparency so the
map shows through. Use current time in UTC.
m = Basemap(projection='mill')
m.bluemarble()
#date = datetime.utcnow()
#date = datetime(2013, 8, 16, 9, 1)
date = datetime(2009, 5, 10, 11, 57)

CS = m.nightshade(date)

lon_Hylaty = 22.5
lat_Hylaty = 49.2

lon_TGF = 180 - 281.2
lat_TGF = 3.6

m.drawgreatcircle(lon_Hylaty, lat_Hylaty, lon_TGF, lat_TGF, linewidth=3, color='b')

plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M%S"))
plt.show()
