import difflib
import functools
import logging
import re
import sqlite3
import tkinter as tk
from tkinter import messagebox
import requests
import xlwt
import json


# init_system()
def option():
    answer = []  # 答案缓存
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s - %(lineno)d"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(
        filename='log.txt',
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT)
    root = tk.Tk()
    root.title("HiCity")
    root.geometry('800x500')
    conn = sqlite3.connect('City.db')
    cursor = conn.cursor()
    cursor.execute('select name from City_num')
    values1 = [x[0] for x in cursor.fetchall()]

    def handler1(event, enter, name_list):  # 文本框输入补全事件函数
        pattern = re.compile(r' ' + enter.get() + r'\S+')
        name = ''
        for x in name_list:
            name += x + ' '
        answer1 = re.search(pattern, name)
        if answer1 is not None:
            enter.insert(tk.INSERT, str(answer1.group())[2:])
        else:
            return

    def handler_consist(func, *args):  # 文本框事件补全函数中继
        return lambda event, fun=func, arg=args: fun(event, *arg)

    def show():  # 确认摁钮函数
        name3 = entry.get()
        if name3 not in values1:
            logging.debug("用户进行了错误输入")
            name_list2 = difflib.get_close_matches(name3, values1)
            if len(name_list2) > 0:
                messagebox.showerror(
                    title='error',
                    message='您输入的城市并不存在，是否想输入以下城市' +
                            str(name_list2))
            else:
                messagebox.showerror(
                    title='error',
                    message='您输入的城市并不存在，并且系统未为您找到最佳匹配')

        else:
            cursor.execute('select * from City_num where name ==?', (name3,))
            id_name = cursor.fetchall()[0][1]
            # request.insert(tk.INSERT, "查询成功，{0}编号是:{1}\n".format(name3, id_name))
            get_forecast(id_name)
            logging.debug("用户成功进行查询，搜索了城市%s,代码为%d,成功输出天气预报" % (name3, id_name))
            answer.append((name3, id_name))

    def backups():  # 备份函数
        logging.debug("系统已为用户进行备份，备份已存储于city.xls")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        worksheet.col(1).width = 3000
        alignment = xlwt.Alignment()
        # 垂直居中
        alignment.vert = xlwt.Alignment.VERT_CENTER
        for i in range(len(answer)):
            worksheet.write(i, 0, answer[i][0])
            worksheet.write(i, 1, answer[i][1])
        workbook.save('city.xls')
        messagebox.showinfo("保存", message="已成功保存于city.xls中")

    def quit1():
        logging.debug("系统已成功退出")
        quit()

    def get_forecast(city_num):
        request1.delete('1.0', 'end')
        weather = requests.get(
            'http://wthrcdn.etouch.cn/weather_mini?citykey=%d' %
            city_num)
        if weather.status_code == 200:
            wea_data = json.loads(weather.content)["data"]["forecast"]
        else:
            return
        list1 = ['日期', '最高温度', '风力', '最低温度', '风向', '天气状况']
        for i in wea_data:
            k = 0
            pattern = re.compile(r'CDATA\[(\S+)\]')
            s = re.search(pattern, i['fengli']).group()
            i['fengli'] = s[6:10]
            message = ''
            for j in i.values():
                message += "{}:{} ".format(list1[k], j)
                k += 1
            message += '\n'
            request1.insert(tk.INSERT, message)

    logging.debug("系统已被成功唤醒")
    my_label = functools.partial(tk.Button, root, font=30, bg='red')
    label1 = my_label(text="欢迎使用本系统", font=40)
    label1.config(width=40, height=2)
    label1.pack()
    label2 = my_label(text="数据正在载入")
    label2.pack()
    for i in range(0, len(values1)):
        label2.config(text="数据正在载入：{:.0f}%".format(i / len(values1) * 100))
        root.update()
    label3 = my_label(text="请输入您想查询的城市")
    label3.place(x=300, y=150)
    entry = tk.Entry(root, width=20, font=20)
    entry.place(x=300, y=200)
    entry.bind('<Tab>', handler_consist(handler1, entry, values1))
    my_button = functools.partial(tk.Button, root)
    button1 = my_button(text='确认')
    button2 = my_button(text='备份', command=backups)
    button2.place(x=400, y=250)
    button3 = my_button(text='退出', command=quit1)
    button1.place(x=350, y=250)
    button3.place(x=450, y=250)
    button1.config(command=show)
    request1 = tk.Text(root, width=50, height=10)
    request1.place(x=230, y=320)
    root.mainloop()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    option()
