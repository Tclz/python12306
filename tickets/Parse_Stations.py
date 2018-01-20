import requests
import re
from pprint import pprint
from stations import stations

def main():
  url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044'
  r=requests.get(url, verify=False)
  pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
  result=re.findall(pattern,r.text)
  pprint(dict(result),indent=4)

if __name__ == '__main__':
    main()
