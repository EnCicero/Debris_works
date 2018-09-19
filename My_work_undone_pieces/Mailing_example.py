# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 11:31:53 2018

@author: lilee
"""

import smtplib  
from email.mime.text import MIMEText  # 引入smtplib和MIMEText  
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


host = 'smtp.163.com'  # 设置发件服务器地址  
port = 25  # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式  
sender = 'Eeway_zhu@163.com'  # 设置发件邮箱，一定要自己注册的邮箱  
pwd = 'az6pcv27py'  # 设置发件邮箱的密码，等会登陆会用到  
receiver_test= ','.join(['2303979372@qq.com'])# 设置邮件接收人，可以是扣扣邮箱  
#receivers = ','.join(['10643XXXX2@qq.com'])
body = '<h1>你好！这里是Eeway</h1>' # 设置邮件正文，这里是支持HTML的
msg = MIMEText(body, 'html') # 设置正文为符合邮件格式的HTML内容  
msg = MIMEMultipart()

puretext = MIMEText(body,'html')
msg.attach(puretext)

# 下面是附件部分 ，这里分为了好几个类型

# 首先是xlsx类型的附件
xlsxpart = MIMEApplication(open('C:/Users/lilee/OneDrive/BaiduNetDisk/2018境外投资策略.pdf', 'rb').read())
xlsxpart.add_header('Content-Disposition', 'attachment', filename='2018.pdf')
msg.attach(xlsxpart)


msg['subject'] = 'Hello world' # 设置邮件标题  
msg['from'] = sender  # 设置发送人  
msg['to'] = receiver_test  # 设置接收人  
  
try:  
    s = smtplib.SMTP(host, port)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL  
    s.login(sender, pwd)  # 登陆邮箱  
    s.sendmail(sender, receiver_test.split(','), msg.as_string())  # 发送邮件！  
    print('Done')
except smtplib.SMTPException:  
    print('Error')