import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl



def normal_plot(time,dd,dn):
    font = {'size'   : 4}
    mpl.rc('font', **font)
    mpl.rcParams['axes.linewidth'] = 0.3
    mpl.rcParams['lines.linewidth'] = 0.3
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['xtick.major.size'] = 2
    mpl.rcParams['ytick.major.size'] = 2
    mpl.rcParams['xtick.major.width'] = 0.3
    mpl.rcParams['ytick.major.width'] = 0.3

    fig = plt.figure(figsize=(3,4))

    ax1 = fig.add_subplot(4,1,1)
    # ax1.set_xticks(np.arange(-40,81,step=10))
    # ax1.set_xlabel('Time after '+str(time)+' UT [ms]')
    ax1.set_ylabel('Bx [pT]')

    ax2 = fig.add_subplot(4,1,2)
    # ax2.set_xticks(np.arange(-40,81,step=10))
    # ax2.set_xlabel('Time after '+str(time)+' UT [ms]')
    ax2.set_ylabel('By [pT]')

    ax3 = fig.add_subplot(4,1,3)
    # ax3.set_xticks(np.arange(-40,81,step=10))
    # ax3.set_xlabel('Time after '+str(time)+' UT [ms]')
    ax3.set_ylabel('B [pT]')

    ax4 = fig.add_subplot(4,1,4)
    # ax4.set_xticks(np.arange(-40,81,step=10))
    # ax4.set_xlabel('Time after '+str(time)+' UT [ms]')
    ax4.set_ylabel('Azimuth [degree]')

    axarr = [ax1,ax2,ax3,ax4]
    [a.set_xlabel('Time after '+str(time)+' UT [ms]') for a in axarr]
    [a.set_xticks(np.arange(-40,81,step=10)) for a in axarr]
    [a.axvline(0,c='gray') for a in axarr]
    [a.axhline(0,c='black') for a in axarr]

    [a.axvline(dd,c='gray',linestyle='dashed') for a in axarr]
    [a.axvline(dn,c='gray',linestyle='dashed') for a in axarr]

    [a.text(dd,0.7,'day',rotation='vertical',color='grey',fontsize=3,ha='right',va='bottom') for a in axarr]
    [a.text(dn,0.7,'night',rotation='vertical',color='grey',fontsize=3,ha='left',va='bottom') for a in axarr]

    fig.subplots_adjust(top=0.92, bottom=0.08, left=0.12, right=0.95, hspace=0.5,
                    wspace=None)
    fig.savefig('fig1.png', dpi = 300)

    # plt.show ()

if __name__ == '__main__':
    normal_plot(time='07:44:01.779',dd=39,dn=42)
