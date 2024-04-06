# импортируем библиотеку tkinter всю сразу
from tkinter import *
from tkinter import messagebox
import hashlib
import connect_BD
import window_root
import socket
import time
from datetime import datetime


# ощистка пользовательских данных
def clear_data(data):
    data = data.replace(' ', '')
    data = data.strip()
    return data


def checked_user(window):
    '''
    #res = socket.gethostbyname(socket.gethostname())
    #res = f"{res}"
    #res = res[0:5]

    #dm = datetime.strptime('01-04-2200', '%d-%m-%Y')

    #if str(res[0:5]) != '10.30' or (time.time() > dm.timestamp()): #str(res[0:5]) != '10.30' or
        messagebox.showwarning('Предупреждение', 'Что-то пошло не так, обратитесь к администратору.')
        return
    '''
    # получаем имя пользователя и пароль
    #global username_entry, password_entry

    username = username_entry.get()
    password = password_entry.get()

    username_clear = clear_data(username)
    password_clear = clear_data(password)

    if username_clear == '' or password_clear == '':
        # если пусты поля ввода
        messagebox.showwarning('Вход в программу', 'Введите логин и пароль')

        # если пользователь что-то ввел, то проверяем
    else:
        # выборка всех пользователей для проверки
        res = connect_BD.sql_get_all_users()
        if res is not None:
            # cписок для создания словаря
            list_users = []
            for user in res:
                list_users.append((str(user[1]), user[2]))

            # cоздаем словарь с ключ-логин значение-пароль
            dict_users = dict(list_users)
            #print(dict_users)
            # проверяем на вхождение пользователя
            if username_clear in dict_users:

                password_hash_user = (hashlib.md5(password_clear.encode('utf-8')).hexdigest())
                password_db = dict_users.get(username_clear)

                # проверка паролей
                if password_db == password_hash_user:
                    #messagebox.showwarning('Вход в программу', f"Пользователь {username_clear}  найден")

                    #id_user, tab_num, pass, fio

                    current_user = []
                    for user in res:
                        if username_clear == str(user[1]):
                            current_user.append((user[0], str(user[1]), user[3], user[4]))


                    # !!!!---вызов главного окна
                    # sql = "SELECT user_id, tab_num, pass, fio, role FROM users WHERE status = 1;"
                    window_root.main_window(window, current_user)

                # если не верный пароль
                else:
                    messagebox.showwarning('Вход в программу', "Неверный пароль")

            else:
                messagebox.showwarning('Вход в программу', f"Пользователь {username} не найден\nили отключён!")

        # for test
        #print(dict_users)
        #pass
        #print(username)
        #print(password)


def form_avtoriz(window):
    global username_entry, password_entry
    # главное окно приложения
    #root = Tk()
    # заголовок окна
    window.title('Вход  -=ITPetrikov=-')
    # размерокна
    #window.geometry('330x180')
    # можно ли изменять размер окна - нет
    window.resizable(False, False)
    window.attributes("-toolwindow", True)
    window.eval('tk::PlaceWindow .')


    # кортежи и словари, содержащие настройки шрифтов и отступов
    font_header = ('Arial', 15, 'bold')
    font_entry = ('Arial', 12)
    label_font = ('Arial', 13)
    base_padding = {'padx': 10, 'pady': 8}
    header_padding = {'padx': 10, 'pady': 12}

    frame_input = Frame(window, highlightbackground="gray", highlightthickness=10)

    # заголовок формы: настроены шрифт (font), отцентрирован (justify), добавлены отступы для заголовка
    # для всех остальных виджетов настройки делаются также
    main_label = Label(frame_input, text='Учёт ИБП', font="Verdana, 17", justify=CENTER, border=1, borderwidth=2)
    # помещаем виджет в окно по принципу один виджет под другим
    main_label.grid(row=1, column=0, columnspan=2, ipadx=100, pady=[10, 0], sticky=W)

    # метка для поля ввода имени
    username_label = Label(frame_input, text='Логин:', font=label_font, **base_padding, fg='#2F4F4F')
    username_label.grid(row=2, column=0, padx=(30,0), sticky=W)

    # поле ввода имени
    username_entry = Entry(frame_input, width=17, bg='#fff', fg='#444', font=font_entry)
    username_entry.grid(row=2, column=1, sticky=W)

    # метка для поля ввода пароля
    password_label = Label(frame_input, text='Пароль:', font=label_font, **base_padding, fg='#2F4F4F')
    password_label.grid(row=3, column=0, padx=(30,0), sticky=W)

    # поле ввода пароля
    password_entry = Entry(frame_input, show="*", width=17, bg='#fff', fg='#444', font=("Arial", 12, 'bold')) #☻
    password_entry.grid(row=3, column=1, sticky=W)

    # кнопка отправки формы
    send_btn = Button(frame_input, text='   Войти   ', command=lambda: checked_user(window), font='Areal 10', fg='#2F4F4F')
    send_btn.grid(row=4, column=1,  padx=(0, 20), sticky=E)

    frame_input.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), ipady=3, ipadx=3)

    #root.mainloop()




