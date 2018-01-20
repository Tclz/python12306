# _*_ coding: utf-8 _*_
import urllib2
import urllib
import cookielib
import json
import re
import ConfigParser
import time
from utility.util import Util
from train_data.get_train_data import Train
from network_request.req import Request

#读取配置文件
cp = ConfigParser.SafeConfigParser()
cp.read("../configure/conf.ini")
user = cp.get('user_info', 'user')
pwd = cp.get('user_info', 'pwd')
from_station = cp.get('station_info', 'from_station')
to_station = cp.get('station_info', 'to_station')
date = cp.get('station_info', 'date')
passengerTicketStr = cp.get('passenger_info','passengerTicketStr')
#print passengerTicketStr
oldPassengerStr = cp.get('passenger_info','oldPassengerStr')
#print oldPassengerStr
# 获得一个opener  使得后续的网络请求使用的是同一个连接
def get_opener():
        c = cookielib.LWPCookieJar()
        cookie = urllib2.HTTPCookieProcessor(c)
        ope = urllib2.build_opener(cookie)
        return ope

def request_verify_code_img(request):
   #请求验证码图片
   req = urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-image?'
                              'login_site=E&module=login&rand=sjrand&0.29060207042569175')
   codeimg = request.post_request(req)
   with open('../img/code.png', 'wb') as fn:
       fn.write(codeimg)
   vcode_position = ['43,47', '43,47', '114,35', '186,37', '255,39', '40,111', '111,107', '177,112', '252,113']
   position = raw_input("请输入验证码位置:").split(',')
   data_vcode_position = []
   for point in position:
       data_vcode_position.append(vcode_position[int(point)])
   code = ','.join(data_vcode_position)
   return code

def submit_verify_code(request,code):
   #提交验证码
   req = urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-check')
   data = {
         'answer': code,
         'login_site': 'E',
         'rand': 'sjrand'
          }
   html = request.post_request_with_parameter(req, data)
   global verfify_result
   verfify_result = False
   result = json.loads(html)
   if result['result_code'] == '4':
         print('验证码校验成功')
         verfify_result = True
   else:
         while verfify_result is not True:
             print('验证码校验失败,正在重新获取...')
             img = request_verify_code_img(request)
             submit_verify_code(request,img)

def login(request):
   req = urllib2.Request('https://kyfw.12306.cn/passport/web/login')
   data ={
       'username': user,
       'password': pwd,
       'appid': 'otn'
           }
   html = request.post_request_with_parameter(req,data)
   if Util.check_json(html):
       result = json.loads(html)
       if result['result_code'] == 0:
          print('登录成功')
       else:
          print ('登录失败,稍后将重试...')
          time.sleep(1)
          login(request)
   else:
       print ('登录失败,稍后将重试...')
       time.sleep(1)
       login(request)

def check_again_after_login(request):
   # uamtk认证
   req = urllib2.Request('https://kyfw.12306.cn/passport/web/auth/uamtk')
   data ={
       'appid': 'otn'
           }
   html = request.post_request_with_parameter(req,data)
   #print(html)
   result = json.loads(html)
   if result['result_code'] == 0:
       print('uamtk认证通过')
       is_check_uamtk = True
   else:
       print('uamtk认证失败')
       is_check_uamtk = False
       return is_check_uamtk

   #uamauthclient认证
   #先提取上一步响应中的数据作为参数
   if is_check_uamtk is True:
       value = result['newapptk']
       req = urllib2.Request('https://kyfw.12306.cn/otn/uamauthclient')
       data = {
           'tk': value
       }
       html = request.post_request_with_parameter(req,data)
       #print(html)
       result = json.loads(html)
       if result['result_code'] == 0:
           print('uamauthclient认证通过')
           return  True
       else:
           print('uamauthclient认证失败')
           return  False

def checkUser(request):
   #检查用户 checkUser
   req=urllib2.Request('https://kyfw.12306.cn/otn/login/checkUser')
   data = {
       '_json_att': ''
   }
   time.sleep(1)
   html = request.post_request_with_parameter(req,data)
   #print(html)
   result = json.loads(html)
   if result['data']['flag'] == True:
       print('检查用户状态通过')
   else:
       print('检查用户状态失败')

def submit_Order_Request(request,secret_str):
   print ('开始提交订单请求')
   data = {
       'secretStr':urllib.unquote(secret_str),
   'train_date': date,
   'back_train_date': '2018-01-18',
   'tour_flag': 'dc',
   'purpose_codes':'ADULT',
   'query_from_station_name':from_station,
   'query_to_station_name': to_station,
   'undefined':''
   }
   #print('secret_Str:')
   #print(secret_str)
   #print('解码后的secret_str:')
   #print(urllib.unquote(secret_str))
   req = urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest')
   html = request.post_request_with_parameter(req,data)
   #print(html)
   result = json.loads(html)
   if result['status']== True:
       print('提交订单请求成功')
       return True
   else:
       print('提交订单请求失败,稍后将进行重试...如果多次失败,请检查是否有未支付订单...')
       time.sleep(5)
       submit_Order_Request(request,secret_str)

def initDc(request):
   #initDc接口 ,初始化订票界面
   req= urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/initDc')
   data = {
       '_json_att': ''
   }
   html = request.post_request_with_parameter(req,data)
   a1 = re.search(r'globalRepeatSubmitToken.+', html).group()
   RepeatSubmitToken = re.sub(r'(globalRepeatSubmitToken)|(=)|(\s)|(;)|(\')', '', a1)
   #print(RepeatSubmitToken)
   b1 = re.search(r'key_check_isChange.+', html).group().split(',')[0]
   key_check_isChange = re.sub(r'(key_check_isChange)|(\')|(:)', '', b1)
   #print(key_check_isChange)
   return (RepeatSubmitToken, key_check_isChange)

def getPassengerDTOs(request,repeatSubmitToken):
   #获取乘客信息
   data = {
       '_json_att': '',
   'REPEAT_SUBMIT_TOKEN':repeatSubmitToken
   }
   req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs')
   html = request.post_request_with_parameter(req,data)
   print ('请求乘客信息...')
   #print(html)
   if Util.check_json(html):
       result = json.loads(html)
       if result['status'] is True:
           print('获取乘客信息成功')
       else:
           # 可能因为网络等原因出错
           print ('获取乘客信息失败,正在进行重试...')
           getQueueCount(request, repeatSubmitToken)
   else:
       print ('获取乘客信息时出错')

def checkOrderInfo(request,repeatSubmitToken):
   print('开始确认订单...')
   time.sleep(1)
   req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo')
   data = {
       'cancel_flag': '2',
   'bed_level_order_num':'000000000000000000000000000000',
   'passengerTicketStr':passengerTicketStr,
   'oldPassengerStr':oldPassengerStr,
   'tour_flag':'dc',
   'randCode': '',
   'whatsSelect':'1',
   '_json_att': '',
   'REPEAT_SUBMIT_TOKEN':repeatSubmitToken
   }
   html = request.post_request_with_parameter(req,data)
   print('正在确认订单...')
   #print(html)
   if Util.check_json(html):
       result = json.loads(html)
       if result['status'] is True:
           print('确认订单信息成功')
       else:
           # 可能因为网络等原因出错
           print ('确认订单信息失败,正在进行重试...')
           time.sleep(3)
   else:
       print ('确认订单信息时出错,重试中...')
       checkOrderInfo(request,repeatSubmitToken)

def getQueueCount(request,repeatSubmitToken,avaliable_trains,date):
   # 检查车票预定队列
   req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount')
   train_date = Util.Formate_date(date)
   data ={
       'train_date': train_date,
   'train_no': avaliable_trains[2],
   'stationTrainCode': avaliable_trains[3],
       #座位类别修改此处
   'seatType': '3',
   'fromStationTelecode':avaliable_trains[6],
   'toStationTelecode':avaliable_trains[7],
   'leftTicket':avaliable_trains[12],
   'purpose_codes':'00',
   'train_location':avaliable_trains[15],
   '_json_att':'',
    'REPEAT_SUBMIT_TOKEN':repeatSubmitToken
   }
   html = request.post_request_with_parameter(req,data)
   print ('检查车次预定队列...')
   #print(html)
   if Util.check_json(html):
       result = json.loads(html)
       if result['status'] is True:
           print('检查车次预定队列ok')
       else:
           # 可能因为网络等原因出错
           print ('检查车次预定队列失败,正在进行重试...')
           time.sleep(3)
           getQueueCount(request,repeatSubmitToken,avaliable_trains,date)
   else:
       print ('检查车次预定队列出错,重试中...')
       getQueueCount(request,repeatSubmitToken, avaliable_trains, date)

def confirmSingleForQueue(request,repeatSubmitToken,key_check_isChange,avaliable_trains):
    req = urllib2.Request('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue')
    #最后一次确认订单
    data ={
    'passengerTicketStr': passengerTicketStr,
    'oldPassengerStr':oldPassengerStr,
    'randCode': '',
    'purpose_codes':'00',
    'key_check_isChange':key_check_isChange,
    'leftTicketStr':avaliable_trains[12],
    'train_location':avaliable_trains[15],
    'choose_seats':'',
    'seatDetailType':'000',
    'whatsSelect':'1',
    'roomType':'00',
    'dwAll':'N',
    '_json_att':'',
    'REPEAT_SUBMIT_TOKEN':repeatSubmitToken
    }
    html = request.post_request_with_parameter(req, data)
    print('进行订单的最终确认...')
    #print(html)
    if Util.check_json(html):
        result = json.loads(html)
        if result['status'] is True:
            # 可能因为网络等原因出错
            print ('购票成功!请尽快登录12306完成支付')
        else:
            print ('订单最终确认失败,正在重新提交...')
            confirmSingleForQueue(request,repeatSubmitToken,key_check_isChange,avaliable_trains)
    else:
        print('订单的最终确认出错')
if __name__ == '__main__':
    opener = get_opener()
    request = Request(opener)
    code = request_verify_code_img(request)
    submit_verify_code(request,code)
    login(request)
    check_again_after_login(request)
    checkUser(request)
    train = Train(from_station,to_station,date,request)
    result = train.query_train_data()
    while result is False:
        result = train.query_train_data()
    #火车数据列表
    train_data = train.get_train_list()
    #print(train_data)
    #待解析的secret_str
    train_secret_str = train_data[0]
    #print(train_secret_str)
    request_order_result = submit_Order_Request(request,train_secret_str)
    if request_order_result is True:
        RepeatSubmitToken, key_check_isChange = initDc(request)
        getPassengerDTOs(request,RepeatSubmitToken)
        checkOrderInfo(request,RepeatSubmitToken)
        getQueueCount(request,RepeatSubmitToken,train_data,date)
        confirmSingleForQueue(request,RepeatSubmitToken,key_check_isChange,train_data)






