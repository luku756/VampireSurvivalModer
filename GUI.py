import json
import os
import sys
import tkinter
import tkinter.font
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
from Controller import Controller


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

    # 언팩
    install_button = tkinter.Button(button_frame, overrelief="groove", fg='black', font=default_font,
                                   text='Install Mode', command=install)

    install_button.pack(side="left", padx=10)


    # 상단 메뉴 추가
    menubar = tkinter.Menu(window)

    # 초기화 메뉴 클릭
    # def click_clear_menu(menu):
    #     for s in Symbols: # 모든 버튼이 안 눌린 상태로 변경
    #         symbol_buttons[s]['button'].config(relief=RAISED)  # 눌린 상태 해제
    #         symbol_buttons[s]['state'] = ButtonState.unpressed
    #         symbol_buttons[s]['button']['background'] = 'SystemButtonFace'
    #
    #     if menu == 'new game':  # 랜덤유닛 선택지도 같이 초기화
    #         # 선택 데이터 초기화
    #         Units.reset_random_unit()
    #         # 심볼 이미지 초기화
    #         for u in Units.get_random_unit_list():
    #             random_unit_selected_symbols[u[0]][0].config(image=symbol_images[Symbols.random_color])  # 이미지 변경
    #             random_unit_selected_symbols[u[0]][1].config(image=symbol_images[Symbols.random_mark])  # 이미지 변경
    #
    #     display_right_units()  # 화면 갱신
    #
    # menubar.add_cascade(label="새 게임", command=partial(click_clear_menu, 'new game'))
    # menubar.add_cascade(label="선택 초기화", command=partial(click_clear_menu, 'clear'))
    # window.config(menu=menubar)
    #
    # # 이미지 정보는 변수를 유지하지 않으면 사라진다. 그러니 미리 불러오기
    # symbol_images = {}
    # for s in Symbols:
    #     img_path = f'resource\\symbols\\{s.value}.png'
    #     symbol_images[s] = PhotoImage(file=resource_path(img_path))
    #
    # # 이미지 정보는 변수를 유지하지 않으면 사라진다. 그러니 미리 불러오기
    # unit_images = {}
    # unit_list = Units.get_unit_list()
    # for unit in unit_list:
    #     img_path = f'resource\\units\\{unit[0]}.png'
    #
    #     # Resizing image to fit on button
    #     # photoimage = PhotoImage(file=img_path).subsample(2, 2)
    #     unit_images[unit[0]] = PhotoImage(file=resource_path(img_path))
    #
    #
    # upper_frame = tkinter.Frame(window)
    # upper_frame.pack(side="top")
    #
    # # 심볼 목록 표시
    # symbol_list_frame = tkinter.LabelFrame(upper_frame, text="심볼 선택")
    # symbol_list_frame.pack(side='left', fill="both", padx=10, pady=10)
    #
    # # 심볼 표시
    # symbol_list_window = tk.Text(symbol_list_frame, wrap="word", width='100', height='15', bg='SystemButtonFace', yscrollcommand=lambda *args: symbol_vsb.set(*args))
    # symbol_vsb = tk.Scrollbar(symbol_list_frame, command=symbol_list_window.yview)
    # symbol_vsb.pack(side="right", fill="y")
    # symbol_list_window.pack(side="left", fill="both", expand=True)
    #
    #
    # # 랜덤 유닛의 속성 선택
    # random_unit_select_symbol = tkinter.LabelFrame(upper_frame,  text="랜덤유닛 속성", width='5')
    # random_unit_select_symbol.pack(side="right")
    #
    # # label = tkinter.Label(random_unit_select_symbol, text="궁정화가 지르콘")
    # # label.pack(side='top')
    #
    # # 랜덤 유닛 심볼 정보
    # random_unit_selected_symbols = {}
    #
    # # 랜덤유닛의 옵션 설정 기능 추가
    # def add_random_unit(upper_widget, name):
    #     def click_menu(clicked, symbol_type, btn, unit_name):
    #         btn.config(image=symbol_images[clicked.value])  # 이미지 변경
    #         Units.set_random_unit_state(unit_name, symbol_type, clicked.value)  # 상태 결정
    #         display_right_units() # 화면 갱신
    #
    #     # 메뉴를 만들어 심볼 선택
    #     def create_menu(widget, unit_name):
    #         menu = tkinter.Menu(widget, tearoff=0)
    #         # print(widget['text'])
    #         if widget['text'] == '컬러랜덤':
    #             for s in ColorSymbols:
    #                 menu.add_command(image=symbol_images[s.value], command=partial(click_menu, s, widget['text'], widget, unit_name))
    #         else:
    #             for s in MarkSymbols:
    #                 menu.add_command(image=symbol_images[s.value], command=partial(click_menu, s, widget['text'], widget, unit_name))
    #
    #         widget["menu"] = menu
    #
    #     te = tkinter.LabelFrame(upper_widget, text=name)
    #
    #     symbol_1 = tkinter.Menubutton(te, image=symbol_images[Symbols.random_color], text=Symbols.random_color.value,
    #                                   relief="raised", direction="right")
    #     symbol_1.pack(side="left")
    #     create_menu(symbol_1, name)
    #
    #     symbol_2 = tkinter.Menubutton(te, image=symbol_images[Symbols.random_mark], text=Symbols.random_mark.value,
    #                                   relief="raised", direction="right")
    #     symbol_2.pack(side="right")
    #
    #     # 심볼을 변수로 관리
    #     random_unit_selected_symbols[name] = [symbol_1, symbol_2]
    #
    #     create_menu(symbol_2, name)
    #     te.pack(side="top", padx=10, pady=10)
    #
    # add_random_unit(random_unit_select_symbol, '궁정 화가 지르콘')
    # add_random_unit(random_unit_select_symbol, '점성술사 래브라')
    #
    # # 심볼 클릭 이벤트. 아래에 디스플레이 되는 목록을 변경한다.
    # # 버튼을 누르면 눌린 상태를 유지하고, 그 상태에서 다시 누르면 원상복구한다.
    # def symbol_click(selected_symbol):
    #     # print(selected_symbol)
    #     if symbol_buttons[selected_symbol]['state'] == ButtonState.unpressed:
    #         symbol_buttons[selected_symbol]['button']['background'] = 'gray'
    #         symbol_buttons[selected_symbol]['button'].config(relief=SUNKEN)  # 눌린 상태 유지
    #         symbol_buttons[selected_symbol]['state'] = ButtonState.pressed
    #     else:
    #         symbol_buttons[selected_symbol]['button'].config(relief=RAISED)  # 눌린 상태 해제
    #         symbol_buttons[selected_symbol]['state'] = ButtonState.unpressed
    #         symbol_buttons[selected_symbol]['button']['background'] = 'SystemButtonFace'
    #     # 현재 ui 갱신
    #     display_right_units()
    #
    # # 심볼과 해당 심볼 버튼 상태
    # symbol_buttons = {}
    #
    # # 심볼 목록 표시
    # def display_symbols():
    #     for s in Symbols:
    #         tag_new_btn = tkinter.Button(symbol_list_frame, overrelief="groove", image=symbol_images[s], text=s.value,
    #                                      command=partial(symbol_click, s))
    #
    #         Tooltip(tag_new_btn, text=s.value)
    #
    #         # 관리할 상태 변수
    #         symbol_buttons[s] = {'button': tag_new_btn, 'state': ButtonState.unpressed}
    #
    #         # text 위젯에 추가
    #         symbol_list_window.configure(state="normal")
    #         symbol_list_window.window_create("insert", window=tag_new_btn, padx=10, pady=10)
    #         symbol_list_window.configure(state="disabled")
    #
    # display_symbols()
    #
    # # 유닛 목록을 표시할 윈도우 생성
    # unit_list_frame = tkinter.LabelFrame(window, text="선택된 심볼의 유닛 목록")
    # unit_list_frame.pack(side='top', fill="both", padx=10, pady=10)
    #
    # unit_list_window = tk.Text(unit_list_frame, wrap="word", height='40',
    #                            bg='SystemButtonFace', yscrollcommand=lambda *args: unit_vsb.set(*args))
    # unit_vsb = tk.Scrollbar(unit_list_frame, command=unit_list_window.yview)
    # unit_vsb.pack(side="right", fill="y")
    # unit_list_window.pack(side="left", fill="both", expand=True)
    #
    # # 현재 선택 상태에 맞는 유닛 목록을 출력한다.
    # def display_right_units():
    #     unit_list = Units.get_unit_list()
    #
    #     unit_list_window.configure(state="normal")
    #     unit_list_window.delete("1.0", "end")
    #     unit_list_window.configure(state="disabled")
    #
    #     for unit in unit_list:
    #         # 첫번째 심볼, 혹은 두번째 심볼이 클릭된 상태
    #         if symbol_buttons[unit[2]]['state'] == ButtonState.pressed or symbol_buttons[unit[3]]['state'] == ButtonState.pressed:
    #
    #             # 등급에 따른 색상 테두리
    #             if unit[1] == Level.bronze:
    #                 color = '#CD7F32'
    #             elif unit[1] == Level.silver:
    #                 color = 'silver'
    #             elif unit[1] == Level.gold:
    #                 color = 'gold'
    #
    #             # 전체 프레임
    #             unit_frame = tkinter.Frame(unit_list_frame,  bg=color) #, command=partial(unit_click, s)
    #
    #
    #             # 패딩 크기, 사실상 테두리 크기
    #             pad_size = 4
    #
    #             unit_btn = tkinter.Label(unit_frame, image=unit_images[unit[0]], text=unit[0])
    #             unit_btn.pack(side='top', pady=(pad_size, 0), padx=pad_size)
    #             Tooltip(unit_btn, text=str(unit[0]))
    #
    #             # 유닛이 지닌 심볼 표시
    #             symbol_frame = tkinter.Frame(unit_frame)
    #
    #             symbol_first = tkinter.Label(symbol_frame, image=symbol_images[unit[2]])
    #             symbol_first.pack(side='left')
    #             Tooltip(symbol_first, text=str(unit[2].value))
    #
    #             symbol_second = tkinter.Label(symbol_frame, image=symbol_images[unit[3]])
    #             symbol_second.pack(side='right')
    #             Tooltip(symbol_second, text=str(unit[3].value))
    #
    #             symbol_frame.pack(side='top', pady=(0, pad_size), padx=pad_size, fill="both", expand=True)
    #
    #
    #             # 관리할 상태 변수
    #             # symbol_buttons[s] = {'button': tag_new_btn, 'state': ButtonState.unpressed}
    #
    #             # text 위젯에 추가
    #             unit_list_window.configure(state="normal")
    #             unit_list_window.window_create("insert", window=unit_frame, padx=10, pady=10)
    #             unit_list_window.configure(state="disabled")


    # 메인루프 시작
    window.mainloop()