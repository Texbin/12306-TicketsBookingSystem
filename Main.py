# 导入模块
import time
import tkinter
import pandas as pd
from PIL import ImageTk, Image
from pandastable import Table
import Data_Query
import Automatic_Buy
from time import strftime
import AccountIO
import sys,os


# 这里时获取打包后图片资源
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




# 获取当前时间
Today = time.strftime("%Y-%m-%d")

# 用来保存查询到的车次号
trains_Number = []

# 保存第一次登录的cookie
Cookie = []

# 查询车次信息
def chick_info(start_place, end_place, start_time, user_type):
    # 获取数据
    try:
        print(start_place.get(), end_place.get(), start_time.get(), user_type)
        trains = Data_Query.get_Information(
            start_place, end_place, start_time, user_type)
        # 将数据转换为DataFrame
        df = pd.DataFrame(trains)
        # 提取车次号
        global trains_Number
        column_name = df.columns[0]
        trains_Number = df[column_name].tolist()  # 将DataFrame转换为列表
        print(trains_Number)
        # 插入数据，展示表格信息
        pt = Table(f, dataframe=df, showtootime_labelar=False,
                   showstatusbar=False)
        pt.show()
        # 刷新
        pt.redraw()
    except:
        tkinter.messagebox.showinfo('提示', '未查询到车次信息！')



# 购票
def buy_ticket(start_Place, end_Place, start_Time, user_type, tree_Number):
    # 判断车次号
    if str(tree_Number.get()) not in trains_Number:
        tkinter.messagebox.showinfo('提示', '车次不存在！')
    else:
        # 找到目标车次号的列表为位置
        index = trains_Number.index(tree_Number.get())
        global Cookie
        # 打开浏览器
        Cookie = Automatic_Buy.Automatic_ticket_purchasing(
            start_Place, end_Place, start_Time, user_type, index, Cookie)


# ==========================================================================================================
# 创建应用程序主窗口
root = tkinter.Tk()

# 设置窗口图标
root.iconbitmap(get_resource_path(r'images/favicon.ico'))

# 设置窗口背景色
root.configure(background='#D3D3D3')

# 设置窗口位置
root.geometry('1080x600+250+120')

# 设置窗口大小不可改变
root.resizable(width=False, height=False)

# 设置窗口标题
root.title('12306车票查询与抢票')

# 设置logo,打开图片文件
img = Image.open(get_resource_path('images/logo.png'))

# 将图片转换为Tkinter支持的格式
img_tk = ImageTk.PhotoImage(img)

# 创建Label小部件来显示图片
label = tkinter.Label(root, image=img_tk)
label.place(x=0, y=0, width=1080, height=160)

# 通知栏
info_Label = tkinter.Label(root,background='white')
info_Label.place(x=380, y=130, width=300, height=20)

messages = [
    "第一次登录请设置登录信息。",
    "如果登录失败,请重新设置登录信息",
    "或检查网络连接是否正常。",
    "预订请设置乘车人等车票信息",
    "预订学生票,乘车人必须为学生",
    "否购会预订失败。",
    "请及时去官网更新乘车人信息。",
    "下单后为了安全，请在手机上支付订单。",
    "本软件纯属学习交流，请勿用于商业用途",
    "如不满意使用，勿喷！谢谢！"
]

i = 0


def scroll_text():
    global i
    if i == 10:
        i = 0
    info_Label.config(text="  注意："+messages[i], fg='red',anchor='w')
    i += 1
    # 每隔3秒钟执行函数
    info_Label.after(4000, scroll_text)


scroll_text()


# 设置登录信息
login_info = tkinter.Button(root, text='设置登录信息', font=(
    '华文彩云', 12, 'bold'), fg='#61f825', background='black', command=lambda root = root :AccountIO.set_login_info(root))
login_info.place(x=35, y=120, width=150, height=30)


# 乘车人信息
login_info = tkinter.Button(root, text='设置乘车人信息', font=(
    '华文彩云', 12, 'bold'), fg='#61f825', background='black', command=lambda root = root :AccountIO.set_seat_info(root))
login_info.place(x=850, y=120, width=180, height=30)

# 设置标签
name = tkinter.Label(root, text='12306车票查询与抢票', font=(
    "华文彩云", 30, "bold"), fg="#0000CD",background='white')
name.place(x=320, y=20, width=420, height=60)

# 设置时间文本标签
time_label = tkinter.Label(root, font=("华文彩云", 15, "bold"), fg="#1E90FF")
time_label.place(x=370, y=80, width=320, height=30)

# 定义显示时间的函数


def showtime():
    # 时间格式化处理
    string = strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text='当前时间：'+string)
    # 每隔 1秒钟执行time函数
    time_label.after(1000, showtime)


# 调用showtime()函数
showtime()
# =========================================================================================================

# 出发站
label = tkinter.Label(root, text='出发站:', font=(
    '', 12, 'bold'), background='#D3D3D3')
label.place(x=20, y=180, width=60, height=30)
start_place = tkinter.Entry(root, font=('', 12, 'bold'), fg='#CD9B1D')
start_place.place(x=90, y=180, width=100, height=30)

# 目的站
label = tkinter.Label(root, text='目的站:', font=(
    '', 12, 'bold'), background='#D3D3D3')
label.place(x=220, y=180, width=60, height=30)
end_place = tkinter.Entry(root, font=('', 12, 'bold'), fg='#CD9B1D')
end_place.place(x=290, y=180, width=100, height=30)

# 出发时间
label = tkinter.Label(root, text='出发时间:', font=(
    '', 12, 'bold'), background='#D3D3D3')
label.place(x=420, y=180, width=80, height=30)
start_time = tkinter.Entry(root, font=('', 12, 'bold'), fg='#38a11b')
start_time.insert(0, Today)
start_time.place(x=510, y=180, width=100, height=30)


# IntVar() 用于处理整数类型的变量
v = tkinter.IntVar()
radio_button1 = tkinter.Radiobutton(
    root, text="普通票", variable=v, value=1, command=lambda x=v.get(): chioce(v.get()))
radio_button1.place(x=640, y=170)
radio_button2 = tkinter.Radiobutton(
    root, text="学生票", variable=v, value=2, command=lambda x=v.get(): chioce(v.get()))
radio_button2.place(x=640, y=195)

# 默认为普通票
radio_button1.select()


def chioce(x):    # 点击单选框设置用户类型
    type = 1
    if x == 2:
        type = 2
    # 重置查询和购买按钮绑定数据
    JB1 = tkinter.Button(root, text='查询', font=('', 12, 'bold'), background='#FFE4B5', command=lambda start_place=start_place,
                         end_place=end_place, start_time=start_time, user_type=type: chick_info(start_place, end_place, start_time, user_type))
    JB1.place(x=750, y=180, width=60, height=30)

    JB2 = tkinter.Button(root, text='预订', font=('', 12, 'bold'), background="#54FF9F", command=lambda start_Place=start_place, end_Place=end_place,
                         start_Time=start_time, user_type=type, tree_Number=tree_Number: buy_ticket(start_Place, end_Place, start_Time, user_type, tree_Number))
    JB2.place(x=970, y=180, width=60, height=30)


# 查询按钮
JB1 = tkinter.Button(root, text='查询', font=('', 12, 'bold'), background='#FFE4B5', command=lambda start_place=start_place,
                     end_place=end_place, start_time=start_time, user_type=1: chick_info(start_place, end_place, start_time, user_type))
JB1.place(x=750, y=180, width=60, height=30)

# 输入车次
tree_Number = tkinter.Entry(root, font=('', 10, 'bold'), fg='#A020F0')
tree_Number.place(x=850, y=180, width=100, height=30)
tree_Number.insert(0, '输入车次序号')

# 购票按钮
JB2 = tkinter.Button(root, text='预订', font=('', 12, 'bold'), background="#54FF9F", command=lambda start_Place=start_place, end_Place=end_place,
                     start_Time=start_time, user_type=1, tree_Number=tree_Number: buy_ticket(start_Place, end_Place, start_Time, user_type, tree_Number))
JB2.place(x=970, y=180, width=60, height=30)

# =========================================================================================================

# 设置展示区
f = tkinter.Frame(root, background="#BEBEBE")
f.place(x=20, y=230, width=1040, height='360')

# 展示窗口
root.mainloop()
