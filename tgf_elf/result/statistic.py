import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime

def plot_geog(data):
    m = Basemap(projection='mill',lon_0=0)
    # plot coastlines, draw label meridians and parallels.
    m.drawcoastlines()
    m.drawparallels(np.arange(-90,90,30), labels=[1,0,0,0])
    m.drawmeridians(np.arange(m.lonmin, m.lonmax+30,60), labels=[0,0,0,1])
    # m.drawmapboundary(fill_color='aqua')
    # m.fillcontinents(color='coral',lake_color='aqua')
    m.scatter(list(data.LON[data.GEOG==0]),list(data.LAT[data.GEOG==0]),3,marker='o',color='red',latlon=True)
    m.scatter(list(data.LON[data.GEOG==1]),list(data.LAT[data.GEOG==1]),3,marker='o',color='green',latlon=True)
    m.scatter(list(data.LON[data.GEOG==2]),list(data.LAT[data.GEOG==2]),3,marker='o',color='blue',latlon=True)
    plt.show()

if __name__ == '__main__':
    data = pd.read_table('/home/foxy/Documents/result_Ela7_180523.txt',sep='\t',index_col=False)

    res = []
    for p,pmin in zip(data.p,data.pmin):
        if pmin!=0:
            res.append(p/pmin)
        else: res.append(0)

    plt.scatter(data.ID,res)
    plt.axhline(1)
    plt.axhline(3)
    plt.show()

    # print(data)
    # # plot_geog(data)
    #
    # plt.scatter(data.COUNTS[data.GEOG==0],data.p[data.GEOG==0],color='red')
    # plt.scatter(data.COUNTS[data.GEOG==1],data.p[data.GEOG==1],color='green')
    # plt.scatter(data.COUNTS[data.GEOG==2],data.p[data.GEOG==2],color='blue')
    # plt.show()
    #
    #
    # plt.hist(data.p[data.GEOG==1],100,color='green')
    # plt.hist(data.p[data.GEOG==2],100,color='blue')
    # plt.hist(data.p[data.GEOG==0],100,color='red')
    # plt.show()
    #
    # dt = lambda x: [datetime.datetime.strptime(xi,"%Y-%m-%dT%H:%M:%S.%f") for xi in x]
    # plt.scatter(data.ID[data.GEOG==0],dt(data.TIMESTAMP[data.GEOG==0]),s=1,color='red')
    # plt.scatter(data.ID[data.GEOG==1],dt(data.TIMESTAMP[data.GEOG==1]),s=1,color='green')
    # plt.scatter(data.ID[data.GEOG==2],dt(data.TIMESTAMP[data.GEOG==2]),s=1,color='blue')
    # plt.show()
    #
    # plt.scatter(data.Bn,data.Bp)
    # plt.show()

    # plt.hist(data.)
