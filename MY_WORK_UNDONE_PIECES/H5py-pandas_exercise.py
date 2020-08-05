# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:10:02 2018

@author: lilee
"""

import h5py
import numpy as np
import pandas as pd

f=h5py.File(r'C:/Users/lilee/Desktop/fujie_de_jijin.hdf5','a')

def print_name(name):
    print(name)

file_list=[]
f.visit(file_list.append)
file_list=file_list[:-2]

first_fund_routes=file_list[0:3]

#numpy法清除缺失成分
#——————————————————————————————————————抓出目标基金并清理部分——————————————————————————
def wesh_blank_target_fund(start):#最多678
    start=start*3-3
    #定位
    first_fund_routes=file_list[start:start+3]
    target_fund_array=f[first_fund_routes[2]][...]
    #target_fund_array=f[r'%s/%s/target_fund'%(i_index,i_name)][...]
    #找出''
    #target_fund_del_index=np.argwhere(target_fund_array=='').T[0]
    #删掉''
    #target_fund_array=np.delete(target_fund_array,target_fund_del_index,axis=0)
    #print(target_fund_array)
    return target_fund_array
#————————————————————————————————————————df化——————————————————————————————————
def creat_dataframe_fund(target_fund_array):
    target_fund_array_info=target_fund_array
#    fill_line=len(target_fund_array_fee)
#    for i in range(0,fill_line-3):
#        target_fund_array_info=np.vstack((target_fund_array_info,['','']))
    #添加抬头
    target_fund_info_dict=dict(zip(range(0,len(target_fund_array_info)),target_fund_array_info))
    target_fund_df_info=pd.DataFrame(target_fund_info_dict,index=['属性','值'])
    return target_fund_df_info

#————————————————————————————————————————字符定位器部分——————————————————————————————————
def string_find_lister(target_string,tag_0,i_start=0):
    tag_apear_seq=[]
    while i_start!=-1:
        i_start=i_start+1
        i_start=target_string.find(tag_0,i_start)
        tag_apear_seq.append(i_start)
    tag_apear_seq=tag_apear_seq[:-1]
    return tag_apear_seq

#————————————————————————————————————————文字解析器部分————————————————————————————————

'''
#比方说：
target_string='申购金额(M)M<100万元,费率1.5%;100万元≤M<500万元,费率1.2%;500万元≤M<1000万元,费率0.8%;M≥1000万元,每笔1000元。'
#以及：
target_string='持有期限(N),N＜7日，费率为1.5%,N≥7日，费率为0.5%。'
#思路，先查找有没有分号；≥，其他符号错，这两个符号很少有错
#二者都有必然是分档费率说明有分档
#必然是第二个M/N起头,['持有期限','申购金额'],断是按资金还是按天数
#按金额尝试'M<100万'[:],['M','万'],'费率(为)1.5%'[-4:],['费率','%']
#按日尝试'N＜7日'[:],['N','日'],'费率(为)1.5%'[-4:],['费率','%']
#可用api为str.find('m',从第几个位置开始)m,str to listp;j'MN
'''
tag_lower=r'≤'
tag_higher=r'＜'
tag_money=[r'M',r'万']
tag_day=[r'N','日']
tag_fee=[r'费率','%']
tag_semicolon=[r'；',r';']
tag_comma=[r'，',r',']
tag_buyer=['特定投资群体','其他投资者','养老金客户']
tag_top=[r'M≥']
#________________________________________录入人员习惯太坑了不做了————————————————————————————————————————————

sample_df=creat_dataframe_fund(wesh_blank_target_fund(1))

for i in range(2,679):
    sample_df=sample_df.append(creat_dataframe_fund(wesh_blank_target_fund(i)))
    print(i)

sample_df.to_excel('C:/Users/lilee/Desktop/爬取结果.xlsx')
    
    
    

                
            
            
        
        
    
    
    
    