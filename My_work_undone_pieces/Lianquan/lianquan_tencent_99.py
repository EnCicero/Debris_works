# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 18:46:37 2018

@author: lilee
"""

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import ctime,sleep
from datetime import datetime


'''文件写入'''
source_excel=pd.read_excel('D:/99/2018年99公益日项目征集表-0709.xlsx','项目列表')


'''清理错误'''
def qq_filter(qq_string):
    try:
        return 'gongyi.qq.com/succor' in qq_string
    except:
        return False

source_excel_traget=source_excel[source_excel['上线项目名称/链接'].notnull()]
source_url=source_excel_traget['上线项目名称/链接']
url_list=np.array(source_url)

qq_target_index=map(qq_filter,url_list)
qq_target_index=list(qq_target_index)
source_url=source_url[qq_target_index]
qualified_qq_url=url_list[qq_target_index]
qualified_excel_traget=source_excel_traget[qq_target_index].drop(['专项基金/专项合作名称','机构名称','机构名称','筹款目标（万）','上线目标'],axis=1)


driver=webdriver.Firefox()
driver.implicitly_wait(5)


'''腾讯数据表单部分'''



'''预设index'''
project_name_index=['项目名称']
policy_supporter_index=['发起方','执行方','公募支持']
project_date_index=['开始时间','结束时间']
project_phase_index=['发起','审核','募款','执行','结束']
founding_index=['目标金额','已筹金额','差额','完成百分比','捐款人数']
qq_df_columns=['url']+project_name_index+policy_supporter_index+project_date_index+['项目阶段']+founding_index


'''项目名称'''
def qq_find_project_name():  
    return [driver.find_element_by_xpath('//*[@id="pj_name"]').text]
'''项目时间+时间格式清洗'''

def qq_find_project_date():
    date_strat_end=driver.find_element_by_xpath('//*[@class="main_top_detail_target_time_value"]').text.split(' 至 ')
    return [pd.Timestamp(datetime.strptime(date_strat_end[0],'%Y-%m-%d')),pd.Timestamp(datetime.strptime(date_strat_end[1],'%Y-%m-%d'))]

'''项目进度+表单清洗'''
def proj_proc_loc(project_phase_list,project_phase_index=project_phase_index):
    try:
        i=project_phase_list.index('completed current')
    except:
        i=project_phase_list.index('not_completed current')
    return [project_phase_index[i]] 
def qq_find_project_procedure():
    project_procedure_1=driver.find_element_by_xpath('//*[@id="status_tips1"]').get_attribute('class')#项目进度
    project_procedure_2=driver.find_element_by_xpath('//*[@id="status_tips2"]').get_attribute('class')
    project_procedure_3=driver.find_element_by_xpath('//*[@id="status_tips3"]').get_attribute('class')
    project_procedure_4=driver.find_element_by_xpath('//*[@id="status_tips4"]').get_attribute('class')
    project_procedure_5=driver.find_element_by_xpath('//*[@id="status_tips5"]').get_attribute('class')
    return proj_proc_loc([project_procedure_1,project_procedure_2,project_procedure_3,project_procedure_4,project_procedure_5])
'''筹款进度'''
def qq_find_founding():
    founding_already=float(driver.find_element_by_xpath('//*[@id="money_already"]').text)
    founding_target=float(driver.find_element_by_xpath('//*[@id="target_span"]').text)
    founding_balance=np.array([founding_already-founding_target,0]).max()
    founding_peicernt=founding_target/founding_already
    founding_donator_num=int(driver.find_element_by_xpath('//*[@id="project_donateNum"]').text)
    return [founding_already,founding_target,founding_balance,founding_peicernt,founding_donator_num]
'''三方信息'''
def qq_find_policy_supporter():
    policy_supporter_initiater=driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[1]/dl/dd').text
    policy_supporter_executer=driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/dl/dd').text
    policy_supporter_public_offer=driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[3]/dl/dt').text
    return [policy_supporter_initiater,policy_supporter_executer,policy_supporter_public_offer]

'''动手抓取'''
def qq_clawing(url):
    driver.get(url)
    try:
        driver.find_element_by_xpath('//*[@href="http://gongyi.qq.com/jjhgy/index.htm"]')
        return [url]+qq_find_project_name()+qq_find_policy_supporter()+qq_find_project_date()+qq_find_project_procedure()+qq_find_founding()
        
    except:
        return np.nan
        print (['网址格式不规范,不接受微信地址,请手动填写'])
    driver.switch_to_window(driver.window_handles[0])
    

    

qq_content=list(map(qq_clawing,qualified_qq_url))
print(qq_content)

qq_dataframe=pd.DataFrame(qq_content,columns=qq_df_columns,index=source_url.index)
pd.merge(qq_dataframe,qualified_excel_traget,left_on='url',right_on='上线项目名称/链接').to_excel('D:/Eeway zhu/99整理.xls','99')








