# -*- coding:utf-8 -*-
import random
import pymysql.cursors
import requests
from bs4 import BeautifulSoup

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='weather',
    charset='utf8'
)
cursor = connect.cursor()
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
headers = {'User-Agent': random.choice(my_headers)}
baseurl = "https://www.tianqi.com"
zhixiashi = ['北京', '天津', '上海', '重庆']
maxCitySize = 3187

def get_city():
    countsql="select count(*) from city"
    cursor.execute(countsql)
    res = cursor.fetchall()
    if res[0][0] == maxCitySize:
        return
    else:
        deleteSql ="delete from city "
        cursor.execute(deleteSql)
        connect.commit()
        url = "https://www.tianqi.com/chinacity.html"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text.encode(html.encoding), 'lxml', from_encoding='utf-8')
        h2list = soup.find('div', class_="citybox").find_all("h2")
        sql = "INSERT INTO city (province, province_p, municipality,municipality_p,area,area_p,city,city_p) VALUES ( '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s' )"
        sum = 0
        for h2 in h2list:
            province = ''
            province_p = ''
            municipality = ''
            municipality_p = ''
            area = ''
            area_p = ''
            cityinfo = h2.find("a")
            print(cityinfo.string)
            if cityinfo.string in zhixiashi:
                province = cityinfo.get_text()
                province_p = cityinfo['href'].replace('/', '', 2)
                municipality = cityinfo.get_text()
                municipality_p = cityinfo['href'].replace('/', '', 2)
                data = (province, province_p, municipality, municipality_p, '', '', municipality, municipality_p)
                cursor.execute(sql % data)
                connect.commit()
                sum = sum + 1;
                print('成功插入', sum, '条数据')
                print(data)

                url = baseurl + cityinfo['href']

                html_zhixiashi = requests.get(url, headers=headers)
                soup_zhixiashi = BeautifulSoup(html_zhixiashi.text.encode(html_zhixiashi.encoding), 'lxml',
                                               from_encoding='utf-8')

                arealist = soup_zhixiashi.find('div', class_="mainWeather").find_all("li")
                del arealist[-1]
                for areaInfo in arealist:
                    area_p = areaInfo.find_all("a")[0]['href'].replace('/', '', 2)
                    area = areaInfo.find_all("a")[0].find("h5").get_text()
                    print(
                        province + ":" + province_p + "," + municipality + ":" + municipality_p + "," + area + ":" + area_p)
                    data = (province, province_p, municipality, municipality_p, area, area_p, area, area_p)
                    cursor.execute(sql % data)
                    connect.commit()
                    sum = sum + 1;
                    print('成功插入', sum, '条数据')
            else:
                province = cityinfo.get_text()
                province_p = cityinfo['href'][10:len(cityinfo['href']) - 1]

                url = baseurl + cityinfo['href']

                html_sheng = requests.get(url, headers=headers)
                soup_sheng = BeautifulSoup(html_sheng.text.encode(html_sheng.encoding), 'lxml',
                                           from_encoding='utf-8')
                racitys = soup_sheng.find('ul', class_="racitys").find_all("li")
                for racity in racitys:
                    municipality = racity.find("b").find("a").get_text()
                    municipality_p = racity.find("b").find("a")['href'].replace('/', '', 2)

                    data = (province, province_p, municipality, municipality_p, '', '', municipality, municipality_p)
                    cursor.execute(sql % data)
                    connect.commit()
                    sum = sum + 1;
                    print('成功插入', sum, '条数据')
                    print(data)

                    arealist = racity.find("span").find_all("a")
                    for areaInfo in arealist:
                        area = areaInfo.get_text()
                        area_p = areaInfo['href'].replace('/', '', 2)
                        print(
                            province + ":" + province_p + "," + municipality + ":" + municipality_p + "," + area + ":" + area_p)
                        data = (province, province_p, municipality, municipality_p, area, area_p, area, area_p)
                        cursor.execute(sql % data)
                        connect.commit()
                        sum = sum + 1;
                        print('成功插入', sum, '条数据')


def get_data(cityp, cityid, startyear, startmonth):
    sql = "INSERT INTO weather (city_p,`date`, temperaturehigh,temperaturelow,weather, wind,id) VALUES ( '%s','%s', '%s', '%s','%s', '%s','%d')"
    errsql = "INSERT INTO errorinfo (city,`year`,`month`) VALUES ( '%s', '%d','%d')"
    base_url = "http://lishi.tianqi.com/"  # /lanzhou/201101.html"
    sucsum = 0
    errsum = 0
    if startyear < 2011:
        year = 2011
    else:
        year = startyear
    month = startmonth
    while year < 2021:
        while month < 13:
            try:
                url = base_url + str(cityp) + "/" + str(year) + "{:0>2d}".format(month) + ".html"
                r = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml', from_encoding='utf-8')
                ul = soup.find('ul', class_="thrui").find_all("li")
                del ul[-1]
                for i in ul:
                    info = (i.get_text().split('\n'))[1: -1]
                    data = (cityp, info[0][0:10], info[1], info[2], info[3], info[4], cityid)
                    cursor.execute(sql % data)
                    connect.commit()
                    sucsum = sucsum + 1
                    print('成功插入', sucsum, '条数据 ; 异常数据', errsum, '条数据')
            except Exception as e:
                errsum = errsum + 1
                errdata = (cityp, year, month)
                print("异常数据" + cityp + ":", year, "/", month)
                cursor.execute(errsql % errdata)
                connect.commit()
                print('成功插入', sucsum, '条数据 ; 异常数据', errsum, '条数据')
                month += 1
                continue
            month += 1
        year += 1
        month = 1


def dealerrdata():
    basesql = "INSERT INTO weather (city_p,`date`, temperaturehigh,temperaturelow,weather, wind,id) VALUES ( '%s','%s', '%s', '%s','%s', '%s','%d')"
    sql = "SELECT `year`,`month`,city FROM `errorinfo`"
    cursor.execute(sql)
    res = cursor.fetchall()
    for line in res:
        year = line[0]
        month = line[1]
        cityp = line[2]
        sql = "SELECT id FROM `city` WHERE city_p='%s'"
        data = (cityp,)
        cursor.execute(sql % data)
        cityid = cursor.fetchall()[0][0]
        try:
            url = "http://lishi.tianqi.com/" + str(cityp) + "/" + str(year) + "{:0>2d}".format(month) + ".html"
            r = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml', from_encoding='utf-8')
            ul = soup.find('ul', class_="thrui").find_all("li")
            del ul[-1]
            for i in ul:
                info = (i.get_text().split('\n'))[1: -1]
                data = (cityp, info[0][0:10], info[1], info[2], info[3], info[4], cityid)
                cursor.execute(basesql % data)
                connect.commit()
            print("解决一条异常数据：" + cityp + ",", year, ",", month)
            sql = "delete from `errorinfo` where city='%s' and `year`='%d' and `month`='%d'"
            data = (cityp, year, month)
            cursor.execute(sql % data)
            connect.commit()
        except Exception as e:
            print("异常数据：" + cityp + ",", year, ",", month)
            print(e)
            continue


if __name__ == '__main__':
    get_city()
    # dealerrdata()
    sqlselect = "select * from city"
    sum = cursor.execute(sqlselect)
    startid = 1
    if (sum == 0):
        deletesql = "DELETE from weather "
        cursor.execute(deletesql)
        connect.commit()
        deletesql = "DELETE from lastfinish "
        cursor.execute(deletesql)
        connect.commit()
        get_city()
    else:
        sqlselect = "select MAX(id) from weather"
        cursor.execute(sqlselect)
        res = cursor.fetchall()
        startid = res[0][0]
        deltesql = "DELETE from weather where `id`='%d'"
        cursor.execute(deltesql % res[0])
        connect.commit()

    sqlselect = "SELECT count(*) FROM `city`"
    cursor.execute(sqlselect)
    res = cursor.fetchall()
    sum = res[0][0]

    while (startid <= sum) and (startid <= 2600):
        sqlselect = "SELECT `city_p` FROM `city` where id='%d'"
        seldata = (startid,)
        cursor.execute(sqlselect % seldata)
        res = cursor.fetchall()
        get_data(res[0][0], startid, 2011, 1)
        startid += 1
