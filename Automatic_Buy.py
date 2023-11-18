from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import AccountIO
from tkinter import simpledialog
import tkinter


def Automatic_ticket_purchasing(start_Place, end_Place, start_Time, user_type, index, Cookie):

    # 判断是否是第一次登录
    if (len(Cookie) == 0):

        try:
            # 读取登录信息
            info = AccountIO.getUserInfo()
            # 账号
            user_name = str(info[1])
            # 密码
            password = str(info[2])
            # #身份证后四位
            id_card = str(info[3])

            # 打开浏览器
            driver = webdriver.Chrome()

            # 打开12306网站
            driver.get("https://kyfw.12306.cn/otn/resources/login.html")

            print(user_name,password,id_card)
            
            # 输入账号密码
            driver.find_element(By.CSS_SELECTOR, "#J-userName").send_keys(user_name)
            driver.find_element(By.CSS_SELECTOR, "#J-password").send_keys(password)

            # 点击登录
            driver.find_element(By.CSS_SELECTOR, "#J-login").click()

            # 延时等待,等待网页加载
            driver.implicitly_wait(10)

            # 输入验证信息
            driver.find_element(By.CSS_SELECTOR, "#id_card").send_keys(id_card)

            # 点击发送验证码
            driver.find_element(By.CSS_SELECTOR, "#verification_code").click()

            # 人工输入验证码
            code = simpledialog.askstring(title='验证码', prompt='输入手机上接收的验证码:')
            driver.find_element(By.CSS_SELECTOR, "#code").send_keys(code)

            # 确认验证
            driver.find_element(By.CSS_SELECTOR, "#sureClick").click()

            # 等待登录成功
            time.sleep(3)

            # 获取cookie
            Cookie = driver.get_cookies()
        except:
            tkinter.messagebox.showinfo('登录失败！', '请检查网络或重置登录信息！')
            return  Cookie
    else:
        # 第二次直接绕过登录，打开浏览器,直接进入登录界面
        driver = webdriver.Chrome()
        # 用来指定cookie属于哪个网站
        driver.get("https://kyfw.12306.cn/otn/resources/login.html")

        print(Cookie)

        # 添加cookie
        for c in Cookie:
            if 'expiry' in c:
                del c['expiry']
            driver.add_cookie(c)

        # 进入登录好的页面
        driver.get("https://kyfw.12306.cn/otn/view/index.html")
        # 等待登录成功
        time.sleep(3)
    try:
        # 点击车票预订
        driver.find_element(By.CSS_SELECTOR, "#link_for_ticket").click()

        # 输入出发地和目的地和时间
        driver.find_element(By.CSS_SELECTOR, "#fromStationText").click()  # 点击输入框
        driver.find_element(By.CSS_SELECTOR, "#fromStationText").clear()  # 清空输入框
        driver.find_element(By.CSS_SELECTOR, "#fromStationText").send_keys(
            str(start_Place.get()))
        # 在下拉框中找到地址
        driver.find_element(
            By.XPATH, f"//*[@id=\"panel_cities\"]//span[text()=\"{start_Place.get()}\"]").click()

        driver.find_element(By.CSS_SELECTOR, "#toStationText").click()
        driver.find_element(By.CSS_SELECTOR, "#toStationText").clear()
        driver.find_element(By.CSS_SELECTOR, "#toStationText").send_keys(
            str(end_Place.get()))
        driver.find_element(
            By.XPATH, f"//*[@id=\"panel_cities\"]//span[text()=\"{end_Place.get()}\"]").click()

        driver.find_element(By.CSS_SELECTOR, "#train_date").click()
        driver.find_element(By.CSS_SELECTOR, "#train_date").clear()
        driver.find_element(By.CSS_SELECTOR, "#train_date").send_keys(
            str(start_Time.get()))
        driver.find_element(By.CSS_SELECTOR, "#train_date").send_keys(Keys.ENTER)

        type = ''
        # 选择车票类型
        if user_type == 1:
            type = 'sf1'
        else:
            type = 'sf2'
        driver.find_element(
            By.CSS_SELECTOR, value=f"input[type='radio'][name='sf'][id={type}]").click()

        # 点击查询
        driver.find_element(By.CSS_SELECTOR, "#query_ticket").click()

        # 这里必须得休眠1-2秒，等结果查询完毕
        time.sleep(2)

        # 点击预订
        index = 2*(index+1) - 1
        # 开发者工具，ctrl+F，找到对应的元素(对应车次的预订按钮)
        driver.find_element(
            By.CSS_SELECTOR, f"#queryLeftTable tr:nth-child({index}) .btn72").click()

        # 等待网页加载完毕
        time.sleep(2)

        # 取得座位信息
        info = AccountIO.getSeatInfo()


        # 选择乘车人
        driver.find_element(By.XPATH, f"//*[@id=\"normal_passenger_id\"]/li/label[text()=\"{info[1]}\"]").click()

        # 选择座席(尝试)
        try:
            driver.find_element(By.XPATH, f"//*[@id=\"seatType_1\"]/option[contains(text(), \"{info[2]}\")]").click()
        except:
            pass

        if user_type == 2:
            # 确认购买学生票
            driver.find_element(By.CSS_SELECTOR, "#dialog_xsertcj_ok").click()

        time.sleep(2)

        # 提交订单
        driver.find_element(By.CSS_SELECTOR, "#submitOrder_id").click()

        # 等待网页加载完毕
        time.sleep(3)

        # 选择座位位置(尝试)
        try:
            if info[3] == 2:   # 过道
                driver.find_element(By.XPATH,'//*[@id="id-seat-sel"]//div[@style=\'display: block;\']//a[@id=\'1D\']').click()
            else:              # 靠窗
                driver.find_element(By.XPATH,'//*[@id="id-seat-sel"]//div[@style=\'display: block;\']//a[@id=\'1F\']').click()
        except:
            pass

        # 选择床位(尝试)
        try:
            if info[4] == 3:   # 上铺
                driver.find_element(By.XPATH, '//*[@id="id-bed-sel"]/div[2]/div/div[3]/div[2]/a[2]').click()
            elif info[4] == 4:              # 中铺
                driver.find_element(By.XPATH, '//*[@id="id-bed-sel"]/div[2]/div/div[2]/div[2]/a[2]').click()
            else:
                driver.find_element(By.XPATH, '//*[@id="id-bed-sel"]/div[2]/div/div[1]/div[2]/a[2]').click()
        except:
            pass

        time.sleep(2)
        #购票
        driver.find_element(By.CSS_SELECTOR, "#qr_submit_id").click()

        time.sleep(3)

        #可能的弹窗
        try:
            driver.find_element(By.CSS_SELECTOR, "#qd_closeDefaultWarningWindowDialog_id").click()
        except:
            pass
        
        # 弹出提示
        tkinter.messagebox.showinfo('预订成功！', '请在手机上支付订单！')

    except:
        tkinter.messagebox.showinfo('预订失败！', '检查车次信息，余票情况，车票类型是否正确！')
        
    return Cookie

#//*[@id="id-bed-sel"]/div[2]/div/div[1]/div[2]/a[2]