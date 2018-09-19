# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 10:13:56 2017

@author: 朱翊崴
"""
import os, sys
import pandas as pd
import tushare as ts
import numpy as np
from datetime import datetime
import time

import smtplib  
from email.mime.text import MIMEText  # 引入smtplib和MIMEText  
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

# ———————————————————————简易介绍及路径显示————————————————————
print('这是4年版本预告投资机')
retval = os.getcwd()
# os.chdir( path )
print(retval)
file_basic_location = 'F:/机器人先生/'
file_full_path_yg = file_basic_location + '财务数据/业绩预告基础数据.xlsx'
file_full_path_ls = file_basic_location + '基础数据/股票列表.xlsx'
flie_full_path_hd = file_basic_location + '投资组合/投资组合.xlsx'
flie_full_path_rp = file_basic_location + '数据生产/业绩预告.xlsx'
flie_full_path_tg = file_basic_location + '数据生产/参考标的.xlsx'

# ————————————————————整理列表股票代码（变量_basic结尾）————————————————————————
print('正在准备基本数据')

stock_list = ts.get_stock_basics()
stock_list.to_excel(file_full_path_ls)
stock_list = pd.read_excel(file_full_path_ls)
list_length = len(stock_list)
for i in range(0, list_length):
    code_basic = stock_list.iat[i, 0]
    # 代码整理（IO读写缺陷）
    code_basic = str(code_basic)
    for x in range(1, 6):
        if len(code_basic) == x:
            code_basic = '0' * (6 - x) + code_basic
    stock_list.iloc[i, 0] = code_basic
print('股票列表读取完成,已存入运存')
# ——————————————————————全面时间默认设置（day,end,start,yesterday)—————————————————————
nowt = datetime.today()
# ——————————————————————时间设置——日线数据（5年）——————————————
end = datetime(nowt.year, nowt.month, nowt.day)
start = datetime(end.year - 5, end.month, end.day)

# ——————————————————————今天—————————————————————————
today = datetime(nowt.year, nowt.month, nowt.day)
if nowt.day == 1 and nowt.month != 1:
    yesterday = datetime(nowt.year, nowt.month - 1, nowt.day)
elif nowt.day == 1 and nowt.month == 1:
    yesterday = datetime(nowt.year - 1, nowt.month, nowt.day)
else:
    yesterday = datetime(nowt.year, nowt.month, nowt.day - 1)
# ——————————————————————字符串化———————————————————————
end = str(end)[0:10]
start = str(start)[0:10]
today = str(today)[0:10]
yesterday = str(yesterday)[0:10]
# ——————————————————————常用日期———————————————————————
day_set = datetime(2017, 1, 1)
day_yes = datetime(2016, 12, 31)  # 默认
delta = day_set - day_yes
today = datetime.today()
day_before_yesterday = today - delta
day_dby = day_before_yesterday
# ——————————————————————持仓统计———————————————————————

sequence = list(np.arange(0, 30))  # 预设，默认30个
holding_tag = ['code', 'name', 'changepercent', 'P/L_pct', 'stock_a', 'stock', 'reference_cost', 'price',
               'market_value', 'P/L']
holding = pd.DataFrame(index=sequence, columns=holding_tag)
print('正在写入投资组合')  # 写入后覆盖
holding = pd.read_excel(flie_full_path_hd)
# —————————————————————排序清理—————————————————————————

holding['index'] = list(range(0, len(holding)))
holding.set_index('index', inplace=True)

# ——————————————————————持仓代码整理（变量_hd结尾）————————————————————————
for i in range(0, len(holding)):
    code_hd = holding.loc[i, 'code']
    code_hd = str(code_hd)
    for x in range(1, 6):
        if len(code_hd) == x:
            code_hd = '0' * (6 - x) + code_hd
    holding.iloc[i, 0] = code_hd
# ——————————————————————开启程序交易信息更新_非实时高频（变量_update结尾）————————————
print('正在更新投资组合信息')
for i in range(0, len(holding)):
    nowt = datetime.today()
    code_update = holding.loc[i, 'code']
    name_update = stock_list.loc[stock_list.loc[:, 'code'] == code_update].iloc[0, 1]
    holding.loc[i, 'name'] = name_update
    # 3当日涨跌changepercent——仅此函数
    dyna_info = pd.read_excel(file_basic_location + '交易数据/股票日线/%s' % code_update + '.xlsx' )
    dyna_info_cal = dyna_info.tail(2)  # 取最近两天（防停牌）
    dyna_info_today = dyna_info.loc[dyna_info.loc[:, 'date'] == today]  # 取当天（如果取的到）
    if dyna_info.empty:
        holding.loc[i, 'changepercent'] = '停牌'
    else:
        change_percent_cal = (dyna_info_cal.iloc[1, 2] - dyna_info_cal.iloc[0, 2]) / dyna_info_cal.iloc[0, 2]
        holding.loc[i, 'changepercent'] = change_percent_cal
    # 5 可用股数——做进交易函数
    # 6 持有股数——做进交易函数
    # 7 平均成本——做进交易函数
    # 4 盈利比率——做进交易函数和本函数
    holding.loc[i, 'P/L_pct'] = (dyna_info_cal.iloc[1, 2] - holding.loc[i, 'reference_cost']) / holding.loc[
        i, 'reference_cost']
    # 8 现价——仅做到这个函数里
    holding.loc[i, 'price'] = dyna_info_cal.iloc[1, 2]
    # 9 市值——仅做到这个函数和交易函数
    holding.loc[i, 'market_value'] = dyna_info_cal.iloc[1, 2] * holding.loc[i, 'stock']
    # 4 盈利数值—做进交易函数和本函数
    holding.loc[i, 'P/L'] = (dyna_info_cal.iloc[1, 2] - holding.loc[i, 'reference_cost']) * holding.loc[i, 'stock']
    # 更新并保存
holding = holding.fillna(0)
holding.to_excel(flie_full_path_hd)


# ——————————————————————交易函数(预设，面对对象）————————————————————————
#     name_cal=stock_list.loc[stock_list.loc[:,'code']==code_hd].iloc[0,1](比较精密的语句）
class stock_to_trade(object):
    share = 0

    # 设置交易必须的参数
    def __init__(self, code, price):
        self.code = code
        self.price = price

    # 买入做多
    def buy(self, share):
        self.share = holding.loc[holding.loc[:, 'code'] == code_tra].iloc[0, 5]
        self.share += share
        index_target = list(holding['code']).index(code_tra)
        holding.loc[index_target, 'stock'] = self.share

    # 限制卖空
    def sell(self, share):
        self.share = holding.loc[holding.loc[:, 'code'] == code_tra].iloc[0, 4]
        if self.share >= share:
            self.share -= share
            index_target = list(holding['code']).index(code_tra)
            holding.loc[index_target, 'stock'] -= share
            holding.loc[index_target, 'stock_a'] = self.share
        else:
            print('超出可用，中国T+1交易')
            return


# ——————————————————————判断系统————————————————————————




# —————————————————————面向用户程序部分开始————————————————————————



while 1:
    print('\r\n你要做什么？\r\n1数据维护\r\n2分析系统\r\n3投资组合交易\r\n4发邮件\r\n0回到初始界面退出\r\n（分析前必须确认当天数据已更新)')
    trigger_layer_1 = input()
    trigger_layer_2 = '0'
    # ————————————————————————————模块1-数据维护————————————————————————
    if trigger_layer_1 == '1' or trigger_layer_1 == 'A' or trigger_layer_1 == 'A0':

        while 1:
            print('\r\n -Tushare:1——业绩预告，2——历史业绩，3——5年日线，4--T+1整理，其他返回——')
            # ——————————————————自动化开关———————————————————————
            if trigger_layer_1 == '1':
                trigger_layer_2 = input()
            # ——————————————————获取业绩预告数据，本地存储（变量结尾_fr）————————————————
            if trigger_layer_2 == '1' or trigger_layer_1 == 'A' or trigger_layer_1 == 'A0':
                # 指令
                print('获取所需数据')
                print('--请输入所需报告所在年数:')
                print('注意提取年报时往前回滚一年')
                print(nowt)
                year_fr = input()
                print('--请输入所需报告所在季度')
                print('*限制为:')
                print('1-一季报(4/30)')
                print('2-中报(8/30)')
                print('3-三季报(10/31)')
                print('4-年报(4/30)')
                # 一年只有4个季节
                season = [1, 2, 3, 4]
                season_fr = input()
                season_fr = int(season_fr)
                season_fr = season[season_fr - 1]
                year_fr = int(year_fr)
                # os.system('cls')清屏
                print('\r\n请不要中断进程，否则后续分析讲出现错误！')
                report_forecast = ts.forecast_data(year_fr, season_fr)
                report_forecast_fro = report_forecast.copy()
                report_forecast_fro.to_excel(file_full_path_yg)

            # ————————————获取历史业绩列表，本地存储——————————————————
            if trigger_layer_2 == '2' or trigger_layer_2 == 'A0':
                if trigger_layer_2 == '2':
                    # 指令
                    print('获取所需数据')
                    print('--请输入所需报告截止年数:')
                    print('注意提取年报时往前回滚一年')
                    print(nowt)
                    year_fr = input()
                    print('--请输入所需报告所在季度')
                    print('*限制为:')
                    print('1-一季报(4/30)')
                    print('2-中报(8/30)')
                    print('3-三季报(10/31)')
                    print('4-年报(4/30)')
                    # 一年只有4个季节
                    season = [1, 2, 3, 4]
                    season_fr = input()
                    season_fr = int(season_fr)
                    season_fr = season[season_fr - 1]
                    year_fr = int(year_fr)
                # os.system('cls')清屏
                # —————————————获取三年市场业绩数据，本地存储——————————————
                writer_rpt = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/业绩主表.xlsx')
                writer_pro = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/盈利主表.xlsx')
                writer_opr = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/营运主表.xlsx')
                writer_gro = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/成长主表.xlsx')
                writer_dbt = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/偿债主表.xlsx')
                writer_cfl = pd.ExcelWriter(file_basic_location + '财务数据/表格分类/现金流主表.xlsx')
                # ——————————————————制作储存器（变量_seq结尾）——————————————————
                rpt_seq = []
                pro_seq = []
                opr_seq = []
                gro_seq = []
                dbt_seq = []
                cfl_seq = []
                k = 0
                for i in range(year_fr - 4, year_fr + 1):
                    # 5年
                    for j in season:
                        # 四个季度
                        if i == year_fr and j == season_fr:
                            # 交互式调节
                            break
                        print('\r\n%s' % i + '年第%s季度' % j)  # 进度条
                        # ——————————————————tushare调取——————————————————
                        rpt = ts.get_report_data(i, j)
                        print('主表 ')
                        pro = ts.get_profit_data(i, j)
                        print('利润')
                        opr = ts.get_operation_data(i, j)
                        print('运营')
                        gro = ts.get_growth_data(i, j)
                        print('成长')
                        dbt = ts.get_debtpaying_data(i, j)
                        print('债务')
                        cfl = ts.get_cashflow_data(i, j)
                        print('现金流')
                        # ——————————————————陈列置入储存器——————————————————
                        rpt_seq.append(rpt)
                        pro_seq.append(pro)
                        opr_seq.append(opr)
                        gro_seq.append(gro)
                        dbt_seq.append(dbt)
                        cfl_seq.append(cfl)

                        # ——————————————————按期分类————————————————————
                        rpt_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度主表' % j + '.xlsx')
                        pro_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度利润表' % j + '.xlsx')
                        opr_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度运营表' % j + '.xlsx')
                        gro_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度成长表' % j + '.xlsx')
                        dbt_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度债务表' % j + '.xlsx')
                        cfl_seq[k].to_excel(file_basic_location + '财务数据/季度分类/%s' % i + '年第%s季度现金流' % j + '.xlsx')

                        # ——————————————————标记sheet——————————————————
                        rpt_seq[k].to_excel(writer_rpt, '%s' % i + '年第%s季度' % j)
                        pro_seq[k].to_excel(writer_pro, '%s' % i + '年第%s季度' % j)
                        opr_seq[k].to_excel(writer_opr, '%s' % i + '年第%s季度' % j)
                        gro_seq[k].to_excel(writer_gro, '%s' % i + '年第%s季度' % j)
                        dbt_seq[k].to_excel(writer_dbt, '%s' % i + '年第%s季度' % j)
                        cfl_seq[k].to_excel(writer_cfl, '%s' % i + '年第%s季度' % j)

                        k += 1

                writer_rpt.save()
                writer_pro.save()
                writer_opr.save()
                writer_gro.save()
                writer_dbt.save()
                writer_cfl.save()

            # ————————————获取股票列表数据，本地存储——————————————————
            if trigger_layer_2 == '3' or trigger_layer_1 == 'A' or trigger_layer_1 == 'A0':
                # ——————————————触发指令——————————————————————————

                sl_len = len(stock_list)  # 计数器用途
                print('\r\n请不要中断进程，否则后续分析讲出现错误！')

                # ——————————————获取5年日线数据，本地存储（变量以k_data)——————————————————
                for i in range(0, sl_len):
                    code_k_data = stock_list.iat[i, 0]  # 计数器用途
                    name_k_data = stock_list.iat[i, 1]  # 计数器用途
                    file_full_path_stock = file_basic_location + '交易数据/股票日线/%s' % code_k_data + '.xlsx'  # 计数器
                    percent_stock = (i + 1) / sl_len * 100  # 计数器
                    print(
                        f"正在处理{percent_stock:.2f}" + '%' + ' %s ' % code_k_data + ' %s ' % name_k_data + file_full_path_stock + '  %s/' % (
                            i + 1) + '%s' % sl_len)  # 显示计数器

                    year_price_5 = ts.get_k_data(code_k_data, start, end)
                    year_price_5.to_excel(file_full_path_stock)
                    time.sleep(0.05)

                print('数据获取完成')
                # ————————————————————T+1——————————————————————————
            if trigger_layer_2 == '4' or trigger_layer_1 == 'A':
                holding['stock_a'] = holding['stock']
                # drop_line = report_forecast.loc[report_forecast.loc[:, '平均增长'] <= 0].index(比较精密的语句）
                # report_forecast.drop(drop_line, inplace=True)(比较精密的语句）
                drop_line = holding.loc[holding.loc[:, 'stock'] == 0].index
                holding.drop(drop_line, inplace=True)
                holding.to_excel(flie_full_path_hd)
                print('T+1处理完成')

            print('\r\n退出')
            break
            # 模块2—————————————————————————分析阶段———————————————————————
    if trigger_layer_1 == '2' or trigger_layer_1 == 'A' or trigger_layer_1 == 'A0':
        print('\r\n正在创建计算环境')
        # 开始计算
        # 创建默认值
        # 重置参数

        info_mine = pd.DataFrame()
        mine = pd.DataFrame()
        performance_high = []
        performance_low = []
        peru_30 = []
        peru_90 = []
        avg_0 = []
        avg_60 = []
        avg_120 = []
        avg_250 = []
        tag_long = []
        report_forecast_rank_pf = pd.DataFrame()
        report_forecast_rank_pm = pd.DataFrame()
        info_mine = pd.DataFrame()  # 地雷用
        mine = pd.DataFrame()  # 地雷用
        # ————————————————————整理预告股票代码（变量_ls结尾）—————————————————————
        print('\r\n信息地雷由于接口错误暂时关闭')
        trigger3 = 0
        report_forecast = pd.read_excel(file_full_path_yg)
        report_length = len(report_forecast)
        for i in range(0, report_length):
            code_ls = report_forecast.iat[i, 0]
            # 代码整理（IO读写缺陷）
            code_ls = str(code_ls)
            for x in range(1, 6):
                if len(code_ls) == x:
                    code_ls = '0' * (6 - x) + code_ls
            report_forecast.iloc[i, 0] = code_ls
        print('\r\n业绩预告读取完成')

        # ——————————————————大量循环开始（变量_rp结尾）————————————————————
        for i in range(0, report_length):
            # 计数器
            code_rp = report_forecast.iat[i, 0]
            name_rp = report_forecast.iat[i, 1]
            pst_rp = (i + 1) / report_length * 100
            print('正在计算%.2f' % pst_rp + '%    ' + '%s' % code_rp + ' %s' % name_rp + '    完成%s' % (i + 1))
            time.sleep(0.01)
            # 范围规整化
            report_value = report_forecast.iat[i, 5]
            # 排除数据源格式不统一为字段
            # ——————————————————————业绩的增长范围提取————————————————————————
            report_value = str(report_value)
            if report_value.find('%') != -1 \
                    and report_value.rfind('%') != -1 \
                    and report_value.rfind('%') != report_value.find('%'):
                left_p_tag = report_value.find('%')
                right_p_tag = report_value.rfind('%')
                low_pf_value = report_value[0:left_p_tag]
                high_pf_value = report_value[left_p_tag + 2:len(report_value) - 1]
            elif report_value.find('%') != -1 \
                    and report_value.rfind('%') != -1 \
                    and report_value.rfind('%') == report_value.find('%'):
                left_p_tag = report_value.find('%')
                high_pf_value = report_value[0:left_p_tag]
                low_pf_value = high_pf_value

            else:
                high_pf_value = report_value
                low_pf_value = report_value
            high_pf_value = float(high_pf_value)
            low_pf_value = float(low_pf_value)
            performance_high.append(high_pf_value)
            performance_low.append(low_pf_value)
            # ——————————————————获取日线计算涨幅———————————————————————————
            file_full_path_ss = file_basic_location + '交易数据/股票日线/%s' % code_rp + '.xlsx'
            year_price_5 = pd.read_excel(file_full_path_ss)

            spot_stock = stock_list.loc[stock_list.loc[:, 'code'] == code_rp]
            day_num = spot_stock.iat[0, 15]
            day_num = str(day_num)
            if spot_stock.iat[0, 15] == 0:  # 新上市
                peru_30.append(0.44)  # 当天涨幅，政策预设
                peru_90.append(0.44)  # 当天涨幅，政策预设
                avg_60.append(0)
                avg_120.append(0)
                avg_250.append(0)
                avg_0.append(0)
                avg_val_60 = 0
                avg_val_120 = 0
                avg_val_250 = 0
            else:
                day_set = datetime(int(day_num[0:4]), int(day_num[4:6]), int(day_num[6:8]))  # 新上市2天内
                if day_set > day_dby:
                    peru_30.append(0.44)  # 当天涨幅，同上
                    peru_90.append(0.44)  # 当天涨幅，同上
                    avg_0.append(0)
                    avg_60.append(0)
                    avg_120.append(0)
                    avg_250.append(0)
                    avg_val_0 = 0
                    avg_val_60 = 0
                    avg_val_120 = 0
                    avg_val_250 = 0

                else:
                    # 30天涨幅
                    analysis_up_30 = year_price_5['close'].tail(30).describe()
                    peru_value_30 = (float(year_price_5['close'].tail(1)) - analysis_up_30[3]) / analysis_up_30[3]
                    peru_30.append(peru_value_30)
                    # 90天涨幅
                    analysis_up_90 = year_price_5['close'].tail(90).describe()
                    peru_value_90 = (float(year_price_5['close'].tail(1)) - analysis_up_90[3]) / analysis_up_90[3]
                    peru_90.append(peru_value_90)
                    # 添加均线系统,准备作图（以后）
                    # 现价
                    avg_val_0 = float(year_price_5['close'].tail(1))
                    avg_0.append(avg_val_0)
                    # 60天
                    year_price_5['SMA60'] = year_price_5['close'].rolling(60).mean()
                    avg_val_60 = float(year_price_5['SMA60'].tail(1))
                    avg_60.append(avg_val_60)
                    # 120天
                    year_price_5['SMA120'] = year_price_5['close'].rolling(120).mean()
                    avg_val_120 = float(year_price_5['SMA120'].tail(1))
                    avg_120.append(avg_val_120)
                    # 250天
                    year_price_5['SMA250'] = year_price_5['close'].rolling(250).mean()
                    avg_val_250 = float(year_price_5['SMA250'].tail(1))
                    avg_250.append(avg_val_250)
                    # 多头提示
            if avg_val_0 > avg_val_60 > avg_val_120 > avg_val_250:
                tag_long.append('是')
            else:
                tag_long.append('否')
                # 信息地雷（已关闭）
            if trigger3 == '1':
                code_rp = report_forecast.iat[i, 0]
                mine = ts.get_notices(code_rp)
                mine = mine[mine.index == 0]
                # 竖向相加
                info_mine = pd.concat([info_mine, mine], axis=0)
        # ——————————————————大量循环结束————————————————————
        print('\f')
        print('\r\n数据合并中......')
        # 合并新参数列
        idxseq = list(range(0, report_length))
        report_forecast['最低增长'] = performance_low
        report_forecast['最高增长'] = performance_high
        report_forecast['价格涨幅30天'] = peru_30
        report_forecast['价格涨幅90天'] = peru_90
        report_forecast['索引'] = idxseq
        report_forecast['现价'] = avg_0
        report_forecast['60天均价'] = avg_60
        report_forecast['120天均价'] = avg_120
        report_forecast['250天均价'] = avg_250
        report_forecast['多头标志'] = tag_long

        report_forecast.set_index(keys='索引', inplace=True)

        # 整理
        report_forecast.drop('range', axis=1, inplace=True)  # 扔掉索引，美观用
        report_forecast['业绩平均增长'] = (report_forecast['最低增长'] + report_forecast['最高增长']) / 2
        report_forecast['增长/价格涨幅90'] = report_forecast['业绩平均增长'] / report_forecast['价格涨幅90天']
        # 信息地雷（弃用）
        if trigger3 == '1':
            info_mine['索引'] = idxseq
            info_mine.set_index(keys='索引', inplace=True)
            report_forecast = pd.concat([report_forecast, info_mine], axis=1)
        # 排序
        report_forecast_main = report_forecast.sort_values(by='增长/价格涨幅90', ascending=False)
        report_forecast_rank_pf = report_forecast.sort_values(by='业绩平均增长', ascending=False)
        report_forecast_rank_pm = report_forecast.sort_values(by='价格涨幅90天', ascending=True)
        # 写入
        writer = pd.ExcelWriter(flie_full_path_rp)
        report_forecast.to_excel(writer, '主表')
        report_forecast_main.to_excel(writer, '价比')
        report_forecast_rank_pf.to_excel(writer, '业绩')
        report_forecast_rank_pm.to_excel(writer, '振幅')
        # 本地
        writer.save()
        # 筛选
        # ———————————————————————————————————策略池再处理部分——————————————————————————————————

        drop_line = report_forecast.loc[report_forecast.loc[:, '多头标志'] == '否'].index
        report_forecast_pool=report_forecast.drop(drop_line)
        drop_line2 = report_forecast_pool.loc[report_forecast.loc[:, '业绩平均增长'] <= 15].index
        report_forecast_pool=report_forecast_pool.drop(drop_line2)
        report_forecast_pool.drop(['最低增长','最高增长','60天均价','120天均价','250天均价','价格涨幅30天','价格涨幅90天','多头标志','增长/价格涨幅90'],axis=1,inplace=True)
        in_tag=report_forecast_pool[['code','report_date']].copy()
        def find_price(code_k_data,report_date):
            try:
                find_price_pd=pd.read_excel(file_basic_location + '交易数据/股票日线/%s' % code_k_data + '.xlsx')
                report_date=datetime.strptime(report_date,'%Y-%m-%d')
                report_date=report_date+delta
                if report_date.weekday()==5:
                    report_date=report_date-delta
                if report_date.weekday()==6:
                    report_date=report_date-delta-delta
                report_date=report_date.strftime('%Y-%m-%d')
                price_in= float(find_price_pd.loc[find_price_pd.loc[:,'date']==report_date].close)
                return price_in
            except:
                return ('No Data')
        in_tag['price']=list(map(find_price,in_tag['code'],in_tag['report_date']))
        in_price=in_tag.pop('price')
        report_forecast_pool.insert(5,'预告价',in_price)
        
        #file_basic_location + '交易数据/股票日线/%s' % code_k_data + '.xlsx'  # 计数器
        #in_tag['pr']=list(map(lambda code_k_data:float(pd.read_excel(file_basic_location + '交易数据/股票日线/%s' % code_k_data + '.xlsx').,in_tag['code']))
        #s.loc[s.loc[:,'date']=='2018-01-08'].close

        
        report_forecast_pool.to_excel(flie_full_path_tg)
        # 计数
        print('\r\n报告计算完成,内存已重置,选出标的已写入内存')
    # ————————————————————————模块3交易模块——————————————————————————————————————
    if trigger_layer_1 == '3':

        # ——————————————————————交易动作（预设，变量_tra结尾）————————————————————————
        # self.share=holding.loc[holding.loc[:,'code']==code_tra].iloc[0,5]（精密代码，参考）
        # self.share += share（精密代码，参考）
        # index_target=list(holding['code']).index(code_tra)（精密代码，参考）
        # holding.loc[index_target,'stock']=self.share（精密代码，参考）
        while 1:
            print(holding)
            print('买输1，卖输0')
            trigger_trade = input()
            if trigger_trade == '1':
                print('输入股票代码')
                code_tra = input()
                code_tra = str(code_tra)
                print('输入数量')
                stock_tra = input()
                stock_tra = int(stock_tra)
                print('输入目标价格')
                price_tra = input()
                price_tra = float(price_tra)
                if code_tra in list(holding.code):
                    trade = stock_to_trade(code_tra, price_tra)
                    trade.buy(stock_tra)  # 利用面向对象预设
                else:
                    holding.loc[len(holding), 'code'] = code_tra  # 利用面向对象预设，要新买另加
                    holding.loc[len(holding) - 1, 'reference_cost'] = price_tra
                    holding.loc[len(holding) - 1, 'stock'] = stock_tra

            elif trigger_trade == '0':
                print('输入股票代码')
                code_tra = input()
                code_tra = str(code_tra)
                print('输入数量')
                stock_tra = input()
                stock_tra = int(stock_tra)
                print('输入目标价格')
                price_tra = input()
                if code_tra in list(holding.code):
                    trade = stock_to_trade(code_tra, price_tra)
                    trade.sell(stock_tra)  # 利用面向对象预设
                else:
                    print('你没有这只股票！')
            else:
                break
                # ——————————————————————每次交易信息更新_非实时高频——————————————————————————

            for i in range(0, len(holding)):
                nowt = datetime.today()
                # 1 holding_tag = ['code', 
                # 2'name_cal', 
                # 3'changepercent_cal',
                # 4'profit_cal', 
                # 5'stock_a_cal', 
                # 6'stock_cal', 不用修改
                # 7'reference_cost_cal', 
                # 8'price_cal', 
                # 9'market_value_cal', 
                # 10'P/L_cal']
                # 2名字name——仅此函数
                code_update = holding.loc[i, 'code']
                name_update = stock_list.loc[stock_list.loc[:, 'code'] == code_update].iloc[0, 1]
                holding.loc[i, 'name'] = name_update
                # 3当日涨跌changepercent——仅此函数
                dyna_info = pd.read_excel(file_basic_location + '交易数据/股票日线/%s' % code_update + '.xlsx' )
                dyna_info_today = dyna_info.loc[dyna_info.loc[:, 'date'] == today]
                if dyna_info.empty:
                    holding.loc[i, 'changepercent'] = '停牌'
                else:
                    dyna_info_cal = dyna_info.tail(2)
                    change_percent_cal = (dyna_info_cal.iloc[1, 2] - dyna_info_cal.iloc[0, 2]) / dyna_info_cal.iloc[ 
                        0, 2]
                    holding.loc[i, 'changepercent'] = change_percent_cal
                # 5 可用股数——做进交易函数
                # 6 持有股数——做进交易函数
                # 7 平均成本——做进交易函数
                # 4 盈利比率——做进交易函数和本函数
                holding.loc[i, 'P/L_pct'] = (dyna_info_cal.iloc[1, 2] - holding.loc[i, 'reference_cost']) / holding.loc[ 
                    i, 'reference_cost']
                # 8 现价——仅做到这个函数里
                holding.loc[i, 'price'] = dyna_info_cal.iloc[1, 2]
                # 9 市值——仅做到这个函数和交易函数
                holding.loc[i, 'market_value'] = dyna_info_cal.iloc[1, 2] * holding.loc[i, 'stock']
                # 4 盈利数值—做进交易函数和本函数
                holding.loc[i, 'P/L'] = (dyna_info_cal.iloc[1, 2] - holding.loc[i, 'reference_cost']) * holding.loc[ 
                    i, 'stock']
                # 更新并保存
            holding = holding.fillna(0)
            holding.to_excel(flie_full_path_hd)

            print('\r\n平均成本以及收益等功能尚未完善，请等待')

    # ——————————————————————————————模块4邮件功能——————————————————————————————————————
    if trigger_layer_1 == '4'or trigger_layer_1 == 'A' or trigger_layer_1 == 'A0':
        print('即将发送邮件')
        
        host = 'smtp.163.com'  # 设置发件服务器地址  
        port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式  
        sender = 'Eeway_zhu@163.com'  # 设置发件邮箱，一定要自己注册的邮箱  
        pwd = 'az6pcv27py'  # 设置发件邮箱的密码，等会登陆会用到  
        receiver = ','.join(['2303979372@qq.com','195759605@qq.com','1044642374@qq.com'])
        receiver_test= ','.join(['2303979372@qq.com'])# 设置邮件接收人，可以是扣扣邮箱  
        #receivers = ','.join(['10643XXXX2@qq.com'])
        body = '<h1>你好！投资数据%s报</h1><p>具体数据见附件如下:</p><p>Supposed_targets:现有模型股票池</p><p>Forecast:投顾量化数据包文件</p><p>数据时效性较强请及时参阅</p>'%(end) # 设置邮件正文，这里是支持HTML的
        msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容  
        msg = MIMEMultipart()

        puretext = MIMEText(body,'html')
        msg.attach(puretext)
        
        # 下面是附件部分 ，这里分为了好几个类型
        
        # 首先是xlsx类型的附件
        xlsxpart = MIMEApplication(open('F:\机器人先生\数据生产\参考标的.xlsx', 'rb').read())
        xlsxpart.add_header('Content-Disposition', 'attachment', filename='Supposed_targets'+end+'.xlsx')
        msg.attach(xlsxpart)
        
        xlsxpart2 = MIMEApplication(open('F:\机器人先生\数据生产\业绩预告.xlsx', 'rb').read())
        xlsxpart2.add_header('Content-Disposition', 'attachment', filename='Forecast'+end+'.xlsx')
        msg.attach(xlsxpart2)
        
        msg['subject'] = 'Hello world' # 设置邮件标题  
        msg['from'] = sender  # 设置发送人  
        msg['to'] = receiver  # 设置接收人  
          
        try:  
            s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL  
            s.login(sender, pwd)  # 登陆邮箱  
            s.sendmail(sender, receiver_test.split(','), msg.as_string())  # 发送邮件！  
            print('Done')
        except smtplib.SMTPException:  
            print('Error')
# ——————————————————————————————模块4邮件功能——————————————————————————————————————
    if trigger_layer_1 == '0':
        print('初始界面')

        print('退出')
        break
