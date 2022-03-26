import json
import os
import sys
import tkinter
import tkinter.font
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
from functools import partial
from Controller import Controller

import logging
from tkinter import END, N, S, E, W, Scrollbar, Text


# 윈도우 창 생성
# 필요한 버튼 : 초기화, 수정 내용 저장, 파일 다시 읽기(전체 읽기)
# 컴파일 시 리소스 가져오기
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_gui():
    # 컨트롤러 생성
    controller = Controller()

    window = tkinter.Tk()

    def close(event):
        window.destroy()  # if you want to bring it back

    window.bind('<Escape>', close)  # esc 로 종료 가능

    # 위치 설정
    window.lift()
    window.attributes('-topmost', 1)
    window.after(1, lambda: window.focus_force())
    window.attributes('-topmost', 0)

    window.title("Vampire Survival Moder by Redwing (v 1.0.0)")
    window.geometry("1100x800+500+100")
    # window.geometry("800x710-2500+700")
    # window.resizable(False, False)

    window.iconbitmap(resource_path('resource\\logo.png'))
    # window.iconphoto(False, tk.PhotoImage(file=resource_path('resource\\아멜리.jpg')))

    # 뱀파이어 서바이벌 타이틀
    img = tkinter.PhotoImage(file="resource\\title.png")
    title_label = tkinter.Label(window, image=img)
    title_label.pack()

    # 탐색기를 열어 폴더 찾기
    def select_path(entry):
        dir_path = filedialog.askdirectory(parent=window, initialdir="/", title='Please select a directory')
        entry.delete(0, len(entry.get()))
        entry.insert(0, dir_path)

    default_font = tkinter.font.Font(size=12, weight="bold")

    # 경로 프레임
    resource_path_frame = tkinter.Frame(window)
    resource_path_frame.pack(side="top")

    resource_label = tkinter.Label(resource_path_frame, text="Resource Path : ", width=15)
    resource_label.pack(side="left")

    resource_entry = tkinter.Entry(resource_path_frame, width=100)
    resource_entry.pack(side="left")

    # 디폴트 경로
    resource_default_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Vampire Survivors"
    if os.path.isdir(resource_default_path):
        resource_entry.insert(0, resource_default_path)

    resource_button = tkinter.Button(resource_path_frame, overrelief="groove", fg='black',
                                     text='Find Dir', command=partial(select_path, resource_entry))

    resource_button.pack(side="left", padx=10)

    # unpack 프레임
    unpack_path_frame = tkinter.Frame(window)
    unpack_path_frame.pack(side="top")

    unpack_label = tkinter.Label(unpack_path_frame, text="Unpacked Path : ", width=15)
    unpack_label.pack(side="left")

    unpack_entry = tkinter.Entry(unpack_path_frame, width=100)
    unpack_entry.pack(side="left")

    # 디폴트 경로
    unpack_default_path = os.path.join(Controller.unpack_dir_name, Controller.resource_dir_name)
    if os.path.isdir(unpack_default_path):
        unpack_entry.insert(0, unpack_default_path)

    unpack_button = tkinter.Button(unpack_path_frame, overrelief="groove", fg='black',
                                   text='Find Dir', command=partial(select_path, unpack_entry))

    unpack_button.pack(side="left", padx=10)

    # mode 프레임
    mode_path_frame = tkinter.Frame(window)
    mode_path_frame.pack(side="top")

    mode_label = tkinter.Label(mode_path_frame, text="Mode Path      : ", width=15)
    mode_label.pack(side="left")

    mode_entry = tkinter.Entry(mode_path_frame, width=100)
    mode_entry.pack(side="left")

    mode_button = tkinter.Button(mode_path_frame, overrelief="groove", fg='black',
                                 text='Find Dir', command=partial(select_path, mode_entry))

    mode_button.pack(side="left", padx=10)

    # 버튼 프레임
    button_frame = tkinter.Frame(window)
    button_frame.pack(side="top", pady=20)

    # 언팩 실행
    def unpack():
        path = resource_entry.get()
        abspath = controller.unpack_resource(path)
        if abspath is None:
            err_msg = f"Wrong Path!\nPlease select Vampire Survival Resource Path!\nex) C:\Program Files (x86)\Steam\steamapps\common\Vampire Survivors"
            messagebox.showerror(title="Error!", message=err_msg)
        else:
            messagebox.showinfo(title="Result", message=f"Unpack Success!\noutput : {abspath}")
            unpack_entry.delete(0, len(unpack_entry.get()))
            unpack_entry.insert(0, unpack_default_path)

    # 언팩
    unpack_button = tkinter.Button(button_frame, overrelief="groove", fg='black', font=default_font,
                                   text='Unpack Resource', command=unpack)

    unpack_button.pack(side="left", padx=10)

    # 리팩 실행
    def repack():
        path = unpack_entry.get()
        abspath = controller.repack_resource(path)
        # abspath = controller.unpack_resource(path)
        if abspath is None:
            err_msg = f"Wrong Path!\nPlease select Vampire Survival Resource Path!\nex) repack_result\\img"
            messagebox.showerror(title="Error!", message=err_msg)
        else:
            messagebox.showinfo(title="Result", message=f"Unpack Success!\noutput : {abspath}")

    # 언팩
    repack_button = tkinter.Button(button_frame, overrelief="groove", fg='black', font=default_font,
                                   text='Repack Resource', command=repack)

    repack_button.pack(side="left", padx=10)

    # 모드 설치
    def install():
        original_path = resource_entry.get()
        mode_path = mode_entry.get()

        if mode_path == "":
            err_msg = f"Please Select Vampire Survival Mode!"
            messagebox.showerror(title="Error!", message=err_msg)
        else:
            abspath = controller.install_mode(original_path, mode_path)
            # abspath = controller.unpack_resource(path)
            if abspath is None:
                err_msg = f"Wrong Path!\nPlease select Vampire Survival Resource Path!\nex) install_result\\img"
                messagebox.showerror(title="Error!", message=err_msg)
            else:
                messagebox.showinfo(title="Result", message=f"Unpack Success!\noutput : {abspath}")

    install_button = tkinter.Button(button_frame, overrelief="groove", fg='black', font=default_font,
                                    text='Install Mode', command=install)

    install_button.pack(side="left", padx=10)

    # log_box = tkinter.Text(window, height=50, width=150)
    # log_box.pack()

    default_text = '1234'
    width, height = 150, 25
    log_box = LoggingHandlerFrame(window)
    # log_box = LoggingHandlerFrame(window, width=width, height=height, wrap='word')

    # set default text if desired
    # log_box.insert(1.0, default_text)
    log_box.pack(side="top")

    # 메인루프 시작
    window.mainloop()



class LoggingHandlerFrame(ttk.Frame):

    class Handler(logging.Handler):
        def __init__(self, widget):
            logging.Handler.__init__(self)
            self.setFormatter(logging.Formatter("%(message)s"))
            self.widget = widget
            self.widget.config(state='disabled')

        def emit(self, record):
            self.widget.config(state='normal')
            self.widget.insert(END, self.format(record) + "\n")
            self.widget.see(END)
            self.widget.config(state='disabled')

    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky=(N,S,E))

        self.text = Text(self, yscrollcommand=self.scrollbar.set, width=150, height=25)
        self.text.grid(row=0, column=0, sticky=(N,S,E,W))

        self.scrollbar.config(command=self.text.yview)

        self.logging_handler = LoggingHandlerFrame.Handler(self.text)
        logger = logging.getLogger()
        logger.addHandler(self.logging_handler)