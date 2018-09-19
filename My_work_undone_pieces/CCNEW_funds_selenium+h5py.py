# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 21:35:18 2018
@author: lilee
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import ctime,sleep
import h5py
import numpy as np

fund_keys=['code','name','type']

f=h5py.File(r'C:\Users\EP\Desktop\fujie_de_jijin.hdf5','a')
dtype_str=h5py.special_dtype(vlen=str)
try:
    test_fund_file=f.create_group('test_fund_file') 
except:
    test_fund_file=f['/test_fund_file']
test_fund_set=test_fund_file.require_dataset('test_fund',(10,2),dtype=dtype_str)

test_fund_name='【 混合型 】 南方新优享 000527'
test_fund_base=test_fund_name.split(' ')

test_fund_basic=[test_fund_base[4],test_fund_base[3],test_fund_base[1]]
test_fund_dict=dict(zip(fund_keys,test_fund_basic))
test_fund_fee={'定期定额申购费率': '申购金额（M）M＜100万，费率为1.5%；100万≤M＜500万，费率为0.9%；500万≤M＜1000万，费率0.3%；M≥1000万，费用每笔1,000元。', '日常申购费率': '申购金额（M）M＜100万，费率为1.5%；100万≤M＜500万，费率为0.9%；500万≤M＜1000万，费率0.3%；M≥1000万，费用每笔1,000元。', '日常赎回费率': '赎回费(N)N＜7日，费率为1.5%；7日≤N＜30日，费率为0.75%；30日≤N＜1年，费率为0.5%；1年≤N＜2年，费率为0.3%；N≥2年，费率为0。', '转换费率': '基金转换费用由转出基金赎回费用及基金申购补差费用构成。'}
test_fund_dict.update(test_fund_fee)
test_fund_len=len(test_fund_dict.keys())
test_fund_basics=np.array(list(zip(list(test_fund_dict.keys()),list(test_fund_dict.values()))))
for i_val in range(0,test_fund_len):
    test_fund_set[0]=test_fund_basics[0]
    
print('样本基金测试结束')


driver=webdriver.Firefox()

driver.implicitly_wait(5)

driver.get("https://up.ccnew.com/mall/views/fund/index.html")
sleep(1)

total_funds_counts=679
tick_funds_counts=0
target_fund_name=''

funds_content_name_list=[]
funds_content_fee_list=[]
funds_content_total_list=dict()

dt=h5py.special_dtype(vlen=str)

def printname(name):
    print(name)
f.visit(printname) 
    

try:
    for i_page in range(1,114):
        for i_fund in range(1,7):
            
            tick_funds_counts=tick_funds_counts+1
            
            i_fund=str(i_fund)
              
            target_fund_name=driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div["+i_fund+"]/b").text
            
            tick_funds_seq=str(tick_funds_counts)

            print(ctime()+''+target_fund_name+'     第'+tick_funds_seq+'只')
                
            target_fund_base=target_fund_name.split(' ')
            target_fund_basic=[target_fund_base[4],target_fund_base[3],target_fund_base[1]]
            target_fund_list=np.array(list(zip(fund_keys,target_fund_basic)))
            try:
                target_group=f.create_group('/'+tick_funds_seq+'/'+target_fund_basic[1])
            except:
                target_group=f['/'+tick_funds_seq+'/'+target_fund_basic[1]]
            #点击购买
            driver.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div["+i_fund+"]/table/tbody/tr/td[7]/a").click() 
            #睡眠两秒请求一次防屏蔽
            sleep(1)  
            
            driver.switch_to_window(driver.window_handles[1])
             
            #睡眠两秒请求一次防屏蔽
            #点击费率按钮，刷出数据
            txt_th=[]
            txt_td=[]
            fee_content_list=dict()
            
            
            target_fund_fee_list=[]
            #业内抓出表单字段
            try:
                sleep(1)
                txt_no = driver.find_element_by_xpath("//table/tbody/tr[1]/td[@colspan='3']").text
                # 检查是否暂无数据
                print(txt_no)
                txt_th=[txt_no]
                txt_td=[txt_no]
            except:
                print('理当存在表格,抓取数据')
                for i_line in range(1,9):
                    i_line=str(i_line)
                    #睡眠两秒请求一次防屏蔽
                    try:
                        txt_th_txt=''
                        txt_td_txt=''
                        #防错误机制
                        i_try=0
                        while txt_td_txt=='' or txt_th_txt=='':
                                i_try +=1
                                sleep(1)
                                driver.find_element_by_xpath("//ul[@id='detail_ul']/li[2]/b/span").click()
                                txt_th_txt=driver.find_element_by_xpath("//div[@id='detail_ul_zjfl']/table/tbody/tr["+i_line+"]/th").text
                                txt_td_txt=driver.find_element_by_xpath("//div[@id='detail_ul_zjfl']/table/tbody/tr["+i_line+"]/td").text
                                if txt_td_txt!=''and txt_th_txt=='' and i_try>=2:
                                    txt_th_txt='抬头信息缺失'
                                if txt_th_txt!=''and txt_td_txt=='' and i_try>=2:
                                    txt_th_txt='内容信息缺失'
                        txt_td.append(txt_td_txt)
                        txt_th.append(txt_th_txt)
                        #fee_content_list=dict(zip(txt_th,txt_td))
                        print(txt_th[-1]+txt_td[-1])
                    except:
                        print('第%s行不存在,跳过'%i_line)
            try:
                target_fund_fee_list=np.array(list(zip(txt_th,txt_td)))
                print('合并表单')
                target_fund_basics=np.vstack((target_fund_list,target_fund_fee_list))
                target_fund_set=target_group.require_dataset('target_fund',(10,2),dtype=dtype_str)
                target_fund_len=len(target_fund_basics)
                for i_val in range(0,target_fund_len):
                    target_fund_set[i_val]=target_fund_basics[i_val]
            except:
                pass
            #funds_content_fee_list.append(fee_content_list)
            print('准备换标的')       
            driver.close()

            print('冲洗文件') 
            f.flush()
            
            driver.switch_to_window(driver.window_handles[0])
            
            if tick_funds_counts==total_funds_counts:
                break
        if tick_funds_counts==total_funds_counts:
            break
        
        driver.find_element_by_xpath("//*[@id='next_page']").click()
        print('点击换页')

        sleep(1) 

except NoSuchElementException as e:
    print(e)
finally:
    print(ctime())
    

f.visit(printname)    
f.flush()
f.close()