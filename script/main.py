"""
北京地铁预约进站 (沙河,天通苑,草房) 辅助抢票系统
@author: zzzzls
@create: 2021-06-17
@version: 0.0.1

"""
import sys
sys.path.append('/Users/apple/Desktop/files/BeijingSubwayAppointmentSystem')

from script.settings import *
from datetime import date, time
import httpx
import asyncio



class TicketSecKill:
    def __init__(self):
        # authorization = input('请输入您的authorization:')
        authorization = 'NWYzZWE4MWYtMDk1MS00Njc3LThlZDAtNzk4MDM3ZTMwM2VkLDE2MjQ2NDMyNTA2MjUsTSthNEJqQVhzUWQ1YUdBc0M0bHo4KzBKaXBBPQ=='
        self.headers = DEFAULT_HEADERS.copy()
        self.headers['authorization'] = authorization
        self.client = httpx.Client(headers=self.headers)
        self.station, self.route_line = self.choice_station()
        self.seckill_date = self.choice_date()
        self.time_slot = self._get_time_solt('07:25')

    def __del__(self):
        self.client.close()

    def choice_station(self):
        """选择预约站点"""
        # station_num = input('请输入站点编号 ==> 1、沙河站  2、天通苑站  3、草房站 : ')
        station_num = '3'
        station = STATION_MAP.get(station_num)['station_name']
        line = STATION_MAP.get(station_num)['line_name']
        print(f'==== {station} 选择成功!')
        return station, line

    def choice_date(self):
        """选择抢票的日期"""
        # seckill_date_str = input('请输入要抢票的日期[YYYY-mm-dd]:')
        seckill_date_str = '2021-06-22'
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

    def _get_time_solt(self, u_time, t_buffer=10):
        """
        生成抢票时间段
        @u_time: str, 订票时间
        @t_buffer: int, 缓冲时间
        """
        res = []
        time_delta_lst = [630, 640, 650, 700, 710, 720, 730, 740,
                          750, 800, 810, 820, 830, 840, 850, 900, 910, 920, 930]

        n = int(u_time.lstrip('0').replace(':', ''))

        time_delta_lst.append(n)
        time_delta_lst.sort()
        index = time_delta_lst.index(n)

        for i in (-2, -1, 1, 2):
            try:
                assert index+i >= 0
                item = time_delta_lst[index+i]
                res.append(f'0{str(item)[0]}{str(item)[1:]}')
            except (IndexError, AssertionError):
                continue
        # TODO 此处暂返回一个时段
        return [f'{res[i]}-{res[i+1]}' for i in range(len(res)-1)][0]
    
    def gen_data(self):
        """
        生成请求的参数
        """
        for _ in range(42):
            data = {"lineName": self.route_line, "snapshotWeekOffset": 0, "stationName": self.station,
                "enterDate": self.seckill_date, "snapshotTimeSlot": "0700-0900", "timeSlot": self.time_slot}
            yield data

    async def _create_appointment(self):
        """
        开始抢票
        """
        gd = self.gen_data()
        async with httpx.AsyncClient(headers=self.headers) as async_client:
            for data in gd:
                r = await async_client.post(URL_MAP['CreateAppointment'], json=data)
                if r and r.status_code == httpx.codes.ok:
                    response = r.json()
                    if response.get('appointmentId'):
                        print('===抢票成功===', response)
                        break
                print('next....')
            else:
                print('===抢票失败===')


t = TicketSecKill()
asyncio.get_event_loop().run_until_complete(t._create_appointment())

