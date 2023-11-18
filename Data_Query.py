# 导入模块
import requests
# 导入数据
from info import stations


def get_Information(start_Place, end_Place, start_Time, user_type):

    # 获取地区代码
    s = stations[start_Place.get()]
    e = stations[end_Place.get()]

    # 获取用户类型
    if user_type == 1:
        user_type = 'ADULT'
        print("成人票")
    else:
        user_type = '0X00'
        print("学生票")

    # 设置请求连接（去开发者工具Header里找到：请求 URL）
    url = f'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={start_Time.get()}&leftTicketDTO.from_station={s}&leftTicketDTO.to_station={e}&purpose_codes={user_type}'
    print(url)

    # 设置请求头（模拟浏览器请求，防止被反爬）
    headers = {
        'cookie': '_uab_collina=169971914884913403505201; JSESSIONID=A7BD559C8C074951282A69AB8E0F47C1; route=495c805987d0f5c8c84b14f60212447d; BIGipServerotn=1306067210.64545.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u5F20%u5BB6%u754C%u897F%2CJXA; _jc_save_fromDate=2023-11-20; _jc_save_toDate=2023-11-12; _jc_save_wfdc_flag=dc; _jc_save_toStation=%u5E7F%u5DDE%u5317%2CGBQ',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # 发送请求
    res = requests.get(url=url, headers=headers)

    # 解析数据
    data = res.json()['data']['result']

    trains = []

    for item in data:
        # 切割字符串，返回列表
        info = item.split('|')
        # 找到列表中元素下表，方便取值
        index = 0

        tree = {"车次": info[3],
                "出发时间": info[8],
                "到达时间": info[9],
                "历时": info[10],
                "商务座": info[25],
                "特等座": info[32],
                "一等座": info[31],
                "二等座": info[30],
                "软卧/一等卧": info[23],
                "硬卧/二等卧": info[28],
                "硬座": info[29],
                "无座": info[26],
                }

        trains.append(tree)
    return trains
