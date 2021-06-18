import random

USERAGENT_LST = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
    # pc端微信
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6303004c)',
    # APP端微信
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.7(0x1800072a) NetType/WIFI Language/zh_CN',
    # 亿通行APP
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 /sa-sdk-ios/sensors-verify/dg.ruubypay.com?production  YiTongXing/4.5.4',
    # 北京交通 / 北京地铁 APP
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
]

DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "pragma": "no-cache",
    'user-agent': random.choice(USERAGENT_LST)
}

STATION_MAP = {
    '1': '沙河站',
    '2': '天通苑站',
    '3': '草房站'
}

URL_MAP = {
    'GetSystemTime': 'https://webapi.mybti.cn/Home/GetSystemTime',
    'GetBalance': 'https://webapi.mybti.cn/Appointment/GetBalance',
    'GetAppointmentList': 'https://webapi.mybti.cn/AppointmentRecord/GetAppointmentList?status=0&lastid='
}
