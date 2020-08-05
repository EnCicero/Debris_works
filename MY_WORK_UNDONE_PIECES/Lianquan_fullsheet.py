# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 14:20:45 2018

@author: lilee
"""

import numpy as np
import pandas as pd
from datetime import datetime
import re

ts_now=pd.Timestamp(datetime.now())

timedelta_day=pd.Timedelta(weeks=0,days=0,hours=24,minutes=0,seconds=0)
timedelta_month=pd.Timedelta(weeks=0,days=30,hours=0,minutes=0,seconds=0)
timedelta_year=pd.Timedelta(weeks=52,days=1,hours=0,minutes=0,seconds=0)

origin_excel=pd.read_excel('E:/99/2018联劝公益专项合作汇总表.xlsx','进行中项目')
origin_excel_to_deal=pd.read_excel('E:/99/2018联劝公益专项合作汇总表.xlsx','待处理项目')
origin_excel_over_deal=pd.read_excel('E:/99/2018联劝公益专项合作汇总表.xlsx','已终结项目')

source_excel=origin_excel.loc[origin_excel[['设立时间','合作周期']].dropna().index]

def find_contract_year(string_1):
    contract_value=re.split('\D',string_1.strip())
    while '' in contract_value:
        contract_value.remove('')
    return int(contract_value[0])

source_excel['签约时长']=source_excel['合作周期'].apply(find_contract_year)
source_excel['到期时间']=source_excel['设立时间']+source_excel['签约时长']*timedelta_year
target_excel=source_excel.loc[source_excel['到期时间']<=ts_now]
target_excel_rest=source_excel.loc[source_excel['到期时间']>ts_now]


writer_rpt = pd.ExcelWriter('E:/Eeway zhu/总表过期整理.xls')

origin_excel.to_excel(writer_rpt,'进行中项目')
target_excel_rest.to_excel(writer_rpt,'已过滤项目')
target_excel.to_excel(writer_rpt,'新近过期项目')
origin_excel_to_deal.to_excel(writer_rpt,'待处理项目')
origin_excel_over_deal.to_excel(writer_rpt,'已终结项目')
writer_rpt.save()

