# _*_ coding: utf-8 _*_
import requests
import re
from pprint import pprint
from stations import stations

# 若车站通信码有更新 可在此进行更新
def main():
  url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044'
  r=requests.get(url, verify=False)
  pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
  result=re.findall(pattern,r.text)
  with open('./update_stations_code.py', 'wb') as fn:
       fn.write(str(dict(result)))


if __name__ == '__main__':
    main()
