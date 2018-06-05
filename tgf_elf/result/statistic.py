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
    data = pd.read_table('/home/foxy/Documents/result_Ela7_180605_2.txt',sep='\t',index_col=False)

    plt.scatter(data.DIST,data.DELTA)
    plt.ylabel('Delta, ms')
    plt.xlabel('Dist, km')
    plt.show()

    res = []
    for p,pmin in zip(data.P,data.PMIN):
        if pmin!=0:
            res.append(p/pmin)
        else: res.append(0)

    res.sort()
    plt.scatter(range(len(res)),res)
    plt.axhline(1,color='red')
    plt.axhline(3,color='green')
    plt.ylabel('P/Pmin')
    plt.show()

    plt.hist(data.BP,100,color='grey',label='total')
    plt.hist(data.BP[data.GEOG==1],100,color='green',label='coastline')
    plt.hist(data.BP[data.GEOG==2],100,color='red',label='continent')
    plt.hist(data.BP[data.GEOG==0],100,color='blue',label='ocean')
    plt.ylabel('Quantity')
    plt.xlabel('Bpulse')
    plt.legend()
    plt.show()

    plt.hist(data.BN,100,color='grey',label='total')
    plt.hist(data.BN[data.GEOG==1],100,color='green',label='coastline')
    plt.hist(data.BN[data.GEOG==2],100,color='red',label='continent')
    plt.hist(data.BN[data.GEOG==0],100,color='blue',label='ocean')
    plt.ylabel('Quantity')
    plt.xlabel('Bnoise')
    plt.legend()
    plt.show()

    plt.hist(data.P,100,color='grey',label='total')
    plt.hist(data.P[data.GEOG==1],100,color='green',label='coastline')
    plt.hist(data.P[data.GEOG==2],100,color='red',label='continent')
    plt.hist(data.P[data.GEOG==0],100,color='blue',label='ocean')
    plt.ylabel('Quantity')
    plt.xlabel('P')
    plt.legend()
    plt.show()

    plt.hist(data.PMIN,100,color='grey',label='total')
    plt.hist(data.PMIN[data.GEOG==1],100,color='green',label='coastline')
    plt.hist(data.PMIN[data.GEOG==2],100,color='red',label='continent')
    plt.hist(data.PMIN[data.GEOG==0],100,color='blue',label='ocean')
    plt.ylabel('Quantity')
    plt.xlabel('Pmin')
    plt.legend()
    plt.show()

    plt.hist(data.PMIN[abs(data['DC'])>0.99],100,color='orange',label='day',alpha=0.5)
    plt.hist(data.PMIN[abs(data['DC'])<0.001],100,color='darkblue',label='night',alpha=0.5)
    plt.ylabel('Quantity')
    plt.xlabel('Pmin')
    plt.legend()
    plt.show()

    plt.scatter(data.DIST,data.CR,color='grey',label='d/n')
    plt.scatter(data.DIST[abs(data['DC'])>0.99],data.CR[abs(data['DC'])>0.99],color='orange',label='day')
    plt.scatter(data.DIST[abs(data['DC'])<0.001],data.CR[abs(data['DC'])<0.001],color='darkblue',label='night')
    plt.ylabel('c(r)')
    plt.xlabel('Dist, km')
    plt.legend()
    plt.show()


    plt.scatter(data.COUNTS[abs(data['DC'])>0.99],data.BP[abs(data['DC'])>0.99],color='orange')
    plt.scatter(data.COUNTS[abs(data['DC'])<0.001],data.BP[abs(data['DC'])<0.001],color='darkblue')
    plt.show()
    #
    # dt = lambda x: [datetime.datetime.strptime(xi,"%Y-%m-%dT%H:%M:%S.%f") for xi in x]
    # plt.clf()
    # plt.hist(dt(data.TIMESTAMP),100)
    # plt.show()


    # dt = lambda x: [datetime.datetime.strptime(xi,"%Y-%m-%dT%H:%M:%S.%f") for xi in x]
    # plt.scatter(dt(data.TIMESTAMP[data.GEOG==0]),data.ID[data.GEOG==0],s=1,color='red')
    # plt.scatter(dt(data.TIMESTAMP[data.GEOG==1]),data.ID[data.GEOG==1],s=1,color='green')
    # plt.scatter(dt(data.TIMESTAMP[data.GEOG==2]),data.ID[data.GEOG==2],s=1,color='blue')
    # plt.show()

    # plt.scatter(data.Bn,data.Bp)
    # plt.show()

    # plt.hist(data.)
