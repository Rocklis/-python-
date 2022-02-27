from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.messagebox import askokcancel
from tkinter.messagebox import askyesnocancel
import tkinter as tk
import os
import sys
import datetime
from tkinter.filedialog import askopenfilename
from merge_Sort import mergeSort
from find_items import find_item1
from find_items import find_exist

# 由相对路径得到绝对路径 ；在程序打包的时候会用到
def get_resources_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


IMAGE_PATH_login = get_resources_path(os.path.join("resources", "login.png"))
LOGO_PATH = get_resources_path(os.path.join("resources", "plane.ico"))
IMAGE_PATH = get_resources_path(os.path.join("resources", "plane_cr.png"))

class LoginWindow:
    def __init__(self):
        self.root_login = tk.Tk()
        self.root_login.title("登入窗口")
        self.root_login.geometry("600x420+420+150")
        self.root_login.iconbitmap(LOGO_PATH)
        self.root_login.resizable(False, False)
        self.root_login["background"] = "white"
        ## widget
        self.style_login = ttk.Style()
        self.style_login.configure("login.TPanedwindow", bg="Azure")
        ## login_label(登入图片）
        self.login_image = tk.PhotoImage(file=IMAGE_PATH_login)
        self.login_label = tk.Label(self.root_login, image=self.login_image)
        self.login_label.place(x=3, y=10)

        ## 定义下方容器，登入标签以及文本框，按钮

        self.botton_pane = ttk.Panedwindow(self.root_login, style="login.TPanedwindow", width=600, height=80)
        self.botton_pane.place(x=0, y=340)
        self.label_user_name = tk.Label(self.botton_pane, text="用户名：", font=("华文黑体", 13, "bold"), bg="white",
                                        fg="black")
        self.label_user_name.place(x=6, y=25)
        self.entry_user = tk.Entry(self.botton_pane, width=15)
        self.entry_user.place(x=80, y=25)
        self.label_user_key = tk.Label(self.botton_pane, text="密码：", font=("华文黑体", 13, "bold"), bg="white",
                                       fg="black")
        self.label_user_key.place(x=200, y=25)
        self.entry_key = tk.Entry(self.botton_pane, width=15,show="*")
        self.entry_key.place(x=270, y=25)

        self.login_button = tk.Button(self.botton_pane, text="登录", font=("华文黑体", 13, "bold"))
        self.login_button.place(x=500, y=20)
        self.login_button.bind("<Button-1>", self.login_handle)

        self.root_login.mainloop()

    # 登入控制函数
    def login_handle(self, event):
        account = {}
        with open("account.txt",mode="r",encoding="utf-8") as ff:   # 读取account文件中的账户
            line_ff = ff.readline()
            while line_ff:
                username = line_ff.strip().split(',')[0]
                password = line_ff.strip().split(',')[1]
                account[username] = password
                line_ff = ff.readline()
        if self.entry_user.get() in account.keys() and self.entry_key.get() == account[self.entry_user.get()]:
            login_user = self.entry_user.get()
            self.root_login.destroy()
            MainWindow(login_user)
        else:
            showinfo(title="温馨提示",message="账号或密码错误")

class MainWindow:

    def __init__(self, name):
        # 自定义的变量

        self.user = name
        self.cur = datetime.datetime.now()
        # 加载gui
        self.root = tk.Tk()
        self.root.title = ("飞机订票系统")
        self.root.geometry("900x640+275+80")
        self.root.iconbitmap(LOGO_PATH)
        self.root.resizable(0, 0)
        self.root["bg"] = "skyblue"
        self.root.protocol("WM_DELETE_WINDOW", self.close_handle)
        self.all_fight_list = []  # 当前Treeview1中的所有信息，时刻随着“增删改查”进行动态的变化
        self.all_seek = []        # Treeview1 当前查找待购的航班记录
        self.find_texts = {}      # Treeview1  得到待购航班查询信息的内容，利用字典，方便进行查询
        self.all_seek2 = []       # Treeview2 当前查找已购的航班记录
        self.find_texts2 = {}     # Treeview2 得到已购航班查询信息的内容，利用字典，方便进行查询
        self.all_selected = []    # 当前Treeview2中的所有信息，时刻随着“增删改查”进行动态的变化
        self.file_path = ""       # 在打开文件时用到的路径
        self.setup_UI()
        self.load_info()
        self.root.mainloop()


    # 窗口关闭协议
    def close_handle(self):
        ret = askyesnocancel(title="退出提示", message="是否保存文件后退出")
        if ret == True:
            self.save()
            self.root.destroy()
        elif ret == False:
            self.root.destroy()
        else:
            pass

    def add_item(self):
        self.top_add = tk.Tk()
        self.top_add.title("添加信息")

        # self.top_add = tk.Toplevel()
        # self.top_add.title("添加航线信息")
        item_all = [[], [], [], [], [], [], [], []]
        item_all[0].append(tk.Label(self.top_add, text="航班号"))
        item_all[1].append(tk.Label(self.top_add, text="出发时间"))
        item_all[2].append(tk.Label(self.top_add, text="到站时间"))
        item_all[3].append(tk.Label(self.top_add, text="起点"))
        item_all[4].append(tk.Label(self.top_add, text="终点"))
        item_all[5].append(tk.Label(self.top_add, text="票价"))
        item_all[6].append(tk.Label(self.top_add, text="余额"))
        item_all[7].append(tk.Label(self.top_add, text="时长"))
        t1 = tk.Entry(self.top_add)
        t2 = tk.Entry(self.top_add)
        t3 = tk.Entry(self.top_add)
        t4 = tk.Entry(self.top_add)
        t5 = tk.Entry(self.top_add)
        t6 = tk.Entry(self.top_add)
        t7 = tk.Entry(self.top_add)
        t8 = tk.Entry(self.top_add)
        item_all[0].append(t1)
        item_all[1].append(t2)
        item_all[2].append(t3)
        item_all[3].append(t4)
        item_all[4].append(t5)
        item_all[5].append(t6)
        item_all[6].append(t7)
        item_all[7].append(t8)
        add_row = 0
        for group in item_all:
            add_column = 0
            for it in group:
                it.grid(row=add_row, column=add_column, padx=3, pady=2)
                add_column += 1
            add_row += 1
        bnt_add = tk.Button(self.top_add, text="确定",
                            command=lambda: self.tree_add(t1.get(), t2.get(), t3.get(), t4.get()
                                                          , t5.get(), t6.get(), t7.get(), t8.get()))
        bnt_add.grid(row=8, column=0, columnspan=2)

        self.top_add.mainloop()

    def tree_add(self, t1, t2, t3, t4, t5, t6, t7, t8):

        for list_one in self.all_fight_list:
            if t1 == list_one[0]:
                showinfo(title='警告', message='不允许有相同的航班号')
                return

        if t1 == '' or t2 == '' or t3 == '' or t4 == '' or t5 == '' or t6 == '' or t7 == '' or t8 == '':
            showinfo(title='警告', message='不允许相关信息为空')
            return
        self.Tree.insert("", index=tk.END, values=(t1, t2, t3, t4, t5, t6, t7, t8))
        self.all_fight_list.append([t1, t2, t3, t4, t5, t6, t7, t8])
        self.top_add.destroy()

    def delete_item(self):
        ret = askokcancel(title="温馨提示", message='确定进行数据的删除')
        if ret:
            id = self.Tree.selection()
            flight_one = list(self.Tree.item(id, 'values'))
            self.all_fight_list.remove(flight_one)
            self.Tree.delete(id)
        else:
            return


    def alter_item(self):
        x = self.Tree.selection()
        content = self.Tree.item(x, "values")
        self.top_alter = tk.Tk()
        self.top_alter.title("修改信息")
        item_all = [[], [], [], [], [], [], [], []]
        item_all[0].append(tk.Label(self.top_alter, text="航班号"))
        item_all[1].append(tk.Label(self.top_alter, text="出发时间"))
        item_all[2].append(tk.Label(self.top_alter, text="到站时间"))
        item_all[3].append(tk.Label(self.top_alter, text="起点"))
        item_all[4].append(tk.Label(self.top_alter, text="终点"))
        item_all[5].append(tk.Label(self.top_alter, text="票价"))
        item_all[6].append(tk.Label(self.top_alter, text="余额"))
        item_all[7].append(tk.Label(self.top_alter, text="时长"))
        t1 = tk.Entry(self.top_alter)
        t1.insert(0, content[0])
        t2 = tk.Entry(self.top_alter)
        t2.insert(0, content[1])
        t3 = tk.Entry(self.top_alter)
        t3.insert(0, content[2])
        t4 = tk.Entry(self.top_alter)
        t4.insert(0, content[3])
        t5 = tk.Entry(self.top_alter)
        t5.insert(0, content[4])
        t6 = tk.Entry(self.top_alter)
        t6.insert(0, content[5])
        t7 = tk.Entry(self.top_alter)
        t7.insert(0, content[6])
        t8 = tk.Entry(self.top_alter)
        t8.insert(0, content[7])
        item_all[0].append(t1)
        item_all[1].append(t2)
        item_all[2].append(t3)
        item_all[3].append(t4)
        item_all[4].append(t5)
        item_all[5].append(t6)
        item_all[6].append(t7)
        item_all[7].append(t8)
        add_row = 0
        for group in item_all:
            add_column = 0
            for it in group:
                it.grid(row=add_row, column=add_column, padx=3, pady=2)
                add_column += 1
            add_row += 1
        bnt_add = tk.Button(self.top_alter, text="确定",
                            command=lambda: self.tree_alter(t1.get(), t2.get(), t3.get(), t4.get()
                                                            , t5.get(), t6.get(), t7.get(), t8.get()))
        bnt_add.grid(row=8, column=0, columnspan=2)
        self.top_alter.mainloop()

    def tree_alter(self, t1, t2, t3, t4, t5, t6, t7, t8):
        if t1 == '' or t2 == '' or t3 == '' or t4 == '' or t5 == '' or t6 == '' or t7 == '' or t8 == '':
            showinfo(title='警告', message='不允许相关信息为空')
            return
        # 这里的逻辑有点不好想，先除去要改的航班号，方便下面的判断,以及添加
        x = self.Tree.selection()
        x_content = list(self.Tree.item(x, 'values'))
        index_before = self.all_fight_list.index(x_content)
        self.all_fight_list.remove(x_content)
        for list_one in self.all_fight_list:
            if t1 == list_one[0]:
                showinfo(title='警告', message="不允许有相同的航班号")
                self.all_fight_list.insert(index_before,x_content)
                return

        x_alter = [t1, t2, t3, t4, t5, t6, t7, t8]
        self.Tree.item(x, values=(t1, t2, t3, t4, t5, t6, t7, t8))
        self.all_fight_list.insert(index_before,x_alter)
        self.top_alter.destroy()

    # Treeview1 找到进行查询的条件，这里用到了字典,这里使用字典可以实现多条件查询
    def find_text(self):
        self.find_texts = {}
        sno = self.Entry_sno.get()
        if (sno != ''):
            self.find_texts['0'] = sno       # '0'是航班号在列表中的下标
        start = self.Entry_start.get()
        if (start != ''):
            self.find_texts['3'] = start    # '3'是出发时间在列表中的下标
        end = self.Entry_end.get()
        if (end != ''):
            self.find_texts['4'] = end      # '4'是到达时间在列表中的下标
        return len(self.find_texts)

    # 这里多条件的查询是使用迭代方法进行的
    def find_item(self):
        number = self.find_text()
        if (number == 0):
            return
        else:
            self.all_seek = []
            all_item_cur = []
            for it in self.Tree.get_children():
                all_item_cur.append(self.Tree.item(it, 'values'))
            self.all_seek = all_item_cur
            for index in self.find_texts.keys():
                self.all_seek = find_item1(self.all_seek, int(index), self.find_texts[index])

            # 如果没有查询到结果，进行相应的提示
            if (len(self.all_seek) == 0):
                showinfo(title="提示", message="无查询结果，请适当修改查询条件")
            # 查询到结果，进行数据的显示
            else:
                self.load_treeview(self.all_seek)

    def find_text2(self):
        self.find_texts2 = {}
        sno = self.Entry_sno_2.get()
        if (sno != ''):
            self.find_texts2['0'] = sno
        start = self.Entry_start_2.get()
        if (start != ''):
            self.find_texts2['3'] = start
        end = self.Entry_end_2.get()
        if (end != ''):
            self.find_texts2['4'] = end
        return len(self.find_texts2)

    def find_item2(self):
        number = self.find_text2()
        if (number == 0):
            return
        else:
            self.all_seek2 = []
            all_item_cur = []
            for it in self.Tree2.get_children():
                all_item_cur.append(self.Tree2.item(it, 'values'))
            self.all_seek2 = all_item_cur
            for index in self.find_texts2.keys():
                self.all_seek2 = find_item1(self.all_seek2, int(index), self.find_texts2[index])

            if (len(self.all_seek2) == 0):
                showinfo(title="提示", message="无查询结果，请适当修改查询条件")
            else:
                self.load_treeview2(self.all_seek2)

    def treeview_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)             # 将“k"ID的记录移动到下表为index的位置
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def treeview_mergesort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l = mergeSort(l, reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.treeview_mergesort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


    def select_item(self):

        self.top_number = tk.Tk()
        self.top_number.title("select")
        label_number = tk.Label(self.top_number, text="请输入票数")
        entry_number = tk.Entry(self.top_number)
        button_number = tk.Button(self.top_number, text="确定", command=lambda: self.select_confirm(entry_number.get()))
        label_number.grid(row=0, column=0)
        entry_number.grid(row=0, column=1)
        button_number.grid(row=0, column=2)

    def select_confirm(self, num):

        num = int(num)
        x = self.Tree.selection()
        x_content = list(self.Tree.item(x, 'values'))
        if num > int(x_content[6]):
            showinfo(title="温馨提示", message="超过了可选的最大票数")
            return
        elif num == int(x_content[6]):

            # 对待购的treeview以及相应的列表更新
            self.all_fight_list.remove(x_content)
            self.load_treeview(self.all_fight_list)
            # 进行已购航班的查询，若已有相应航班号的记录，只需修改次数即可，如果没有进行相应记录的添加
            index_x_2 = find_exist(self.all_selected, x_content[0])
            if index_x_2 != -1:
                self.all_selected[index_x_2][6] = str(int(self.all_selected[index_x_2][6]) + num)  # 如果已经存在，只需改变相应的记录的次数
                self.load_treeview2(self.all_selected)
            else:
                x_content[6] = str(num)
                self.all_selected.append(x_content)
                self.load_treeview2(self.all_selected)
        else:

            # 对待购的treeview以及相应的列表更新
            index_x = self.all_fight_list.index(x_content)
            self.all_fight_list[index_x][6] = str(int(self.all_fight_list[index_x][6]) - num)
            x_content[6] = str(int(x_content[6]) - num)
            self.Tree.item(x, values=x_content)

            # 进行已购航班的查询，若已有相应航班号的记录，只需修改次数即可，如果没有进行相应记录的添加
            index_x_2 = find_exist(self.all_selected, x_content[0])
            if index_x_2 != -1:
                self.all_selected[index_x_2][6] = str(int(self.all_selected[index_x_2][6]) + num)  # 如果已经存在，只需改变相应的记录的次数
                self.load_treeview2(self.all_selected)
            else:
                x_content[6] = str(num)
                self.all_selected.append(x_content)
                self.load_treeview2(self.all_selected)
        self.top_number.destroy()


    def cancel_selected(self):

        self.top_number2 = tk.Tk()
        self.top_number2.title("cancel")
        label_number = tk.Label(self.top_number2, text="请输入票数")
        entry_number = tk.Entry(self.top_number2)
        button_number = tk.Button(self.top_number2, text="确定", command=lambda: self.cancel_confirm(entry_number.get()))
        label_number.grid(row=0, column=0)
        entry_number.grid(row=0, column=1)
        button_number.grid(row=0, column=2)

    def cancel_confirm(self, num):
        num = int(num)
        x = self.Tree2.selection()
        x_content = list(self.Tree2.item(x, 'values'))
        if num > int(x_content[6]):
            showinfo(title="温馨提示", message="超过了可退的最大票数")
            return
        elif num == int(x_content[6]):
            # 对已购的treeview以及相应的列表更新
            self.all_selected.remove(x_content)
            self.load_treeview2(self.all_selected)
            # 进行代购航班的查询，若已有相应航班号的记录，只需修改次数即可，如果没有进行相应记录的添加
            index_x_2 = find_exist(self.all_fight_list, x_content[0])
            if index_x_2 != -1:
                self.all_fight_list[index_x_2][6] = str(
                    int(self.all_fight_list[index_x_2][6]) + num)  # 如果已经存在，只需改变相应的记录的次数
                self.load_treeview(self.all_fight_list)
            else:
                x_content[6] = str(num)
                self.all_fight_list.append(x_content)
                self.load_treeview(self.all_fight_list)
        else:
            # 对已购的treeview以及相应的列表更新
            index_x = self.all_selected.index(x_content)
            self.all_selected[index_x][6] = str(int(self.all_selected[index_x][6]) - num)
            x_content[6] = str(int(x_content[6]) - num)
            self.Tree2.item(x, values=x_content)

            # 进行代购航班的查询，若已有相应航班号的记录，只需修改次数即可，如果没有进行相应记录的添加
            index_x_2 = find_exist(self.all_fight_list, x_content[0])
            if index_x_2 != -1:
                self.all_fight_list[index_x_2][6] = str(
                    int(self.all_fight_list[index_x_2][6]) + num)  # 如果已经存在，只需改变相应的记录的次数
                self.load_treeview(self.all_fight_list)
            else:
                x_content[6] = str(num)
                self.all_fight_list.append(x_content)
                self.load_treeview(self.all_fight_list)

        self.top_number2.destroy()


    def save(self):

        with open("待购航班情况.txt", mode='w', encoding='utf-8', newline='') as f:
            for line in self.all_fight_list:
                f.writelines(",".join(line) + '\n')

        with open("已购航班情况.txt", mode="w", encoding='utf-8', newline='') as f2:
            for line2 in self.all_selected:
                f2.writelines(",".join(line2) + '\n')

    def setup_UI(self):

        # # 设定Style
        # self.Style01 = ttk.Style()
        # self.Style01.configure("left.TPanedwindow",background = "Azure")
        # self.Style01.configure("right.TPanedwindow", background="Azure")
        # self.Style01.configure("TButton",width = 10,font = ("华文黑体",15,"bold"))

        # Top_banner
        self.start_image = tk.PhotoImage(file=IMAGE_PATH)
        self.Lable_image = tk.Label(self.root, image=self.start_image)
        self.Lable_image.pack()
        self.user_label = tk.Label(self.root, text="当前用户：%s" % self.user, font=("华文黑体", 15, "bold"), bg="white",
                                   fg="black")
        self.user_label.place(x=650, y=35)
        self.date = tk.Label(self.root, text="当前日期：{}".format(self.cur.date()), font=("华文黑体", 15, "bold"), bg="white",
                             fg="black")
        self.date.place(x=650, y=60)
        # 设定选项卡
        self.notebook = ttk.Notebook(self.root)
        self.frame1 = tk.Frame()
        self.frame2 = tk.Frame()
        self.frame3 = tk.Frame()

        # frame1:左边容器及按钮组件
        self.Pane_left = tk.PanedWindow(self.frame1, width=162, bg="Azure")
        self.Pane_left.pack(fill=tk.Y, side=tk.LEFT, padx=2, pady=2)

        self.Button_add = tk.Button(self.Pane_left, text="信息添加", width=13, font=("华文黑体", 12, "bold"),
                                    command=self.add_item)
        self.Button_add.place(x=5, y=10)
        self.Button_alter = tk.Button(self.Pane_left, text="信息修改", width=13, font=("华文黑体", 12, "bold"),
                                      command=self.alter_item)
        self.Button_alter.place(x=5, y=40)
        self.Button_delete = tk.Button(self.Pane_left, text="信息删除", width=13, font=("华文黑体", 12, "bold"),
                                       command=self.delete_item)
        self.Button_delete.place(x=5, y=70)
        self.Button_select = tk.Button(self.Pane_left, text="选票", width=13, font=("华文黑体", 12, "bold"),
                                       command=self.select_item)
        self.Button_select.place(x=5, y=100)
        self.Button_modify = tk.Button(self.Pane_left, text="导入文件", width=13, font=("华文黑体", 12, "bold"),
                                       command=self.openfile)
        self.Button_modify.place(x=5, y=420)
        self.Button_save = tk.Button(self.Pane_left, text="保存数据", width=13, font=("华文黑体", 12, "bold"),
                                     command=self.save)
        self.Button_save.place(x=5, y=450)

        self.notebook.add(self.frame1, text="可选余票")
        self.notebook.add(self.frame2, text="已选购")
        self.notebook.add(self.frame3, text="客户信息")
        self.notebook.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)

        # frame1右边: 容器，查询、TreeView

        self.Pane_right = tk.PanedWindow(self.frame1, width=720, bg="Azure")
        self.Pane_right.pack(fill=tk.Y, side=tk.LEFT, padx=2, pady=2)

        # LabelFrame
        self.LabelFrame_query = tk.LabelFrame(self.Pane_right, text="航班信息查询", width=720, height=70)
        self.LabelFrame_query.place(x=2, y=2)
        # 添加控件
        self.Label_sno = tk.Label(self.LabelFrame_query, text="航班号：")
        self.Label_sno.place(x=5, y=13)
        self.Entry_sno = tk.Entry(self.LabelFrame_query, width=12)
        self.Entry_sno.place(x=50, y=10)

        self.Label_start = tk.Label(self.LabelFrame_query, text="起点：")
        self.Label_start.place(x=160, y=13)
        self.Entry_start = tk.Entry(self.LabelFrame_query, width=12)
        self.Entry_start.place(x=200, y=10)

        self.Label_end = tk.Label(self.LabelFrame_query, text="终点：")
        self.Label_end.place(x=300, y=13)
        self.Entry_end = tk.Entry(self.LabelFrame_query, width=12)
        self.Entry_end.place(x=340, y=10)

        self.Button_query = tk.Button(self.LabelFrame_query, text="查询", width=4, command=self.find_item)
        self.Button_query.place(x=520, y=10)
        self.Button_all = tk.Button(self.LabelFrame_query, text="显示全部", width=8,
                                    command=lambda: self.load_treeview(self.all_fight_list))
        self.Button_all.place(x=590, y=10)

        # 添加TreeView控件
        self.Tree = ttk.Treeview(self.Pane_right, columns=("sno", "st_time",
                                                           "fi_time", "origin", "destination", "price", "remaining",
                                                           "time"),
                                 show="headings", height=20)

        # 设置每一个列的宽度和对齐的方式
        self.Tree.column("sno", width=90, anchor="center")
        self.Tree.column("st_time", width=100, anchor="center")
        self.Tree.column("fi_time", width=100, anchor="center")
        self.Tree.column("origin", width=100, anchor="center")
        self.Tree.column("destination", width=100, anchor="center")
        self.Tree.column("price", width=70, anchor="center")
        self.Tree.column("remaining", width=80, anchor="center")
        self.Tree.column("time", width=70, anchor="center")
        # 设置每个列的标题
        self.Tree.heading("sno", text="航班号", command=lambda: self.treeview_sort_column(self.Tree, 'sno', False))
        self.Tree.heading("st_time", text="出发时间",
                          command=lambda: self.treeview_sort_column(self.Tree, 'st_time', False))
        self.Tree.heading("fi_time", text="到站时间",
                          command=lambda: self.treeview_sort_column(self.Tree, 'fi_time', False))
        self.Tree.heading("origin", text="起点",
                          command=lambda: self.treeview_sort_column(self.Tree, 'origin', False))
        self.Tree.heading("destination", text="终点",
                          command=lambda: self.treeview_sort_column(self.Tree, 'destination', False))
        self.Tree.heading("price", text="票价", command=lambda: self.treeview_mergesort_column(self.Tree, 'price', False))
        self.Tree.heading("remaining", text="余额",
                          command=lambda: self.treeview_mergesort_column(self.Tree, 'remaining', False))
        self.Tree.heading("time", text="时长", command=lambda: self.treeview_sort_column(self.Tree, 'time', False))

        self.Tree.place(x=2, y=72)
        self.VScroll1 = tk.Scrollbar(self.Pane_right, orient='vertical', command=self.Tree.yview)
        self.VScroll1.place(relx=0.980, rely=0.14, relwidth=0.024, relheight=0.86)
        # 给treeview添加配置
        self.Tree.configure(yscrollcommand=self.VScroll1.set)

        # frame2 左边组件：
        self.Pane_left_2 = tk.PanedWindow(self.frame2, width=162, bg="Azure")
        self.Pane_left_2.pack(fill=tk.Y, side=tk.LEFT, padx=2, pady=2)
        self.Button_cancel = tk.Button(self.Pane_left_2, text="退票", width=13, font=("华文黑体", 12, "bold"),
                                       command=self.cancel_selected)
        self.Button_cancel.place(x=5, y=10)

        # frame2 右边组件：
        self.Pane_right_2 = tk.PanedWindow(self.frame2, width=720, bg="Azure")
        self.Pane_right_2.pack(fill=tk.Y, side=tk.LEFT, padx=2, pady=2)

        self.Tree2 = ttk.Treeview(self.Pane_right_2, columns=("sno", "st_time",
                                                              "fi_time", "origin", "destination", "price", "remaining",
                                                              "time"),
                                  show="headings", height=20)

        # 设置每一个列的宽度和对齐的方式
        self.Tree2.column("sno", width=90, anchor="center")
        self.Tree2.column("st_time", width=100, anchor="center")
        self.Tree2.column("fi_time", width=100, anchor="center")
        self.Tree2.column("origin", width=100, anchor="center")
        self.Tree2.column("destination", width=100, anchor="center")
        self.Tree2.column("price", width=70, anchor="center")
        self.Tree2.column("remaining", width=80, anchor="center")
        self.Tree2.column("time", width=70, anchor="center")
        # 设置每个列的标题
        self.Tree2.heading("sno", text="航班号", command=lambda: self.treeview_sort_column(self.Tree2, 'sno', False))
        self.Tree2.heading("st_time", text="出发时间",
                           command=lambda: self.treeview_sort_column(self.Tree2, 'st_time', False))
        self.Tree2.heading("fi_time", text="到站时间",
                           command=lambda: self.treeview_sort_column(self.Tree2, 'fi_time', False))
        self.Tree2.heading("origin", text="起点",
                           command=lambda: self.treeview_sort_column(self.Tree2, 'origin', False))
        self.Tree2.heading("destination", text="终点",
                           command=lambda: self.treeview_sort_column(self.Tree2, 'destination', False))
        self.Tree2.heading("price", text="票价",
                           command=lambda: self.treeview_mergesort_column(self.Tree2, 'price', False))
        self.Tree2.heading("remaining", text="余额",
                           command=lambda: self.treeview_mergesort_column(self.Tree2, 'remaining', False))
        self.Tree2.heading("time", text="时长", command=lambda: self.treeview_sort_column(self.Tree2, 'time', False))

        self.Tree2.place(x=2, y=72)
        self.VScroll1_2 = tk.Scrollbar(self.Pane_right_2, orient='vertical', command=self.Tree2.yview)
        self.VScroll1_2.place(relx=0.980, rely=0.14, relwidth=0.024, relheight=0.86)
        # 给treeview添加配置
        self.Tree2.configure(yscrollcommand=self.VScroll1_2.set)

        # LabelFrame
        self.LabelFrame_query_2 = tk.LabelFrame(self.Pane_right_2, text="航班信息查询", width=720, height=70)
        self.LabelFrame_query_2.place(x=2, y=2)
        # 添加控件
        self.Label_sno_2 = tk.Label(self.LabelFrame_query_2, text="航班号：")
        self.Label_sno_2.place(x=5, y=13)
        self.Entry_sno_2 = tk.Entry(self.LabelFrame_query_2, width=12)
        self.Entry_sno_2.place(x=50, y=10)

        self.Label_start_2 = tk.Label(self.LabelFrame_query_2, text="起点：")
        self.Label_start_2.place(x=160, y=13)
        self.Entry_start_2 = tk.Entry(self.LabelFrame_query_2, width=12)
        self.Entry_start_2.place(x=200, y=10)

        self.Label_end_2 = tk.Label(self.LabelFrame_query_2, text="终点：")
        self.Label_end_2.place(x=300, y=13)
        self.Entry_end_2 = tk.Entry(self.LabelFrame_query_2, width=12)
        self.Entry_end_2.place(x=340, y=10)

        self.Button_query_2 = tk.Button(self.LabelFrame_query_2, text="查询", width=4, command=self.find_item2)
        self.Button_query_2.place(x=520, y=10)
        self.Button_all_2 = tk.Button(self.LabelFrame_query_2, text="显示全部", width=8,
                                      command=lambda: self.load_treeview2(self.all_selected))
        self.Button_all_2.place(x=590, y=10)

    def load_info(self):
        try:
            self.all_fight_list = []
            with open(file="待购航班情况.txt", mode="r", encoding="utf-8") as fd:
                # 一次读一行
                current_line = fd.readline()
                while current_line:
                    temp_list = current_line.strip().split(",")  # 长字符串分割层三个
                    self.all_fight_list.append(temp_list)
                    # 读取下一行,读完了循环就结束了
                    current_line = fd.readline()
            self.all_selected = []
            with open(file="已购航班情况.txt", mode="r", encoding="utf-8") as f:
                # 一次读一行
                current_line = f.readline()
                while current_line:
                    temp_list = current_line.strip().split(",")  # 长字符串分割层三个
                    self.all_selected.append(temp_list)
                    # 读取下一行,读完了循环就结束了
                    current_line = f.readline()
        except:
            showinfo("系统消息", "文件读取出现异常！")
        self.load_treeview(self.all_fight_list)
        self.load_treeview2(self.all_selected)

    def openfile(self):
        self.file_path = askopenfilename()
        if self.file_path == "":
            return
        self.load_file_flight_info()
        self.load_treeview(self.all_fight_list)
        # 重新导入文件，刷新Tree2和其对应的列表
        delete_all_tree2 = self.Tree2.get_children()
        for id in delete_all_tree2:
            self.Tree2.delete(id)
        self.all_selected = []


    def load_file_flight_info(self):
        if not os.path.exists(self.file_path):
            showinfo("系统消息", "提供的文件名不存在！")
        else:
            try:
                self.all_fight_list = []
                with open(file=self.file_path, mode="r", encoding="utf-8") as fd:
                    # 一次读一行
                    current_line = fd.readline()
                    while current_line:
                        temp_list = current_line.strip().split(",")  # 长字符串分割层三个
                        self.all_fight_list.append(temp_list)
                        # 读取下一行,读完了循环就结束了
                        current_line = fd.readline()
            except:
                showinfo("系统消息", "文件读取出现异常！")

    def load_treeview(self, current_list: list):
        # 每次加载前先进行数据的清除
        for row in self.Tree.get_children():
            self.Tree.delete(row)
        # 判断是否有数据：
        if len(current_list) == 0:
            showinfo("系统消息", "没有数据加载")
        else:
            for index in range(len(current_list)):
                self.Tree.insert("", index, values=(current_list[index][0], current_list[index][1],
                                                    current_list[index][2], current_list[index][3],
                                                    current_list[index][4], current_list[index][5],
                                                    current_list[index][6], current_list[index][7]))

    def load_treeview2(self, current_list: list):
        # 每次加载前先进行数据的清除
        for row in self.Tree2.get_children():
            self.Tree2.delete(row)
        # 判断是否有数据：
        if len(current_list) == 0:
            showinfo("系统消息", "没有数据加载")
        else:
            for index in range(len(current_list)):
                self.Tree2.insert("", index, values=(current_list[index][0], current_list[index][1],
                                                     current_list[index][2], current_list[index][3],
                                                     current_list[index][4], current_list[index][5],
                                                     current_list[index][6], current_list[index][7]))


if __name__ == '__main__':
    LoginWindow()
