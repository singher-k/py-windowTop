import tkinter as tk
import pyautogui
from pynput.mouse import Controller
import ctypes



def update_text():
    global a
    a=0
    if a != 0:
        top_label.after_cancel(a)
    #text = entry.get("1.0", "end")
    f=open('todo.txt','r',encoding='utf-8')
    text=f.read()
    top_label.config(text=text,anchor='w')
    a = top_label.after(1000, update_text)  # 每秒更新一次
    f.close()


def hide_entry():
    global checkVisible
    checkVisible=1
    #print('checkVisible*****',checkVisible)
    entry.pack_forget()  # 隐藏输入框
    entry.unbind("<Return>")  # 取消回车键绑定


def on_label_click(event):
    global x, y
    x, y = event.x, event.y

def on_label_drag(event):
    global x, y
    new_x = (event.x_root - x) - (top_label.winfo_width() // 2)
    new_y = (event.y_root - y) - (top_label.winfo_height() // 2)

    # 检查边界，确保字符串不会超出显示区域
    if new_x < 0:
        new_x = 0
    elif new_x + top_label.winfo_width() > screen_width:
        new_x = screen_width - top_label.winfo_width()

    if new_y < 0:
        new_y = 0
    elif new_y + top_label.winfo_height() > screen_height:
        new_y = screen_height - top_label.winfo_height()

    root.geometry(f"+{new_x}+{new_y}")

def show_label():
    if not mouse:
        return
    if not mouse.position:
        return 
    if mouse.position[1]<=1 and mouse.position[0] < 500:
        new_x=root.winfo_x()
        new_y=0
        root.geometry(f"+{new_x}+{new_y}")
    else:
        #root.withdraw()  # 隐藏窗口
        new_x=root.winfo_x()
        new_y=top_label.winfo_height()*-1
        root.geometry(f"+{new_x}+{new_y}")


checkVisible=0

# 获取锁屏状态
SPI_GETSCREENSAVERRUNNING = 114

root = tk.Tk()
root.overrideredirect(True)  # 隐藏窗口边框和标题栏
root.attributes("-topmost", True)  # 将窗口置于最顶层

entry = tk.Text(root)
entry.pack()
entry.focus()  # 设置输入框获得焦点
hide_entry()
#entry.bind("<Return>", lambda event: hide_entry())  # 按下回车键后隐藏输入框

top_label = tk.Label(root, text="",font=('Arial',18), fg="yellow", bg="black",anchor='w',justify='left',wraplength=500)
top_label.pack()

# 鼠标控制器
mouse = Controller()

update_text()  # 启动更新文本的函数

root.update_idletasks()  # 确保窗口已经被创建

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
top_label.bind("<Button-1>", on_label_click)  # 绑定鼠标左键点击事件
top_label.bind("<B1-Motion>", on_label_drag)  # 绑定鼠标左键拖动事件



while True:

    is_screen_saver_running = ctypes.windll.user32.SystemParametersInfoW(114, 0, 0, 0)
    
    # 判断是否锁屏
    if is_screen_saver_running:
        # 锁屏时的逻辑处理
        # 暂停逻辑的运行
        pass
    else:
        
        root.update()  # 更新窗口

        if top_label["text"]:
            top_label.config()  # 显示字符串时背景透明
        else:
            top_label.config(bg="black")  # 字符串为空时背景为黑色

        #top_label.bind("<Button-1>", on_label_click)  # 绑定鼠标左键点击事件
        #top_label.bind("<B1-Motion>", on_label_drag)  # 绑定鼠标左键拖动事件

        # 获取当前鼠标位置
        #print('当前鼠标位置： {}'.format(mouse.position))

        if checkVisible > 0:
            show_label()


root.mainloop()
