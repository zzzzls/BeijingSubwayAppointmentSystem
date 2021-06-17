"""
北京地铁预约进站 (沙河,天通苑,草房) 辅助抢票系统
@author: zzzzls
@create: 2021-06-17
@version: 0.0.1

"""

import httpx
import random

from datetime import date, timedelta

class TicketSecKill:
    def __init__(self):
        self.authorization = input('请输入您的authorization:')
        
        self.station_map = {
            '1': '沙河站',
            '2': '天通苑站',
            '3': '草房站'
        }

        self.rand_ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36', # Chrome
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6303004c)', # pc端微信
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x1800072a) NetType/WIFI Language/zh_CN', # APP端微信
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 /sa-sdk-ios/sensors-verify/dg.ruubypay.com?production  YiTongXing/4.5.4',  # 亿通行APP
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', # 北京交通 / 北京地铁 APP
        ]

        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "authorization": self.authorization,
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "dnt": "1",
            "pragma": "no-cache",
            "user-agent": random.choice(self.rand_ua)
        }

        self.url_dct = {
            'GetSystemTime': 'https://webapi.mybti.cn/Home/GetSystemTime',
            'GetBalance': 'https://webapi.mybti.cn/Appointment/GetBalance',
            'GetAppointmentList': 'https://webapi.mybti.cn/AppointmentRecord/GetAppointmentList?status=0&lastid='
        }

        self.client = httpx.Client(headers=self.base_headers)

        self.choice_station()

    def choice_station(self):
        """选择预约站点"""
        station_num = input('请输入站点编号 ==> 1、沙河站  2、天通苑站  3、草房站 : ')
        self.station = self.station_map.get(station_num, '沙河站')
        print(f'==== {self.station} 选择成功!')

    def _get_tomorrow(self):
        """
        获取第二天日期
        TODO 检测第二天是否为工作日 装饰器
        """
        today = date.today()
        day_delta = timedelta(days=1)
        return (today+day_delta).strftime('%Y%m%d')

    def _get_today(self):
        """
        获取今天日期
        TODO 检测今天是否为工作日
        """
        today = date.today()
        return today.strftime('%Y%m%d')
        

    def _get_system_time(self):
        """
        获取系统时间
        """
        res = self.client.get(
            url=self.url_dct['GetSystemTime']
        )
        return res

    def _get_balance(self):
        """
        查询余票
        """
        data = {"timeSlot":"0630-0930","stationName":self.station,"enterDates":[self._get_today()]}
        res = self.client.post(self.url_dct['GetBalance'], json=data)
        return res

    def _get_appointmentList(self):
        """
        查询预约到的票
        """
        res = self.client.post(self.url_dct['GetAppointmentList'])
        return res

    def __del__(self):
        self.client.close()

t = TicketSecKill()
print(t._get_appointmentList().text)

