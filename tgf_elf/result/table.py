import pandas as pd
import numpy as np

if __name__ == '__main__':
    data = pd.read_table('/home/foxy/Documents/result_Ela7_180606.txt',sep='\t',index_col=False)
    data = data[:100]
    with open('/home/foxy/Documents/image_diploma/result.csv','w') as f:
		if res is not None:
			f.write("%d\t%f\t%f\t%s\t%d\t%d\t%f\t%d\t%f\t%d\t%d\t%d\t%f\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n" % (idd,args.lon,args.lat,str(args.datetime),counts,geog,dur,res['dist'], \
			 res['day coef'],res['calc dd'],res['calc dn'],res['real delay'], \
			 res['B pulse'],res['B noise'],res['c(r)'],res['P'],res['P min'],res['Ap'],res['An'],res['A']))
