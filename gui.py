import re
import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("instagram spider")
        self.window.geometry("1500x800")
        self.cap = None
        self.keyword
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


        self.keyword = tk.StringVar()
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

        # self.combobox_label = tk.Label(self.left_frame, text="Select camera:", font="microsoftYahei")
        # self.combobox_label.grid(row=2, column=0, sticky=tk.E)


        self.switch_button = tk.Button(self.left_frame,text="open camera",height=1,width=11, command=self.combine_camera, font="microsoftYahei")
        self.switch_button.grid(row=2, column=2,sticky=tk.W)

        self.window.mainloop()

    def show_message(self,error='',color="black"):
        """
        show the error message
        """
        self.label_error['text'] = error
        self.keyword_entry['foreground'] = color

    def validate(self,value):
        """
        scan interval entry validation rules
        """
        pattern = re.compile(r'^[a-zA-Z\u4e00-\u9fff0-9]+$')
        if bool(pattern.match(pattern,value)):
            return True
        self.show_message("ok")
        print("show ")
        return False

    def invalidate(self):
        self.show_message("关键词不能有空格或者特殊字符!","red")

    def submit(self):
        self.log_text.focus()
        try:
            self.keyword = self.keyword_entry.get()

            self.log_text.config(state="normal")
            self.log_text.insert("end","System: Scan interval has been changed to "+self.keyword+" s\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        except ValueError:
            return False
    def clear_log(self):
        """
        clear log text 
        """

        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
    
    # control camera switch by button 
    def combine_camera(self):
        if self.cap == None:
            self.open_camera()
        else:
            self.close_camera()



    