# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 14:49:17 2018

@author: lilee
"""

#Eeway_zhu_token
#8bcbc4cad87b526848b20ce1fcb75af216953fa922000772234d8038
import tushare as ts

ts.set_token('8bcbc4cad87b526848b20ce1fcb75af216953fa922000772234d8038')#自己的token
pro = ts.pro_api()
pro.stock_basic(exchange_id='', fields='symbol,name,list_date,list_status')#获取基础列表