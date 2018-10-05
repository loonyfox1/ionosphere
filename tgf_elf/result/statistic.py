from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    data7 = pd.read_table('/home/foxy/Documents/result_Ela7_180606.txt',sep='\t',index_col=False)
    data1 = pd.read_table('/home/foxy/Documents/result_Ela10_180606.txt',sep='\t',index_col=False)
    data7 = data7.dropna()
    data1 = data1.dropna()
    # plot_geog(data7)

    # print(len(data7),len(data1))
    # print(len(set(data7.ID).intersection(set(data1.ID))))
    # print(len(data7.ID[data7.P/data7.PMIN<=1])/len(data7.ID))
    # print(len(data1.ID[data7.P/data1.PMIN<=1])/len(data1.ID))

    ###### statistic of impulses ##################
    # res7 = []
    # for p,pmin in zip(data7.P,data7.PMIN):
    #     if pmin!=0:
    #         res7.append(p/pmin)
    #     else: res7.append(0)
    # res1 = []
    # for p,pmin in zip(data1.P,data1.PMIN):
    #     if pmin!=0:
    #         res1.append(p/pmin)
    #     else: res1.append(0)
    # res7.sort()
    # res1.sort()
    #
    # plt.scatter(range(len(res7)),np.log(res7),color='darkgreen',s=1)
    # # plt.scatter(range(min(data1.ID),min(data1.ID)+len(res1)),np.log(res1),color='darkred',s=1,label='Ela 10')
    # plt.axhline(np.log(1),color='grey',linestyle='--')
    # plt.axhline(np.log(3),color='grey',linestyle='--')
    # plt.text(50,np.log(1)+0.1,s='$P/P_{min} = 1$',color='grey')
    # plt.text(50,np.log(3)+0.1,s='$P/P_{min} = 3$',color='grey')
    # # plt.legend()
    # plt.ylabel('log$(P/P_{min})$')
    # plt.xlabel('Sorted ID')
    # plt.show()
    ###############################################

    ########## angles ############################
    # plt.scatter(360-data7.ATGF,data7.AP,color='violet',label='CG$+$',s=4)
    # plt.scatter(360-data7.ATGF,data7.AN,color='green',label='CG$-$',s=4)
    # # plt.scatter(360-data1.ATGF,data1.AP,color='purple',label='CG$+$ Ela 10 ',s=4)
    # # plt.scatter(360-data1.ATGF,data1.AN,color='darkslategrey',label='CG$-$ Ela 10 ',s=4)
    #
    # plt.plot(range(360),range(360),color='grey',linestyle='--')
    # plt.plot(range(180),range(180,360),color='grey',linestyle='--')
    # plt.plot(range(180,360),range(180),color='grey',linestyle='--')
    #
    # plt.xlabel('$360^{\circ} - A_{tgf}$')
    # plt.ylabel('A')
    # plt.legend()
    # plt.show()
    ##############################################

    ########### histograms of p ################
    # print(np.mean(data1.P[data1.GEOG==0]))
    # print(np.mean(data7.P[data7.GEOG==0]))
    #
    # print(len(data7.P[data7.GEOG==2]))
    # print(len(data1.P[data1.GEOG==2]))

    ax0 = plt.subplot(121)
    ax0.hist(data7.P,200,color='grey',label='total',alpha=0.5)
    ax0.hist(data7.P[data7.GEOG==1],200,color='green',label='coastline',alpha=0.5)
    ax0.hist(data7.P[data7.GEOG==2],150,color='red',label='continent',alpha=0.5)
    ax0.hist(data7.P[data7.GEOG==0],100,color='blue',label='ocean',alpha=0.5)
    ax0.legend()
    ax0.set_ylabel('Quantity')
    ax0.set_xlabel('$P$, $C\cdot km$')

    ax1 = plt.subplot(122)
    ax1.hist(data7.PMIN,100,color='grey',label='total',alpha=0.5)
    ax1.hist(data7.PMIN[data7.GEOG==1],100,color='green',label='coastline',alpha=0.5)
    ax1.hist(data7.PMIN[data7.GEOG==0],100,color='blue',label='ocean',alpha=0.5)
    ax1.hist(data7.PMIN[data7.GEOG==2],100,color='red',label='continent',alpha=0.5)
    ax1.set_ylabel('Quantity')
    ax1.set_xlabel('$P_{min}$, $C\cdot km$')

    # ax2 = plt.subplot(223,sharex=ax0)
    # ax2.hist(data1.P*5.04,250,color='grey',label='total',alpha=0.5)
    # ax2.hist(data1.P[data1.GEOG==1]*5.04,200,color='green',label='coastline',alpha=0.5)
    # ax2.hist(data1.P[data1.GEOG==0]*5.04,15,color='blue',label='ocean',alpha=0.5)
    # ax2.hist(data1.P[data1.GEOG==2]*5.04,80,color='red',label='continent',alpha=0.5)
    # ax2.set_ylabel('Quantity')
    # ax2.set_xlabel('$P$, $C\cdot km$')
    #
    # ax4 = plt.subplot(224,sharex=ax1)
    # ax4.hist(data1.PMIN*5.04,50,color='grey',label='total',alpha=0.5)
    # ax4.hist(data1.PMIN[data1.GEOG==1]*5.04,50,color='green',label='coastline',alpha=0.5)
    # ax4.hist(data1.PMIN[data1.GEOG==0]*5.04,25,color='blue',label='ocean',alpha=0.5)
    # ax4.hist(data1.PMIN[data1.GEOG==2]*5.04,20,color='red',label='continent',alpha=0.5)
    # ax4.set_ylabel('Quantity')
    # ax4.set_xlabel('$P_{min}$, $C\cdot km$')

    plt.show()
    ##############################################

    ############## day night p min ##############
    # print(np.mean(data7.PMIN[abs(data7.DC)<0.001]))

    # plt.hist(data7.PMIN[abs(data7.DC)>0.99],40,color='orange',label='day',alpha=0.5)
    # plt.hist(data7.PMIN[abs(data7.DC)<0.001],40,color='darkblue',label='night',alpha=0.5)
    # plt.ylabel('Quantity')
    # plt.xlabel('$P_{min}$, $C\cdot km$')
    # plt.legend()
    # plt.show()
    ###############################################

    ################ c(r) ##########################
    # # ax1 = plt.subplot(121)
    # plt.scatter(data7.DIST,(data7.CR**2)**0.5,c=abs(data7.DC),label='d/n',cmap=plt.cm.rainbow)
    # # ax1.set_ylabel('$c(r)$')
    # # ax1.set_xlabel('$r$, $km$')
    #
    # # plt.subplot(122,sharey=ax1)
    # plt.scatter(data1.DIST,(data1.CR**2/304.9*51.8)**0.5,c=abs(data1.DC),label='d/n')
    # plt.ylabel('$c(r)$')
    # plt.xlabel('$r$, $km$')
    # plt.colorbar(label='Day coefficient')
    # plt.show()
    ##############################################

    ################ c(r) ##########################
    # plt.scatter(data7.DIST,data7.CR,c=abs(data7.DC),label='d/n',cmap=plt.cm.rainbow)
    # plt.ylabel('$c(r)$')
    # plt.xlabel('$r$, $km$')
    # plt.colorbar(label='Day coefficient')
    # plt.show()
    ##############################################

    # for id in data1.ID:
    #     plt.errorbar(data7.P[data7.ID==id],data1.P[data1.ID==id]*5.04,
    #                  yerr=data1.PMIN[data1.ID==id]*5.04,xerr=data7.PMIN[data7.ID==id],
    #                  color='blue',fmt='--o',ecolor='grey', capthick=2)
    # plt.plot(range(int(max(data1.P))),range(int(max(data1.P))),color='black',linestyle='--')
    # plt.ylabel('Ela 10 $P$, $C\cdot km$')
    # plt.xlabel('Ela7 $P$, $C\cdot km$')
    # plt.show()

    # plt.scatter(data7.COUNTS[abs(data7['DC'])>0.99],data7.BP[abs(data7['DC'])>0.99],color='orange')
    # plt.scatter(data7.COUNTS[abs(data7['DC'])<0.001],data7.BP[abs(data7['DC'])<0.001],color='darkblue')
    # plt.show()

    #################### delta ##################
    # plt.errorbar(data7.DIST,data7.DELTA,yerr=[data7.DELTA-data7.DN+1/175.96*1e3,data7.DD-data7.DELTA+1/175.96*1e3],fmt='o',capsize=2,color='grey',zorder=0,alpha=0.5)
    # plt.errorbar(data7.DIST,data7.DELTA,yerr=[data7.DELTA-data7.DN,data7.DD-data7.DELTA],fmt='o',capsize=2,color='black',zorder=1,alpha=0.5)
    # plt.scatter(data7.DIST,data7.DELTA,c=abs(data7.DC),cmap=plt.cm.rainbow,zorder=2)
    # plt.xlabel('$r$, km')
    # plt.ylabel('Delta, ms')
    # plt.colorbar(label='Day coefficient')
    # plt.show()
    ###############################################

    plt.scatter(data7.P[abs(data7.DC)>0.99],data7.COUNTS[abs(data7.DC)>0.99],color='blue')
    plt.scatter(data7.P[abs(data7.DC)<0.01],data7.COUNTS[abs(data7.DC)<0.01],color='green')
    plt.show()


    # print(len(data7.ID[data7.AN>data7.ATGF-20][data7.AN>data7.ATGF+20]))
