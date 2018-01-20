# _*_ coding: utf-8 _*_
from train_code.stations import stations
import urllib2
import json
from utility.util import Util

class Train:
    def __init__(self,from_station,to_station,date,request):
        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.request = request
        self.train_list = None

    def get_train_list(self):
        return self.train_list

    def find_certain_ticket(self, raw_trains):
        for raw_train in raw_trains:
            data_list = raw_train.split('|')
            n = data_list[28]
            # 有 '\u6709'  无 '\u65e0'
            if n != '\u65e0' and n != '':
                return True
        return False

    def query_train_data(self):
        print ('正在查询所选列车余票情况...')
        # 将中文车站名转换为相应的通信码
        f_station = stations.get(self.from_station)
        # print(f_station)
        t_station = stations.get(self.to_station)
        # print(t_station)
        url = ('https://kyfw.12306.cn/otn/leftTicket/queryZ?'
               'leftTicketDTO.train_date={}&'
               'leftTicketDTO.from_station={}&'
               'leftTicketDTO.to_station={}&'
               'purpose_codes=ADULT').format(self.date, f_station, t_station)
        req = urllib2.Request(url)
        html = self.request.post_request(req)
        if Util.check_json(html):
            print ('已经获取到目标线路的车次信息...')
            # 解析得到火车的数据
            result = json.loads(html)
            raw_trains = result['data']['result']
            result = self.find_certain_ticket(raw_trains)
            if result:
                for raw_train in raw_trains:
                    data_list = raw_train.split('|')
                    n = data_list[28]
                    #print n
                    if n != '\u65e0' and n != '':
                        #train_secret_str = data_list[0]
                        self.train_list = data_list
                        break
            else:
                print ('暂时没有符合您要求的车票,建议更换座次类别后再试...')
                exit(1)
            #print (self.train_list)
            #print(train_secret_str)
            # 网络等原因也许会导致查询失败
            if self.train_list is None:
                 print ('没有找到符合要求的车票,正在尝试重新查询...')
                 return False
            return True
        else:
            print ('查询余票失败,尝试重新查询...')
            return False



