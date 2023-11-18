import tkinter as tk
from tkinter import messagebox
import pandas as pd


# 获取用户信息
def getUserInfo():
    info = pd.read_csv('user_info.csv').iloc[0].tolist()
    return info

# 获取座位信息
def getSeatInfo():
    seat = pd.read_csv('seat_info.csv').iloc[0].tolist()
    return seat


# 设置用户信息
def set_login_info(root):

    #取取用户信息
    info = getUserInfo()

   #创建应用程序子窗口
    son = tk.Toplevel(root)

    # 设置窗口标题
    son.title('登录信息')

    # 设置窗口位置
    son.geometry('250x150+600+300')

    # 设置手机号
    user_name = tk.Label(son, text='手机号：')
    user_name.place(x=10, y=10)
    user_name_entry = tk.Entry(son)
    user_name_entry.place(x=60, y=10)
    user_name_entry.insert(0, str(info[1]))


    # 设置密码
    sit_type = tk.Label(son, text='密码：')
    sit_type.place(x=10, y=40)
    sit_type_entry = tk.Entry(son, show="*")
    sit_type_entry.place(x=60, y=40)
    sit_type_entry.insert(0, str(info[2]))

    # 身份验证
    id_card = tk.Label(son, text='身份证号后四位：')
    id_card.place(x=10, y=70)
    id_card_entry = tk.Entry(son)
    id_card_entry.place(x=110, y=70, width=60, height=20)
    id_card_entry.insert(0, str(info[3]))

    def retuen_info():
        if (user_name_entry.get() == '' or user_name_entry.get() is None or sit_type_entry.get() == '' or sit_type_entry.get() is None or id_card_entry.get() == '' or id_card_entry.get() is None):
            tk.messagebox.showinfo('提示', '请填写完整信息!')
            son.destroy()
        else:
            info = [[user_name_entry.get(), sit_type_entry.get(),id_card_entry.get()]]
            # 保存用户信息
            columns = ['手机号', '密码', '身份证号']
            pd.DataFrame(info,columns=columns).to_csv('user_info.csv')
            tk.messagebox.showinfo('提示', '信息已保存!')
            son.destroy()

    # 创建按钮
    button = tk.Button(
        son, text='确定', command=retuen_info, background='green')
    button.place(x=110, y=100, width=60)

    son.mainloop()


# 基本信息设置
def  set_seat_info(root):

    # 取座位信息
    info = getSeatInfo()

    # 创建子窗口
    son = tk.Toplevel(root)

    # 设置窗口标题
    son.title('设置坐席和偏好')

    # 设置窗口位置
    son.geometry('280x210+600+300')

    # 设置乘车人
    user_name = tk.Label(son, text='乘车人姓名：')
    user_name.pack()
    user_name_entry = tk.Entry(son)
    user_name_entry.pack()
    user_name_entry.insert(0, str(info[1]))

    # 设置席别
    sit_menu = tk.Label(son ,text='席别：')
    sit_menu.pack()
    var = tk.StringVar()
    var.set(str(info[2]))
    sit_menu_entry = tk.OptionMenu(son, var, "特等座", "一等座", "二等座", "软卧", "硬卧", "硬座", "无座","一等卧","二等卧","商务座")
    sit_menu_entry.pack()

    # 设置座位位置
    # IntVar() 用于处理整数类型的变量
    panel1 = tk.Frame(son)
    panel1.pack()
    v1 = tk.IntVar()
    radio_button1 = tk.Radiobutton(panel1, text="靠窗", variable=v1, value=1)
    radio_button1.pack(side='left')
    radio_button2 = tk.Radiobutton(panel1, text="过道", variable=v1, value=2)
    radio_button2.pack(side='right')

    # 初始化座位位置
    if(info[3] == 1):
        radio_button1.select()
    else:
        radio_button2.select()

    # 设置床位
    bed_menu = tk.Label(son, text='床位：')
    bed_menu.pack()
    panel2 = tk.Frame(son)
    panel2.pack()
    v2 = tk.IntVar()
    radio_button3 = tk.Radiobutton(panel2, text="上铺", variable=v2, value=3)
    radio_button3.pack(side='left')

    radio_button4 = tk.Radiobutton(panel2, text="中铺", variable=v2, value=4)
    radio_button4.pack(side='left')

    radio_button5 = tk.Radiobutton(panel2, text="下铺", variable=v2, value=5)
    radio_button5.pack(side='left')

    # 初始化床位
    if(info[4] == 3):
        radio_button3.select()
    elif(info[4] == 4):
        radio_button4.select()
    else:
        radio_button5.select()
    
    def retuen_info():

        if (user_name_entry.get() == '' or user_name_entry.get() == 'None'):
            tk.messagebox.showinfo('提示', '请填写完整信息!')
        else:
            info = [[user_name_entry.get(), var.get(), v1.get(), v2.get()]]    
            # 保存用户信息
            columns = ['乘车人姓名', '席别', '座位位置','床位']
            pd.DataFrame(info,columns=columns).to_csv('seat_info.csv')
            tk.messagebox.showinfo('提示', '信息已保存!')
            son.destroy()

    # 创建按钮
    button = tk.Button(
        son, text='确定', command=retuen_info, background='green')
    button.pack()

    son.mainloop()
