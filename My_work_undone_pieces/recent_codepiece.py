# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:26:32 2018

@author: Eeway
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:13:16 2018

@author: Eeway
"""

import tushare as ts

from tkinter import Tk, Scrollbar, Frame ,Label,StringVar,Button
from tkinter.ttk import Treeview

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_finance import candlestick_ohlc
from matplotlib.dates import DateFormatter,WeekdayLocator,DayLocator,MONDAY,date2num

from datetime import datetime
import time 

class k_line(Frame):
    msec=500
    figure_default=Figure(figsize=(5,4),dpi=100) 
    sample_k_line_list=[]
    pic=figure_default.add_subplot(111)
    code='sh'
    _day=20
    def __init__(self,parent=None,**kw):
            Frame.__init__(self, parent, kw)
            self._running = False
            self.flag  = True
            self.timestr1 = StringVar()
            self.timestr2 = StringVar()
            self.make_Widgets()
            self.get_k_line_data(self._day)
    def get_k_line_data(self,day):
        sample_k=ts.get_k_data(str(self.code))
        sample_k_copy=sample_k.copy().iloc[:,:-1].tail(day)
        _close=sample_k_copy['close']
        sample_k_copy.drop(labels='close',axis=1,inplace=True)
        sample_k_copy.insert(4,'close',_close)
        sample_k_copy.date=[date2num(datetime.strptime(date,"%Y-%m-%d"))  for date in sample_k_copy.date]
        sample_k_copy_list=list()
        for i in range(len(sample_k_copy)):
            sample_k_copy_list.append(sample_k_copy.iloc[i,:]) 
        self.sample_k_line_list=sample_k_copy_list
    def get_real_time_quote_k_data(self):
        real_time_quote_k_data=ts.get_realtime_quotes(str(self.code))
        real_time_quote_k_data.date=[date2num(datetime.strptime(date,"%Y-%m-%d"))  for date in real_time_quote_k_data.date]
        real_time_quote_k_data.rename(columns={'price':'close'},inplace=True)  
        _date=real_time_quote_k_data.pop('date')
        _close=real_time_quote_k_data.pop('close')
        real_time_quote_k_data.insert(0,'date',_date)
        real_time_quote_k_data.insert(6,'close',_close)
        real_time_quote_k_data_copy=real_time_quote_k_data.loc[0,[i for i in real_time_quote_k_data.columns if i in['date','open','high','low','close','volume']]].copy()
        real_time_quote_k_data_copy=real_time_quote_k_data_copy.astype(np.float64)
        if self.sample_k_line_list[-1].date == real_time_quote_k_data_copy.date:
            self.sample_k_line_list[-1]=real_time_quote_k_data_copy
        else : self.sample_k_line_list.append(real_time_quote_k_data_copy)
    def make_Widgets(self):
        l1 = Label(self, textvariable = self.timestr1)
        l2 = Label(self, textvariable = self.timestr2)
        l1.grid(row=1,column=1)
        l2.grid(row=1,column=2)
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False
    def draw_k_line(self):
        self.get_real_time_quote_k_data()
        self.figure_default.clf()
        self.pic=self.figure_default.add_subplot(111)
        mondays = WeekdayLocator(MONDAY)
        weekFormatter=DateFormatter('%y %b %d')
        self.pic.xaxis.set_major_locator(mondays)
        self.pic.xaxis.set_minor_locator(DayLocator())
        self.pic.xaxis.set_major_formatter(weekFormatter)
        self.pic.set_title('投资组合净值趋势') 
        candlestick_ohlc(self.pic,self.sample_k_line_list,width=0.7,colorup='r',colordown='g')
        plt.setp(self.pic.get_xticklabels(),rotation=30,horizontalalignment='center',fontsize=8)
        self.canvas.show()
    def _update(self):
        self._settime()
        self.draw_k_line()
        self.timer = self.after(self.msec, self._update)
    def _settime(self):
        today1 = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        time1 = str(time.strftime('%H:%M:%S', time.localtime(time.time())))
        self.timestr1.set(today1)
        self.timestr2.set(time1)
    def start(self):
        self._update() 
        self.grid()
        
class holding_tree_view(Frame):
    _holding=[] 
    def __init__(self,parent=None,**kw):
            Frame.__init__(self, parent, kw)
            self.make_excel_view()
            self.show_holdings()
            self.treeviewClick()
    def get_holdings(self):
        self._holding=list([['300676','华大基因','130.11','10%','30.13%','3.01%'],
                                 ['002230','科大讯飞','43.97','10%','29.77%','2.98%']])
    def show_holdings(self):
        self.get_holdings()
        for i in range(len(self._holding)):        
            self.tree.insert('', i, values=self._holding[i])
    def treeviewClick(self,event=None):
        pass      
    def make_excel_view(self):
        self.scrollBar = Scrollbar(self)
        self.scrollBar.pack(side='right', fill='y')       
          
        self.tree = Treeview(self,columns=('c1', 'c2', 'c3','c4', 'c5', 'c6'),show="headings",yscrollcommand=self.scrollBar.set)        
        
        self.tree.column('c1', width=80, anchor='center')
        self.tree.column('c2', width=80, anchor='center')
        self.tree.column('c3', width=80, anchor='center')
        self.tree.column('c4', width=80, anchor='center')
        self.tree.column('c5', width=80, anchor='center')
        self.tree.column('c6', width=80, anchor='center')
        
        self.tree.heading('c1', text='代码')
        self.tree.heading('c2', text='名称')
        self.tree.heading('c3', text='买入成本历史位置')
        self.tree.heading('c4', text='占组合市值比例')
        self.tree.heading('c5', text='盈亏比例')
        self.tree.heading('c6', text='绩效贡献')
        self.tree.pack(side='left', fill='y')
        
        self.scrollBar.config(command=self.tree.yview)
        self.tree.bind('<Button-1>',self.treeviewClick)
    
    
    
if __name__ =='__main__' :
    def main():     
        root=Tk()
        #root.geometry('800x650')
        root.resizable(False, False)
        root.title('test')
        
        Frame_Default_1=Frame(root,bd=2,relief='groove',width=500)
        Frame_Default_1.grid(row=1,column=1)       
        
        Frame_1=Frame(Frame_Default_1,bd=2,relief='sunken',width=500,height=600)
        Frame_1.pack()
        
        to_k_line=k_line(Frame_1)
        refresher = Button(Frame_1,text = '组合K线图',command = to_k_line.start)
        refresher.grid()
        to_k_line.canvas=FigureCanvasTkAgg(to_k_line.figure_default,Frame_1)
        to_k_line.canvas.show()
        to_k_line.canvas.get_tk_widget().grid()
        
        Label(Frame_Default_1,text='组合持仓').pack()

        Frame_2=Frame(Frame_Default_1,bd=2,relief='sunken',width=500,height=100)
        Frame_2.pack()
        
        to_holdings=holding_tree_view(Frame_2)
        to_holdings.pack()
        

        root.mainloop()
    main()