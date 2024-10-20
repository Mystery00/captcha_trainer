# coding=utf-8
import hashlib
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import os, shutil


class VCodeMarker:
    def __init__(self):
        self.image_list = []
        self.index = 0
        self.total = 0
        self.image_old = 'E:\\Downloads\\xhu-jwc\\vcode-failed\\'
        self.image_new = 'E:\\Downloads\\xhu-jwc\\mark\\'

        self.window = Tk()
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        ww = 400
        wh = 200
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        self.window.title("验证码标记工具")

        self.file_path = Label(self.window, text='当前文件名称：')
        self.file_path.pack(side=TOP)

        frame1 = Frame(self.window)
        frame1.pack()
        self.image = Label(frame1)
        self.image.pack(side=TOP)
        self.input = Entry(frame1, bd=2)
        self.input.pack(side=BOTTOM)

        def func(event):
            self.input.delete(0, END)

        self.input.bind("<BackSpace>", func)  # 键盘事件
        self.input.bind('<KeyPress>',
                        lambda e: e if e.keycode != 299 and e.char in set(
                            '0123456789abcdefghijklmnopqrstuvwxyz') else "break")
        self.input.bind('<Key-Return>', self.rename)

        frame2 = Frame(self.window)
        frame2.pack(side=BOTTOM)
        self.progress = Label(frame2, text=str(self.index) + '/' + str(self.total))
        self.progress.pack(side=LEFT)
        self.button = Button(frame2, text='开始', command=self.get_image_list)
        self.button.pack(side=RIGHT)

        self.window.mainloop()

    def show_image(self):
        if self.index >= self.total:
            messagebox.showinfo('提示', '已完成')
            self.window.destroy()
            return
        self.file_path.config(text='当前文件名称：' + os.path.basename(self.image_list[self.index]))
        self.pilImage = Image.open(self.image_list[self.index])
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image.configure(image=self.tkImage)
        self.progress.config(text=str(self.index) + '/' + str(self.total))

    def get_image_list(self):
        self.index = 0
        for file in os.listdir(self.image_old):
            file_path = os.path.join(self.image_old, file)
            self.image_list.append(file_path)
            self.total += 1
        self.show_image()

    def rename(self, event):
        old_name = self.image_list[self.index]
        name = self.input.get()
        if len(name) != 6:
            messagebox.showinfo('提示', '验证码长度必须为6')
            return
        self.input.delete(0, END)
        with open(old_name, 'rb') as f:
            data = f.read()
        file_md5 = hashlib.md5(data).hexdigest()
        f.close()
        new_file_path = self.image_new + name + '_' + file_md5 + '.png'
        shutil.move(old_name, new_file_path)
        self.index += 1
        self.show_image()


VCodeMarker()
