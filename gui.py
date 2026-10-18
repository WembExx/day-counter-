import customtkinter as ctk
from tkinter import messagebox
import day_counter
import threading
from functools import partial
import pystray
from PIL import Image

class App():
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry('500x300')
        self.root.resizable(width=False, height=False)
        self.root.title('Counter Days')
        self.root.iconbitmap('icon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        # ================== THREADS ================== #
        self.thread_tray = threading.Thread(target=self.start_tray)
        self.thread_tray.start()
        
        self.thread_display_time = threading.Thread(target=self.display_time, daemon=True)
        self.thread_display_time.start()

        # ============================================= #

        # ================== GUI ================== #

        self.title_frame = ctk.CTkFrame(master=self.root, width=400, height=50)
        self.title_frame.pack(pady=10)
        self.title_frame.pack_propagate(False)

        self.label_title = ctk.CTkLabel(master=self.title_frame, text='Counter Days', font=('Arial', 40, 'bold'))
        self.label_title.pack()

        self.frame = ctk.CTkFrame(master=self.root, width=400, height=55)
        self.frame.pack(pady=0)
        self.frame.pack_propagate(False)

        self.label_start_date = ctk.CTkLabel(master=self.frame, text=f'Дата запуска: {day_counter.start_date()}', font=('Arial', 15))
        self.label_start_date.pack()

        self.label_current_date = ctk.CTkLabel(master=self.frame, text=f'Текущая дата: {day_counter.current_date()}', font=('Arial', 15))
        self.label_current_date.pack()

        self.frame2 = ctk.CTkFrame(master=self.root, width=200, height=50)
        self.frame2.pack(pady=(20, 0))
        self.frame2.pack_propagate(False)

        self.label_elapsed_time = ctk.CTkLabel(master=self.frame2, text=day_counter.show(), font=('Arial', 20, 'bold'))
        self.label_elapsed_time.pack(pady=10)

        self.frame3 = ctk.CTkFrame(master=self.root)
        self.frame3.pack(pady=(10, 20))

        self.label_confirm_date = ctk.CTkLabel(master=self.frame3, text='Укажите дату: ', font=('Arial', 20, 'bold'))
        self.label_confirm_date.grid(column=0, row=0)

        self.entry_date = ctk.CTkEntry(master=self.frame3, width=80, placeholder_text='01.01.2001')
        self.entry_date.grid(column=1, row=0)

        self.entry_time = ctk.CTkEntry(master=self.frame3, width=50, placeholder_text='12:00')
        self.entry_time.grid(column=2, row=0, padx=10)

        self.btn_confirm_date = ctk.CTkButton(master=self.frame3, fg_color='#6A5ACD', text='Старт', font=('Arial', 15, 'bold'), width=100, command=self.reset_start_date)
        self.btn_confirm_date.grid(column=3, row=0, padx=10)

        self.btn_reset_date = ctk.CTkButton(master=self.root, fg_color='#6A5ACD', font=('Arial', 15, 'bold'), text='Сбросить счетчик', command=self.confirm_reset, height=40, width=100)
        self.btn_reset_date.pack()

        self.root.mainloop()

        # ====================================== #

    def confirm_reset(self):
        self.confirm_window = ctk.CTkToplevel()
        self.confirm_window.geometry('300x150')
        self.confirm_window.title('Подтвердите выбор')
        self.confirm_window.iconbitmap('icon.ico')
        self.confirm_window.resizable(width=False, height=False)
        self.confirm_window.after(200, self.bring_to_front)

        self.confirm_window.after(200, lambda: self.confirm_window.grab_set())

        self.frame_title = ctk.CTkFrame(master=self.confirm_window)
        self.frame_title.pack(pady=20)
        self.label = ctk.CTkLabel(master=self.frame_title, text='Сбросить счетчик?', font=('Arial', 20))
        self.label.pack()

        self.frame4 = ctk.CTkFrame(master=self.confirm_window)
        self.frame4.pack(pady=10)

        self.btn_confirm = ctk.CTkButton(master=self.frame4, text='Сброс', width=100, fg_color='#6A5ACD', command=partial(self.reset_date, True))
        self.btn_confirm.grid(column=1, row=0, padx=(10, 0))

        self.btn_refuce = ctk.CTkButton(master=self.frame4, text='Отмена', width=100, fg_color='#6A5ACD', command=partial(self.reset_date, False))
        self.btn_refuce.grid(column=0, row=0, padx=(0, 10))

    def bring_to_front(self):
        self.confirm_window.lift()
        self.confirm_window.focus_force()
        self.confirm_window.grab_set()

    def reset_start_date(self):
        date = str(self.entry_date.get())
        time = str(self.entry_time.get())
        answer = day_counter.string_to_date(date, time)
        if answer[0] == True:
            self.label_start_date.configure(text=f'Дата запуска: {day_counter.start_date()}')
        elif answer[0] == False:
            messagebox.showerror('Ошибка', answer[1])

    def display_time(self):
        while True:
            self.label_elapsed_time.configure(text=day_counter.show())
            self.label_current_date.configure(text=f'Текущая дата: {day_counter.current_date()}')

    def reset_date(self, action):
        if action == True:
            day_counter.reset_date()
            self.label_start_date.configure(text=f'Дата запуска: {day_counter.start_date()}')
            self.confirm_window.destroy()
        else: 
            self.confirm_window.destroy()

    # ================= TRAY ==================== #

    def create_image(self):
        self.image = Image.open('icon.ico')
        return self.image

    def on_quit(self, icon):
        icon.stop()
        self.root.after(0, self.root.destroy)

    def on_click(self):
        self.root.after(0, self.root.deiconify)

    def start_tray(self):
        self.menu = pystray.Menu(
        pystray.MenuItem('Показать', self.on_click, default=True),
        pystray.MenuItem('Выход', self.on_quit)
        )

        icon = pystray.Icon('test_icon', self.create_image(), 'Counter Days', self.menu)
        icon.run()

    # =========================================== #

def main():
    App()

if __name__ == '__main__':
    main()