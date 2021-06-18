"""
北京地铁预约进站 (沙河,天通苑,草房) 辅助抢票系统
@author: zzzzls
@create: 2021-06-17
@version: 0.0.1

"""
import sys
sys.path.append('/Users/apple/Desktop/files/BeijingSubwayAppointmentSystem')

from script.settings import *
from datetime import date
import httpx

class TicketSecKill:
    def __init__(self):
        # authorization = input('请输入您的authorization:')
        authorization = 'NWYzZWE4MWYtMDk1MS00Njc3LThlZDAtNzk4MDM3ZTMwM2VkLDE2MjQ2NDMyNTA2MjUsTSthNEJqQVhzUWQ1YUdBc0M0bHo4KzBKaXBBPQ=='
        self.headers = DEFAULT_HEADERS.copy()
        self.headers['authorization'] = authorization
        self.client = httpx.Client(headers=self.headers)
        self.station = self.choice_station()
        # self.seckill_date = self.choice_date()
        self.seckill_date = '20210621'

    def choice_station(self):
        """选择预约站点"""
        station_num = input('请输入站点编号 ==> 1、沙河站  2、天通苑站  3、草房站 : ')
        station = STATION_MAP.get(station_num, '沙河站')
        print(f'==== {station} 选择成功!')
        return station

    def choice_date(self):
        """选择抢票的日期"""
        seckill_date_str = input('请输入要抢票的日期[YYYY-mm-dd]:')
        year, month, day = seckill_date_str.split('-')
        seckill_date = date(int(year), int(month), int(day))
        if 0 <= seckill_date.weekday() <= 4:
            return seckill_date.strftime('%Y%m%d')
        else:
            raise ValueError(f'{seckill_date_str} 不是工作日')

    def _get_system_time(self):
        """
        获取系统时间
        """
        res = self.client.get(
            url=URL_MAP['GetSystemTime']
        )
        return res

    def _get_balance(self):
        """
        查询余票
        """
        data = {"timeSlot": "0630-0930", "stationName": self.station,
                "enterDates": [self.seckill_date]}
        res = self.client.post(URL_MAP['GetBalance'], json=data)
        return res

    def _get_appointmentList(self):
        """
        查询预约到的票
        """
        res = self.client.post(URL_MAP['GetAppointmentList'])
        return res

    def __del__(self):
        self.client.close()


t = TicketSecKill()
print(t._get_balance().json())
