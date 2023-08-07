import re
import tkinter as tk
from tkinter import ttk
import json
import os

DATA_PATH = "./gui_to_spider.json"

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("instagram spider")
        self.window.geometry("1500x800")
        self.amount = 0
        self.keyword = ""
        self.mode = "recent"
        self.mode_list = ["top", "recent"]
        self.create_widgets()
        
    def create_widgets(self):
        self.left_frame = tk.Frame(self.window)
        self.left_frame.pack(side="left",padx=5, pady=5, fill="y")

        self.right_frame = tk.Frame(self.window)
        self.right_frame.pack(side="right", padx=5, pady=5, fill="y")


        self.log_text = tk.Text(self.right_frame, font="microsoftYahei", width=60, height=20,state="disabled")
        self.log_text.pack(side="bottom", anchor="se")

        self.clear_butn = tk.Button(self.right_frame, font="microsoftYahei",height=1, text="clear log", command=self.clear_log)
        self.clear_butn.pack(side="bottom",anchor="sw")


        # self.str_interval.set(str(self.interval/1000))
        vcmd = (self.window.register(self.validate),"%P")
        ivcmd = (self.window.register(self.invalidate),)
        self.keyword_label = tk.Label(self.left_frame, text="标签(关键词):",font="microsoftYahei")
        self.keyword_entry = ttk.Entry(self.left_frame, width=18, font="microsoftYahei", textvariable= self.keyword,validate="focusout",validatecommand=vcmd,invalidcommand=ivcmd)#interval submit entry
        self.submit_button = tk.Button(self.left_frame, text="提交数据",height=1,width=11, command=self.submit,font="microsoftYahei")
        self.label_error = tk.Label(self.left_frame,fg="red")

        self.keyword_label.grid(row=0, column=0,sticky=tk.E)
        self.keyword_entry.grid(row=0, column=1,sticky=tk.W)
        self.label_error.grid(row=1,column=1,sticky=tk.NW)
        self.submit_button.grid(row=0, column=2)

        self.combobox_label = tk.Label(self.left_frame, text="获取数据模式:", font="microsoftYahei")
        self.combobox_label.grid(row=2, column=0, sticky=tk.E)

        self.mode_combobox = ttk.Combobox(self.left_frame, values=self.mode_list, font="microsoftYahei",state="readonly",width=18)
        self.mode_combobox.current(0)
        self.mode_combobox.grid(row=2,column=1,sticky=tk.W)

        self.amount_label = tk.Label(self.left_frame,  text="查找数目:", font="microsoftYahei")
        self.amount_label.grid(row=3, column=0, sticky=tk.E)

        self.amount_entry = tk.Entry(self.left_frame, font="microsoftYahei", width=18)
        self.amount_entry.grid(row=3, column=1, sticky=tk.W)

        self.launch_button = tk.Button(self.left_frame, text="启动", font="microsoftYahei", command=self.launch, height=1, width=11)
        self.launch_button.grid(row=4, column=1, sticky=tk.E)

        self.data_change()
        self.window.mainloop()
        return self.window

    def show_message(self,error='',color="black"):
        """
        show the error message
        """
        self.label_error['text'] = error
        self.keyword_entry['foreground'] = color

    def validate(self, value):
        """
        scan interval entry validation rules
        """
        pattern = re.compile(r'^[a-zA-Z\u4e00-\u9fff0-9]+$')
        if pattern.match(value) is not None:
            return True
        self.show_message("ok")
        print(value)
        return False

    def invalidate(self):
        self.show_message("关键词不能有空格或者特殊字符!","red")

    def submit(self):
        self.log_text.focus()
        try:
            self.keyword = self.keyword_entry.get()
            self.mode = self.mode_combobox.get()
            self.amount = self.amount_entry.get()
            self.log_text.config(state="normal")
            self.log_text.insert("end","keyword: "+self.keyword+" s\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        except ValueError:
            return False
        
    def launch(self):
        os.system("python bot_ctrl.py")
    
    def clear_log(self):
        """
        clear log text 
        """
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
    
    def data_change(self):
        with open(DATA_PATH, "r") as file:
            data = json.load(file)
        data['keyword'] = self.keyword
        data['amount'] = self.amount
        data['mode'] = self.mode

        with open(DATA_PATH, "w") as file:
            json.dump(data, file)
                