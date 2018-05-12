# -*- coding: utf-8 -*-

import ssl
import urllib2
import sqlite3

def get_station_name():
    ver = sys.argv[1]
    base_url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version="
    url = base_url+ ver
    
    #目的为了通过未认证的12306证书
    ssl._create_default_https_context = ssl._create_unverified_context

    req = urllib2.Request(url)
    req.add_header("Referer","https://kyfw.12306.cn/otn/leftTicket/init")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36")
    names = urllib2.urlopen(req).read()    
    
    with open("station_name.txt", 'wb') as f:
        f.write(names) 
    #创建数据库
    conn = sqlite3.connect("station.db")  
    print 'Opened database successfully'  
    #创建station表  
    cursor = conn.cursor()
    cursor.execute('create table station (ID int primary key, NAME varchar(20), CODE varchar(20))')  
    print 'Table created successfully'  
    
    itemsTmp = names.split("'")
    if len(itemsTmp) == 3:
        items = itemsTmp[1].split("@")
        for item in items:
            if item == "":
                continue
                
            info = item.split("|")
            cursor.execute("insert into station(ID,NAME,CODE) values(%d,'%s','%s')" %(int(info[5])+1,info[1],info[2]))
        cursor.close()
        conn.commit()
        conn.close()
            
if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    get_station_name()