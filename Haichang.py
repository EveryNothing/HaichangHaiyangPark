# -*- coding: utf-8 -*-
"""
Created on Sun June 5 17:54:35 2022

@author: xici
"""

from datetime import datetime
import requests
import re
import json,os,shutil
from hyper.contrib import HTTP20Adapter
import time
import winsound

thecookies={}
proxies=None
session=requests.Session()

headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type":"application/json;charset=utf-8",
        
        "Host": "weixin.haichangchina.com",
        "Pragma": "no-cache",
        "Referer": "https://weixin.haichangchina.com/order/ticket/ticket2022060100520018?parkId=10",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36"
      }

def overwriteCookie(newcookie):
    global thecookies
    thecookies.items
    for key, value in newcookie.items():
        thecookies[key]=value

def openLoginPage():
    global thecookies
    url='https://weixin.haichangchina.com/login?redir=/member'
    res=requests.get(url,proxies=proxies,verify=False)
    print(res.text)
    xcookies = requests.utils.dict_from_cookiejar(res.cookies)
    thecookies['Hm_lvt_30a118fe48f00ddd1f2a68d92e5f7a8f']=(int)(datetime.now().timestamp())
    thecookies['Hm_lpvt_30a118fe48f00ddd1f2a68d92e5f7a8f']=(int)(datetime.now().timestamp())
    overwriteCookie(xcookies)
    print(thecookies)

def login(loginName,loginPass):
    global thecookies
    openLoginPage()
    loginurl='https://weixin.haichangchina.com/leaguerLogin?loginName=%s&loginPass=%s'%(loginName,loginPass)
    res=requests.get(loginurl,data={"loginName":loginName,"loginPass":loginPass},proxies=proxies,verify=False)
    print(res.text)
    xcookies = requests.utils.dict_from_cookiejar(res.cookies)
    thecookies['Hm_lpvt_30a118fe48f00ddd1f2a68d92e5f7a8f']=(int)(datetime.now().timestamp())
    overwriteCookie(xcookies)
    print(thecookies)
    #print(res.json()[0]['status'])
    return res.json()[0]['status']==200

def fastRegAccount(loginName,realName,idcard):
    urlconfig='https://weixin.haichangchina.com/fastregByAccount?loginName=%s&realName=%s&idcard=%s'%(loginName,realName,idcard)
    res = requests.get(urlconfig,headers=headers,cookies=thecookies,proxies=proxies)
    #res.text
    print(res.json())

def json2paramString(data):
    ret=""
    for key, value in data.items():
        #print(key,value)
        if len(ret)>0:
            ret=ret+"&"
        ret=ret+key+"="+value
    return ret

def cookie2String(cookies):
    ret=""
    for key, value in cookies.items():
        #print(key,value)
        if len(ret)>0:
            ret=ret+"; "
        ret=ret+("%s=%s"%(key,value))
    return ret

#仅限家庭套票
def subOrder(realName,idcard,mobile,ticketDate):
    #多张家庭套票
    # data={
    #     "rateCode": "ticket2022060100520018",
    #     "beginDate": "2022-06-07",
    #     "endDate": "2022-06-07",
    #     "parkId": "10",
    #     "couponCode": "", 
    #     "couponCheckCode": " ",
    #     "amount": "3",
    #     "linkMans": "陈冬",
    #     "teles": "13777887654",
    #     "idNos": "632323190605265563",
    #     "linkMans": "刘洋",
    #     "idNos": "632323190605263648",
    #     "linkMans": "蔡旭坤",
    #     "idNos": "632323190605261247"
    # }
    #单张家庭套票
    data={
        "rateCode": "ticket2022060100520018",
        "beginDate": ticketDate,
        "endDate": ticketDate,
        "parkId": "10",
        "couponCode": "", 
        "couponCheckCode": " ",
        "amount": "1",
        "linkMans": realName,
        "teles": mobile,
        "idNos": idcard
    }
    paramstr=json2paramString(data)
    paramcookiestr=cookie2String(thecookies)
    order_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length":"0",
        
        "Cookie": paramcookiestr,
        "Host": "weixin.haichangchina.com",
        "Origin":"http://weixin.haichangchina.com",

        "Pragma": "no-cache",
        "Referer": "https://weixin.haichangchina.com/order/ticket/ticket2022060100520018?parkId=10",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36"
        
      }

    url="https://weixin.haichangchina.com/order/ticket?%s"%paramstr
    #print("request: "+url)

    res=requests.post(url,headers=order_headers,data=data,proxies=proxies,verify=False) #cookies=thecookies,
    print(res.text)
    xcookies = requests.utils.dict_from_cookiejar(res.cookies)
    thecookies['Hm_lpvt_30a118fe48f00ddd1f2a68d92e5f7a8f']=(int)(datetime.now().timestamp())
    overwriteCookie(xcookies)
    #print(thecookies)
    try:
        return res.json()[0]['status']==200
    except:
        return False

def notice(freq,duration,count):
    while count>0:
        winsound.Beep(freq,duration)
        count=count-1

def noticeSuccess():
    notice(600,300,100)

def noticeFail():
    notice(1600,500,3)

def walk(loginName,loginPass,realName,idcard,mobile,ticketDate):
    logined=login(loginName,loginPass)
    if logined:
        print('--------登录成功-----------')
        while(True):
            print('---开始下单---')
            ordered=subOrder(realName,idcard,mobile,ticketDate)
            if ordered:
                print('order success')
                noticeSuccess()
                break
            else:
                print('order failed')
                time.sleep(3)
    else:
        print('-----------登录失败-----------')
        noticeFail()

loginName = "13777887654" #登录手机号
loginPass = "123456" #登录密码

realName = "刘洋" #参观人取票人真实姓名
idcard = "632323190605265563" #参观人取票人真实身份证号
mobile = "13777887654" #参观人取票人手机号

ticketDate = "2022-06-07" #参观日期

#logined=login(loginName,loginPass)
#print(logined)
# logined=False
# if logined:
#     print('登录成功')
#     while(True):
#         ordered=subOrder(realName,idcard,mobile,ticketDate)
#         if ordered:
#             print('order success')
#             noticeSuccess()
#             break
#         else:
#             print('order failed')
#             time.sleep(3)
# else:
#     print('登录失败')
#     noticeFail()

#此参数购买一张家庭套票
walk(loginName,loginPass,realName,idcard,mobile,ticketDate)
