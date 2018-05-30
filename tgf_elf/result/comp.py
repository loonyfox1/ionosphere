from __future__ import division
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data7 = pd.read_table('/home/foxy/Documents/result_Ela7_180529.txt')
data1 = pd.read_table('/home/foxy/Documents/result_Ela10_180529.txt')

# for id in data1.ID:
#     try:
#         print(data7.P[data7.ID==id].values[0],data1.P[data1.ID==id].values[0])
#         # plt.scatter(id,data7.P[data7.ID==id],color='red')
#         # plt.scatter(id,data1.P[data1.ID==id],color='blue')
#         plt.scatter(data7.P[data7.ID==id].values[0],data1.P[data1.ID==id].values[0],color='blue')
#     except:
#         pass
# plt.plot(range(700),range(700),color='black')
# plt.show()

# plt.subplot(2,2,1)
# for id in data1.ID:
#     try:
#         # print(data7.DELTA[data7.ID==id].values[0],data1.DELTA[data1.ID==id].values[0])
#         plt.scatter(data7.DELTA[data7.ID==id].values[0],data1.DELTA[data1.ID==id].values[0],color='blue')
#     except:
#         pass
# plt.plot(range(100),range(100),color='black')
# plt.xlabel('ELA 7')
# plt.ylabel('ELA 10')
# plt.title('DELTA')
#
# plt.subplot(2,2,2)
# for id in data1.ID:
#     try:
#         # print(data7.BP[data7.ID==id].values[0],data1.BP[data1.ID==id].values[0])
#         plt.scatter(data7.BP[data7.ID==id].values[0],data1.BP[data1.ID==id].values[0],color='blue')
#     except:
#         pass
# plt.plot(range(100),range(100),color='black')
# plt.xlabel('ELA 7')
# plt.ylabel('ELA 10')
# plt.title('BP')

# plt.subplot(2,2,3)
res = []
for id in data1.ID:
    try:
        res.append((data1.CR[data1.ID==id].values[0]/data7.CR[data7.ID==id].values[0])**2)
        plt.scatter(data7.CR[data7.ID==id].values[0],data1.CR[data1.ID==id].values[0],color='blue')
    except:
        pass
plt.plot(range(30000),range(30000),color='black')
plt.xlabel('ELA 7')
plt.ylabel('ELA 10')
plt.title('CR')
plt.show()

# plt.plot(res)
plt.scatter(range(len(res)),res)
plt.show()
# plt.subplot(2,2,4)
# for id in data1.ID:
#     try:
#         # print(data7.P[data7.ID==id].values[0],data1.P[data1.ID==id].values[0])
#         plt.scatter(data7.P[data7.ID==id].values[0],data1.P[data1.ID==id].values[0],color='blue')
#     except:
#         pass
# plt.plot(range(900),range(900),color='black')
# plt.xlabel('ELA 7')
# plt.ylabel('ELA 10')
# plt.title('P')

# plt.show()
