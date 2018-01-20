"""Train Tickets Query via CLI

Usage:
     tickets [-dgktz] <from> <to> <date>

Options:
     -h --help     Show this screen.
	 -d            动车
	 -g            高铁
	 -k            快速
	 -t            特快
	 -z            直达

"""
import requests
from docopt import docopt
from stations import stations
from prettytable import PrettyTable
from colorama import Fore
import json
def cli():
  arguments = docopt(__doc__,version='Tickets 1.0')
  from_station = stations.get(arguments.get('<from>'),None)
  to_station = stations.get(arguments.get('<to>'),None)
  date = arguments.get('<date>')
  options = ''.join([key for key ,value in arguments.items() if value is True])
  url = ('https://kyfw.12306.cn/otn/leftTicket/queryZ?'
        'leftTicketDTO.train_date={}&'
		'leftTicketDTO.from_station={}&'
		'leftTicketDTO.to_station={}&'
		'purpose_codes=ADULT').format(date,from_station,to_station)
  key_list = []
  value_list = []
  for key,value in stations.items():
      key_list.append(key)
      value_list.append(value)
      
  r=requests.get(url)
  raw_trains = r.json()['data']['result']
  pt = PrettyTable()
  pt._set_field_names('车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split())
  for raw_train in raw_trains:
      data_list = raw_train.split('|')
      train_no = data_list[3]
      initial = train_no[0].lower()
      if not options or initial in options:
        from_station_code = data_list[6]
        to_station_code = data_list[7]
        from_station_index = value_list.index(from_station_code)
        to_station_index = value_list.index(to_station_code)
        from_station_name = key_list[from_station_index]
        to_station_name = key_list[to_station_index] 
        start_time = data_list[8]
        arrive_time = data_list[9]
        time_duration = data_list[10]
        first_class_seat = data_list[31]
        second_class_seat = data_list[30]
        soft_sleep = data_list[23] or '--'
        hard_sleep = data_list[28] or '--'
        hard_seat= data_list[29] or '--'
        no_seat = data_list[26] or '--'

        pt.add_row([
           train_no,
           '\n'.join([Fore.GREEN + from_station_name + Fore.RESET,Fore.RED +to_station_name + Fore.RESET]),
           '\n'.join([Fore.GREEN + start_time + Fore.RESET,Fore.RED + arrive_time+ Fore.RESET]),
           time_duration,
           first_class_seat,
           second_class_seat,
           soft_sleep,
           hard_sleep,
           hard_seat,
	       no_seat
	              ])
  print(pt)
if __name__ == '__main__':
      cli()
