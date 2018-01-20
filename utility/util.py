# _*_ coding: utf-8 _*_
import json
import time

class Util:
    @staticmethod
    def check_json(object):
        try:
            json.loads(object)
        except ValueError:
            return False
        return True

    @staticmethod
    def Formate_date(date):
        """
            将传递的字符串转化为时间
            :param param: 时间： 2017-12-29
            :return: Fri Dec 29 2017 00:00:00 GMT+0800 (中国标准时间)
            """
        ts = time.mktime(time.strptime(date, "%Y-%m-%d"))
        s = time.ctime(ts)
        t1 = s[0:11] + s[20:] + " 00:00:00 GMT+0800 (中国标准时间)"
        return t1