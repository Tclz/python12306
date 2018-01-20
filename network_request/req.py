# _*_ coding: utf-8 _*_
import urllib2
import urllib
import cookielib

class Request:
    def __init__(self,ope):
        self.opener = ope
    def post_request_with_parameter(self,req, data):
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0')
        req.add_header('Referer', 'https://kyfw.12306.cn/otn/login/init')
        data = urllib.urlencode(data)  # 将字典类型转换成查询字符串
        html = self.opener.open(req, data=data).read()
        return html
    def post_request(self,req):
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0')
        html = self.opener.open(req).read()
        return html

