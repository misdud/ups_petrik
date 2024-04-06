import hashlib
import template_raport as raport
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from tkcalendar import DateEntry

import connect_BD

# кортежи и словари, содержащие настройки шрифтов
font_header = ('Arial', 11)
font_entry = ('Arial', 11)
label_font = ('Arial', 11)

basic_style_lab_frame = {'background': '#ccc', 'foreground': 'dark slate gray', 'font': 'Helvetica 11'}
basic_style_entry_frame = {'font': 'Helvetica 11'}
basic_style_bottom = {'background': '#ccc', 'foreground': '#004D40', 'font': 'Helvetica 10'}

# установка текущего глобального юзера и фрейма
current_user = None
labelframe_treeview = ''

# --для передачи StringVar в свойства ибп
frame_values_ups_global = None
# --для передачи комментов
text_ups_comment = None

# -- для Переместить ups в другое отделение
tree_id_depart_select = None
# -- для изменения статуса  ups при сверке с тем что есть
status_ups = ()

# -- для изменений в таблице
tree_global = None
item_select_global = None
tree = None

select_depart_global = None

# -- для изменений в сведений
labelframe_top_left_global = None


# блокировка главного окна
def dismiss(window):
    window.grab_release()
    window.destroy()


def clear_text_strip(data):
    if data:
        return data.strip()
    else:
        return False


def ups_count_status():
    res = connect_BD.sql_ups_count()
    return res


def clear_value_ups():
    global frame_values_ups_global, text_ups_comment

    frame_values_ups_global.select_depart_val.set('')
    frame_values_ups_global.room_val.set('')
    frame_values_ups_global.item_number_val.set('')
    frame_values_ups_global.model_val.set('')

    frame_values_ups_global.type_battery_val.set('')
    frame_values_ups_global.model_intrface_val.set('')
    frame_values_ups_global.is_modul_val.set('')
    frame_values_ups_global.akb_count_val.set('')

    frame_values_ups_global.capacity_val.set('')
    frame_values_ups_global.volt_val.set('')
    frame_values_ups_global.type_terminal_val.set('')
    frame_values_ups_global.type_size_val.set('')

    frame_values_ups_global.status_work.set('')
    frame_values_ups_global.status_replace.set('')
    frame_values_ups_global.status_repair.set('')

    frame_values_ups_global.entry_fio_val.set('')
    text_ups_comment.delete(0.0, END)

    # - для управления кнопками и др свойствами для Свойства ИБП
    frame_values_ups_global.id_ups.set(0)


def create_raport(result_sql):
    # - если ничего не найдено
    if len(result_sql) < 1:
        messagebox.showinfo('Поиск', 'Ничего не найдено, попробуйте выбрать другой вариант.')
        return

    import template_raport as raport
    now_date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name_file = 'Raport_Ups_'
    name_file += now_date
    template = '<tr>' \
               '  <td>{0}</td>  <td align="right">{1}</td>  <td align="right">{2}</td>  <td align="right">{3}</td>  <td align="right">{4}</td>' \
               '  <td align="right">{5}</td>  <td align="right">{6}</td>  <td align="right">{7}</td>  <td align="right">{8}</td>' \
               '  <td align="right">{9}</td>  <td align="right">{10}</td>  <td align="right">{11}</td>  <td align="right">{12}</td> ' \
               '  <td>{13}</td>  <td>{14}</td> <td>{15}</td>' \
               ' </tr>'
    try:
        with open(f"{name_file}.html", 'w', encoding="utf-8") as html:
            html.write(raport.template_heder)
            num = 1
            for x in result_sql:
                html.write(template.format(num, x[0], x[1], x[2], x[3], x[4],
                                           x[5], x[6], f"{x[7]}\\{x[8]}A/h\\{x[9]}V",
                                           f"{x[10]}\\{x[11]} ({x[10] + x[11]})", x[12], x[13], x[14], x[15], x[16],
                                           x[17]))
                num += 1
            html.write(raport.template_bottom.format(len(result_sql), date))
    except BaseException as e:
        messagebox.showwarning('Error', f"Что-то пошло не так. \n{e} \nПопробуйте ещё раз.")
    else:
        messagebox.showinfo('Информация', f"В текущей папке создан файл: {name_file}.html.")


def create_raport_on_select():
    wind_raport = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
    wind_raport.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_raport))  # перехватываем нажатие на крестик
    wind_raport.attributes("-toolwindow", False)
    # wind_add_user.geometry('362x250')
    x = (wind_raport.winfo_screenwidth() - wind_raport.winfo_reqwidth()) / 2
    y = (wind_raport.winfo_screenheight() - wind_raport.winfo_reqheight()) / 2
    wind_raport.geometry("+%d+%d" % (x - 100, y - 210))
    wind_raport.title("Отчеты по  ИБП")
    wind_raport.resizable(False, False)

    frame_raport = LabelFrame(wind_raport, padx=10, pady=10, text="Выбор по критериям", font=('Arial', 11),
                              highlightbackground="#ccc", highlightthickness=0)

    # -------------------SELECT----DEPART---------------
    depart_select_id = 0

    def select_depart_id(event):
        nonlocal depart_select_id
        selection = combobox_depart.get()
        if result_sql_departs:
            for val in result_sql_departs:
                if str(selection) == str(val[1]):
                    depart_select_id = val[0]
                    break

        # print(id_depart_select, 'id_depart_select')

    sql = "SELECT depart_id, short_name  FROM departments   ORDER BY  short_name;"
    result_sql_departs = connect_BD.sql_get_data(sql)

    only_departs_list = []
    if result_sql_departs:
        only_departs_list.extend(x[1] for x in result_sql_departs)

    # изначально с в списке пустое значение,
    # по умолчанию будет выбран  пустой элемент
    frame_raport.select_depart = StringVar(frame_raport, value='')

    # для установки отделения в поиск после добавления
    global select_depart_global
    select_depart_global = frame_raport.select_depart

    lbl_depart = Label(frame_raport, basic_style_lab_frame, text="Отделение:", background='#F0F0F0')
    lbl_depart.grid(row=0, column=0, padx=(30, 0), pady=(20, 5), sticky=E)

    combobox_depart = ttk.Combobox(frame_raport, width=23, textvariable=frame_raport.select_depart,
                                   values=only_departs_list, background='#FDFBE1', state="readonly")
    combobox_depart.grid(row=0, column=1, pady=(20, 5), sticky=W)
    combobox_depart.bind("<<ComboboxSelected>>", select_depart_id)

    # +-------------------------------------------------------------------------------------------------
    check_style2 = ttk.Style()
    check_style2.configure("My_check2.TCheckbutton",  # имя стиля
                           font="helvetica 10",  # шрифт
                           foreground="#004D40",  # цвет текста
                           padding=(1, 1, 1, 1),  # отступы
                           background="#f0f0f0")  # фоновый цвет
    check_style2.map("My_check2.TCheckbutton", background=[("active", "darkgrey")])

    enabled_is_work1 = IntVar(value=0)

    checkbutton_is_work = ttk.Checkbutton(frame_raport, text="Не в работе", variable=enabled_is_work1,
                                          style="My_check2.TCheckbutton")
    checkbutton_is_work.grid(row=1, column=1, padx=(0, 0), pady=(10, 0), sticky=W)
    # *-------------------------------------------------------------------------------------------------

    enabled_is_replace1 = IntVar(value=0)

    checkbutton_is_replace = ttk.Checkbutton(frame_raport, text="Требуется замена АКБ",
                                             variable=enabled_is_replace1, style="My_check2.TCheckbutton")
    checkbutton_is_replace.grid(row=2, column=1, padx=(0, 0), pady=(10, 10), sticky=W)
    # --------------------------------------------------------------------------------------------------

    enabled_is_repair1 = IntVar(value=0)

    checkbutton_is_repair = ttk.Checkbutton(frame_raport, text="В ремонте", variable=enabled_is_repair1,
                                            style="My_check2.TCheckbutton")
    # checkbutton_is_repair.state(["selected"])
    checkbutton_is_repair.grid(row=3, column=1, padx=(0, 0), sticky=W)

    # --------------------------------------------------------------------------------------------------

    def get_sql_for_raport(depart_select_id, enabled_is_work, enabled_is_replace, enabled_is_repair):

        if not bool(depart_select_id) and not bool(enabled_is_work) and not bool(enabled_is_replace) and not bool(
                enabled_is_repair):
            return
        else:
            if depart_select_id != 0 and enabled_is_work and enabled_is_replace and enabled_is_repair:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_all(param)
            elif depart_select_id != 0 and enabled_is_work and enabled_is_replace:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_work_replace(param)
            elif depart_select_id != 0 and enabled_is_replace and enabled_is_repair:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_replace_repair(param)
            elif depart_select_id != 0 and enabled_is_work:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_work(param)
            elif depart_select_id != 0 and enabled_is_replace:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_replace(param)
            elif depart_select_id != 0 and enabled_is_repair:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_depart_repair(param)
            elif enabled_is_work and enabled_is_replace and enabled_is_repair:
                result_sql = connect_BD.sql_get_ups_raport_work_repair_replace()
            elif enabled_is_work and enabled_is_replace:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_work_replace_only()
            elif enabled_is_work and enabled_is_repair:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_work_repair()
            elif enabled_is_replace and enabled_is_repair:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_work_replace_repair()
            elif depart_select_id != 0:
                param = (depart_select_id,)
                result_sql = connect_BD.sql_get_ups_raport_only_depart(param)
            elif enabled_is_work:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_only_work()
            elif enabled_is_repair:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_only_repair()
            elif enabled_is_replace:  # --------------------------
                result_sql = connect_BD.sql_get_ups_raport_only_replace()
            else:
                result_sql = []

        create_raport(result_sql)

    btn_raport = ttk.Button(frame_raport, text='  Сформировать  ',
                            command=lambda: get_sql_for_raport(depart_select_id, enabled_is_work1.get(),
                                                               enabled_is_replace1.get(), enabled_is_repair1.get()))
    btn_raport.grid(row=4, column=1, pady=(20, 0), sticky=W)

    frame_raport.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))
    wind_raport.grab_set()  # захватываем польз-льский ввод


def search_ups(id_depart_select=False, id_model_select=False, item_number='', select_count_main_element=100,
               enabled_is_replace=False, enabled_is_repair=False):
    # -- если пустые значения для поиска то выходим

    # print(111, id_depart_select, id_model_select, item_number, select_count_main_element, enabled_is_replace, enabled_is_repair)
    if not id_depart_select and (not id_model_select) and (item_number == '') and (not enabled_is_replace) and (
            not enabled_is_repair):
        return

    # ---очищаем поля Свойства ИБП
    clear_value_ups()
    # ------------End---------------
    if item_number != '' and item_number.isdigit() and len(item_number) > 0:
        param = (item_number, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_table_param_like(param)
    elif id_depart_select and id_model_select and enabled_is_replace and enabled_is_repair:
        param = (id_depart_select, id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_model_replace_repair(param)
    elif id_depart_select and id_model_select and enabled_is_replace:
        param = (id_depart_select, id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_model_replace(param)
    elif id_depart_select and id_model_select and enabled_is_repair:
        param = (id_depart_select, id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_model_repair(param)
    elif id_depart_select and enabled_is_repair and enabled_is_replace:
        param = (id_depart_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_replace_and_repair(param)
    elif id_model_select and enabled_is_repair and enabled_is_replace:
        param = (id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_model_and_repair_replace(param)
    elif enabled_is_repair and enabled_is_replace:
        param = (select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_replace_and_repair(param)
    elif id_depart_select and enabled_is_replace:
        param = (id_depart_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_and_replace(param)
    elif id_depart_select and enabled_is_repair:
        param = (id_depart_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_depart_and_repair(param)
    elif id_model_select and enabled_is_repair:
        param = (id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_model_and_repair(param)
    elif id_model_select and enabled_is_replace:
        param = (id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_model_and_replace(param)
    elif enabled_is_replace:
        param = (select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_replace_elements(param)
    elif enabled_is_repair:
        param = (select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_repair(param)
    elif id_depart_select and id_model_select:
        param = (id_depart_select, id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_table_param_id_depart_id_model(param)
    elif id_depart_select and not id_model_select:
        param = (id_depart_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_table_param_id_depart(param)  # рабочий
    elif id_model_select and not id_depart_select:
        param = (id_model_select, select_count_main_element)
        ups_searh = connect_BD.sql_get_ups_main_table_param_id_model(param)
    else:
        ups_searh = connect_BD.sql_get_ups_main_table()

    show_main_treeview(ups_searh)


def show_value_treeview_ups(select_ups=None):
    global frame_values_ups_global, text_ups_comment, tree_id_depart_select, status_ups
    # - при обновлении когда выбран елемент
    if select_ups == '': return

    if select_ups is not None:
        # берем из строки цифры кол всего акб т.е. то что в скобках
        cnt = select_ups[9].replace(')', '')
        cnt = cnt.split('(')
        capcity = select_ups[8].split('\\')

        # -- Для работы с конкретным ИБП в Cвойствах ИБП
        frame_values_ups_global.id_ups.set(select_ups[23])

        # --Для смены отделения (сверка с тем что выбрано в таблице с тем что указал пользователь)
        tree_id_depart_select = select_ups[1]

        status_ups = (select_ups[10], select_ups[11], select_ups[13])

        frame_values_ups_global.select_depart_val.set(select_ups[1])
        frame_values_ups_global.room_val.set(select_ups[2])
        frame_values_ups_global.item_number_val.set(select_ups[4])
        frame_values_ups_global.model_val.set(select_ups[5])

        frame_values_ups_global.type_battery_val.set(select_ups[19])
        frame_values_ups_global.model_intrface_val.set(select_ups[18])
        frame_values_ups_global.is_modul_val.set(select_ups[20])
        frame_values_ups_global.akb_count_val.set(cnt[1])

        frame_values_ups_global.capacity_val.set(capcity[1])
        frame_values_ups_global.volt_val.set(capcity[2])
        frame_values_ups_global.type_terminal_val.set(select_ups[16])
        frame_values_ups_global.type_size_val.set(select_ups[17])

        frame_values_ups_global.status_work.set(select_ups[10])
        frame_values_ups_global.status_replace.set(select_ups[11])
        frame_values_ups_global.status_repair.set(select_ups[13])

        frame_values_ups_global.entry_fio_val.set(select_ups[22])

        text_ups_comment.delete(0.0, END)
        text_ups_comment.insert(0.0, select_ups[21])

    del select_ups


def show_main_treeview(ups=None, flag_clear_values_ups=False, id_depart_select=False):
    global tree_global, labelframe_treeview, item_select_global

    # для стилей при подсветке если обновление идет
    item_select_global = None

    # - если пришел c поиска
    if id_depart_select:
        ups = connect_BD.sql_get_ups_depart_main_table(id_depart_select)

    if ups is None:
        ups = connect_BD.sql_get_ups_main_table()

    ups_edit = []
    num = 1
    for val in ups:
        ups_edit.append(tuple([num, val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                               f"{val[7]}\\{val[8]}Ah\\{val[9]}V", f"{val[10]}\\{val[11]} ({val[10] + val[11]})",
                               val[12], val[13], val[14], val[15], val[16],
                               val[17], val[18], val[19], val[20], val[21], val[22], val[23], val[24], val[25]]))
        num += 1

    # -очищаем перед вставкой
    tree_global.delete(*tree_global.get_children())
    # добавляем данные
    for ups_one in ups_edit:
        tree_global.insert("", END, values=ups_one)

    # - - очищаем значения полей Свойств UPS при обновлении
    if flag_clear_values_ups:
        clear_value_ups()

    # -- для изменений в таблице
    # tree_global = tree_global

    del ups
    del ups_edit


def is_data_text_fio(data):
    if data is False: return False
    if data.strip():
        for let in data:
            if let in [':', ';', ',', '/', '[', ']', '*', '+', '@', '!', '#', '№', '$', '&', '(', ')', '^', '=']:
                return False
        return True
    else:
        return False


def add_ups(wind_add_ups, id_depart_select, id_model_select, entry_room, entry_serial_number,
            entry_item_number, now_date, text_ups_comment, frame_add_ups_status_is_work):
    global select_depart_global, labelframe_top_left_global
    entry_room = entry_room.strip()
    entry_serial_number = entry_serial_number.strip()
    entry_item_number = entry_item_number.strip()

    if not all([id_depart_select, id_model_select, entry_room, entry_item_number]):
        messagebox.showinfo('Информация', "Заполните все обязательные поля.")
        return

    try:
        entry_item_number = int(entry_item_number)
    except Exception:
        messagebox.showwarning('Передупреждение', "Инв.\\номенкл. № должен содержать только цифры.")
        return
    text_ups_comment = text_ups_comment.strip()

    entry_time = str(now_date)
    if '.' in entry_time:
        entry_time = now_date.replace('.', '-')
        entry_time = entry_time.split('-')
        entry_time = f"{entry_time[2]}-{entry_time[1]}-{entry_time[0]}"

    if not entry_serial_number:
        entry_serial_number = 'н/д'
    if not text_ups_comment:
        text_ups_comment = 'н/д'

    params = (
        id_depart_select, id_model_select, current_user[0][0], entry_serial_number, entry_room, entry_item_number,
        'н/д',
        'н/д',
        entry_time, text_ups_comment, frame_add_ups_status_is_work)

    # -----проверка на дубликат записи по Инв.\номенкл. №
    res_duble = connect_BD.sql_get_duble_ups(entry_item_number)
    if res_duble:
        wind_add_ups.withdraw()
        result = messagebox.askyesno('Внимание',
                                     f"Вы пытаетесь добавтить Инв.\\номенкл. №: '{entry_item_number}'\nкоторый уже есть в таблице. Продолжить?")
        if result:
            res = connect_BD.sql_insert_ups(params)
            if res:
                # - закрываем окно
                wind_add_ups.destroy()
                messagebox.showinfo('Информация', f"Источник беcперебойного питания № '{entry_item_number}' добавлен.")

                # - для изменений в сведениях
                labelframe_top_left_global.all_ups_count.set(int(labelframe_top_left_global.all_ups_count.get()) + 1)
                return
        else:
            wind_add_ups.deiconify()
            return

    res = connect_BD.sql_insert_ups(params)

    if res:
        # - закрываем окно
        wind_add_ups.destroy()
        messagebox.showinfo('Информация', f"Источник беcперебойного питания № '{entry_item_number}' добавлен.")

        # - обновляем содержимое окна после добавления и показываем в отделе где выбран поиск если он в поиске
        search_ups(id_depart_select, id_model_select=None)

        # - сбрасываем поиск отдела
        select_depart_global.set('')
        # show_main_treeview(ups=None, flag_clear_values_ups=True, id_depart_select=id_depart_select)

        # - очищаем поля свойств ups
        clear_value_ups()
        # - для изменений в сведениях
        labelframe_top_left_global.all_ups_count.set(int(labelframe_top_left_global.all_ups_count.get()) + 1)


def add_ups_form():
    if current_user[0][3] not in ['Meнеджер', 'Админ']:  # "Supper_Admin_UPS",
        messagebox.showinfo('Информация', f"Пользователь с ролью '{current_user[0][3]}' не может добавить ИБП")
    else:
        wind_add_ups = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
        wind_add_ups.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_add_ups))  # перехватываем нажатие на крестик
        wind_add_ups.attributes("-toolwindow", False)
        x = (wind_add_ups.winfo_screenwidth() - wind_add_ups.winfo_reqwidth()) / 2
        y = (wind_add_ups.winfo_screenheight() - wind_add_ups.winfo_reqheight()) / 2
        wind_add_ups.geometry("+%d+%d" % (x - 100, y - 230))
        wind_add_ups.title("Добавление ИБП")
        wind_add_ups.resizable(False, False)

        frame_add_ups = LabelFrame(wind_add_ups, padx=10, pady=10, text="Информация о ИБП", font=('Arial', 11),
                                   highlightbackground="#ccc", highlightthickness=0)

        # -------------------SELECT----DEPART---------------
        id_depart_select = 0

        def select_depart(event):
            nonlocal id_depart_select
            selection = combobox_depart.get()
            if res_sql_departs:
                for val in res_sql_departs:
                    if str(selection) == str(val[1]):
                        id_depart_select = val[0]
                        break

        res_sql_departs = connect_BD.sql_get_on_status_depart()

        only_departs_list = []
        if res_sql_departs:
            only_departs_list.extend(x[1] for x in res_sql_departs)

        # изначально с в списке пустое значение,
        # по умолчанию будет выбран  пустой элемент
        frame_add_ups.select_depart = StringVar(frame_add_ups, value='')

        lbl_model_type_akb = Label(frame_add_ups, text="Отделение:", font=label_font)
        lbl_model_type_akb.grid(row=0, column=0, pady=(15, 5), sticky=E)

        combobox_depart = ttk.Combobox(frame_add_ups, width=23, textvariable=frame_add_ups.select_depart,
                                       values=only_departs_list, background='#FDFBE1', state="readonly")
        combobox_depart.grid(row=0, column=1, pady=(15, 5), sticky=W)
        combobox_depart.bind("<<ComboboxSelected>>", select_depart)

        # -------------------------------------------------------
        lbl_room = Label(frame_add_ups, text="Помещение:", font=label_font)
        lbl_room.grid(row=1, column=0, sticky=E)
        entry_room = Entry(frame_add_ups, font=font_entry, background='#FDFBE1')
        entry_room.grid(row=1, column=1, pady=(5, 5), ipady=3, sticky=W)

        # -------------------SELECT----MODEL-----UPS------------
        id_model_select = 0

        def select_model(event):
            nonlocal id_model_select
            selection_model = combobox_model.get()
            if res_sql_models:
                for val in res_sql_models:
                    if str(selection_model) == str(val[1]):
                        id_model_select = val[0]
                        break

            # print(id_model_select, 'id_model_select')

        res_sql_models = connect_BD.sql_get_on_status_model()

        only_models_list = []
        if res_sql_models:
            only_models_list.extend(x[1] for x in res_sql_models)

        # изначально в списке пустое значение
        # по умолчанию будет выбран  пустой элемент
        frame_add_ups.select_model = StringVar(frame_add_ups, value='')

        lbl_model = Label(frame_add_ups, text="Модель:", font=label_font)
        lbl_model.grid(row=2, column=0, pady=(5, 5), sticky=E)

        combobox_model = ttk.Combobox(frame_add_ups, width=23, textvariable=frame_add_ups.select_model,
                                      values=only_models_list, background='#FDFBE1', state="readonly")
        combobox_model.grid(row=2, column=1, pady=(5, 5), sticky=W)
        combobox_model.bind("<<ComboboxSelected>>", select_model)

        # -------------------Item--Number------------
        lbl_serial_number = Label(frame_add_ups, text="Серийный №:", font=label_font)
        lbl_serial_number.grid(row=3, column=0, sticky=E)
        entry_serial_number = Entry(frame_add_ups, font=font_entry)
        entry_serial_number.grid(row=3, column=1, pady=(5, 5), ipady=3, sticky=W)

        lbl_item_number = Label(frame_add_ups, text="Инв.\номенкл. №:", font=label_font)
        lbl_item_number.grid(row=4, column=0, sticky=E)
        entry_item_number = Entry(frame_add_ups, font=font_entry, background='#FDFBE1')
        entry_item_number.grid(row=4, column=1, pady=(5, 5), ipady=3, sticky=W)

        # - Дата ввода
        insert_date = ["Нет", "Да"]
        # по умолчанию будет выбран последний элемент
        frame_add_ups.select_is_input_date = StringVar(frame_add_ups, value=insert_date[0])

        lbl_date = Label(frame_add_ups, text="Внести дату ввода:", font=label_font)
        lbl_date.grid(row=5, column=0, pady=(5, 5), sticky=E)

        spinbox_date = Spinbox(frame_add_ups, width=5, textvariable=frame_add_ups.select_is_input_date,
                               values=insert_date, wrap=True, state="readonly")
        spinbox_date.grid(row=5, column=1, ipady=1, pady=(5, 5), sticky=W)

        now_date = datetime.now().strftime('%d.%m.%Y')

        lbl_time = Label(frame_add_ups, text="Дата ввода:", font=label_font)
        lbl_time.grid(row=6, column=0, pady=(5, 5), sticky=E)

        labl_time2 = Entry(frame_add_ups, width=12)
        labl_time2.delete(0, END)
        labl_time2.insert(0, now_date)
        labl_time2.configure(state='disabled')
        labl_time2.grid(row=6, column=1, pady=(5, 5), sticky=W)

        # -for check
        status = False
        entry_time1 = ''

        def check(*args):
            nonlocal now_date, labl_time2, entry_time1, status
            if frame_add_ups.select_is_input_date.get() == "Да":
                labl_time2.destroy()
                entry_time1 = DateEntry(frame_add_ups)
                entry_time1.grid(row=6, column=1, pady=(5, 5), sticky=W)
                now_date1 = entry_time1.get_date()
                now_date = str(now_date1)
                now_date = now_date.replace('-', '.')
                now_date = now_date.split('.')
                now_date = f"{now_date[2]}.{now_date[1]}.{now_date[0]}"
                status = True

            else:
                if status:
                    entry_time1.destroy()
                    status = False
                labl_time2 = Entry(frame_add_ups, width=12)
                labl_time2.delete(0, END)
                labl_time2.insert(0, now_date)
                labl_time2.configure(state='disabled')
                labl_time2.grid(row=6, column=1, pady=(5, 5), sticky=W)

        frame_add_ups.select_is_input_date.trace_add("read", check)
        frame_add_ups.select_is_input_date.set("Нет")  # для установки по молчанию, чтоб поле не было выбрано

        # ------------------------------------------------------------------------------
        lbl_is_work = Label(frame_add_ups, text="В работе:", font=label_font)
        lbl_is_work.grid(row=8, column=0, pady=(7, 7), sticky=E)

        status_on = "Да"
        status_of = "Нет"

        frame_add_ups.status = StringVar(frame_add_ups,
                                         value=status_on)  # по умолчанию будет выбран элемент с value=status_on

        status_on_btn = ttk.Radiobutton(frame_add_ups, text=status_on, variable=frame_add_ups.status, value=status_on)
        status_on_btn.grid(rowspan=1, row=8, column=1, pady=(7, 7), sticky='nw')

        status_of_btn = ttk.Radiobutton(frame_add_ups, text=status_of, variable=frame_add_ups.status, value=status_of)
        status_of_btn.grid(rowspan=1, row=8, column=1, pady=(7, 7), padx=(42, 0), sticky='nw')

        lbl_ups_comment = Label(frame_add_ups, text="Комментарии:", font=label_font)
        lbl_ups_comment.grid(row=9, column=0, pady=(15, 0), sticky=NE)
        text_ups_comment = ScrolledText(frame_add_ups, width=20, height=5, font=font_entry, wrap="word")
        text_ups_comment.grid(row=9, column=1, pady=(15, 30), sticky=NW)

        # -----------------------------------------------------------

        frame_add_ups.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))

        btn_add_model = ttk.Button(wind_add_ups, text='Создать',
                                   command=lambda: add_ups(wind_add_ups, id_depart_select, id_model_select,
                                                           entry_room.get()[0:25], entry_serial_number.get()[0:25],
                                                           entry_item_number.get()[0:15],
                                                           now_date if not status else entry_time1.get_date(),
                                                           text_ups_comment.get("1.0", END)[0:200],
                                                           frame_add_ups.status.get()))

        btn_add_model.grid(row=1, columnspan=2, column=0, padx=(0, 130), pady=(15, 10), sticky='e')

        btn_add_model_cancel = ttk.Button(wind_add_ups, text='Отмена', command=lambda: dismiss(wind_add_ups))
        btn_add_model_cancel.grid(row=1, columnspan=2, column=0, padx=(0, 10), pady=(15, 10), sticky='e')

        wind_add_ups.grab_set()  # захватываем польз-льский ввод


def list_model_form():
    wind_list_model_ipb = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
    wind_list_model_ipb.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(wind_list_model_ipb))  # перехватываем нажатие на крестик
    wind_list_model_ipb.attributes("-toolwindow", False)
    # wind_list_user.geometry('790x460')
    x = (wind_list_model_ipb.winfo_screenwidth() - wind_list_model_ipb.winfo_reqwidth()) / 2
    y = (wind_list_model_ipb.winfo_screenheight() - wind_list_model_ipb.winfo_reqheight()) / 2
    wind_list_model_ipb.geometry("+%d+%d" % (x - 560, y - 230))
    wind_list_model_ipb.title("Список моделей ИБП")
    wind_list_model_ipb.resizable(False, False)
    # wind_list_depart['bg'] = '#ccc'

    wind_list_model_ipb.rowconfigure(0, weight=6)
    wind_list_model_ipb.rowconfigure(1, weight=2)

    frame_list_modul_ipb = LabelFrame(wind_list_model_ipb, text="Модели ИБП", font=('Arial', 11),
                                      highlightbackground="#ccc", highlightthickness=1)

    # определяем данные для отображения ---------------------------------------------------------------------
    models = connect_BD.sql_get_status_on_models()

    # проверка ну дубль при изменении
    short_name_list = []

    models_ipb_edit = []
    num = 1
    for model in models:
        models_ipb_edit.append(
            tuple([num, model[5], model[6], model[7], model[8], model[18], model[10], model[11],
                   f"{model[2]}\{model[3]}Ah\{model[4]}V",
                   f"{model[12]}\\{model[16]} ({model[12] + model[16]})", model[13], model[1], model[19], model[9],
                   model[17], model[14], model[15], model[16], model[0]]))
        num += 1

        short_name_list.append(model[6])

    # определяем столбцы
    columns = (
        "number", "name", "short_name", "power", "interface", "status", "type_battery", "type_box", "type_akb",
        "count_element", "is_modul", "user", "data_create",
        "info", "comment", "name_modul", "type_battery_modul", "count_element_modul", "model_id")

    tree = ttk.Treeview(frame_list_modul_ipb, columns=columns, show="headings", height=15)
    tree.grid(row=0, column=0)

    def sort(col, reverse):
        nonlocal tree
        # получаем все значения столбцов в виде отдельного списка
        lst = [(tree.set(k, col), k) for k in tree.get_children("")]
        # сортируем список
        lst.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(lst):
            tree.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        tree.heading(col, command=lambda: sort(col, not reverse))

    # определяем заголовки с выпавниваем по левому краю
    tree.heading("number", text="#", anchor=E)
    tree.heading("name", text="Наименование", anchor='center', command=lambda: sort(1, False))
    tree.heading("short_name", text="Корот. наимен.", anchor=E, command=lambda: sort(2, False))  # anchor='center'
    tree.heading("power", text="Мощность(W)", anchor=E, command=lambda: sort(3, False))  # anchor='center'
    tree.heading("interface", text="Интерфейсы", anchor=E, command=lambda: sort(4, False))
    tree.heading("status", text="Вкл.\Выкл.", anchor=E, command=lambda: sort(5, False))
    tree.heading("type_battery", text="Тип ИБП", anchor=E, command=lambda: sort(6, False))  # anchor='center'
    tree.heading("type_box", text="Тип корпуса", anchor=E, command=lambda: sort(7, False))  # anchor='center'
    tree.heading("type_akb", text="Тип\Ah\V", anchor=E, command=lambda: sort(8, False))  # anchor='center'
    tree.heading("count_element", text="Кол. осн.\доп.\Σ", anchor=E, command=lambda: sort(9, False))  # anchor='center'
    tree.heading("is_modul", text="Модульный", anchor=E, command=lambda: sort(10, False))  # anchor='center'
    tree.heading("user", text="Создал\Изменил", anchor=E, command=lambda: sort(11, False))
    tree.heading("data_create", text="Дата создания\изм.", anchor=E, command=lambda: sort(12, False))

    # --скрытые в таблице
    tree.heading("info", text="info", anchor=E)
    tree.heading("comment", text="comment", anchor=E)
    tree.heading("name_modul", text="name_modul", anchor=E)
    tree.heading("type_battery_modul", text="type_battery_modul", anchor=E)
    tree.heading("count_element_modul", text="count_element_modul", anchor=E)
    tree.heading("model_id", text="id", anchor=E)

    # показаны в таблице + настройки
    tree.column("#1", stretch=NO, anchor=E, width=30)  # number
    tree.column("#2", stretch=YES, anchor=E, width=120)  # name
    tree.column("#3", stretch=NO, anchor=E, width=110)  # short_name capacity anchor='center'
    tree.column("#4", stretch=NO, anchor=E, width=100)  # power
    tree.column("#5", stretch=NO, anchor=E, width=100)  # interface
    tree.column("#6", stretch=NO, anchor=E, width=80)  # status
    tree.column("#7", stretch=NO, anchor=E, width=80)  # type_battery
    tree.column("#8", stretch=NO, anchor=E, width=100)  # type_box
    tree.column("#9", stretch=NO, anchor=E, width=170)  # type_akb
    tree.column("#10", stretch=NO, anchor=E, width=100)  # count_element
    tree.column("#11", stretch=NO, anchor=E, width=90)  # is_modul
    tree.column("#12", stretch=NO, anchor=E, width=120)  # user
    tree.column("#13", stretch=NO, anchor=E, width=150)  # data_create

    # --скрытые в таблице
    tree.column("#14", stretch=NO, anchor=E, width=0)  # hidden
    tree.column("#15", stretch=NO, anchor=E, width=0)  # hidden
    tree.column("#16", stretch=NO, anchor=E, width=0)  # hidden
    tree.column("#17", stretch=NO, anchor=E, width=0)  # hidden
    tree.column("#18", stretch=NO, anchor=E, width=0)  # hidden
    tree.column("#19", stretch=NO, anchor=E, width=0)  # hidden

    # - отображаем указанные колонки
    # tree['displaycolumns'] = ("number", "...")

    # добавляем данные
    for one_model in models_ipb_edit:
        tree.insert("", END, text=one_model[2], values=one_model)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(frame_list_modul_ipb, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_values_modul = LabelFrame(wind_list_model_ipb, text="Свойства", font=('Arial', 11),
                                    highlightbackground="#ccc", highlightthickness=1)

    # -------------START---COLUMN 0-1-------------------------------------------------
    lbl_name = Label(frame_values_modul, text="Наименование:", font=label_font)
    lbl_name.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky=E)
    entry_name = Entry(frame_values_modul, basic_style_entry_frame)
    entry_name.insert(0, '')
    entry_name.configure(state='disabled')
    entry_name.grid(row=0, column=1, pady=(0, 0), sticky=W)

    lbl_name_short = Label(frame_values_modul, text="Короткое наим.:", font=label_font)
    lbl_name_short.grid(row=1, column=0, padx=(10, 0), pady=(5, 5), sticky=E)
    entry_name_short = Entry(frame_values_modul, basic_style_entry_frame, background='#FDFBE1')
    entry_name_short.insert(0, '')
    # entry_name_short.configure(state='disabled')
    entry_name_short.grid(row=1, column=1, pady=(5, 5), sticky=W)

    lbl_power = Label(frame_values_modul, text="Мощность(W):", font=label_font)
    lbl_power.grid(row=2, column=0, padx=(10, 0), pady=(0, 5), sticky=E)
    entry_power = Entry(frame_values_modul, basic_style_entry_frame, background='#FDFBE1')
    entry_power.insert(0, '')
    # entry_power.configure(state='disabled')
    entry_power.grid(row=2, column=1, pady=(0, 5), sticky=W)

    # --- radiobutton status on\off
    status_on = "Вкл."
    status_off = "Выкл."

    frame_values_modul.status = StringVar(frame_values_modul, value=status_off)  # по умолчанию будет выбран элемент

    status_on_btn = ttk.Radiobutton(frame_values_modul, text=status_on, variable=frame_values_modul.status,
                                    value=status_on)
    status_on_btn.grid(row=3, column=1, pady=(3, 5), sticky=NW)

    status_off_btn = ttk.Radiobutton(frame_values_modul, text=status_off, variable=frame_values_modul.status,
                                     value=status_off)
    status_off_btn.grid(row=3, column=1, pady=(3, 5), padx=(50, 0), sticky=NW)
    # -----------END COLOMN 0-1------------------------------------------------------------------

    # -----------START---COLUMN 2-3------------------------------------------------------------------
    # - список видов
    types = ["Off-line", "Interactive", "On-line"]
    # по умолчанию будет выбран последний элемент
    frame_values_modul.select_type = StringVar(frame_values_modul, value=types[0])

    lbl_model_type = Label(frame_values_modul, text="Тип ИБП:", font=label_font)
    lbl_model_type.grid(row=0, column=2, pady=(5, 5), sticky=E)

    # label_type = ttk.Label(frame_values_modul, textvariable=frame_values_modul.select_type, background='#f0f0f0')
    # label_type.grid(row=0, column=3)
    spinbox_type_box = ttk.Spinbox(frame_values_modul, width=20, textvariable=frame_values_modul.select_type,
                                   values=types,
                                   state="readonly", wrap=True, background='#f0f0f0')
    spinbox_type_box.grid(row=0, column=3, ipady=1, pady=(5, 5), sticky=W)

    # - список по расположению
    types_position = ["Стоечный", "Напольный", "Шкаф", "Другой"]
    # по умолчанию будет выбран последний элемент
    frame_values_modul.select_type_position = StringVar(frame_values_modul, value=types_position[0])

    lbl_model_type_position = Label(frame_values_modul, text="Тип корпуса:", font=label_font)
    lbl_model_type_position.grid(row=1, column=2, ipady=1, pady=(5, 5), sticky=E)

    # label_type_pos = ttk.Label(frame_values_modul, textvariable=frame_values_modul.select_type_position)
    # label_type_pos.grid(row=1, column=3)
    spinbox_pos = ttk.Spinbox(frame_values_modul, width=20, textvariable=frame_values_modul.select_type_position,
                              values=types_position, wrap=True, state="readonly")
    spinbox_pos.grid(row=1, column=3, ipady=1, pady=(5, 5), sticky=W)

    # - список типов АКБ
    res = connect_BD.sql_get_status_on_type_akb()
    types_akb_dic = {}
    # "SELECT type_id, type_akb, capacity, volt, FROM typesakb WHERE status == 1 ORDER BY capacity, volt;"
    if res:  # если не пуст список включённых при выборе
        for akb in res:
            types_akb_dic[akb[0]] = f"{akb[1]}\\{akb[2]}Ah\\{akb[3]}V"

    # изначально  в списке пустое значение, проводим проверку на вставку id в def add_model---------!!!!!
    types_akb = []
    for d in types_akb_dic.values():
        types_akb.append(d)
    # по умолчанию будет выбран 1-й пустой элемент
    frame_values_modul.select_type_akb = StringVar(frame_values_modul, value='')

    lbl_model_type_akb = Label(frame_values_modul, text="Тип АКБ\A/h\V:", font=label_font)
    lbl_model_type_akb.grid(row=2, column=2, padx=(40, 0), pady=(5, 5), sticky=E)

    # label_type_akb = ttk.Label(frame_values_modul, textvariable=frame_values_modul.select_type_akb)
    # label_type_akb.grid(row=2, column=3)
    combobox_akb_type = ttk.Combobox(frame_values_modul, width=25, textvariable=frame_values_modul.select_type_akb,
                                     values=types_akb, state="readonly")
    combobox_akb_type.grid(row=2, column=3, pady=(5, 5), sticky=W)

    # по умолчанию будет выбран 2
    frame_values_modul.select_count_main_element = StringVar(frame_values_modul, value='2')

    lbl_model_count_main = Label(frame_values_modul, text="Кол-во АКБ:", font=label_font)
    lbl_model_count_main.grid(row=3, column=2, pady=(5, 5), sticky=NE)

    # label_count_main = ttk.Label(frame_values_modul, textvariable=frame_values_modul.select_count_main_element)
    # label_count_main.grid(row=3, column=3, sticky=NW)
    spinbox_count_main = ttk.Spinbox(frame_values_modul, width=5,
                                     textvariable=frame_values_modul.select_count_main_element, from_=1.0, to=20.0,
                                     wrap=True, state="readonly")
    spinbox_count_main.grid(row=3, column=3, ipady=1, pady=(5, 5), sticky=NW)
    # -----------END---COLUMN 2-3---------------------------------------------------------------------

    # -----------START---COLUMN 4-5-------------------------------------------------------------------
    lbl_interface = Label(frame_values_modul, text="Интерфесы:", font=label_font)
    lbl_interface.grid(row=0, column=4, padx=(10, 0), pady=(0, 0), sticky=E)
    entry_interface = Entry(frame_values_modul, basic_style_entry_frame, width=20)
    entry_interface.insert(0, '')
    entry_interface.grid(row=0, column=5, pady=(0, 0), sticky=W)

    lbl_dop_info = Label(frame_values_modul, text="Доп. информ.:", font=label_font)
    lbl_dop_info.grid(row=1, column=4, padx=(10, 0), pady=(5, 5), sticky=E)
    entry_dop_info = Entry(frame_values_modul, basic_style_entry_frame, width=20)
    entry_dop_info.insert(0, '')
    entry_dop_info.grid(row=1, column=5, pady=(5, 5), sticky=W)

    lbl_model_comment = Label(frame_values_modul, text="Комментарии:", font=label_font)
    lbl_model_comment.grid(row=2, column=4, padx=(40, 0), pady=(10, 0), sticky=NE)
    text_model_comment = ScrolledText(frame_values_modul, width=20, height=5, font=font_entry, wrap="word")
    text_model_comment.grid(row=2, rowspan=2, column=5, pady=(10, 5), sticky=NW)
    # -----------END---COLUMN 4-5---------------------------------------------------------------------

    # -----------START---COLUMN 6-7-------------------------------------------------------------------
    # - модульный
    types_modul = ["Нет", "Да"]
    # по умолчанию будет выбран последний элемент
    frame_values_modul.select_type_modul = StringVar(frame_values_modul, value=types_modul[0])

    lbl_model_type_modul = Label(frame_values_modul, text="Модульный:", font=label_font)
    lbl_model_type_modul.grid(row=0, column=6, padx=(40, 0), pady=(5, 5), sticky=W)

    # label_type_modul = ttk.Label(frame_values_modul, textvariable=frame_values_modul.select_type_modul)
    # label_type_modul.grid(row=0, column=6, padx=(130, 0), sticky=W)
    spinbox_modul = ttk.Spinbox(frame_values_modul, width=5, textvariable=frame_values_modul.select_type_modul,
                                values=types_modul, wrap=True, state="readonly")
    spinbox_modul.grid(row=0, column=6, padx=(130, 0), ipady=1, pady=(5, 5), sticky=W)

    frame_add_model_modul = LabelFrame(frame_values_modul, padx=10, pady=2, text="Доп. модуль", font=('Arial', 11))

    lbl_model_info_modul = Label(frame_add_model_modul, text="Модель модуля:", font=label_font)
    lbl_model_info_modul.grid(row=0, column=0, sticky=E)

    entry_model_dop_info = Entry(frame_add_model_modul, basic_style_entry_frame)

    # - список типов АКБ
    # types_akb= [] берём пустой по умолчанию ''
    # по умолчанию будет выбран последний элемент
    frame_add_model_modul.select_type_akb_modul = StringVar(frame_add_model_modul, value='')

    lbl_model_type_akb_modul = Label(frame_add_model_modul, text="Тип АКБ\A/h\V:", font=label_font)
    lbl_model_type_akb_modul.grid(row=1, column=0, pady=(5, 5), sticky=E)
    # entry_dop_model_type = Entry(frame_add_model_modul, font=font_entry)
    # label_type_akb_modul = ttk.Label(frame_add_model_modul, width=50,
    #                                textvariable=frame_add_model_modul.select_type_akb_modul)
    # label_type_akb_modul.grid(row=1, column=1, sticky=E)
    combobox_akb_modul = ttk.Combobox(frame_add_model_modul, width=25,
                                      textvariable=frame_add_model_modul.select_type_akb_modul,
                                      values=types_akb)  # state="disabled"

    # - количества в модуле ------------------------------------------------------------------------------------
    count_dop_element = [str(x) for x in range(1, 13)]
    # по умолчанию будет выбран 2 элементa
    frame_add_model_modul.select_count_dop_element = StringVar(frame_add_model_modul, value='2')

    lbl_model_count_dop = Label(frame_add_model_modul, text="АКБ в модуле:", font=label_font)
    lbl_model_count_dop.grid(row=2, column=0, pady=(5, 5), sticky=E)

    # label_count_dop = ttk.Label(frame_add_model_modul, textvariable=frame_add_model_modul.select_count_dop_element)
    # label_count_dop.grid(row=2, column=1, sticky=W)
    # combobox_count_dop = ttk.Combobox(frame_add_model_modul, textvariable=frame_add_model_modul.select_count_dop_element, values=count_dop_element, state="disabled")
    spinbox_count_dop = ttk.Spinbox(frame_add_model_modul, width=5,
                                    textvariable=frame_add_model_modul.select_count_dop_element, from_=1.0, to=20.0,
                                    wrap=True, state="readonly")

    # -----------END---COLUMN 6-7--------------------------------------------------------------------

    def check(*args):
        if frame_values_modul.select_type_modul.get() == "Да":
            frame_add_model_modul.configure(background='#CCC')
            lbl_model_info_modul.configure(background='#CCC')
            lbl_model_type_akb_modul.configure(background='#CCC')
            lbl_model_count_dop.configure(background='#CCC')
            entry_model_dop_info.configure(state='normal')
            entry_model_dop_info.configure(background='#FDFBE1')
            # entry_dop_model_type.configure(state='normal')
            # entry_dop_model_type.configure(background='#FDFBE1')
            combobox_akb_modul.configure(state='readonly')
            combobox_akb_modul.set(types_akb[0])  # берём верхний
            spinbox_count_dop.configure(state='readonly')
            spinbox_count_dop.set(count_dop_element[1])

        else:
            frame_add_model_modul.configure(background='#F0F0F0')
            lbl_model_info_modul.configure(background='#F0F0F0')
            lbl_model_type_akb_modul.configure(background='#F0F0F0')
            lbl_model_count_dop.configure(background='#F0F0F0')
            entry_model_dop_info.delete(0, END)
            entry_model_dop_info.configure(state='disabled')
            # entry_dop_model_type.delete(0, END)
            # entry_dop_model_type.configure(state='disabled')
            combobox_akb_modul.set('')
            combobox_akb_modul.configure(state='disabled')
            spinbox_count_dop.set('')
            spinbox_count_dop.configure(state='disabled')

    frame_values_modul.select_type_modul.trace_add("write", check)
    frame_values_modul.select_type_modul.set("Нет")  # для установки по молчанию, чтоб поле не было выбрано
    entry_model_dop_info.grid(row=0, column=1, pady=(5, 5), sticky=W)
    # entry_dop_model_type.grid(row=1, column=1, pady=(5, 5), sticky=W)
    combobox_akb_modul.grid(row=1, column=1, pady=(5, 5), sticky=W)
    spinbox_count_dop.grid(row=2, column=1, pady=(5, 5), sticky=W)

    def OnClick_model(event):
        # - выборка данных из строки
        try:
            item_select = tree.selection()
            select_model = tree.item(item_select)['values']
        except Exception as e:
            messagebox.showinfo('Информация', 'Выберите только одну модель.')
            return 0

        entry_name.configure(state='normal')
        entry_name.delete(0, END)
        entry_name.insert(0, select_model[1])
        entry_name.configure(state='disabled')

        entry_name_short.delete(0, END)
        entry_name_short.insert(0, select_model[2])

        entry_power.delete(0, END)
        entry_power.insert(0, select_model[3])

        if select_model[5] == 1:
            frame_values_modul.status.set(status_on)

        else:
            frame_values_modul.status.set(status_off)

        spinbox_type_box.set(select_model[6])
        spinbox_pos.set(select_model[7])
        combobox_akb_type.set(select_model[8])

        split_count_element = select_model[9].split('\\')  # -> array ['08', '06(15)']

        spinbox_count_main.set(int(split_count_element[0]))

        all_count_akb = f"Всего: {str(int(split_count_element[0]) + select_model[17]) + '  ' if len(str(int(split_count_element[0]) + select_model[17])) < 2 else int(split_count_element[0]) + select_model[17]}"
        # если выбран то отображаем ИТОГО
        if entry_name.get():
            entry_summa_akb = Entry(frame_values_modul, width=10)
            entry_summa_akb.delete(0, END)
            entry_summa_akb.insert(0, all_count_akb)
            entry_summa_akb.configure(state='disabled')
            entry_summa_akb.grid(row=3, column=3, ipady=1, pady=(5, 0), sticky=NE)

        entry_interface.delete(0, END)
        entry_interface.insert(0, select_model[4])

        entry_dop_info.delete(0, END)
        entry_dop_info.insert(0, select_model[13])

        text_model_comment.delete(0.1, END)
        text_model_comment.insert(0.1, select_model[14])

        spinbox_modul.set(select_model[10])

        # если имеется  доп.модуль, то отображаем его свойства
        if select_model[10] in ['Да']:
            entry_model_dop_info.delete(0, END)
            entry_model_dop_info.insert(0, select_model[15])

            combobox_akb_modul.set(select_model[16])
            spinbox_count_dop.set(select_model[17])

    # - изменяем значение полей, но с проверкой
    def edit_value_model():

        global id_type_akb, current_user

        if current_user[0][3] not in ("Supper_Admin_UPS", 'Админ'):
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user[0][3]}' не может изменять!")
            return

        # если ничего не выбрано то и не сравниваем и не изменяем
        if entry_name.get() == '': return
        try:
            # выбираем данные из выделенного пользователя
            item_select = tree.selection()
            selected_model = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только одну модель.')
            return

        if (str(entry_name_short.get().strip()) != str(selected_model[2])) or \
                (str(entry_power.get().strip()) != str(selected_model[3])) or \
                (str(frame_values_modul.status.get()) != str(("Вкл." if selected_model[5] == 1 else 'Выкл.'))) or \
                (str(spinbox_type_box.get()) != str(selected_model[6])) or \
                (str(spinbox_pos.get()) != str(selected_model[7])) or \
                (str(combobox_akb_type.get()) != str(selected_model[8])) or \
                (str(spinbox_count_main.get()) != str(selected_model[9].split('\\')[0])) or \
                (str(text_model_comment.get(0.1, END).strip()) != str(selected_model[14])) or \
                (str(entry_interface.get().strip()) != str(selected_model[4])) or \
                (str(entry_dop_info.get().strip()) != str(selected_model[13])) or \
                (str(spinbox_modul.get()) != str(selected_model[10])) or \
                ((str('нет') if str(entry_model_dop_info.get().strip()) == '' else str(
                    entry_model_dop_info.get().strip())) != str(selected_model[15])) or \
                ((str('нет') if str(combobox_akb_modul.get()) == '' else str(combobox_akb_modul.get())) != str(
                    selected_model[16])) or \
                ((str('0') if str(spinbox_count_dop.get()) == '' else str(spinbox_count_dop.get())) != str(
                    selected_model[17])):

            # print('есть изменения')

            # -если пустой тип акб, значит не выбран
            if not combobox_akb_type.get():
                messagebox.showwarning('Предупреждение', "Выберите тип АКБ\A/h\V для модели.")
                return

            if str(spinbox_modul.get()) != str(selected_model[10]) and (spinbox_modul.get() == 'Да'):
                if not entry_model_dop_info.get().strip():
                    messagebox.showwarning('Предупреждение', "Укажите модель для доп. модуля.")
                    return
                if not combobox_akb_modul.get():
                    messagebox.showwarning('Предупреждение', "Выберите тип АКБ\A/h\V для доп. модуля.")
                    return entry_dop_info.get().strip()

            # - ИЩЕМ ID ТИПА АКБ
            # - берём список типов АКБ
            # res = connect_BD.sql_get_status_on_type_akb()
            res = connect_BD.sql_get_status_type_akb()
            types_akb_dic = {}
            # "SELECT type_id, type_akb, capacity, volt, FROM typesakb WHERE status == 1 ORDER BY capacity, volt;"
            if res:  # если не пуст список включённых при выборе
                for akb in res:
                    types_akb_dic[akb[
                        0]] = f"{akb[1]}\\{akb[2]}Ah\\{akb[3]}V"  # {entry_type.get()}\{entry_capacity.get()}Ah\{entry_volt.get()}

                # print(types_akb_dic)
                types_akb = []
                for d in types_akb_dic.values():
                    types_akb.append(d)

                id_type_akb = [id_key for id_key, value in types_akb_dic.items() if
                               value == combobox_akb_type.get()]  # combobox_akb.get()]

            params_list = [id_type_akb[0], current_user[0][0], entry_name_short.get().strip(),
                           entry_power.get().strip(), 1 if frame_values_modul.status.get() == "Вкл." else 0,
                           spinbox_type_box.get(), spinbox_pos.get(), spinbox_count_main.get(),
                           text_model_comment.get(0.1, END).strip(),
                           'н/д' if entry_interface.get().strip() == '' else entry_interface.get().strip(),
                           'н/д' if entry_dop_info.get().strip() == '' else entry_dop_info.get().strip(),
                           spinbox_modul.get(),
                           'нет' if entry_model_dop_info.get().strip() == '' else entry_model_dop_info.get().strip(),
                           'нет' if combobox_akb_modul.get() == '' else combobox_akb_modul.get(),
                           '0' if spinbox_count_dop.get() == '' else spinbox_count_dop.get(),
                           selected_model[18]]

            # соблюдение уникального названия в столбце <короткое имя>
            if entry_name_short.get().strip() in short_name_list and entry_name_short.get().strip() != selected_model[
                2]:
                messagebox.showinfo('Информация',
                                    f"Короткое имя модуля '{entry_name_short.get().strip()}' уже используется.\nУкажите другое.")
                entry_name_short.delete(0, END)
                entry_name_short.insert(0, selected_model[2])
                return

            # print(entry_name_short.get().strip(), short_name_list)

            result = messagebox.askyesno('Внимание',
                                         f"Вы точно хотите внести изменения в модель\n '{entry_name.get().strip()}'?")
            if result:
                params = tuple(params_list)
                res_sql = connect_BD.sql_update_models(params)
                # print('------params-->', params)

                if res_sql:
                    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # - меняем на новые значения в таблице (строку)
                    tree.item(item_select, values=(
                        selected_model[0], selected_model[1], params[2], params[3], params[9], params[4],
                        params[5], params[6], combobox_akb_type.get(),
                        f"{spinbox_count_main.get()}\\{spinbox_count_dop.get() if spinbox_count_dop.get() else '0'} ({str(int(spinbox_count_main.get()) + int(spinbox_count_dop.get() if spinbox_count_dop.get() else 0))})",
                        params[11], current_user[0][2], date_time, params[10], params[8],
                        params[12], params[13], params[14], params[15]))

                    all_count_akb = f"Всего: {str(int(spinbox_count_main.get()) + int(spinbox_count_dop.get() if spinbox_count_dop.get() else 0)) + '  ' if len(str(int(spinbox_count_main.get()) + int(spinbox_count_dop.get() if spinbox_count_dop.get() else 0))) < 2 else int(spinbox_count_main.get()) + int(spinbox_count_dop.get() if spinbox_count_dop.get() else 0)}"
                    # если выбран то отображаем ИТОГО
                    if entry_name.get():
                        entry_summa_akb = Entry(frame_values_modul, width=10)
                        entry_summa_akb.delete(0, END)
                        entry_summa_akb.insert(0, all_count_akb)
                        entry_summa_akb.configure(state='disabled')
                        entry_summa_akb.grid(row=3, column=3, ipady=1, pady=(5, 0), sticky=NE)
            # else:
            #   dismiss(wind_list_model_ipb)

    btn_edit_model = ttk.Button(frame_values_modul, text='Изменить', command=edit_value_model)
    btn_edit_model.grid(row=4, columnspan=7, column=7, padx=(0, 5), pady=(5, 5), sticky='e')

    btn_list_model_cancel = ttk.Button(wind_list_model_ipb, text='Закрыть',
                                       command=lambda: dismiss(wind_list_model_ipb))
    btn_list_model_cancel.grid(row=2, column=2, padx=(0, 10), pady=(0, 10), sticky='e')

    tree.bind("<<TreeviewSelect>>", OnClick_model)

    frame_list_modul_ipb.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), columnspan=3)
    frame_values_modul.grid(row=1, column=0, columnspan=4, padx=(10, 10), pady=(0, 10), sticky=NSEW)
    frame_add_model_modul.grid(row=1, rowspan=4, columnspan=2, column=6, padx=(40, 10), pady=(3, 0), sticky=NW)

    wind_list_model_ipb.grab_set()  # захватываем польз-льский ввод


def add_model(wind_add_model, entry_name_model, entry_name_model_short, entry_model_power,
              entry_model_interface, entry_model_info, text_model_comment, status, spinbox_type_box,
              spinbox_pos, combobox_akb_type,
              spinbox_count_main,
              spinbox_modul,
              entry_model_dop_info,
              combobox_akb_modul,  # entry_dop_model_type,
              spinbox_count_dop):
    if not clear_text_strip(entry_name_model.get()) or (not clear_text_strip(entry_name_model_short.get())) or (
            not clear_text_strip(entry_model_power.get())):
        messagebox.showinfo('Информация', "Заполните все обязательные поля.")
        return
    # --проверка на выбор типов АКБ в основном и дополнительном модуле
    if not combobox_akb_type.get():
        messagebox.showwarning('Предупреждение', "Не выбран тип АКБ. Выберите тип.")
        return
    if spinbox_modul.get() == 'Да' and (not combobox_akb_modul.get()):
        messagebox.showwarning('Предупреждение',
                               "Указан доп. модуль, но не выбран тип АКБ.\nВыберите тип АКБ в модуле.")
        return

    if spinbox_modul.get() == 'Да' and (not clear_text_strip(entry_model_dop_info.get())):
        messagebox.showwarning('Предупреждение', "Указан доп. модуль, но не указана модель модуля.")
        return

    # - ИЩЕМ ID ТИПА АКБ
    # - берём список типов АКБ
    res = connect_BD.sql_get_status_on_type_akb()
    types_akb_dic = {}
    # "SELECT type_id, type_akb, capacity, volt, FROM typesakb WHERE status == 1 ORDER BY capacity, volt;"
    if res:  # если не пуст список включённых при выборе
        for akb in res:
            types_akb_dic[akb[0]] = f"{akb[1]}\\{akb[2]}Ah\\{akb[3]}V"

        types_akb = []
        for d in types_akb_dic.values():
            types_akb.append(d)

        id_type_akb = [id_key for id_key, value in types_akb_dic.items() if
                       value == combobox_akb_type.get()]  # combobox_akb.get()]

    # - удаляем пробелы
    entry_name_model = clear_text_strip(entry_name_model.get()[0:25])
    entry_name_model_short = clear_text_strip(entry_name_model_short.get()[0:20])
    entry_model_power = clear_text_strip(entry_model_power.get()[0:10])
    entry_model_interface = clear_text_strip(entry_model_interface.get()[0:30]) if clear_text_strip(
        entry_model_interface.get().strip()) else ''
    entry_model_info = clear_text_strip(entry_model_info.get()[0:30]) if clear_text_strip(
        entry_model_info.get().strip()) else ''
    text_model_comment = clear_text_strip(text_model_comment.get("1.0", END)[0:150])  # ------------check \n
    status = 1 if status.get() == "Вкл." else 0
    spinbox_type_box = clear_text_strip(spinbox_type_box.get())
    spinbox_pos = clear_text_strip(spinbox_pos.get())
    id_type_akb = id_type_akb[0]
    spinbox_count_main = clear_text_strip(spinbox_count_main.get())
    spinbox_modul = clear_text_strip(spinbox_modul.get())
    entry_model_dop_info = clear_text_strip(
        entry_model_dop_info.get()[0:30]) if entry_model_dop_info.get().strip() else 'нет'
    combobox_akb_modul = clear_text_strip(combobox_akb_modul.get()) if combobox_akb_modul.get() else 'нет'
    spinbox_count_dop = clear_text_strip(spinbox_count_dop.get()) if spinbox_count_dop.get() else 0

    if entry_model_interface == '':
        entry_model_interface = 'н/д'
    if entry_model_info == '':
        entry_model_info = 'н/д'

    params = (
        id_type_akb, current_user[0][0], entry_name_model, entry_name_model_short, entry_model_power,
        entry_model_interface,
        entry_model_info, spinbox_type_box,
        spinbox_pos, spinbox_count_main, spinbox_modul, entry_model_dop_info, combobox_akb_modul,
        spinbox_count_dop, text_model_comment, status)

    # добавляем модель в таблицу
    res = connect_BD.sql_insert_model(params)
    # INSERT INTO models(type_elemt_id, user_id, name, short_name, power, interface, info, type_battery
    # type_box, count_element, is_modul, name_modul, type_battery_modul, count_element_modul, comment,
    # status)
    # VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime')) '''

    if res:
        # - закрываем окно
        wind_add_model.destroy()
        messagebox.showinfo('Информация', f"Модель ИБП '{entry_name_model_short[0:20]}'  добавлена.")


def add_model_form():
    if current_user[0][3] not in ('Админ'):  # "Supper_Admin_UPS",
        messagebox.showinfo('Информация', f"Пользователь с ролью '{current_user[0][3]}' не может добавить модель!")
    else:
        wind_add_model = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
        wind_add_model.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_add_model))  # перехватываем нажатие на крестик
        wind_add_model.attributes("-toolwindow", False)
        # wind_add_user.geometry('362x250')
        x = (wind_add_model.winfo_screenwidth() - wind_add_model.winfo_reqwidth()) / 2
        y = (wind_add_model.winfo_screenheight() - wind_add_model.winfo_reqheight()) / 2
        wind_add_model.geometry("+%d+%d" % (x - 230, y - 210))
        wind_add_model.title("Добавление модели")
        wind_add_model.resizable(False, False)
        # wind_add_depart['bg'] = '#ccc'

        frame_add_model = LabelFrame(wind_add_model, padx=10, pady=10, text="Информация о модели", font=('Arial', 11),
                                     highlightbackground="seashell4", highlightthickness=0)

        lbl_name_model = Label(frame_add_model, text="Наименование:", font=label_font)
        lbl_name_model.grid(row=0, column=0, sticky=E)
        entry_name_model = Entry(frame_add_model, font=font_entry, background='#FDFBE1')
        entry_name_model.grid(row=0, column=1, pady=(5, 5), sticky=W)

        lbl_name_model_short = Label(frame_add_model, text="Короткое наимен.:", font=label_font)
        lbl_name_model_short.grid(row=1, column=0, sticky=E)
        entry_name_model_short = Entry(frame_add_model, font=font_entry, background='#FDFBE1')
        entry_name_model_short.grid(row=1, column=1, pady=(5, 5), sticky=W)

        lbl_model_power = Label(frame_add_model, text="Мощность(W):", font=label_font)
        lbl_model_power.grid(row=2, column=0, sticky=E)
        entry_model_power = Entry(frame_add_model, font=font_entry, background='#FDFBE1')
        entry_model_power.grid(row=2, column=1, pady=(5, 5), sticky=W)

        lbl_model_interface = Label(frame_add_model, text="Интерфейсы:", font=label_font)
        lbl_model_interface.grid(row=3, column=0, sticky=E)
        entry_model_interface = Entry(frame_add_model, font=font_entry)
        entry_model_interface.grid(row=3, column=1, pady=(5, 5), sticky=W)

        lbl_model_info = Label(frame_add_model, text="Доп. информация:", font=label_font)
        lbl_model_info.grid(row=4, column=0, sticky=E)
        entry_model_info = Entry(frame_add_model, font=font_entry)
        entry_model_info.grid(row=4, column=1, pady=(5, 5), sticky=W)

        lbl_model_comment = Label(frame_add_model, text="Комментарии:", font=label_font)
        lbl_model_comment.grid(row=5, column=0, pady=(20, 0), sticky=NE)
        text_model_comment = ScrolledText(frame_add_model, width=20, height=5, font=font_entry, wrap="word")
        text_model_comment.grid(row=5, column=1, pady=(20, 30), sticky=NW)

        status_on = "Вкл."
        status_of = "Выкл."

        frame_add_model.status = StringVar(frame_add_model,
                                           value=status_on)  # по умолчанию будет выбран элемент с value=status_on

        status_on_btn = ttk.Radiobutton(frame_add_model, text=status_on, variable=frame_add_model.status,
                                        value=status_on)
        status_on_btn.grid(rowspan=1, row=5, column=1, pady=(120, 0), sticky='nw')

        status_of_btn = ttk.Radiobutton(frame_add_model, text=status_of, variable=frame_add_model.status,
                                        value=status_of)
        status_of_btn.grid(rowspan=1, row=5, column=1, pady=(120, 0), padx=[50, 0], sticky='nw')

        label_style = ttk.Style()
        label_style.configure("My_spim_style.TSpinbox", font="helvetica 11")

        # - список видов
        types = ["Off-line", "Interactive", "On-line"]
        # по умолчанию будет выбран последний элемент
        frame_add_model.select_type = StringVar(frame_add_model, value=types[0])

        lbl_model_type = Label(frame_add_model, text="Тип ИБП:", font=label_font)
        lbl_model_type.grid(row=0, column=2, pady=(5, 5), sticky=E)

        # label_type = ttk.Label(frame_add_model, width=20,  textvariable=frame_add_model.select_type, background='#f0f0f0',)
        # label_type.grid(row=0, column=3)
        spinbox_type_box = ttk.Spinbox(frame_add_model, width=25, textvariable=frame_add_model.select_type,
                                       values=types,
                                       state="readonly", wrap=True, background='#f0f0f0',
                                       style="My_spim_style.TSpinbox")
        spinbox_type_box.grid(row=0, column=3, ipady=1, pady=(5, 5), sticky=W)

        # - список по расположению
        types_position = ["Стоечный", "Напольный", "Шкаф"]
        # по умолчанию будет выбран последний элемент
        frame_add_model.select_type_position = StringVar(frame_add_model, value=types_position[0])

        lbl_model_type_position = Label(frame_add_model, text="Тип корпуса:", font=label_font)
        lbl_model_type_position.grid(row=1, column=2, ipady=1, pady=(5, 5), sticky=E)

        # label_type_pos = ttk.Label(frame_add_model, width=20,  textvariable=frame_add_model.select_type_position)
        # label_type_pos.grid(row=1, column=3)
        spinbox_pos = ttk.Spinbox(frame_add_model, width=25, textvariable=frame_add_model.select_type_position,
                                  values=types_position, wrap=True, state="readonly", style="My_spim_style.TSpinbox")
        spinbox_pos.grid(row=1, column=3, ipady=1, pady=(5, 5), sticky=W)

        # - список типов АКБ
        res = connect_BD.sql_get_status_on_type_akb()
        types_akb_dic = {}
        # "SELECT type_id, type_akb, capacity, volt, FROM typesakb WHERE status == 1 ORDER BY capacity, volt;"
        if res:  # если не пуст список включённых при выборе
            for akb in res:
                types_akb_dic[akb[
                    0]] = f"{akb[1]}\\{akb[2]}Ah\\{akb[3]}V"  # {entry_type.get()}\{entry_capacity.get()}Ah\{entry_volt.get()}
        # else:
        # 10000 просто для отображения нулевого
        # types_akb_dic[10000] = ''

        # изначально список в списке пустое значение, проводим проверку на вставку id в def add_model---------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        types_akb = []
        for d in types_akb_dic.values():
            types_akb.append(d)
        # по умолчанию будет выбран 1-й пустой элемент
        frame_add_model.select_type_akb = StringVar(frame_add_model, value='')

        lbl_model_type_akb = Label(frame_add_model, text="Тип АКБ\A/h\V:", font=label_font)
        lbl_model_type_akb.grid(row=2, column=2, pady=(5, 5), sticky=E)

        # label_type_akb = Label(frame_add_model, width=20, textvariable=frame_add_model.select_type_akb, style="My_spim_style.TSpinbox")
        # label_type_akb.grid(row=2, column=3)
        combobox_akb_type = ttk.Combobox(frame_add_model, width=25, textvariable=frame_add_model.select_type_akb,
                                         values=types_akb, state="readonly", style="My_spim_style.TSpinbox")
        combobox_akb_type.grid(row=2, column=3, pady=(5, 5), sticky=W)

        # по умолчанию будет выбран 2
        frame_add_model.select_count_main_element = StringVar(frame_add_model, value='2')

        lbl_model_count_main = Label(frame_add_model, text="Кол-во АКБ.:", font=label_font)
        lbl_model_count_main.grid(row=3, column=2, pady=(5, 5), sticky=E)

        # label_count_main = ttk.Label(frame_add_model, textvariable=frame_add_model.select_count_main_element)
        # label_count_main.grid(row=3, column=3, sticky=W)
        spinbox_count_main = Spinbox(frame_add_model, width=5,
                                     textvariable=frame_add_model.select_count_main_element, from_=1.0, to=30.0,
                                     wrap=True, state="readonly")
        spinbox_count_main.grid(row=3, column=3, ipady=1, pady=(5, 5), sticky=W)

        # - модульный
        types_modul = ["Нет", "Да"]
        # по умолчанию будет выбран последний элемент
        frame_add_model.select_type_modul = StringVar(frame_add_model, value=types_modul[0])

        lbl_model_type_modul = Label(frame_add_model, text="Модульный:", font=label_font)
        lbl_model_type_modul.grid(row=4, column=2, pady=(5, 5), sticky=E)

        # label_type_modul = ttk.Label(frame_add_model, textvariable=frame_add_model.select_type_modul)
        # label_type_modul.grid(row=4, column=3, sticky=W)
        spinbox_modul = Spinbox(frame_add_model, width=5, textvariable=frame_add_model.select_type_modul,
                                values=types_modul, wrap=True, state="readonly")
        spinbox_modul.grid(row=4, column=3, ipady=1, pady=(5, 5), sticky=W)
        # -----------------------------------------------------------

        frame_add_model_modul = LabelFrame(frame_add_model, padx=10, pady=10, text="Доп. модуль", font=('Arial', 10))

        lbl_model_info_modul = Label(frame_add_model_modul, text="Модель модуля:", font=label_font)
        lbl_model_info_modul.grid(row=0, column=0, sticky=E)

        entry_model_dop_info = Entry(frame_add_model_modul, font=font_entry)

        # - список АКБ_modul
        # types_akb= [] берём пустой по умолчанию ''
        # по умолчанию будет выбран последний элемент
        frame_add_model_modul.select_type_akb_modul = StringVar(frame_add_model_modul, value='')

        lbl_model_type_akb_modul = Label(frame_add_model_modul, text="Тип АКБ\A/h\V:", font=label_font)
        lbl_model_type_akb_modul.grid(row=1, column=0, pady=(5, 5), sticky=E)
        # entry_dop_model_type = Entry(frame_add_model_modul, font=font_entry)
        # label_type_akb_modul = Label(frame_add_model_modul, width=20,
        #                                textvariable=frame_add_model_modul.select_type_akb_modul)
        # label_type_akb_modul.grid(row=1, column=1, sticky=E)
        combobox_akb_modul = ttk.Combobox(frame_add_model_modul, width=25,
                                          textvariable=frame_add_model_modul.select_type_akb_modul,
                                          values=types_akb, style="My_spim_style.TSpinbox")  # state="disabled"

        # - количества в модуле ------------------------------------------------------------------------------------
        count_dop_element = [str(x) for x in range(1, 13)]
        # по умолчанию будет выбран 2 элементa
        frame_add_model_modul.select_count_dop_element = StringVar(frame_add_model_modul, value='2')

        lbl_model_count_dop = Label(frame_add_model_modul, text="АКБ в модуле:", font=label_font)
        lbl_model_count_dop.grid(row=2, column=0, pady=(5, 5), sticky=E)

        # label_count_dop = ttk.Label(frame_add_model_modul, width=3, textvariable=frame_add_model_modul.select_count_dop_element)
        # label_count_dop.grid(row=2, column=1, sticky=W)
        # combobox_count_dop = ttk.Combobox(frame_add_model_modul, textvariable=frame_add_model_modul.select_count_dop_element, values=count_dop_element, state="disabled")
        spinbox_count_dop = ttk.Spinbox(frame_add_model_modul, width=5,
                                        textvariable=frame_add_model_modul.select_count_dop_element, from_=1.0, to=30.0,
                                        wrap=True, state="readonly")

        # spinbox_count_main.grid(row=3, column=3, ipady=1, pady=(5, 5), sticky=W)

        def check(*args):
            if frame_add_model.select_type_modul.get() == "Да":
                frame_add_model_modul.configure(background='#CCC')
                lbl_model_info_modul.configure(background='#CCC')
                lbl_model_type_akb_modul.configure(background='#CCC')
                lbl_model_count_dop.configure(background='#CCC')
                entry_model_dop_info.configure(state='normal')
                entry_model_dop_info.configure(background='#FDFBE1')
                # entry_dop_model_type.configure(state='normal')
                # entry_dop_model_type.configure(background='#FDFBE1')
                combobox_akb_modul.configure(state='readonly')
                combobox_akb_modul.set(types_akb[0])  # берём верхний
                spinbox_count_dop.configure(state='readonly')
                spinbox_count_dop.set(count_dop_element[1])

            else:
                frame_add_model_modul.configure(background='#F0F0F0')
                lbl_model_info_modul.configure(background='#F0F0F0')
                lbl_model_type_akb_modul.configure(background='#F0F0F0')
                lbl_model_count_dop.configure(background='#F0F0F0')
                entry_model_dop_info.delete(0, END)
                entry_model_dop_info.configure(state='disabled')
                # entry_dop_model_type.delete(0, END)
                # entry_dop_model_type.configure(state='disabled')
                combobox_akb_modul.set('')
                combobox_akb_modul.configure(state='disabled')
                spinbox_count_dop.set('')
                spinbox_count_dop.configure(state='disabled')

        frame_add_model.select_type_modul.trace_add("write", check)
        frame_add_model.select_type_modul.set("Нет")  # для установки по молчанию, чтоб поле не было выбрано
        entry_model_dop_info.grid(row=0, column=1, pady=(5, 5), sticky=W)
        # entry_dop_model_type.grid(row=1, column=1, pady=(5, 5), sticky=W)
        combobox_akb_modul.grid(row=1, column=1, pady=(5, 5), sticky=W)
        spinbox_count_dop.grid(row=2, column=1, pady=(5, 5), sticky=W)

        # -----------------------------------------------------------

        frame_add_model.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))
        frame_add_model_modul.grid(row=5, columnspan=2, column=2, padx=(15, 10), pady=(10, 0))

        btn_add_model = ttk.Button(wind_add_model, text='Создать',
                                   command=lambda: add_model(wind_add_model, entry_name_model, entry_name_model_short,
                                                             entry_model_power,
                                                             entry_model_interface, entry_model_info,
                                                             text_model_comment,
                                                             frame_add_model.status, spinbox_type_box,
                                                             spinbox_pos, combobox_akb_type,
                                                             spinbox_count_main,
                                                             spinbox_modul,
                                                             entry_model_dop_info,
                                                             combobox_akb_modul,  # entry_dop_model_type,
                                                             spinbox_count_dop))
        btn_add_model.grid(row=2, columnspan=2, column=0, padx=(0, 130), pady=(15, 10), sticky='e')

        btn_add_model_cancel = ttk.Button(wind_add_model, text='Отмена', command=lambda: dismiss(wind_add_model))
        btn_add_model_cancel.grid(row=2, columnspan=2, column=0, padx=(0, 10), pady=(15, 10), sticky='e')

        wind_add_model.grab_set()  # захватываем польз-льский ввод


def list_type_akb():
    wind_list_type_akb = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
    wind_list_type_akb.protocol("WM_DELETE_WINDOW",
                                lambda: dismiss(wind_list_type_akb))  # перехватываем нажатие на крестик
    wind_list_type_akb.attributes("-toolwindow", False)
    # wind_list_user.geometry('790x460')
    x = (wind_list_type_akb.winfo_screenwidth() - wind_list_type_akb.winfo_reqwidth()) / 2
    y = (wind_list_type_akb.winfo_screenheight() - wind_list_type_akb.winfo_reqheight()) / 2
    wind_list_type_akb.geometry("+%d+%d" % (x - 300, y - 210))
    wind_list_type_akb.title("Список типов АКБ")
    wind_list_type_akb.resizable(False, False)
    # wind_list_depart['bg'] = '#ccc'

    wind_list_type_akb.rowconfigure(0, weight=6)
    wind_list_type_akb.rowconfigure(1, weight=1)

    frame_list_type_akb = LabelFrame(wind_list_type_akb, text="Типы АКБ", font=('Arial', 11),
                                     highlightbackground="#ccc", highlightthickness=1)

    # определяем данные для отображения ---------------------------------------------------------------------
    types_akbs = connect_BD.sql_get_all_status_type()
    types_akb_edit = []
    num = 1
    for akb in types_akbs:
        types_akb_edit.append(
            tuple([num, akb[0], akb[1], float(akb[2]), akb[3], akb[4], akb[5], akb[6], akb[7], akb[8], akb[9]]))
        num += 1

    # определяем столбцы
    columns = (
        "number", "type_akb", "capacity", "volt", "type_terminal", "type_size", "dop_info", "status", "user",
        "data_create",
        "type_id")

    tree = ttk.Treeview(frame_list_type_akb, columns=columns, show="headings")
    tree.grid(row=0, column=0)

    def sort(col, reverse):
        nonlocal tree
        # получаем все значения столбцов в виде отдельного списка
        lst = [(tree.set(k, col), k) for k in tree.get_children("")]
        # сортируем список
        lst.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(lst):
            tree.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        tree.heading(col, command=lambda: sort(col, not reverse))

    # определяем заголовки с выпавниваем по левому краю
    tree.heading("number", text="#", anchor=E)
    tree.heading("type_akb", text="Тип", anchor='center', command=lambda: sort(1, False))
    tree.heading("capacity", text="Емкость(A/h)", anchor=E, command=lambda: sort(2, False))  # anchor='center'
    tree.heading("volt", text="Вольт(V)", anchor=E, command=lambda: sort(3, False))  # anchor='center'
    tree.heading("type_terminal", text="Тип клем", anchor=E, command=lambda: sort(4, False))  # anchor='center'
    tree.heading("type_size", text="Типоразмер", anchor=E, command=lambda: sort(5, False))  # anchor='center'
    tree.heading("dop_info", text="Инфо", anchor=E, command=lambda: sort(6, False))  # anchor='center'
    tree.heading("status", text="Вкл.\Выкл.", anchor=E, command=lambda: sort(7, False))
    tree.heading("user", text="Создал\Изменил", anchor=E, command=lambda: sort(8, False))
    tree.heading("data_create", text="Дата создания\изм.", anchor=E, command=lambda: sort(9, False))
    tree.heading("type_id", text="id", anchor=E)

    # настраиваем столбцы
    tree.column("#1", stretch=NO, anchor=E, width=30)  # number
    tree.column("#2", stretch=NO, anchor=E, width=100)  # type_akb
    tree.column("#3", stretch=NO, anchor=E, width=100)  # capacity anchor='center'
    tree.column("#4", stretch=NO, anchor=E, width=80)  # volt
    tree.column("#5", stretch=NO, anchor=E, width=80)  # type_terminal
    tree.column("#6", stretch=NO, anchor=E, width=100)  # type_size
    tree.column("#7", stretch=NO, anchor=E, width=0)  # дdop_info
    tree.column("#8", stretch=NO, anchor=E, width=80)  # status
    tree.column("#9", stretch=NO, anchor=E, width=120)  # user
    tree.column("#10", stretch=NO, anchor=E, width=150)  # data_create
    tree.column("#11", stretch=NO, anchor=E, width=0)  # type_id

    # - отображаем указанные колонки
    # tree['displaycolumns'] = ("number", "type_akb", "capacity", "volt", "type_terminal", "type_size", "dop_info", "status", "user", "data_create", "type_id")

    # добавляем данные
    for one_akb in types_akb_edit:
        tree.insert("", END, text=one_akb[2], values=one_akb)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(frame_list_type_akb, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --------------------------------------------------------------------------
    frame_values_type = LabelFrame(wind_list_type_akb, text="Свойства", font=('Arial', 11), highlightbackground="#ccc",
                                   highlightthickness=1)

    lbl_type = Label(frame_values_type, text="Тип:", font=font_header)
    lbl_type.grid(row=0, column=0, padx=(10, 0), sticky=E)
    entry_type = Entry(frame_values_type, basic_style_entry_frame)
    entry_type.insert(0, '')
    entry_type.configure(state='disabled')
    entry_type.grid(row=0, column=1, sticky=W)

    # по умолчанию будет выбран 1.0
    frame_values_type.select_сapacity = StringVar(frame_values_type, value='1.0')

    lbl_capacity = Label(frame_values_type, text="Емкость (A/h):", font=font_header)
    lbl_capacity.grid(row=1, column=0, sticky=E)
    entry_capacity = Spinbox(frame_values_type, font=font_header, textvariable=frame_values_type.select_сapacity,
                             width=10, from_=1.0,
                             to=130.0, increment=0.1, wrap=True,
                             state='readonly')  # textvariable=frame_add_type.select_сapacity,
    entry_capacity.grid(row=1, column=1, pady=(5, 5), sticky=W)

    # по умолчанию будет выбран 1.0
    frame_values_type.select_volt = StringVar(frame_values_type, value='1.0')
    lbl_volt = Label(frame_values_type, text="Вольт (V):", font=font_header)
    lbl_volt.grid(row=2, column=0, sticky=E)
    entry_volt = Spinbox(frame_values_type, font=font_header, textvariable=frame_values_type.select_volt, width=10,
                         from_=1.0, to=230.0,
                         increment=0.1, wrap=True, state='readonly')
    entry_volt.grid(row=2, column=1, sticky=W)

    # --- radiobutton status on\off
    status_on = "Вкл."
    status_of = "Выкл."

    frame_values_type.status = StringVar(frame_values_type, value=status_of)  # по умолчанию будет выбран элемент

    status_on_btn = ttk.Radiobutton(frame_values_type, text=status_on, variable=frame_values_type.status,
                                    value=status_on)
    status_on_btn.grid(row=3, column=1, pady=(5, 5), sticky='w')

    status_of_btn = ttk.Radiobutton(frame_values_type, text=status_of, variable=frame_values_type.status,
                                    value=status_of)
    status_of_btn.grid(row=3, column=1, pady=(5, 5), padx=(50, 0), sticky='w')

    lbl_type_terminal = Label(frame_values_type, text="Тип клем:", font=font_header)
    lbl_type_terminal.grid(row=0, column=2, padx=(10, 0), sticky=E)
    entry_lbl_type_terminal = Entry(frame_values_type, basic_style_entry_frame)
    entry_lbl_type_terminal.insert(0, '')
    entry_lbl_type_terminal.grid(row=0, column=3, pady=(5, 5), sticky=W)

    lbl_type_size = Label(frame_values_type, text="Типоразмер:", font=font_header)
    lbl_type_size.grid(row=1, column=2, sticky=E)
    entry_type_size = Entry(frame_values_type, basic_style_entry_frame)
    entry_type_size.insert(0, '')
    entry_type_size.grid(row=1, column=3, sticky=W)

    lbl_dop_info = Label(frame_values_type, text="Доп. информация:", font=font_header)
    lbl_dop_info.grid(row=2, column=2, pady=(5, 0), sticky=E)
    entry_dop_info = Entry(frame_values_type, basic_style_entry_frame, width=54)
    entry_dop_info.insert(0, '')
    entry_dop_info.grid(row=2, column=3, columnspan=3, pady=(5, 0), sticky=W)

    lbl_select = Label(frame_values_type, text="Вид при выборе:", font=font_header)
    lbl_select.grid(row=3, column=2, pady=(5, 0), sticky=E)
    entry_select = Label(frame_values_type, font="Arial 10 bold roman")
    entry_select.grid(row=3, column=3, columnspan=2, pady=(5, 0), sticky=W)

    lbl_create_name_type = Label(frame_values_type, text="Создал(изм.):", font=font_header)
    lbl_create_name_type.grid(row=0, column=4, padx=(10, 0), sticky=E)
    entry_create_name_type = Entry(frame_values_type, basic_style_entry_frame, )
    entry_create_name_type.insert(0, '')
    entry_create_name_type.configure(state='disabled')
    entry_create_name_type.grid(row=0, column=5, pady=(5, 5), sticky=W)

    lbl_create_data_type = Label(frame_values_type, text="Дата:", font=font_header)
    lbl_create_data_type.grid(row=1, column=4, sticky=E)
    entry_create_data_type = Entry(frame_values_type, basic_style_entry_frame)
    entry_create_data_type.insert(0, '')
    entry_create_data_type.configure(state='disabled')
    entry_create_data_type.grid(row=1, column=5, sticky=W)

    def edit_value_type_akb():
        global current_user

        if current_user[0][3] not in ('Админ'):
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user[0][3]}' не может изменять!")
            return

        # если ничего не выбрано то и не сравниваем и не изменяем
        if entry_type.get() == '': return

        # выбираем данные из выделенного пользователя
        try:
            item_select = tree.selection()
            selected_type_akb = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только один тип.')
            return

        if (str(entry_capacity.get()) != str(selected_type_akb[2])) or (
                str(entry_volt.get()) != str(selected_type_akb[3])) or \
                (str((entry_lbl_type_terminal.get()).strip()) != str(selected_type_akb[4])) or (
                str((entry_type_size.get()).strip()) != str(selected_type_akb[5])) or \
                (str((entry_dop_info.get()).strip()) != str(selected_type_akb[6])) or (
                str(frame_values_type.status.get()) != str(("Вкл." if selected_type_akb[7] == 1 else 'Выкл.'))):

            params_duble = (
                selected_type_akb[10], selected_type_akb[1], [str(entry_capacity.get())][0], str(entry_volt.get()))
            # print(params_duble, 'PARAMS FOF SELECT DB-------------')

            res_duble = connect_BD.sql_select_typesakb_duble(params_duble)
            # print(res_duble, 'RESULT SELECT DB------------')

            # print('есть изменения')

            if res_duble == []:
                # текущее время
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # UPDATE typesakb SET capacity=?, volt=?, type_terminal=?, type_size=?, dop_info=?, status=?, data_create=?, user_id=?  WHERE type_id=?
                params = ([str(entry_capacity.get())][0], [str(entry_volt.get())][0],
                          [(entry_lbl_type_terminal.get()).strip()][0][0:20],
                          [(entry_type_size.get()).strip()][0][0:20], [(entry_dop_info.get()).strip()][0][0:50],
                          [1 if frame_values_type.status.get() == 'Вкл.' else 0][0], date_time, current_user[0][0],
                          selected_type_akb[10])
                # print(params, 'insert BD PARAMS-----------------')

                # - сохраняем в бд
                res = connect_BD.sql_update_typesakb(params)

                # - меняем новые значения в таблице
                if res:
                    tree.item(item_select, values=(
                        selected_type_akb[0], selected_type_akb[1], float(params[0]), float(params[1]), params[2],
                        params[3], params[4], params[5], current_user[0][2], date_time,
                        selected_type_akb[10]))

                    if str(frame_values_type.status.get()) == "Вкл.":
                        frame_values_type.status.set(status_on)
                        entry_select['text'] = ''
                        entry_select['fg'] = 'green'
                        entry_select['text'] = f"{entry_type.get()}\{entry_capacity.get()}Ah\{entry_volt.get()}V"
                    else:
                        frame_values_type.status.set(status_of)
                        entry_select['text'] = ''
                        entry_select['fg'] = 'red'
                        entry_select[
                            'text'] = f"{entry_type.get()}\{entry_capacity.get()}Ah\{entry_volt.get()}V - Выкл."

                    entry_create_name_type.configure(state='normal')
                    entry_create_name_type.delete(0, END)
                    entry_create_name_type.insert(0, selected_type_akb[8])
                    entry_create_name_type.configure(state='disabled')

                    entry_create_data_type.configure(state='normal')
                    entry_create_data_type.delete(0, END)
                    entry_create_data_type.insert(0, date_time)
                    entry_create_data_type.configure(state='disabled')

            else:
                messagebox.showwarning('Передупреждение',
                                       f"Невозможно выполнить.\nВозможно вы патаетесь изменить НА уже существующие\nзначения: тип АКБ, емкость, напряжение.")

        else:
            pass
            # print('нет изменений')

    btn_edit_type = ttk.Button(frame_values_type, text='Изменить', command=edit_value_type_akb)
    btn_edit_type.grid(row=3, columnspan=6, pady=(10, 10), sticky='e')

    btn_list_type_cancel = ttk.Button(wind_list_type_akb, text='Закрыть', command=lambda: dismiss(wind_list_type_akb))
    btn_list_type_cancel.grid(row=2, column=2, padx=(0, 10), pady=(0, 10), sticky='e')

    def OnClick(event):

        try:
            # - выборка данных из строки
            item_select = tree.selection()
            select_type = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только один тип.')
            return

        entry_type.configure(state='normal')
        entry_type.delete(0, END)
        entry_type.insert(0, select_type[1])
        entry_type.configure(state='disabled')

        entry_capacity.configure(state='normal')
        entry_capacity.delete(0, END)
        entry_capacity.insert(0, str(float(select_type[2])))
        entry_capacity.configure(state='readonly')

        entry_volt.configure(state='normal')
        entry_volt.delete(0, END)
        entry_volt.insert(0, str(float(select_type[3])))
        entry_volt.configure(state='readonly')

        if select_type[7] == 1:
            frame_values_type.status.set(status_on)
            entry_select['text'] = ''
            entry_select['fg'] = 'green'
            entry_select['text'] = f"{entry_type.get()}\\{entry_capacity.get()}Ah\\{entry_volt.get()}V"
        else:
            frame_values_type.status.set(status_of)
            entry_select['text'] = ''
            entry_select['fg'] = 'red'
            entry_select['text'] = f"{entry_type.get()}\\{entry_capacity.get()}Ah\\{entry_volt.get()}V - Выкл."

        entry_lbl_type_terminal.delete(0, END)
        entry_lbl_type_terminal.insert(0, select_type[4])

        entry_type_size.delete(0, END)
        entry_type_size.insert(0, select_type[5])

        entry_dop_info.delete(0, END)
        entry_dop_info.insert(0, select_type[6])

        entry_create_name_type.configure(state='normal')
        entry_create_name_type.delete(0, END)
        entry_create_name_type.insert(0, select_type[8])
        entry_create_name_type.configure(state='disabled')

        entry_create_data_type.configure(state='normal')
        entry_create_data_type.delete(0, END)
        entry_create_data_type.insert(0, select_type[9])
        entry_create_data_type.configure(state='disabled')

    tree.bind("<<TreeviewSelect>>", OnClick)
    frame_list_type_akb.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), columnspan=3)
    frame_values_type.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(0, 10), sticky=NSEW)

    wind_list_type_akb.grab_set()  # захватываем польз-льский ввод


def add_type_akb(wind_add_type_akb, combobox_klassif, select_capacity, spinbox_volt, entry_type_terminal, entry_size,
                 entry_info, status):
    # - удаляем пробелы
    entry_type_terminal = clear_text_strip(entry_type_terminal.get()[0:20])
    entry_type_terminal = entry_type_terminal if entry_type_terminal else 'н/д'
    entry_size = clear_text_strip(entry_size.get()[0:20])
    entry_size = entry_size if entry_size else 'н/д'
    entry_info = clear_text_strip(entry_info.get()[0:50])
    entry_info = entry_info if entry_info else 'н/д'

    status = 1 if status.get() == "Вкл." else 0

    params = (
        combobox_klassif.get(), select_capacity.get(), spinbox_volt.get(), entry_type_terminal, entry_size, entry_info,
        status, current_user[0][0])

    # добавляем тип в таблицу
    res = connect_BD.sql_insert_type_akb(params)

    if res:
        # - закрываем окно
        wind_add_type_akb.destroy()
        messagebox.showinfo('Информация', "Тип АКБ добавлен.")


def add_type_akb_form():
    if current_user[0][3] not in ('Админ',):  # "Supper_Admin_UPS",
        messagebox.showinfo('Информация', f"Пользователь с ролью '{current_user[0][3]}' не может добавить тип!")
    else:
        wind_add_type_akb = Toplevel(background='#999999', highlightbackground="#ccc",
                                     highlightthickness=0)  # width=255, height=365,
        wind_add_type_akb.protocol("WM_DELETE_WINDOW",
                                   lambda: dismiss(wind_add_type_akb))  # перехватываем нажатие на крестик
        wind_add_type_akb.attributes("-toolwindow", False)
        # wind_add_user.geometry('362x250')
        x = (wind_add_type_akb.winfo_screenwidth() - wind_add_type_akb.winfo_reqwidth()) / 2
        y = (wind_add_type_akb.winfo_screenheight() - wind_add_type_akb.winfo_reqheight()) / 2
        wind_add_type_akb.geometry("+%d+%d" % (x - 100, y - 210))
        wind_add_type_akb.title("Добавление типа АКБ")
        wind_add_type_akb.resizable(False, False)
        # wind_add_user['bg'] = '#ccc'

        frame_add_type = LabelFrame(wind_add_type_akb, padx=10, pady=10, text="Тип АКБ", font=('Arial', 11),
                                    highlightbackground="#ccc", highlightthickness=1)

        # - список классификаций АКБ
        klassif = ["Св.-кис.", "Св.-кис.(AGM)", "Св.-кис.(GEL)", "Ni-Cd", "Ni-MH", "Li-ion", "Другой"]
        # по умолчанию будет выбран последний элемент
        frame_add_type.klassif = StringVar(frame_add_type, value=klassif[1])

        lbl_type_akb = Label(frame_add_type, text="АКБ:", font=label_font)
        lbl_type_akb.grid(row=0, column=0, pady=(5, 5), sticky=E)

        label_klassif = ttk.Label(frame_add_type, font=font_header, textvariable=frame_add_type.klassif)
        label_klassif.grid(row=0, column=1)
        combobox_klassif = ttk.Combobox(frame_add_type, font=font_header, textvariable=frame_add_type.klassif,
                                        values=klassif, width=19,
                                        state="readonly")
        combobox_klassif.grid(row=0, pady=(5, 5), column=1, sticky='w')

        # по умолчанию будет выбран 7.5
        frame_add_type.select_сapacity = StringVar(frame_add_type, value='7.5')

        lbl_сapacity = Label(frame_add_type, text="Емкость(A/h):", font=label_font)
        lbl_сapacity.grid(row=1, column=0, pady=(5, 5), sticky=E)

        spinbox_сapacity = Spinbox(frame_add_type, font=font_header, textvariable=frame_add_type.select_сapacity,
                                   width=5, from_=1.0,
                                   to=130.0, increment=0.1, wrap=True, state="readonly")
        spinbox_сapacity.grid(row=1, column=1, ipady=1, pady=(5, 5), sticky=W)

        frame_add_type.select_volt = StringVar(frame_add_type, value='12.0')

        lbl_volt = Label(frame_add_type, text="Напряжение(V):", font=label_font)
        lbl_volt.grid(row=2, column=0, pady=(5, 5), sticky=E)

        spinbox_volt = Spinbox(frame_add_type, font=font_header, textvariable=frame_add_type.select_volt, width=5,
                               from_=1.0,
                               to=230.0, increment=0.1, wrap=True, state="readonly")
        spinbox_volt.grid(row=2, column=1, ipady=1, pady=(5, 5), sticky=W)

        lbl_type_terminal = Label(frame_add_type, text="Тип клемм:", font=font_header)
        lbl_type_terminal.grid(row=3, column=0, sticky=E)
        entry_type_terminal = Entry(frame_add_type, basic_style_entry_frame)
        entry_type_terminal.grid(row=3, column=1, pady=(5, 5), sticky=W)

        lbl_size = Label(frame_add_type, text="Типоразмер батареи:", font=font_header)
        lbl_size.grid(row=4, column=0, sticky=E)
        entry_size = Entry(frame_add_type, basic_style_entry_frame)
        entry_size.grid(row=4, column=1, pady=(5, 5), sticky=W)

        lbl_info = Label(frame_add_type, text="Доп. информация:", font=font_header)
        lbl_info.grid(row=5, column=0, sticky=E)
        entry_info = Entry(frame_add_type, basic_style_entry_frame)
        entry_info.grid(row=5, column=1, pady=(5, 5), sticky=W)

        # --- radiobutton
        status_on = "Вкл."
        status_of = "Выкл."

        frame_add_type.status = StringVar(frame_add_type,
                                          value=status_on)  # по умолчанию будет выбран элемент с value=status_on

        status_on_btn = ttk.Radiobutton(frame_add_type, text=status_on, variable=frame_add_type.status, value=status_on)
        status_on_btn.grid(row=6, column=1, sticky='w')

        status_of_btn = ttk.Radiobutton(frame_add_type, text=status_of, variable=frame_add_type.status, value=status_of)
        status_of_btn.grid(row=6, column=1, padx=(50, 0), sticky='w')

        btn_add_user = ttk.Button(wind_add_type_akb, text='Создать',
                                  command=lambda: add_type_akb(wind_add_type_akb, combobox_klassif,
                                                               frame_add_type.select_сapacity, spinbox_volt,
                                                               entry_type_terminal, entry_size, entry_info,
                                                               frame_add_type.status))
        btn_add_user.grid(row=1, column=0, padx=(0, 0), pady=(15, 10))

        btn_add_user_cancel = ttk.Button(wind_add_type_akb, text='Отмена', command=lambda: dismiss(wind_add_type_akb))
        btn_add_user_cancel.grid(row=1, column=0, padx=(0, 10), pady=(15, 10), sticky='e')

        frame_add_type.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))
        wind_add_type_akb.grab_set()  # захватываем польз-льский ввод


def add_depart(wind_add_depart, entry_name_depart, entry_name_depart_short, status):
    entry_name_depart = entry_name_depart.get()
    entry_name_depart_short = entry_name_depart_short.get()
    status = status.get()

    # - удаляем пробелы
    entry_name_depart = clear_text_strip(entry_name_depart)
    entry_name_depart_short = clear_text_strip(entry_name_depart_short)

    status = 1 if status == "Вкл." else 0

    if entry_name_depart and (1 < len(entry_name_depart) < 50) and is_data_text_fio(entry_name_depart):
        if entry_name_depart_short and len(entry_name_depart_short) < 15:

            # departments(name, short_name, status, id_user, data_create)
            # sql_insert_depart(params):
            params = (entry_name_depart, entry_name_depart_short, status, current_user[0][0])

            # добавляем пользователя в таблицу
            res = connect_BD.sql_insert_depart(params)

            # - закрываем окно
            wind_add_depart.destroy()

            if res:
                messagebox.showinfo('Информация', "Отделение добавлено.")

        else:
            messagebox.showinfo('Информация', "Короткое имя должно содержать до 15 символов\n(используется в отчётах)!")
    else:
        messagebox.showinfo('Информация', "Имя должно содержать 2-50 символов!")


def add_depart_form():
    if current_user[0][3] not in ('Админ',):  # "Supper_Admin_UPS",
        messagebox.showinfo('Информация', f"Пользователь с ролью '{current_user[0][3]}' не может добавить отделение!")
    else:
        wind_add_depart = Toplevel(background='#999999', highlightbackground="#ccc",
                                   highlightthickness=0)  # width=255, height=365,
        wind_add_depart.protocol("WM_DELETE_WINDOW",
                                 lambda: dismiss(wind_add_depart))  # перехватываем нажатие на крестик
        wind_add_depart.attributes("-toolwindow", False)
        # wind_add_user.geometry('362x250')
        x = (wind_add_depart.winfo_screenwidth() - wind_add_depart.winfo_reqwidth()) / 2
        y = (wind_add_depart.winfo_screenheight() - wind_add_depart.winfo_reqheight()) / 2
        wind_add_depart.geometry("+%d+%d" % (x - 100, y - 210))
        wind_add_depart.title("Добавление отделения")
        wind_add_depart.resizable(False, False)
        # wind_add_depart['bg'] = '#ccc'

        frame_add_depart = LabelFrame(wind_add_depart, padx=10, pady=10, text="Информация по отделению",
                                      font=('Arial', 11), highlightbackground="#ccc", highlightthickness=1)

        lbl_name_depart = Label(frame_add_depart, text="Наименование:", font=font_header)
        lbl_name_depart.grid(row=0, column=0, sticky=E)
        entry_name_depart = Entry(frame_add_depart, basic_style_entry_frame, background='#FDFBE1')
        entry_name_depart.grid(row=0, column=1, sticky=W)

        lbl_name_depart_short = Label(frame_add_depart, text="Короткое наимен.:", font=font_header)
        lbl_name_depart_short.grid(row=1, column=0, sticky=E)
        entry_name_depart_short = Entry(frame_add_depart, basic_style_entry_frame, background='#FDFBE1')
        entry_name_depart_short.grid(row=1, column=1, pady=(5, 5), sticky=W)

        status_on = "Вкл."
        status_of = "Выкл."

        frame_add_depart.status = StringVar(frame_add_depart,
                                            value=status_on)  # по умолчанию будет выбран элемент с value=status_on

        status_on_btn = ttk.Radiobutton(frame_add_depart, text=status_on, variable=frame_add_depart.status,
                                        value=status_on)
        status_on_btn.grid(row=3, column=1, sticky='w')

        status_of_btn = ttk.Radiobutton(frame_add_depart, text=status_of, variable=frame_add_depart.status,
                                        value=status_of)
        status_of_btn.grid(row=3, column=1, padx=(50, 0), sticky='w')

        btn_add_user = ttk.Button(wind_add_depart, text='Создать',
                                  command=lambda: add_depart(wind_add_depart, entry_name_depart,
                                                             entry_name_depart_short, frame_add_depart.status))
        btn_add_user.grid(row=1, column=0, padx=(0, 10), pady=(15, 10))

        btn_add_user_cancel = ttk.Button(wind_add_depart, text='Отмена', command=lambda: dismiss(wind_add_depart))
        btn_add_user_cancel.grid(row=1, column=0, padx=(0, 10), pady=(15, 10), sticky='e')
        frame_add_depart.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))
        wind_add_depart.grab_set()  # захватываем польз-льский ввод


def list_depart_form():
    wind_list_depart = Toplevel(background='#999999', highlightbackground="#ccc",
                                highlightthickness=0)  # width=800, height=500
    wind_list_depart.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_list_depart))  # перехватываем нажатие на крестик
    wind_list_depart.attributes("-toolwindow", False)
    # wind_list_user.geometry('790x460')
    x = (wind_list_depart.winfo_screenwidth() - wind_list_depart.winfo_reqwidth()) / 2
    y = (wind_list_depart.winfo_screenheight() - wind_list_depart.winfo_reqheight()) / 2
    wind_list_depart.geometry("+%d+%d" % (x - 230, y - 210))
    wind_list_depart.title("Список отделений")
    wind_list_depart.resizable(False, False)
    # wind_list_depart['bg'] = '#ccc'

    wind_list_depart.rowconfigure(0, weight=6)
    wind_list_depart.rowconfigure(1, weight=1)

    frame_list_depart = LabelFrame(wind_list_depart, text="Отделения", font=('Arial', 11), highlightbackground="#ccc",
                                   highlightthickness=1)

    # определяем данные для отображения ---------------------------------------------------------------------
    departs = connect_BD.sql_get_all_status_depart()
    departs_edit = []
    num = 1
    for dep in departs:
        departs_edit.append(tuple([num, dep[0], dep[1], dep[2], dep[3], dep[4], dep[5]]))
        num += 1

    # определяем столбцы
    columns = ("number", "name", "short_name", "status", "user", "data_create", 'id')

    tree = ttk.Treeview(frame_list_depart, columns=columns, show="headings")
    tree.grid(row=0, column=0)

    def sort(col, reverse):
        nonlocal tree
        # получаем все значения столбцов в виде отдельного списка
        lst = [(tree.set(k, col), k) for k in tree.get_children("")]
        # сортируем список
        lst.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(lst):
            tree.move(k, "", index)
        # в след. раз сортируем в обратном порядке
        tree.heading(col, command=lambda: sort(col, not reverse))

    # определяем заголовки с выпавниваем по левому краю
    tree.heading("number", text="#", anchor=E)
    tree.heading("name", text="Наименование", anchor=E, command=lambda: sort(1, False))
    tree.heading("short_name", text="Короткое наим.", anchor=E, command=lambda: sort(2, False))  # anchor='center'
    tree.heading("status", text="Вкл.\Выкл.", anchor=E, command=lambda: sort(3, False))
    tree.heading("user", text="Создал\Изменил", anchor=E, command=lambda: sort(4, False))
    tree.heading("data_create", text="Дата создания\изм.", anchor=E, command=lambda: sort(5, False))
    tree.heading("id", text="id", anchor=E)

    # настраиваем столбцы
    tree.column("#1", stretch=NO, anchor=E, width=30)
    tree.column("#2", stretch=NO, anchor=E, width=150)
    tree.column("#3", stretch=NO, anchor=E, width=150)  # anchor='center'
    tree.column("#4", stretch=NO, anchor=E, width=80)
    tree.column("#5", stretch=NO, anchor=E, width=120)
    tree.column("#6", stretch=NO, anchor=E, width=170)
    tree.column("#7", stretch=NO, anchor=E, width=0)  # 0 - скрыт

    # - отображаем указанные колонки
    tree['displaycolumns'] = ("number", "name", "short_name", "status", "user", "data_create", 'id')

    # добавляем данные
    for depart in departs_edit:
        tree.insert("", END, text=depart[2], values=depart)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(frame_list_depart, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # --------------------------------------------------------------------------
    frame_values_depart = LabelFrame(wind_list_depart, text="Свойства", font=('Arial', 11), highlightbackground="#ccc",
                                     highlightthickness=1)

    lbl_depart_name = Label(frame_values_depart, text="Наименование:", font=font_header)
    lbl_depart_name.grid(row=0, column=0, padx=[10, 0], sticky=E)
    entry_depart_name = Entry(frame_values_depart, basic_style_entry_frame)
    entry_depart_name.insert(0, '')
    entry_depart_name.configure(state='disabled')
    entry_depart_name.grid(row=0, column=1, pady=[5, 10], sticky=W)

    lbl_create_name = Label(frame_values_depart, text="Создал(изм.):", font=font_header)
    lbl_create_name.grid(row=0, column=2, padx=[10, 0], sticky=E)
    entry_create_name = Entry(frame_values_depart, basic_style_entry_frame)
    entry_create_name.insert(0, '')
    entry_create_name.configure(state='disabled')
    entry_create_name.grid(row=0, column=3, pady=[5, 10], sticky=W)

    lbl_short_name = Label(frame_values_depart, text="Короткое наим.:", font=font_header)
    lbl_short_name.grid(row=1, column=0, sticky=E)
    entry_short_name = Entry(frame_values_depart, basic_style_entry_frame)
    entry_short_name.insert(0, '')
    entry_short_name.grid(row=1, column=1, sticky=W)

    lbl_create_data = Label(frame_values_depart, text="Дата:", font=font_header)
    lbl_create_data.grid(row=1, column=2, sticky=E)
    entry_create_data = Entry(frame_values_depart, basic_style_entry_frame)
    entry_create_data.insert(0, '')
    entry_create_data.configure(state='disabled')
    entry_create_data.grid(row=1, column=3, sticky=W)

    # --- radiobutton
    status_on = "Вкл."
    status_of = "Выкл."

    frame_values_depart.status = StringVar(frame_values_depart, value=status_of)  # по умолчанию будет выбран элемент

    status_on_btn = ttk.Radiobutton(frame_values_depart, text=status_on, variable=frame_values_depart.status,
                                    value=status_on)
    status_on_btn.grid(row=2, column=1, pady=(5, 5), sticky='w')

    status_of_btn = ttk.Radiobutton(frame_values_depart, text=status_of, variable=frame_values_depart.status,
                                    value=status_of)
    status_of_btn.grid(row=2, column=1, pady=(5, 5), padx=(50, 0), sticky='w')

    def edit_value_depart():
        global current_user
        if current_user[0][3] not in ('Админ'):
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user[0][3]}' не может изменять!")
            return
        try:
            # выбираем данные из выделенного пользователя
            item_select = tree.selection()
            select_depart = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только одно отделение.')
            return

        if entry_short_name.get() and entry_depart_name.get():
            # - проверка были ли изменения в форме, если нет то выходим.
            if entry_short_name.get() != select_depart[2] or (
                    (1 if frame_values_depart.status.get() == 'Вкл.' else 0) != select_depart[3]):
                # - проверка на  корретность вода
                if (len(entry_short_name.get()) > 1) and (len(entry_short_name.get()) < 15):

                    # текущее время
                    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # '''UPDATE departments SET short_name=?, status=?, data_create=?, user_id=?  WHERE depart_id=?'''e=?'''
                    params = (
                        [(entry_short_name.get()).strip()][0],
                        [1 if frame_values_depart.status.get() == 'Вкл.' else 0][0],
                        date_time, current_user[0][0], select_depart[6])

                    # - сохраняем в бд
                    connect_BD.sql_update_depart(params)

                    # - меняем новые значения в таблице
                    tree.item(item_select, values=(
                        select_depart[0], select_depart[1], params[0], params[1], current_user[0][2], date_time,
                        select_depart[6]))

                    # изменяем значения в полях для просмотра
                    entry_create_name.configure(state='normal')
                    entry_create_name.delete(0, END)
                    entry_create_name.insert(0, current_user[0][2])
                    entry_create_name.configure(state='disabled')

                    entry_create_data.configure(state='normal')
                    entry_create_data.delete(0, END)
                    entry_create_data.insert(0, date_time)
                    entry_create_data.configure(state='disabled')

                else:
                    messagebox.showinfo('Информация',
                                        "Короткое наименование не должен быть пустым\nминимум: 2 смв.(используется в отчётах)!")

    btn_edit_depart = ttk.Button(frame_values_depart, text='Изменить', command=edit_value_depart)
    btn_edit_depart.grid(row=3, columnspan=4, pady=(0, 10), sticky='e')

    btn_list_depart_cancel = ttk.Button(wind_list_depart, text='Закрыть', command=lambda: dismiss(wind_list_depart))
    btn_list_depart_cancel.grid(row=2, column=2, padx=(0, 10), pady=(0, 10), sticky='e')

    def OnClick(event):
        try:
            # - выборка данных из строки
            item_select = tree.selection()
            select_depart = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только одно отделение.')
            return

        entry_depart_name.configure(state='normal')
        entry_depart_name.delete(0, END)
        entry_depart_name.insert(0, select_depart[1])
        entry_depart_name.configure(state='disabled')

        entry_create_name.configure(state='normal')
        entry_create_name.delete(0, END)
        entry_create_name.insert(0, select_depart[4])
        entry_create_name.configure(state='disabled')

        entry_create_data.configure(state='normal')
        entry_create_data.delete(0, END)
        entry_create_data.insert(0, select_depart[5])
        entry_create_data.configure(state='disabled')

        entry_short_name.delete(0, END)
        entry_short_name.insert(0, select_depart[2])

        if select_depart[3] == 1:
            frame_values_depart.status.set(status_on)
        else:
            frame_values_depart.status.set(status_of)

    tree.bind("<<TreeviewSelect>>", OnClick)
    frame_list_depart.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), columnspan=3)
    frame_values_depart.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(0, 10), ipadx=20, sticky=NSEW)

    wind_list_depart.grab_set()  # захватываем польз-льский ввод


def is_data_int(data):
    if data is False: return False
    if data.strip():
        if data.isdigit():
            return True
        else:
            return False
    else:
        return False


def list_user_form():
    wind_list_user = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
    wind_list_user.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_list_user))  # перехватываем нажатие на крестик
    wind_list_user.attributes("-toolwindow", False)
    # wind_list_user.geometry('790x460')
    x = (wind_list_user.winfo_screenwidth() - wind_list_user.winfo_reqwidth()) / 2
    y = (wind_list_user.winfo_screenheight() - wind_list_user.winfo_reqheight()) / 2
    wind_list_user.geometry("+%d+%d" % (x - 250, y - 210))
    wind_list_user.title("Список пользователей")
    wind_list_user.resizable(False, False)
    # wind_list_user['bg'] = '#ccc'

    wind_list_user.rowconfigure(0, weight=6)
    wind_list_user.rowconfigure(1, weight=1)

    frame_list_user = LabelFrame(wind_list_user, text="Все пользователи", font=('Arial', 11),
                                 highlightbackground="#ccc", highlightthickness=1)

    # определяем данные для отображения ---------------------------------------------------------------------
    users = connect_BD.sql_get_all_status_users()
    users_edit = []
    num = 1
    for dep in users:
        users_edit.append(tuple([dep[0], num, dep[1], dep[2], dep[3], dep[4], dep[5]]))
        num += 1

    # определяем столбцы
    columns = ("id", "number", "tab_num", "fio", "status", "role", "data_create")

    tree = ttk.Treeview(frame_list_user, columns=columns, show="headings")

    tree.grid(row=0, column=0)

    def sort(col, reverse):
        nonlocal tree
        # получаем все значения столбцов в виде отдельного списка
        lst = [(tree.set(k, col), k) for k in tree.get_children("")]
        # сортируем список
        lst.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(lst):
            tree.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        tree.heading(col, command=lambda: sort(col, not reverse))

    # определяем заголовки с выпавниваем по левому краю
    tree.heading("id", text="id", anchor=E)
    tree.heading("number", text="#", anchor=E)
    tree.heading("tab_num", text="Табельный №", anchor=E, command=lambda: sort(2, False))
    tree.heading("fio", text="ФИО", anchor='center', command=lambda: sort(3, False))
    tree.heading("status", text="Вкл.\Выкл.", anchor=E, command=lambda: sort(4, False))
    tree.heading("role", text="Роль", anchor=E, command=lambda: sort(5, False))
    tree.heading("data_create", text="Дата создания", anchor=E, command=lambda: sort(6, False))

    # настраиваем столбцы
    tree.column("#1", stretch=NO, anchor=E, width=30)
    tree.column("#2", stretch=NO, anchor=E, width=30)
    tree.column("#3", stretch=NO, anchor=E, width=120)
    tree.column("#4", stretch=NO, anchor=E, width=150)
    tree.column("#5", stretch=NO, anchor=E, width=80)
    tree.column("#6", stretch=NO, anchor=E, width=130)
    tree.column("#7", stretch=NO, anchor=E, width=170)

    # - отображаем указанные колонки
    tree['displaycolumns'] = ("number", "tab_num", "fio", "status", "role", "data_create")

    # добавляем данные
    for user in users_edit:
        tree.insert("", END, values=user)

    # добавляем вертикальную прокрутку
    scrollbar = ttk.Scrollbar(frame_list_user, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # ------------------------------------------------------------------------------

    frame_values_user = LabelFrame(wind_list_user, text="Свойства", font=('Arial', 11), highlightbackground="#ccc",
                                   highlightthickness=1)
    # кортежи и словари, содержащие настройки шрифтов
    # font_header = ('Arial', 11)

    lbl_tab_num = Label(frame_values_user, text="Табельный номер:", font=font_header)
    lbl_tab_num.grid(row=1, column=0, padx=(10, 0), sticky=E)
    entry_tab_num = Entry(frame_values_user, basic_style_entry_frame)
    entry_tab_num.insert(0, '')
    entry_tab_num.configure(state='disabled')
    entry_tab_num.grid(row=1, column=1, pady=(10, 10), sticky=W)

    lbl_fio = Label(frame_values_user, text="ФИО:", font=font_header)
    lbl_fio.grid(row=2, column=0, sticky=E)
    entry_fio = Entry(frame_values_user, basic_style_entry_frame)
    entry_fio.insert(0, '')
    entry_fio.grid(row=2, column=1, sticky=W)

    # --- radiobutton
    status_on = "Вкл."
    status_of = "Выкл."

    frame_values_user.status = StringVar(frame_values_user,
                                         value=status_on)  # по умолчанию будет выбран элемент с value=status_on

    status_on_btn = ttk.Radiobutton(frame_values_user, text=status_on, variable=frame_values_user.status,
                                    value=status_on)
    status_on_btn.grid(row=3, column=1, pady=(5, 5), sticky='w')

    status_of_btn = ttk.Radiobutton(frame_values_user, text=status_of, variable=frame_values_user.status,
                                    value=status_of)
    status_of_btn.grid(row=3, column=1, padx=(50, 0), sticky='w')
    # print(frame_add_user.status.get())

    # - список ролей
    roles = ["Админ", "Meнеджер", "Просмотрщик"]
    # по умолчанию будет выбран последний элемент
    frame_values_user.role = StringVar(frame_values_user, value=roles[2])

    label_role = ttk.Label(frame_values_user, font=font_header, textvariable=frame_values_user.role)
    label_role.grid(row=4, column=1)
    combobox = ttk.Combobox(frame_values_user, font=font_header, textvariable=frame_values_user.role, values=roles,
                            state="readonly",
                            width=17)
    combobox.grid(row=4, column=1, sticky='w')

    def edit_value_user():
        global current_user
        if current_user[0][3] not in ("Supper_Admin_UPS", 'Админ'):
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user[0][3]}' не может изменять!")
            return

        try:
            # выбираем данные из выделенного пользователя
            item_select = tree.selection()
            select_user = tree.item(item_select)['values']
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только одного пользователя.')
            return

        if entry_tab_num.get():
            if entry_fio.get():
                # - проверка были ли изменения в форме, если нет то выходим.
                if entry_fio.get() == select_user[3] and (
                        (1 if frame_values_user.status.get() == 'Вкл.' else 0) == select_user[4]) and (
                        frame_values_user.role.get() == select_user[5]):
                    return
                # - проверка на  корретность вода
                if is_data_text_fio(entry_fio.get()) and (
                        (len(entry_fio.get()) > 5 and len(entry_fio.get()) < 25)) and (
                        (((entry_fio.get()).replace('.', '')).replace(' ', '')).isalpha()):
                    params = ([(entry_fio.get()).strip()][0], [1 if frame_values_user.status.get() == 'Вкл.' else 0][0],
                              [frame_values_user.role.get()][0], [entry_tab_num.get()][0])

                    # - сохраняем в бд
                    connect_BD.sql_update_user(params)

                    # - меняем новые значения в таблице
                    tree.item(item_select, values=(
                        select_user[0], select_user[1], select_user[2], params[0], params[1], params[2],
                        select_user[6]))

                else:
                    messagebox.showinfo('Информация',
                                        "ФИО не должен быть пустым(мин:6 смв.),\nналичие спецсимволов не допускается!")

            else:
                messagebox.showwarning('Предупреждение',
                                       "ФИО не должен быть пустым(мин:6 смв.),\nналичие спецсимволов не допускается!")

        else:
            return

    btn_user_reset_pass = ttk.Button(frame_values_user, text='Изменить', command=edit_value_user)
    btn_user_reset_pass.grid(row=5, column=1, pady=(10, 10), sticky='w')

    # ---смена пароля ----------------------------------------
    frame_values_user_reset_password = LabelFrame(wind_list_user, text="Смена пароля ", font=('Arial', 11),
                                                  highlightbackground="#ccc", highlightthickness=1)
    # кортежи и словари, содержащие настройки шрифтов
    # font_header = ('Arial', 11)

    lbl_fio_pass = Label(frame_values_user_reset_password, text="Для пользователя:", font=font_header)
    lbl_fio_pass.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
    entry_tab_pass = Entry(frame_values_user_reset_password, basic_style_entry_frame)
    entry_tab_pass.insert(0, '')
    entry_tab_pass.configure(state='disabled')
    entry_tab_pass.grid(row=0, column=1, pady=(10, 0), sticky=E)

    lbl_pass_new = Label(frame_values_user_reset_password, text="Введите пароль:", font=font_header)
    lbl_pass_new.grid(row=1, column=0, pady=[10, 0], sticky=E)
    entry_pass_new = Entry(frame_values_user_reset_password, basic_style_entry_frame, show='*')
    entry_pass_new.insert(0, '')
    entry_pass_new.grid(row=1, column=1, pady=[10, 0], sticky=E)

    def reset_password():
        if current_user[0][3] in ("Supper_Admin_UPS", 'Админ'):
            if entry_tab_pass.get():
                if entry_pass_new.get() and len(entry_pass_new.get()) > 5:
                    params_passw_reset = (
                        (hashlib.md5(((entry_pass_new.get()).strip()).encode('utf-8')).hexdigest()),
                        entry_tab_pass.get())
                    connect_BD.sql_reset_password(params_passw_reset)
                    entry_pass_new.delete(0, END)
                    messagebox.showinfo('Информация', "Пароль изменён!")

                else:
                    messagebox.showinfo('Информация', "Пароль не должен быть пустым\nи содержать не менее 6 символов!")
            else:
                return
        else:
            messagebox.showinfo('Информация', "У вас недостаточно прав \nдля для выполнения этой операциии!")

    btn_user_reset_pass = ttk.Button(frame_values_user_reset_password, text='Сменить', command=reset_password)
    btn_user_reset_pass.grid(row=2, column=1, pady=[10, 0], sticky='e')

    btn_list_user_cancel = ttk.Button(wind_list_user, text='Закрыть', command=lambda: dismiss(wind_list_user))
    btn_list_user_cancel.grid(row=3, column=1, padx=[0, 10], pady=[0, 10], sticky='e')

    def OnClick(event):
        try:
            # зоголовки тоже обрабатываем(выбираются этим методом) см. ниже 1
            item_select = tree.selection()
            select_user = tree.item(item_select)['values']
            ####---------select_user = tree.item(item_select)['values']
            # tab_num1 = tree.item(item_select)['values'][1]
        except Exception:
            messagebox.showinfo('Информация', 'Выберите только одного пользователя.')
            return

        entry_tab_num.configure(state='normal')
        entry_tab_num.delete(0, END)
        entry_tab_num.insert(0, select_user[2])
        entry_tab_num.configure(state='disabled')

        # -- для смены пароля
        entry_tab_pass.configure(state='normal')
        entry_tab_pass.delete(0, END)
        entry_tab_pass.insert(0, select_user[2])
        entry_tab_pass.configure(state='disabled')

        entry_fio.delete(0, END)
        entry_fio.insert(0, select_user[3])

        if select_user[4] == 1:
            frame_values_user.status.set(status_on)
        else:
            frame_values_user.status.set(status_of)

        # - установка роли
        frame_values_user.role.set(select_user[5])

    # frame_list_user.focus_set()
    # tree.bind("<ButtonRelease-1>", OnDoubleClick)
    tree.bind("<<TreeviewSelect>>", OnClick)
    frame_list_user.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), columnspan=2)
    frame_values_user.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), ipadx=20, sticky=NSEW)
    frame_values_user_reset_password.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), ipadx=20, sticky=NSEW)

    wind_list_user.grab_set()  # захватываем польз-льский ввод


def add_user(wind_add_user, tab_num, password, fio, status, role):
    entry_tab_num = tab_num.get()
    entry_password = password.get()
    entry_fio = fio.get()
    status = status.get()
    role = role.get()
    # - удаляем пробелы
    entry_tab_num = clear_text_strip(entry_tab_num)
    entry_password = clear_text_strip(entry_password)
    entry_fio = clear_text_strip(entry_fio)

    status = 1 if status == "Вкл." else 0

    if is_data_int(entry_tab_num) and (len(entry_tab_num) == 6):
        if entry_password and len(entry_password) > 5:
            if is_data_text_fio(entry_fio) and (len(entry_fio) > 5) and (
                    ((entry_fio.replace('.', '')).replace(' ', '')).isalpha()):

                password_hash_user = (hashlib.md5((entry_password.strip()).encode('utf-8')).hexdigest())

                # users(tab_num, pass,  fio, status, role, data_create)
                params = (entry_tab_num, password_hash_user, entry_fio, status, role)

                # добавляем пользователя в таблицу
                res = connect_BD.sql_insert_user(params)

                # - закрываем окно
                wind_add_user.destroy()

                if res:
                    messagebox.showinfo('Информация', "Пользователь добавлен.")

            else:
                messagebox.showinfo('Информация', "Наличие спецсимволов не допускается!")
        else:
            messagebox.showinfo('Информация', "Пароль должен содержать не менее 6 символов!")
    else:
        messagebox.showinfo('Информация', "Табельный номер должен содержать только 6 цифр!")


def add_user_form():
    if current_user[0][3] not in ("Supper_Admin_UPS", 'Админ'):
        messagebox.showinfo('Информация',
                            f"Пользователь с ролью '{current_user[0][3]}' не может добавлять пользователей!")
    else:
        wind_add_user = Toplevel(background='#999999', highlightbackground="#ccc", highlightthickness=0)
        wind_add_user.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_add_user))  # перехватываем нажатие на крестик
        wind_add_user.attributes("-toolwindow", False)
        # wind_add_user.geometry('362x250')
        x = (wind_add_user.winfo_screenwidth() - wind_add_user.winfo_reqwidth()) / 2
        y = (wind_add_user.winfo_screenheight() - wind_add_user.winfo_reqheight()) / 2
        wind_add_user.geometry("+%d+%d" % (x - 100, y - 210))
        wind_add_user.title("Добавление пользователя")
        wind_add_user.resizable(False, False)
        # wind_add_user['bg'] = '#ccc'

        frame_add_user = LabelFrame(wind_add_user, padx=10, pady=10, text="Персональная информация", font=('Arial', 11),
                                    highlightbackground="#ccc", highlightthickness=0)

        # кортежи и словари, содержащие настройки шрифтов
        # font_header = ('Arial', 10)

        lbl_tab_num = Label(frame_add_user, text="Табельный номер:", font=font_header)
        lbl_tab_num.grid(row=0, column=0, sticky=E)
        entry_tab_num = Entry(frame_add_user, basic_style_entry_frame, background='#FDFBE1')
        entry_tab_num.grid(row=0, column=1, sticky=W)

        lbl_password = Label(frame_add_user, text="Пароль:", font=font_header)
        lbl_password.grid(row=1, column=0, sticky=E)
        entry_password = Entry(frame_add_user, basic_style_entry_frame, show="*", background='#FDFBE1')
        entry_password.grid(row=1, column=1, pady=(5, 5), sticky=W)

        lbl_fio = Label(frame_add_user, text="ФИО:", font=font_header)
        lbl_fio.grid(row=2, column=0, sticky=E)
        entry_fio = Entry(frame_add_user, basic_style_entry_frame, background='#FDFBE1')
        entry_fio.grid(row=2, column=1, sticky=W)

        # --- radiobutton
        status_on = "Вкл."
        status_of = "Выкл."

        frame_add_user.status = StringVar(frame_add_user,
                                          value=status_on)  # по умолчанию будет выбран элемент с value=status_on

        status_on_btn = ttk.Radiobutton(frame_add_user, text=status_on, variable=frame_add_user.status, value=status_on)
        status_on_btn.grid(row=3, column=1, pady=(5, 5), sticky='w')

        status_of_btn = ttk.Radiobutton(frame_add_user, text=status_of, variable=frame_add_user.status, value=status_of)
        status_of_btn.grid(row=3, column=1, pady=(5, 5), padx=[50, 0], sticky='w')

        # - список ролей
        roles = ["Админ", "Meнеджер", "Просмотрщик"]
        # по умолчанию будет выбран последний элемент
        frame_add_user.role = StringVar(frame_add_user, value=roles[2])

        label_role = ttk.Label(frame_add_user, font=font_header, textvariable=frame_add_user.role)
        label_role.grid(row=4, column=1)
        combobox = ttk.Combobox(frame_add_user, font=font_header, textvariable=frame_add_user.role, values=roles,
                                state="readonly")
        combobox.grid(row=4, column=1, sticky='w')

        btn_add_user = ttk.Button(wind_add_user, text='Создать',
                                  command=lambda: add_user(wind_add_user, entry_tab_num, entry_password, entry_fio,
                                                           frame_add_user.status, combobox))
        btn_add_user.grid(row=1, column=0, padx=(0, 0), pady=(15, 10))

        btn_add_user_cancel = ttk.Button(wind_add_user, text='Отмена', command=lambda: dismiss(wind_add_user))
        btn_add_user_cancel.grid(row=1, column=0, padx=(0, 10), pady=(15, 10), sticky='e')

        frame_add_user.grid(row=0, column=0, padx=(10, 10), pady=(20, 0))
        wind_add_user.grab_set()  # захватываем польз-льский ввод


def main_window(window, current_user_avtoriz=None):  # -----for сведения
    global current_user, basic_style_lab_frame, basic_style_bottom, all_ups_count_global, all_no_work_count_global, all_replace_element_ups_count_global, all_repair_count_global
    current_user = current_user_avtoriz

    # --Глобальные стили----------
    style = ttk.Style()
    style.theme_use('winnative')

    label_style = ttk.Style()
    label_style.configure("My_label_style.TLabel", font="helvetica 14")

    # удаление всех виджетов главного окна
    for el in window.winfo_children():
        el.destroy()

    window.title('Учёт ИБП  -=ITPetrikov=-')
    # на весь экран
    window.state('zoomed')
    window.geometry("700x500+50+50")
    window.minsize(1920, 1010)
    # window.overrideredirect(1)
    window.attributes("-toolwindow", False)
    window.resizable(1, 1)

    window.columnconfigure(0, minsize=200, weight=3, pad=5)
    window.columnconfigure(1, weight=7)
    # window.columnconfigure(2, weight=1)

    window.rowconfigure(0, weight=2)
    window.rowconfigure(1, weight=6)  # change weight to 4
    window.rowconfigure(2, weight=1)

    frame_top = Frame(window, bg='#ccc')  # bg='dim grey'
    frame_middle = Frame(window, bg='#ccc')  # bg='grey46'
    frame_bottom = Frame(window, bg='#ccc')  # bg='grey'

    # разбиваем прямо в центре на две строки
    # frame_middle.rowconfigure(0, weight=7)
    # frame_middle.rowconfigure(1, weight=3)

    frame_left = Frame(window, bg='#ccc', highlightbackground="seashell4", highlightthickness=1)

    label_name = Label(frame_left, text='ИБП', font=('Verdana', 30, 'bold'), background='#ccc', fg='#0078D7')
    label_name.grid(row=0, column=0, pady=(1, 0))

    label_name_2 = Label(frame_left, text='-=учёт=-', font=('Arial', 11, 'bold'), background='#ccc', fg='green')
    label_name_2.grid(row=0, column=0, pady=(67, 0))

    # basic_style_bottom = {'background': '#ccc', 'foreground': '#004D40', 'font': 'Helvetica 10'}
    # basic_style_lab_frame = {'background': '#ccc', 'foreground': 'dark slate gray', 'font': 'Helvetica 10 bold'}

    # ----- left ----Frame---------------
    # для ибп --------------------------

    def update_and_show_main_treeview():

        # - изменяем цвет статусных радиокнопок по умолчанию
        radiobutton_on_off_style.configure("My_radbut_Reset.TRadiobutton",  # имя стиля
                                           font="helvetica 11",  # шрифт
                                           foreground="#004D59",  # цвет текста 004D40
                                           padding=(1, 5, 2, 0),  # отступы
                                           background="#B5BFC7")  # фоновый цвет#E8E802
        radiobutton_on_off_style.map("My_radbut1.TRadiobutton", background=[('active', 'yellow')])  # 90D3F9

        status_on_btn_work.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_work.configure(style='My_radbut_Reset.TRadiobutton')
        status_on_btn_replace.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_replace.configure(style='My_radbut_Reset.TRadiobutton')
        status_on_btn_repair.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_repair.configure(style='My_radbut_Reset.TRadiobutton')

        # - поиск и показ всех
        show_main_treeview(ups=None, flag_clear_values_ups=True)

    button_style = ttk.Style()
    button_style.configure("My_buttom_style.TButton",  # имя стиля
                           font="helvetica 11",  # шрифт
                           foreground="#004D59",  # цвет текста 004D40
                           padding=(1, 3, 1, 3),  # отступы
                           background="#B5BFC7")  # фоновый цвет#E8E802
    button_style.map("My_buttom_style.TButton", background=[('active', 'green')])  # 90D3F9
    button_style.map("My_buttom_style.TButton", foreground=[('active', '#1B231C')])  # 90D3F9

    labelframe_IPB = LabelFrame(frame_left, basic_style_lab_frame, text="ИБП", font='Arial 11 bold')
    buttom_all_list_ipb = ttk.Button(labelframe_IPB, text='Обновить список ИБП', command=update_and_show_main_treeview,
                                     style="My_buttom_style.TButton")
    buttom_all_list_ipb.grid(row=0, column=0, padx=5, pady=(10, 2), ipadx=5, ipady=5, sticky='nsew')

    buttom_create_ipb = ttk.Button(labelframe_IPB, text='Добавить ИБП', command=add_ups_form,
                                   style="My_buttom_style.TButton")
    buttom_create_ipb.grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky='nsew')
    # -- end

    # для моделей ибп --------------------------
    labelframe_Model = LabelFrame(frame_left, basic_style_lab_frame, text="Модели ИБП", font='Arial 11 bold')
    buttom_all_list_model = ttk.Button(labelframe_Model, text='Список моделей ', command=list_model_form,
                                       style="My_buttom_style.TButton")
    buttom_all_list_model.grid(row=0, column=0, padx=5, pady=(10, 2), ipadx=5, ipady=5, sticky='nsew')

    buttom_create_model = ttk.Button(labelframe_Model, text='  Добавить модель    ', command=add_model_form,
                                     style="My_buttom_style.TButton")
    buttom_create_model.grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky='nsew')
    # -- end

    # для моделей АКБ --------------------------
    labelframe_Akb = LabelFrame(frame_left, basic_style_lab_frame, text="Типы АКБ", font='Arial 11 bold')
    buttom_all_list_akb = ttk.Button(labelframe_Akb, text='Список типов', command=list_type_akb,
                                     style="My_buttom_style.TButton")
    buttom_all_list_akb.grid(row=0, column=0, padx=5, pady=(10, 2), ipadx=5, ipady=5, sticky='nsew')

    buttom_create_akb = ttk.Button(labelframe_Akb, text='       Добавить тип      ',
                                   command=add_type_akb_form, style="My_buttom_style.TButton")
    buttom_create_akb.grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky='nsew')
    # -- end АКБ

    # для Отделений
    labelframe_Otdelenia = LabelFrame(frame_left, basic_style_lab_frame, text="Отделения", font='Arial 11 bold')
    buttom_all_list_otdel = ttk.Button(labelframe_Otdelenia, text='Список отделений',
                                       command=list_depart_form, style="My_buttom_style.TButton")
    buttom_all_list_otdel.grid(row=0, column=0, padx=5, pady=(10, 2), ipadx=5, ipady=5, sticky='nsew')

    buttom_create_otdel = ttk.Button(labelframe_Otdelenia, text=' Добавить отделение',
                                     command=add_depart_form, style="My_buttom_style.TButton")
    buttom_create_otdel.grid(row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky='nsew')
    # -- end отделения

    # для Пользователей
    labelframe_User = LabelFrame(frame_left, basic_style_lab_frame, text="Пользователи", font='Arial 11 bold')
    buttom_all_list_user = ttk.Button(labelframe_User, text='Список польз-телей', command=list_user_form,
                                      style="My_buttom_style.TButton")
    buttom_all_list_user.grid(row=0, column=0, padx=5, pady=(10, 2), ipadx=5, ipady=5, sticky='nsew')

    buttom_create_user = ttk.Button(labelframe_User, text='Добавить польз-теля', command=add_user_form,
                                    style="My_buttom_style.TButton")
    buttom_create_user.grid(row=1, column=0, padx=5, pady=(2, 10), ipadx=5, ipady=5, sticky='nsew')
    # -- end

    # для Отчетов
    labelframe_Raport = LabelFrame(frame_left, basic_style_lab_frame, text="Отчёты", font='Arial 11 bold')
    buttom_otdel_raport = ttk.Button(labelframe_Raport, text='      По состоянию      ',
                                     command=create_raport_on_select, style="My_buttom_style.TButton")
    buttom_otdel_raport.grid(row=0, column=0, padx=5, pady=(10, 0), ipadx=5, ipady=5, sticky='nsew')

    def show_info():
        wind_info = Toplevel()
        wind_info.protocol("WM_DELETE_WINDOW", lambda: dismiss(wind_info))  # перехватываем нажатие на крестик
        wind_info.attributes("-toolwindow", False)
        # wind_add_user.geometry('362x250')
        x = (wind_info.winfo_screenwidth() - wind_info.winfo_reqwidth()) / 2
        y = (wind_info.winfo_screenheight() - wind_info.winfo_reqheight()) / 2
        wind_info.geometry("+%d+%d" % (x - 100, y - 210))
        wind_info.title("О программе")
        wind_info.resizable(False, False)

        frame_show_info = LabelFrame(wind_info, padx=2, pady=2, text="Инфо", font=('Arial', 10),
                                     highlightbackground="#F0F0F0", highlightthickness=0)

        labl_info = Label(frame_show_info,
                          text='Program: Учёт ИБП, v.1.0  2024  \nDeveloper: Dudko Mikhail\nDesigned for: Petrikov, Republic Belarus \ Lic. key 775i \nDeveloper contact: promsoft-1@ya.ru\n  \n© 2024 Dudko Mikhail All Rights Reserved')
        labl_info.grid(row=0, column=0)

        frame_show_info.grid(row=0, column=0, padx=(10, 10), pady=(20, 10))
        wind_info.grab_set()  # захватываем польз-льский ввод

    buttom_abount_programm = ttk.Button(frame_left, text='  О программе  ', command=show_info)
    buttom_abount_programm.grid(row=7, column=0, padx=(19, 10), pady=(20, 0))

    # ------------------------------------------------------------
    # --------End----------------left---------frame---------------

    # для top +--------------------------------
    labelframe_top = LabelFrame(frame_top, basic_style_lab_frame, text="Поиск ИБП", relief=GROOVE, bg="#ccc",
                                font='Arial 10 bold')  # basic_style_lab_frame,

    # style = ttk.Style()
    # ttk.Style().configure(".", font="helvetica 17", foreground="#004D40", padding=1, background="#B2DFDB")
    # tyle.configure("TLabel", font="helvetica 15", foreground="#004D40", padding=1, background="#90D3F9")

    # -------------------SELECT----DEPART---------------
    depart_select_id = 0

    def select_depart_id(event):
        nonlocal depart_select_id
        selection = combobox_depart.get()
        if result_sql_departs:
            for val in result_sql_departs:
                if str(selection) == str(val[1]):
                    depart_select_id = val[0]
                    break

        # print(id_depart_select, 'id_depart_select')

    sql = "SELECT depart_id, short_name  FROM departments   ORDER BY  short_name;"
    result_sql_departs = connect_BD.sql_get_data(sql)

    only_departs_list = []
    if result_sql_departs:
        only_departs_list.extend(x[1] for x in result_sql_departs)

    # изначально с в списке пустое значение,
    # по умолчанию будет выбран  пустой элемент
    labelframe_top.select_depart = StringVar(labelframe_top, value='')

    # для установки отделения в поиск после добавления
    global select_depart_global
    select_depart_global = labelframe_top.select_depart

    lbl_depart = Label(labelframe_top, basic_style_lab_frame, text="Отделение:")  # style='My_label_style.TLabel'
    lbl_depart.grid(row=0, column=0, padx=(30, 0), pady=(20, 5), sticky=E)

    combobox_depart = ttk.Combobox(labelframe_top, width=23, textvariable=labelframe_top.select_depart,
                                   values=only_departs_list, background='#FDFBE1', state="readonly")
    combobox_depart.grid(row=0, column=1, pady=(20, 5), sticky=W)
    combobox_depart.bind("<<ComboboxSelected>>", select_depart_id)

    # -------------------SELECT----MODEL-----UPS------------
    model_select_id = 0

    def selected_model(event):
        nonlocal model_select_id
        selection_model = combobox_model.get()
        if res_sql_models:
            for val in res_sql_models:
                if str(selection_model) == str(val[1]):
                    model_select_id = val[0]
                    break

        # print(id_model_select, 'id_model_select')

    sql = "SELECT model_id, short_name FROM models ORDER BY  short_name;"
    res_sql_models = connect_BD.sql_get_data(sql)
    # res_sql_models = connect_BD.sql_get_all_status_model()

    only_models_list = []
    if res_sql_models:
        only_models_list.extend(x[1] for x in res_sql_models)

    # изначально в списке пустое значение
    # по умолчанию будет выбран  пустой элемент
    labelframe_top.select_model = StringVar(labelframe_top, value='')

    lbl_model = Label(labelframe_top, basic_style_lab_frame, text="Модель:")
    lbl_model.grid(row=1, column=0, pady=(5, 5), sticky=E)

    combobox_model = ttk.Combobox(labelframe_top, width=23, textvariable=labelframe_top.select_model,
                                  values=only_models_list, background='#FDFBE1', state="readonly")
    combobox_model.grid(row=1, column=1, pady=(5, 5), sticky=W)
    combobox_model.bind("<<ComboboxSelected>>", selected_model)

    item_number = StringVar(labelframe_top, value='')
    label_item_number = Label(labelframe_top, basic_style_lab_frame, text="Инв.\номенкл. №:")
    label_item_number.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky=E)
    entry_item_number = ttk.Entry(labelframe_top, textvariable=item_number, width=15)
    entry_item_number.grid(row=0, column=3, padx=(2, 0), pady=(20, 0), sticky=W)

    lbl_count_search = Label(labelframe_top, basic_style_lab_frame, text="Отображать по:")
    lbl_count_search.grid(row=1, column=2, pady=(5, 5), sticky=NE)

    labelframe_top.select_count_main_element = StringVar(labelframe_top, value=250)

    spinbox_count_ups = ttk.Spinbox(labelframe_top, width=3,
                                    textvariable=labelframe_top.select_count_main_element, from_=50, to=1000,
                                    increment=50,
                                    wrap=True, state="readonly")
    spinbox_count_ups.grid(row=1, column=3, ipady=1, pady=(5, 5), sticky=NW)

    check_style = ttk.Style()
    check_style.configure("My_check.TCheckbutton",  # имя стиля
                          font="helvetica 11",  # шрифт
                          foreground="#004D40",  # цвет текста
                          padding=(1, 5, 2, 0),  # отступы
                          background="#ccc")  # фоновый цвет
    check_style.map("My_check.TCheckbutton", background=[("active", "darkgrey")])

    ttk.Style().configure("TCheckbutton", font="helvetica 8", foreground="#004D40", padding=8, background="#B2DFDB")

    enabled_is_replace = IntVar()

    checkbutton_is_replace = ttk.Checkbutton(labelframe_top, text="Требуется замена АКБ        ",
                                             variable=enabled_is_replace, style="My_check.TCheckbutton")
    checkbutton_is_replace.grid(row=0, column=4, padx=(30, 0), pady=(12, 0), sticky='we')

    enabled_is_repair = IntVar()

    checkbutton_is_repair = ttk.Checkbutton(labelframe_top, text="В ремонте", variable=enabled_is_repair,
                                            style="My_check.TCheckbutton")
    checkbutton_is_repair.grid(row=1, column=4, padx=(30, 0), sticky='we')

    def clear_status_rediobuttom():
        # - изменяем цвет статусных радиокнопок по умолчанию
        radiobutton_on_off_style.configure("My_radbut_Reset.TRadiobutton",  # имя стиля
                                           font="helvetica 11",  # шрифт
                                           foreground="#004D59",  # цвет текста 004D40
                                           padding=(1, 5, 2, 0),  # отступы
                                           background="#B5BFC7")  # фоновый цвет#E8E802
        radiobutton_on_off_style.map("My_radbut1.TRadiobutton", background=[('active', 'yellow')])  # 90D3F9

        status_on_btn_work.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_work.configure(style='My_radbut_Reset.TRadiobutton')
        status_on_btn_replace.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_replace.configure(style='My_radbut_Reset.TRadiobutton')
        status_on_btn_repair.configure(style='My_radbut_Reset.TRadiobutton')
        status_of_btn_repair.configure(style='My_radbut_Reset.TRadiobutton')

    def reset_entry_depart_model():
        nonlocal depart_select_id, model_select_id, entry_item_number, enabled_is_replace, enabled_is_repair

        # - -- если пусты значения значит не чистим
        if (depart_select_id == 0 or (not depart_select_id)) and (model_select_id == 0 or (not model_select_id)):
            if not (bool(entry_item_number.get())):
                if not (bool(enabled_is_replace.get())) and (not (bool(enabled_is_repair.get()))):
                    return

        labelframe_top.select_depart.set('')
        depart_select_id = False
        labelframe_top.select_model.set('')
        model_select_id = False
        entry_item_number.delete(0, END)
        enabled_is_replace.set(False)
        enabled_is_repair.set(False)

        # ---очищаем поля Свойства ИБП
        clear_value_ups()

        # -- очищаем подстветку кнопок
        clear_status_rediobuttom()

        # отображаем все
        show_main_treeview()

    buttom_search_depart = ttk.Button(labelframe_top, text='Очистить', command=reset_entry_depart_model)
    buttom_search_depart.grid(row=3, columnspan=5, padx=(0, 109), pady=(5, 5), sticky='e')

    def search_ups_and_update_color(depart_select_id, model_select_id, item_number, select_count_main_element,
                                    enabled_is_replace, enabled_is_repair):

        # - изменяем цвет статусных радиокнопок по умолчанию
        clear_status_rediobuttom()

        # - поиск
        search_ups(depart_select_id, model_select_id, item_number, select_count_main_element, enabled_is_replace,
                   enabled_is_repair)

    buttom_search_depart = ttk.Button(labelframe_top, text='Найти',
                                      command=lambda: search_ups_and_update_color(depart_select_id,
                                                                                  model_select_id,
                                                                                  item_number.get(),
                                                                                  labelframe_top.select_count_main_element.get(),
                                                                                  enabled_is_replace.get(),
                                                                                  enabled_is_repair.get()))
    buttom_search_depart.grid(row=3, columnspan=5, pady=(5, 5), padx=(0, 0), sticky='e')

    # средняя верхняя позиция
    labelframe_top.grid(row=0, column=0, columnspan=10, pady=(20, 0), padx=(1, 0), ipadx=10, sticky='nsew')

    # --------------сведения_ИТОГО
    global labelframe_top_left_global
    labelframe_top_left = LabelFrame(frame_top, basic_style_lab_frame, text="Всего:", relief=GROOVE, bg="#ccc",
                                     font='Arial 10 bold')  # basic_style_lab_frame,
    labelframe_top_left_global = labelframe_top_left
    lbl_ups_all = Label(labelframe_top_left, basic_style_lab_frame, text="ИБП в учёте:")
    lbl_ups_all.grid(row=0, column=0, padx=(5, 1), pady=(15, 5), sticky=E)

    labelframe_top_left.all_ups_count = IntVar(labelframe_top_left, value=0)
    entry_ups_all = Entry(labelframe_top_left, basic_style_lab_frame, textvariable=labelframe_top_left.all_ups_count,
                          width=10, state='readonly')
    entry_ups_all.grid(row=0, column=1, pady=(15, 5), sticky=W)
    # ---------------------------------------------------
    lbl_ups_all_no_work = Label(labelframe_top_left, basic_style_lab_frame, text="Не в работе:")
    lbl_ups_all_no_work.grid(row=1, column=0, padx=(5, 1), pady=(5, 5), sticky=E)

    labelframe_top_left.all_no_work_count = IntVar(labelframe_top_left, value=0)
    entry_ups_all_no_work = Entry(labelframe_top_left, basic_style_lab_frame,
                                  textvariable=labelframe_top_left.all_no_work_count, width=10, state='readonly')
    entry_ups_all_no_work.grid(row=1, column=1, pady=(5, 5), sticky=W)
    # ---------------------------------------------------
    lbl_ups_all_replace_element = Label(labelframe_top_left, basic_style_lab_frame, text="Требуется замена АКБ:")
    lbl_ups_all_replace_element.grid(row=2, column=0, padx=(5, 1), pady=(5, 5), sticky=E)

    labelframe_top_left.all_replace_element_ups_count = IntVar(labelframe_top_left, value=0)
    entry_ups_all_replace_element = Entry(labelframe_top_left, basic_style_lab_frame,
                                          textvariable=labelframe_top_left.all_replace_element_ups_count, width=10,
                                          state='readonly')
    entry_ups_all_replace_element.grid(row=2, column=1, pady=(5, 5), sticky=W)
    # ---------------------------------------------------
    lbl_ups_all_repair = Label(labelframe_top_left, basic_style_lab_frame, text="В ремонте:")
    lbl_ups_all_repair.grid(row=3, column=0, padx=(5, 1), pady=(5, 5), sticky=E)

    labelframe_top_left.all_repair_count = IntVar(labelframe_top_left, value=0)
    entry_ups_all_repair = Entry(labelframe_top_left, basic_style_lab_frame,
                                 textvariable=labelframe_top_left.all_repair_count, state='readonly', width=10)
    entry_ups_all_repair.grid(row=3, column=1, pady=(5, 5), sticky=W)

    # -------------------------------------------------------
    labelframe_top_left.grid(row=0, column=10, columnspan=5, pady=(20, 0), padx=(1, 0), ipadx=10, sticky='nsew')

    # --- для  middle---------------------------

    global labelframe_treeview, tree_global  # для обновления списка после добавления ups
    labelframe_treeview_loc = LabelFrame(frame_middle, basic_style_lab_frame, text="Таблица ИБП", bg='#ccc',
                                         font='Arial 10 bold')

    # определяем столбцы
    columns = ("number", "depart", "room", "serial_number", "item_number", "model", "model_type_box", "model_power",
               "type_akb", "count_element", "is_work", "is_replace", "data_replace_el", "is_repair", "data_repair",
               "data_create", "type_terminal", "type_size", "interface", "type_battery", "is_modul", "comment", "fio",
               "ups_id")

    style = ttk.Style()
    style.theme_use('winnative')
    style.configure(".", font="helvetica 11", foreground="#004D40", padding=1, background="#90D3F9")
    style.configure("Treeview.Heading", font=('Areal', 10, 'bold'), foreground='#3C4455', lightcolor="#ffc61e",
                    bordercolor="#ffc61e", darkcolor="#ffc61e")
    style.configure("Treeview", lightcolor="#ffc61e", bordercolor="#ffc61e", darkcolor="#ffc61e")

    tree_loc = ttk.Treeview(labelframe_treeview_loc, columns=columns, show="headings", height=25)
    tree_loc.grid(row=0, column=0)

    def sort(col, reverse):
        nonlocal tree_loc
        # получаем все значения столбцов в виде отдельного списка
        lst = [(tree_loc.set(k, col), k) for k in tree_loc.get_children("")]
        # сортируем список
        lst.sort(reverse=reverse)
        # переупорядочиваем значения в отсортированном порядке
        for index, (_, k) in enumerate(lst):
            tree_loc.move(k, "", index)
        # в следующий раз выполняем сортировку в обратном порядке
        tree_loc.heading(col, command=lambda: sort(col, not reverse))

        # --Очищаем значение полей свойств
        # clear_value_ups()

    # определяем заголовки с выпавниваем по левому краю
    tree_loc.heading("number", text="#", anchor=E)
    tree_loc.heading("depart", text="Отделение", anchor=E, command=lambda: sort(1, False))
    tree_loc.heading("room", text="Помещение", anchor=E, command=lambda: sort(2, False))
    tree_loc.heading("serial_number", text="Серийный №", anchor=E, command=lambda: sort(3, False))
    tree_loc.heading("item_number", text="Инв.\\номенкл. №", anchor=E, command=lambda: sort(4, False))
    tree_loc.heading("model", text="Модель", anchor=E, command=lambda: sort(5, False))
    tree_loc.heading("model_type_box", text="Тип корпуса", command=lambda: sort(6, False))
    tree_loc.heading("model_power", text="Мощность(W)", anchor=E, command=lambda: sort(7, False))
    tree_loc.heading("type_akb", text="Тип АКБ(Ah\V)", anchor=E, command=lambda: sort(8, False))
    tree_loc.heading("count_element", text="Кол. осн\\доп.\\Σ", anchor=E, command=lambda: sort(9, False))
    tree_loc.heading("is_work", text="В работе", anchor=E, command=lambda: sort(10, False))
    tree_loc.heading("is_replace", text="Треб. замена АКБ", anchor=E, command=lambda: sort(11, False))
    tree_loc.heading("data_replace_el", text="Дата посл.замены", anchor=E, command=lambda: sort(12, False))
    tree_loc.heading("is_repair", text="В ремотне", anchor=E, command=lambda: sort(13, False))
    tree_loc.heading("data_repair", text="В ремонте с", anchor=E, command=lambda: sort(14, False))
    tree_loc.heading("data_create", text="Дата ввода", anchor=E, command=lambda: sort(15, False))

    tree_loc.heading("type_terminal", text="type_terminal", anchor=E)
    tree_loc.heading("type_size", text="type_size", anchor=E)
    tree_loc.heading("interface", text="interface", anchor=E)
    tree_loc.heading("type_battery", text="type_battery", anchor=E)
    tree_loc.heading("is_modul", text="is_modul", anchor=E)
    tree_loc.heading("comment", text="comment", anchor=E)
    tree_loc.heading("fio", text="fio", anchor=E)
    tree_loc.heading("ups_id", text="id", anchor=E)

    # настраиваем столбцы
    tree_loc.column("#1", stretch=NO, anchor=E, width=35, minwidth=20)
    tree_loc.column("#2", stretch=NO, anchor=E, width=125, minwidth=120)
    tree_loc.column("#3", stretch=NO, anchor=E, width=125, minwidth=120)
    tree_loc.column("#4", stretch=NO, anchor=E, width=100, minwidth=100)
    tree_loc.column("#5", stretch=NO, anchor=E, width=100, minwidth=80)
    tree_loc.column("#6", stretch=NO, anchor=E, width=120, minwidth=100)
    tree_loc.column("#7", stretch=NO, anchor=E, width=100, minwidth=80)
    tree_loc.column("#8", stretch=NO, anchor=E, width=105, minwidth=80)
    tree_loc.column("#9", stretch=NO, anchor=E, width=175, minwidth=190)
    tree_loc.column("#10", stretch=NO, anchor=E, width=110, minwidth=100)
    tree_loc.column("#11", stretch=NO, anchor=E, width=70, minwidth=70)
    tree_loc.column("#12", stretch=NO, anchor=E, width=120, minwidth=80)
    tree_loc.column("#13", stretch=NO, anchor=E, width=120, minwidth=80)
    tree_loc.column("#14", stretch=NO, anchor=E, width=80, minwidth=80)
    tree_loc.column("#15", stretch=NO, anchor=E, width=90, minwidth=80)
    tree_loc.column("#16", stretch=NO, anchor=E, width=90, minwidth=80)

    tree_loc.column("#17", stretch=NO, anchor=E, width=0)  # type_terminal
    tree_loc.column("#18", stretch=NO, anchor=E, width=0)  # type_size
    tree_loc.column("#19", stretch=NO, anchor=E, width=0)  # interface
    tree_loc.column("#20", stretch=NO, anchor=E, width=0)  # type_battery
    tree_loc.column("#21", stretch=NO, anchor=E, width=0)  # is_modul
    tree_loc.column("#22", stretch=NO, anchor=E, width=0)  # comment
    tree_loc.column("#23", stretch=NO, anchor=E, width=0)  # fio
    tree_loc.column("#24", stretch=NO, anchor=E, width=0)  # id

    # - отображаем указанные колонки
    tree_loc['displaycolumns'] = (
        "number", "depart", "room", "serial_number", "item_number", "model", "model_type_box", "model_power",
        "type_akb", "count_element", "is_work", "is_replace", "data_replace_el", "is_repair", "data_repair",
        "data_create", "type_terminal", "type_size", "interface", "type_battery", "is_modul", "comment", "fio",
        "ups_id")
    labelframe_treeview = labelframe_treeview_loc
    tree_global = tree_loc

    # определяем данные для отображения -и вызываем таблицу с данными -------------------`1
    show_main_treeview()
    # show_main_treeview(labelframe_treeview)

    # добавляем вертикальную прокрутку
    scrollbarY = ttk.Scrollbar(labelframe_treeview, orient=VERTICAL, command=tree_loc.yview)
    tree_loc.configure(yscroll=scrollbarY.set)
    scrollbarY.grid(row=0, column=1, sticky="ns")

    # добавляем гориз. прокрутку
    scrollbarX = ttk.Scrollbar(labelframe_treeview, orient=HORIZONTAL, command=tree_loc.xview)
    tree_loc.configure(xscroll=scrollbarX.set)
    scrollbarX.grid(row=1, column=0, sticky="nwe")

    # -- для изменений в таблице
    # tree_global = tree

    def OnClick_ups(event):
        global item_select_global
        # - выборка данных из строки
        item_select = None
        select_up = None
        try:
            item_select = tree_loc.selection()
            select_ups = tree_loc.item(item_select)['values']
            item_select_global = item_select
        except Exception as e:
            messagebox.showinfo('Информация', 'Выберите только один ИБП.')
            return 0
        # --вызываем функцию для внесения в поля Свайств ИБП значений и передаем значение по строке select_ups
        show_value_treeview_ups(select_ups)

    tree_loc.bind("<<TreeviewSelect>>", OnClick_ups)
    labelframe_treeview_loc.grid(row=0, column=0, sticky='new')

    # ------------------------for ---- test---

    # labelframe_middle_bottom = LabelFrame(frame_middle, basic_style_lab_frame, text="Свойства", bg='gray43')
    frame_values_ups = LabelFrame(frame_middle, basic_style_lab_frame, text="Свойства ИБП", bg='#ccc',
                                  font='Arial 10 bold')

    # ------------------------------------------

    # -------------START---COLUMN 0-1-------------------------------------------------

    # -------------------SELECT----DEPART---------------
    id_depart_select = 0

    def select_depart(event):
        nonlocal id_depart_select
        selection = combobox_depart_val.get()
        if res_sql_departs:
            for val in res_sql_departs:
                if str(selection) == str(val[1]):
                    id_depart_select = val[0]
                    break

        # - Очищаем поле Помещение если был выбран другой отдел (для кнопки =Переместить=)
        frame_values_ups.room_val.set('')

    res_sql_departs = connect_BD.sql_get_on_status_depart()

    only_departs_list = []
    if res_sql_departs:
        only_departs_list.extend(x[1] for x in res_sql_departs)

    # изначально с в списке пустое значение,
    # по умолчанию будет выбран  пустой элемент
    frame_values_ups.select_depart_val = StringVar(frame_values_ups, value='')

    lbl_depart_val = Label(frame_values_ups, basic_style_lab_frame, text="Отделение:")
    lbl_depart_val.grid(row=0, column=0, pady=(5, 5), sticky=E)

    combobox_depart_val = ttk.Combobox(frame_values_ups, width=23, textvariable=frame_values_ups.select_depart_val,
                                       values=only_departs_list, background='#FDFBE1', state="readonly")
    combobox_depart_val.grid(row=0, column=1, pady=(5, 5), sticky=W)
    combobox_depart_val.bind("<<ComboboxSelected>>", select_depart)

    lbl_room_val = Label(frame_values_ups, basic_style_lab_frame, text="Помещение:")
    lbl_room_val.grid(row=1, column=0, pady=(5, 0), sticky=E)
    frame_values_ups.room_val = StringVar(frame_values_ups, value='')
    entry_room_val = ttk.Entry(frame_values_ups, textvariable=frame_values_ups.room_val, font=font_entry,
                               background='#FDFBE1', width=19)
    entry_room_val.grid(row=1, column=1, pady=(5, 0), sticky=W)

    lbl_item_number_val = Label(frame_values_ups, basic_style_lab_frame, text="Инв.\номенкл. №:")
    lbl_item_number_val.grid(row=2, column=0, padx=(10, 0), pady=(5, 0), sticky=E)
    frame_values_ups.item_number_val = StringVar(frame_values_ups, value='')
    entry_item_number_val = Entry(frame_values_ups, basic_style_entry_frame,
                                  textvariable=frame_values_ups.item_number_val, width=19)
    entry_item_number_val.configure(state='disabled')
    entry_item_number_val.grid(row=2, column=1, pady=(5, 0), sticky=W)

    frame_values_ups.id_ups = IntVar(frame_values_ups, value=0)
    lbl_id_ups = Label(frame_values_ups, textvariable=frame_values_ups.id_ups)

    def search_ups_OR_show_main_treeview():
        nonlocal depart_select_id, model_select_id

        if depart_select_id or model_select_id:
            search_ups(depart_select_id, model_select_id)
            # search_ups(labelframe_treeview, depart_select_id, model_select_id)
        else:
            # show_main_treeview(labelframe_treeview, ups=None, flag_clear_values_ups=True)
            show_main_treeview(ups=None, flag_clear_values_ups=True)

    def move_ups_depart(select_depart_val, room_val):
        global tree_id_depart_select, tree_global, item_select_global
        nonlocal res_sql_departs, current_user_avtoriz

        if current_user_avtoriz[0][3] not in ['Meнеджер', 'Админ']:  # "Supper_Admin_UPS",
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user_avtoriz[0][3]}' не может выполнить.")
            return

        if not select_depart_val and not room_val:
            return
        if not room_val:
            messagebox.showwarning('Предупреждение', 'Заполните поле "Помещение".')
            return
        new_name_depart = ''
        if res_sql_departs:
            for val in res_sql_departs:
                if str(select_depart_val) == str(val[1]):
                    select_dep_id = val[0]
                    new_name_depart = val[1]
                if str(tree_id_depart_select) == str(val[1]):
                    id_tree_depart = val[0]
        else:
            messagebox.showinfo('Информация', 'Что-то пошло не так!')
            return

        if id_tree_depart != select_dep_id:
            res = messagebox.askyesno('Внимание', f'Вы точно хотите переместить выбранный ИБП в \n{select_depart_val}?')
            if res:
                param = (current_user_avtoriz[0][0], int(select_dep_id), room_val, int(frame_values_ups.id_ups.get()))
                connect_BD.sql_update_id_depart(param)

                # - обновляем содержимое окна после добавления и показываем в отделе куда перемещён
                search_ups(select_dep_id, id_model_select=None)

            else:
                tree_global.selection_set(item_select_global)

    buttom_edit_depart = ttk.Button(frame_values_ups, text='  Переместить  ',
                                    command=lambda: move_ups_depart(frame_values_ups.select_depart_val.get(),
                                                                    frame_values_ups.room_val.get()))
    buttom_edit_depart.state(['disabled'])
    buttom_edit_depart.grid(row=3, column=1, padx=(0, 0), pady=(5, 0), sticky=W)

    # -------------START---COLUMN 2-3-------------------------------------------------
    lbl_model_val = Label(frame_values_ups, basic_style_lab_frame, text="Модель ИБП:")
    lbl_model_val.grid(row=0, column=2, padx=(20, 0), pady=(5, 0), sticky=E)
    frame_values_ups.model_val = StringVar(frame_values_ups, value='')
    entry_model_val = Entry(frame_values_ups, basic_style_entry_frame, textvariable=frame_values_ups.model_val,
                            width=15)
    entry_model_val.configure(state='disabled')
    entry_model_val.grid(row=0, column=3, pady=(5, 0), sticky=W)

    lbl_type_battery_val = Label(frame_values_ups, basic_style_lab_frame, text="Тип ИБП:")
    lbl_type_battery_val.grid(row=1, column=2, padx=(10, 0), pady=(5, 0), sticky=E)
    frame_values_ups.type_battery_val = StringVar(frame_values_ups, value='')
    entry_type_battery_val = Entry(frame_values_ups, basic_style_entry_frame,
                                   textvariable=frame_values_ups.type_battery_val, width=15)
    entry_type_battery_val.configure(state='disabled')
    entry_type_battery_val.grid(row=1, column=3, pady=(5, 0), sticky=W)

    lbl_model_intrface_val = Label(frame_values_ups, basic_style_lab_frame, text="Интерфейсы:")
    lbl_model_intrface_val.grid(row=2, column=2, padx=(10, 0), pady=(5, 0), sticky=E)
    frame_values_ups.model_intrface_val = StringVar(frame_values_ups, value='')
    entry_model_intrface_val = Entry(frame_values_ups, basic_style_entry_frame,
                                     textvariable=frame_values_ups.model_intrface_val, width=15)
    entry_model_intrface_val.configure(state='disabled')
    entry_model_intrface_val.grid(row=2, column=3, pady=(5, 0), sticky=W)

    lbl_is_modul_val = Label(frame_values_ups, basic_style_lab_frame, text="Модульный:")
    lbl_is_modul_val.grid(row=3, column=2, padx=(10, 0), pady=(0, 0), sticky=E)
    frame_values_ups.is_modul_val = StringVar(frame_values_ups, value='')
    entry_is_modul_val = Entry(frame_values_ups, textvariable=frame_values_ups.is_modul_val, width=4)
    entry_is_modul_val.configure(state='disabled')
    entry_is_modul_val.grid(row=3, column=3, pady=(0, 0), sticky=W)

    lbl_akb_count_val = Label(frame_values_ups, basic_style_lab_frame, text="Кол.АКБ:")
    lbl_akb_count_val.grid(row=3, column=3, padx=(0, 25), pady=(0, 0), sticky=E)
    frame_values_ups.akb_count_val = StringVar(frame_values_ups, value='')
    entry_akb_count_val = Entry(frame_values_ups, textvariable=frame_values_ups.akb_count_val, width=4)
    entry_akb_count_val.configure(state='disabled')
    entry_akb_count_val.grid(row=3, column=3, sticky=E)

    # -------------START---COLUMN 4-5-----------------------------------------------
    lbl_capacity_val = Label(frame_values_ups, basic_style_lab_frame, text="Емкость(А/h):")
    lbl_capacity_val.grid(row=0, column=4, padx=(5, 0), pady=(5, 0), sticky=E)
    frame_values_ups.capacity_val = StringVar(frame_values_ups, value='')
    entry_capacity_val = Entry(frame_values_ups, basic_style_entry_frame, textvariable=frame_values_ups.capacity_val,
                               width=15)
    entry_capacity_val.configure(state='disabled')
    entry_capacity_val.grid(row=0, column=5, pady=(5, 0), sticky=W)

    lbl_volt_val = Label(frame_values_ups, basic_style_lab_frame, text="Вольт(V):")
    lbl_volt_val.grid(row=1, column=4, padx=(5, 0), pady=(5, 0), sticky=E)
    frame_values_ups.volt_val = StringVar(frame_values_ups, value='')
    entry_volt_val = Entry(frame_values_ups, basic_style_entry_frame, textvariable=frame_values_ups.volt_val, width=15)
    entry_volt_val.configure(state='disabled')
    entry_volt_val.grid(row=1, column=5, pady=(5, 0), sticky=W)

    lbl_type_terminal_val = Label(frame_values_ups, basic_style_lab_frame, text="Тип клем:")
    lbl_type_terminal_val.grid(row=2, column=4, padx=(5, 0), pady=(5, 0), sticky=E)
    frame_values_ups.type_terminal_val = StringVar(frame_values_ups, value='')
    entry_type_terminal_val = Entry(frame_values_ups, basic_style_entry_frame,
                                    textvariable=frame_values_ups.type_terminal_val, width=15)
    entry_type_terminal_val.configure(state='disabled')
    entry_type_terminal_val.grid(row=2, column=5, pady=(5, 0), sticky=W)

    lbl_type_size_val = Label(frame_values_ups, basic_style_lab_frame, text="Типоразмер:")
    lbl_type_size_val.grid(row=3, column=4, padx=(20, 0), pady=(0, 0), sticky=E)
    frame_values_ups.type_size_val = StringVar(frame_values_ups, value='')
    entry_type_size_val = Entry(frame_values_ups, basic_style_entry_frame, textvariable=frame_values_ups.type_size_val,
                                width=15)
    entry_type_size_val.configure(state='disabled')
    entry_type_size_val.grid(row=3, column=5, pady=(0, 0), sticky=W)

    # -------------START---COLUMN 6-7-------------------------------------------------
    radiobutton_on_off_style = ttk.Style()
    radiobutton_on_off_style.configure("My_radbut.TRadiobutton",  # имя стиля
                                       font="helvetica 11",  # шрифт
                                       foreground="#004D40",  # цвет текста
                                       padding=(1, 5, 2, 0),  # отступы
                                       background="#B5BFC7")  # фоновый цвет
    radiobutton_on_off_style.map("My_radbut.TRadiobutton", background=[('active', '#90D3F9')])

    lbl_is_work = Label(frame_values_ups, basic_style_lab_frame, text="В работе:")
    lbl_is_work.grid(row=0, column=6, pady=(5, 0), sticky=E)

    status_on_work = "Да"
    status_of_work = "Нет"

    frame_values_ups.status_work = StringVar(frame_values_ups,
                                             value='')  # по умолчанию будет выбран ''

    status_on_btn_work = ttk.Radiobutton(frame_values_ups, text=status_on_work, variable=frame_values_ups.status_work,
                                         value=status_on_work, style="My_radbut.TRadiobutton")
    status_on_btn_work.grid(row=0, column=7, pady=(7, 0), sticky='nw')

    status_of_btn_work = ttk.Radiobutton(frame_values_ups, text=status_of_work, variable=frame_values_ups.status_work,
                                         value=status_of_work, style="My_radbut.TRadiobutton")
    status_of_btn_work.grid(row=0, column=7, pady=(7, 0), padx=(50, 0), sticky='nw')

    # ---------------------------------------------------------------------------------
    lbl_is_replace = Label(frame_values_ups, basic_style_lab_frame, text="Треб. замена АКБ:")
    lbl_is_replace.grid(row=1, column=6, padx=(20, 0), pady=(5, 0), sticky=E)

    status_on_replace = "Да"
    status_of_replace = "Нет"

    frame_values_ups.status_replace = StringVar(frame_values_ups,
                                                value='')  # по умолчанию будет выбран ''

    status_on_btn_replace = ttk.Radiobutton(frame_values_ups, text=status_on_replace,
                                            variable=frame_values_ups.status_replace, value=status_on_replace,
                                            style="My_radbut.TRadiobutton")
    status_on_btn_replace.grid(row=1, column=7, pady=(5, 0), sticky='nw')

    status_of_btn_replace = ttk.Radiobutton(frame_values_ups, text=status_of_replace,
                                            variable=frame_values_ups.status_replace, value=status_of_replace,
                                            style="My_radbut.TRadiobutton")
    status_of_btn_replace.grid(row=1, column=7, pady=(5, 0), padx=(50, 0), sticky='nw')

    # ------------------------------------------------------------------------------------
    lbl_is_repair = Label(frame_values_ups, basic_style_lab_frame, text="В ремонте:")
    lbl_is_repair.grid(row=2, column=6, pady=(5, 0), sticky=E)

    status_on_repair = "Да"
    status_of_repair = "Нет"

    frame_values_ups.status_repair = StringVar(frame_values_ups,
                                               value='')  # по умолчанию будет выбран ''

    status_on_btn_repair = ttk.Radiobutton(frame_values_ups, text=status_on_repair,
                                           variable=frame_values_ups.status_repair, value=status_on_repair,
                                           style="My_radbut.TRadiobutton")
    status_on_btn_repair.grid(row=2, column=7, pady=(5, 0), sticky='nw')

    status_of_btn_repair = ttk.Radiobutton(frame_values_ups, text=status_of_repair,
                                           variable=frame_values_ups.status_repair, value=status_of_repair,
                                           style="My_radbut.TRadiobutton")
    status_of_btn_repair.grid(row=2, column=7, pady=(5, 0), padx=(50, 0), sticky='nw')

    def check_select_id(*args):
        global item_select_global
        if frame_values_ups.id_ups.get() == 0:
            buttom_edit_statsus.state(['disabled'])
            buttom_save_comment.state(['disabled'])
            buttom_edit_depart.state(['disabled'])
            buttom_close_repair_ups.state(['disabled'])
            buttom_replace_elem_ups.state(['disabled'])
            buttom_raport_ups.state(['disabled'])
            buttom_delete_ups.state(['disabled'])
        else:
            buttom_edit_statsus.state(['!disabled'])
            buttom_save_comment.state(['!disabled'])
            buttom_edit_depart.state(['!disabled'])
            buttom_close_repair_ups.state(['!disabled'])
            buttom_replace_elem_ups.state(['!disabled'])
            buttom_raport_ups.state(['!disabled'])
            buttom_delete_ups.state(['!disabled'])

            if item_select_global is not None:
                radiobutton_on_off_style = ttk.Style()

                if tree_loc.item(item_select_global)['values'][11] == "Да":

                    radiobutton_on_off_style.configure("My_radbutOn.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#E8E802")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut1.TRadiobutton", background=[('active', '#90D3F9')])

                    status_of_btn_work.configure(style='My_radbutOn.TRadiobutton')
                    status_on_btn_replace.configure(style='My_radbutOn.TRadiobutton')
                    status_on_btn_repair.configure(style='My_radbutOn.TRadiobutton')

                else:
                    radiobutton_on_off_style.configure("My_radbut.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#B5BFC7")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut.TRadiobutton", background=[('active', '#90D3F9')])

                    status_of_btn_work.configure(style='My_radbut.TRadiobutton')
                    status_on_btn_replace.configure(style='My_radbut.TRadiobutton')
                    status_on_btn_repair.configure(style='My_radbut.TRadiobutton')

                if tree_loc.item(item_select_global)['values'][10] == "Нет":

                    radiobutton_on_off_style.configure("My_radbutOn.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#E8E802")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut1.TRadiobutton", background=[('active', '#90D3F9')])

                    status_of_btn_work.configure(style='My_radbutOn.TRadiobutton')


                else:
                    radiobutton_on_off_style.configure("My_radbut.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#B5BFC7")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut.TRadiobutton", background=[('active', '#90D3F9')])

                    status_of_btn_work.configure(style='My_radbut.TRadiobutton')

                if tree_loc.item(item_select_global)['values'][13] == "Да":

                    radiobutton_on_off_style.configure("My_radbutOn.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#E8E802")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut1.TRadiobutton", background=[('active', '#90D3F9')])

                    status_on_btn_repair.configure(style='My_radbutOn.TRadiobutton')

                else:
                    radiobutton_on_off_style.configure("My_radbut.TRadiobutton",  # имя стиля
                                                       font="helvetica 11",  # шрифт
                                                       foreground="#004D40",  # цвет текста
                                                       padding=(1, 5, 2, 0),  # отступы
                                                       background="#B5BFC7")  # фоновый цвет
                    radiobutton_on_off_style.map("My_radbut.TRadiobutton", background=[('active', '#90D3F9')])

                    status_on_btn_repair.configure(style='My_radbut.TRadiobutton')

    frame_values_ups.id_ups.trace_add("write", check_select_id)

    def edit_status_work_replace_repair(status_work, status_replace, status_repair, id_ups):
        global status_ups, tree_global, item_select_global
        nonlocal current_user_avtoriz, tree_loc

        if current_user_avtoriz[0][3] not in ['Meнеджер', 'Админ']:
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user_avtoriz[0][3]}' не может изменять!")
            return

        number = tree_loc.item(item_select_global)['values'][4]
        select_user_status = tuple([status_work.get(), status_replace.get(), status_repair.get()])

        # - если есть изменения от пользавателя
        if status_ups != select_user_status:
            now_date = datetime.now().strftime('%Y-%m-%d')
            id_ups = int(id_ups.get())

            # -- проверка на в работе
            if status_ups[0] != select_user_status[0]:

                param = (current_user_avtoriz[0][0], select_user_status[0], id_ups)
                # --если устанавливаем в работе:
                if status_ups[0] == "Нет" and (select_user_status[0] == "Да"):
                    connect_BD.sql_update_status_work_ups(param)
                    tree_loc.set(item_select_global, 10, select_user_status[0])
                    tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                    tree_loc.selection_set(item_select_global)
                    labelframe_top_left.all_no_work_count.set(int(labelframe_top_left.all_no_work_count.get()) - 1)

                    # --если снимаем в работе
                else:
                    res = messagebox.askyesno('Внимание', "Вы точно хотите изменить статус на <Не в работе>?")
                    if res:
                        param = (current_user_avtoriz[0][0], select_user_status[0], id_ups)
                        connect_BD.sql_update_status_work_ups(param)

                        tree_loc.set(item_select_global, 10, select_user_status[0])
                        tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                        tree_loc.selection_set(item_select_global)
                        labelframe_top_left.all_no_work_count.set(int(labelframe_top_left.all_no_work_count.get()) + 1)

                    else:
                        frame_values_ups.status_work.set('Да')

                # --проверка на замену AКБ
            if status_ups[1] != select_user_status[1]:
                selected_ups = tree_global.item(item_select_global)['values']
                # - если требуется замена АКБ
                if status_ups[1] == "Нет" and (select_user_status[1] == "Да"):
                    res1 = messagebox.askyesno('Внимание',
                                               "Вы точно хотите изменить статус на \n<Требуется замена АКБ>?")
                    if res1:
                        date_edit = selected_ups[12] if len(selected_ups[12]) > 5 else 'н/д'
                        param_edit_elem = (current_user_avtoriz[0][0], select_user_status[1], date_edit, id_ups)
                        connect_BD.sql_update_status_replace_element_ups(param_edit_elem)

                        tree_loc.set(item_select_global, 11, select_user_status[1])
                        tree_loc.set(item_select_global, 12, date_edit)
                        tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                        tree_loc.selection_set(item_select_global)

                        # - для изменений в сведениях
                        labelframe_top_left.all_replace_element_ups_count.set(
                            int(labelframe_top_left.all_replace_element_ups_count.get()) + 1)
                    else:
                        frame_values_ups.status_replace.set("Нет")
                    # - Иначе
                else:
                    res2 = messagebox.askyesno('Внимание',
                                               f"Оформить замену АКБ в ИБП инв. № {tree_loc.item(item_select_global)['values'][4]}?")
                    if res2:
                        date_edit = now_date  # if len(selected_ups[12]) > 5 else now_date
                        param_edit_elem = (current_user_avtoriz[0][0], select_user_status[1], date_edit, id_ups)
                        connect_BD.sql_update_status_replace_element_ups(param_edit_elem)

                        tree_loc.set(item_select_global, 11, select_user_status[1])
                        tree_loc.set(item_select_global, 12, date_edit)
                        tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                        tree_loc.selection_set(item_select_global)

                        # - для изменений в сведениях
                        labelframe_top_left.all_replace_element_ups_count.set(
                            int(labelframe_top_left.all_replace_element_ups_count.get()) - 1)
                    else:
                        frame_values_ups.status_replace.set("Да")

                # -- проверка на ремонт
            if status_ups[2] != select_user_status[2]:

                # --если устанавливаем ремонт ИБП:
                if status_ups[2] == "Нет" and (select_user_status[2] == "Да"):

                    param_date = (current_user_avtoriz[0][0], select_user_status[2], now_date, id_ups)

                    connect_BD.sql_update_status_repair_ups(param_date)

                    tree_loc.set(item_select_global, 13, select_user_status[2])
                    tree_loc.set(item_select_global, 14, now_date)
                    tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                    tree_loc.selection_set(item_select_global)
                    # - для изменений в сведениях
                    labelframe_top_left.all_repair_count.set(int(labelframe_top_left.all_repair_count.get()) + 1)

                    # --если снимаем ремонт
                else:
                    res = messagebox.askyesno('Внимание', f"Вы точно хотите закрыть ремонт ИБП инв. № {number}?")
                    if res:
                        param_date = (current_user_avtoriz[0][0], select_user_status[2], 'н/д', id_ups)
                        connect_BD.sql_update_status_repair_ups(param_date)

                        tree_loc.set(item_select_global, 13, select_user_status[2])
                        tree_loc.set(item_select_global, 14, 'н/д')
                        tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                        tree_loc.selection_set(item_select_global)
                        # - для изменений в сведениях
                        labelframe_top_left.all_repair_count.set(int(labelframe_top_left.all_repair_count.get()) - 1)

    # else:
    #    return

    buttom_edit_statsus = ttk.Button(frame_values_ups, text='Изменить',
                                     command=lambda: edit_status_work_replace_repair(frame_values_ups.status_work,
                                                                                     frame_values_ups.status_replace,
                                                                                     frame_values_ups.status_repair,
                                                                                     frame_values_ups.id_ups))
    buttom_edit_statsus.state(['disabled'])
    buttom_edit_statsus.grid(row=3, column=7, padx=(0, 0), pady=(5, 5))

    # -------------------------------------------------------------------------------------------
    # -------------START---COLUMN 8-9-------------------------------------------------
    lbl_fio_val = Label(frame_values_ups, basic_style_lab_frame, text="Создал\изм.:")
    lbl_fio_val.grid(row=0, column=8, padx=(0, 0), pady=(0, 0), sticky=E)
    frame_values_ups.entry_fio_val = StringVar(frame_values_ups, value='')
    entry_fio_val = Entry(frame_values_ups, basic_style_entry_frame, textvariable=frame_values_ups.entry_fio_val,
                          width=22)
    entry_fio_val.configure(state='disabled')
    entry_fio_val.grid(row=0, column=9, pady=(0, 0), sticky=W)

    lbl_ups_comment_val = Label(frame_values_ups, basic_style_lab_frame, text="Комментарии:")
    lbl_ups_comment_val.grid(row=1, column=8, padx=(20, 0), pady=(5, 0), sticky=NE)
    frame_values_ups.ups_comment_val = StringVar(frame_values_ups, value='')

    text_ups_comment_val = ScrolledText(frame_values_ups, width=20, height=3, font=font_entry, wrap="word")
    text_ups_comment_val.insert(0.0, frame_values_ups.ups_comment_val.get())

    # *--для передачи черех tree
    global text_ups_comment

    text_ups_comment = text_ups_comment_val
    text_ups_comment_val.grid(row=1, rowspan=3, column=9, pady=(5, 0), sticky=NW)

    def save_comment(text_ups_comment, id_ups):
        global tree_global, item_select_global
        nonlocal current_user_avtoriz

        id_ups = int(id_ups.get())
        text = text_ups_comment.get(0.0, END)
        text = text.strip('\n')

        param = (current_user_avtoriz[0][0], text, id_ups)

        connect_BD.sql_save_comment(param)
        tree_global.set(item_select_global, 22, current_user_avtoriz[0][2])
        tree_global.set(item_select_global, 21, 'Сохранение...')
        tree_global.set(item_select_global, 21, text)
        tree_global.selection_set(item_select_global)

    buttom_save_comment = ttk.Button(frame_values_ups, text='Сохранить',
                                     command=lambda: save_comment(text_ups_comment_val, frame_values_ups.id_ups))
    buttom_save_comment.state(['disabled'])
    buttom_save_comment.grid(row=3, column=9, padx=(0, 0), pady=(0, 0), sticky=E)

    # -------------START---COLUMN 10-11-------------------------------------------------
    def close_repair(id_ups):
        global tree_global, item_select_global
        nonlocal current_user_avtoriz, tree_loc

        if current_user_avtoriz[0][3] not in ['Meнеджер', 'Админ']:  # "Supper_Admin_UPS",
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user_avtoriz[0][3]}' не может изменять!")
            return

        select_ups = tree_loc.item(item_select_global)['values'][13]
        number = tree_loc.item(item_select_global)['values'][4]

        if select_ups == 'Да':
            res = messagebox.askyesno('Внимание', f"Вы точно хотите закрыть ремонт ИБП инв. № {number}?")
            if res:
                id_ups = int(id_ups.get())
                param_date = (current_user_avtoriz[0][0], 'Нет', 'н/д', id_ups)
                connect_BD.sql_update_status_repair_ups(param_date)

                tree_global.set(item_select_global, 13, 'Нет')
                tree_global.set(item_select_global, 14, 'н/д')
                tree_global.set(item_select_global, 22, current_user_avtoriz[0][2])
                tree_global.selection_set(item_select_global)
                frame_values_ups.status_repair.set('Нет')

                # - для изменений в сведениях
                labelframe_top_left.all_repair_count.set(int(labelframe_top_left.all_repair_count.get()) - 1)
        else:
            messagebox.showinfo('Внимание', 'Выбраный ИПБ сейчас не в ремонте. Выберите другой.')

    buttom_close_repair_ups = ttk.Button(frame_values_ups, text='  Закрыть ремонт ИПБ  ',
                                         command=lambda: close_repair(frame_values_ups.id_ups))
    buttom_close_repair_ups.state(['disabled'])
    buttom_close_repair_ups.grid(row=0, column=10, padx=(20, 0), pady=(0, 0), sticky=E)

    def replace_element(id_ups):
        global item_select_global
        nonlocal current_user_avtoriz, tree_loc

        if current_user_avtoriz[0][3] not in ['Meнеджер', 'Админ']:  # "Supper_Admin_UPS",
            messagebox.showinfo('Информация',
                                f"Пользователь с ролью '{current_user_avtoriz[0][3]}' не может изменять!")
            return

        select_ups = tree_loc.item(item_select_global)['values']

        if select_ups[11] == 'Да':
            res = messagebox.askyesno('Внимание', f"Оформить замену АКБ в ИБП инв. № {select_ups[4]}?")
            if res:
                id_ups = int(id_ups.get())
                now_date = datetime.now().strftime('%Y-%m-%d')
                date_edit = now_date  # if len(select_ups[12]) > 5 else 'н/д'
                param_edit_elem = (current_user_avtoriz[0][0], 'Нет', date_edit, id_ups)
                connect_BD.sql_update_status_replace_element_ups(param_edit_elem)

                tree_loc.set(item_select_global, 11, 'Нет')
                tree_loc.set(item_select_global, 12, date_edit)
                tree_loc.set(item_select_global, 22, current_user_avtoriz[0][2])
                tree_loc.selection_set(item_select_global)
                frame_values_ups.status_repair.set('Нет')

                # - для изменений в сведениях
                labelframe_top_left.all_replace_element_ups_count.set(
                    int(labelframe_top_left.all_replace_element_ups_count.get()) - 1)
        else:
            messagebox.showinfo('Внимание', 'Выбраному ИПБ не требуется замена АКБ. Выберите другой.')

    buttom_replace_elem_ups = ttk.Button(frame_values_ups, text=' Оформить замену АКБ ',
                                         command=lambda: replace_element(frame_values_ups.id_ups))
    buttom_replace_elem_ups.state(['disabled'])
    buttom_replace_elem_ups.grid(row=1, column=10, padx=(0, 0), pady=(0, 0), sticky=E)

    def print_raport():
        global tree_global, item_select_global

        select_ups = tree_global.item(item_select_global)['values']
        # --------
        now_date = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        name_file = 'raport_ups_'
        template_start = '''
        <style>
        table.GeneratedTable {
          width: 100%;
          background-color: #ffffff;
          border-collapse: collapse;
          border-width: 2px;
          border-color: #313335;
          border-style: solid;
          color: #000000;
        }
        
        table.GeneratedTable td, table.GeneratedTable th {
          border-width: 2px;
          border-color: #313335;
          border-style: solid;
          padding: 3px;
        }
        
        table.GeneratedTable thead {
          background-color: #ccc;
        }
        </style>
        
        <table class="GeneratedTable">
        <html>
        <head>
        <meta charset="UTF-8">
        </head>
        <title>Raport UPS</title>
        <body>  
          <thead>
          <p style="color:#ccc; padding: 0px; margin: 0px;">Developer: Dudko M.</p>
          <p style="color:#ccc; padding: 0px; margin: 0px;">Designed for: Petrikov, Republic Belarus \ Lic. key 775i</p>
          <p style="color:#ccc; padding: 0px; margin: 0px;">Developer contact: promsoft-1@ya.ru</p>
          <h3 style="padding-top: 20px;">Отчёт по ИБП</h3>
            <tr>
                <th>Отделение<br></th>
                <th>Помещение</th>
                <th>Серийный №</th>
                <th>Инв.№</th>
                <th>Модель</th>
                <th>Тип корпуса</th>
                <th>Мощность(W)</th>
                <th>Тип АКБ(Ah\V)</th>
                <th>Кол. осн\доп.\Σ</th>
                <th>В работе</th>
                <th>Треб. зам.АКБ</th>
                <th>Дата замены</th>
                <th>В ремотне</th>
                <th>В ремонте с</th>
                <th>Дата ввода</th>
            </tr>
          </thead>
          <tbody>
        '''
        template = '<tr><td>{0}</td>  <td>{1}</td>  <td>{2}</td>  <td>{3}</td>  <td>{4}</td>  <td>{5}</td>  <td>{6}</td>  <td>{7}</td>  <td>{8}</td>  <td>{9}</td>  <td>{10}</td>  <td>{11}</td>  <td>{12}</td>  <td>{13}</td>  <td>{14}</td>  </tr>'
        template_end = '</tbody> </table></body></html>'
        name_file += now_date
        try:
            with open(f"{name_file}.html", 'w', encoding="utf-8") as html:
                html.write(template_start)
                html.write(template.format(select_ups[1], select_ups[2], select_ups[3], select_ups[4], select_ups[5],
                                           select_ups[6], select_ups[7], select_ups[8], select_ups[9], select_ups[10],
                                           select_ups[11], select_ups[12], select_ups[13], select_ups[14],
                                           select_ups[15]))
                html.write(template_end)
        except BaseException as e:
            messagebox.showwarning('Error', f"Что-то пошло не так. \n{e} \nПопробуйте ещё раз.")
        else:
            messagebox.showinfo('Информация', f"В текущей папке создан файл: {name_file}.html.")

    buttom_raport_ups = ttk.Button(frame_values_ups, text='   Распечатать   ', command=print_raport)
    buttom_raport_ups.state(['disabled'])
    buttom_raport_ups.grid(row=2, column=10, padx=(0, 0), pady=(5, 0), sticky=E)

    buttom_style = ttk.Style()
    buttom_style.configure("My_delete.TButton",  # имя стиля
                           font="helvetica 11",  # шрифт
                           foreground="#004D40",  # цвет текста
                           padding=1,  # отступы
                           background="#B2DFDB")  # фоновый цвет
    buttom_style.map('My_delete.TButton', background=[('active', 'red')])

    def delete_ups(id_ups):
        global tree_global, item_select_global
        nonlocal current_user_avtoriz
        id_ups = int(id_ups.get())

        if current_user_avtoriz[0][3] in ['Админ']:
            res = messagebox.askyesno('Внимание', 'Вы точно хотите удалить из базы ИБП?')
            if res:
                connect_BD.sql_delete_ups(id_ups)

                # удаляем из таблицы
                tree_global.delete(item_select_global)

                # - сбрасываем ID
                item_select_global = None

                # - очищаем свойства ИПБ
                clear_value_ups()

                # - для изменений в сведениях
                labelframe_top_left.all_ups_count.set(int(labelframe_top_left.all_ups_count.get()) - 1)

        else:
            messagebox.showwarning('Предупреждение', 'Только пользователь с ролью "Админ" может удалять!')

    buttom_delete_ups = ttk.Button(frame_values_ups, text='   Удалить ИБП  ',
                                   command=lambda: delete_ups(frame_values_ups.id_ups), style='My_delete.TButton')
    buttom_delete_ups.state(['disabled'])
    buttom_delete_ups.grid(row=3, column=10, padx=(0, 0), pady=(0, 0), sticky=E)

    global frame_values_ups_global
    # ---аттрибуты выше уже созданы и передыются в глобольную переменную фрейма Свойства ИБП
    frame_values_ups_global = frame_values_ups

    # ------------------------------------------
    # ------------------------------------------
    frame_values_ups.grid(row=1, padx=(1, 0), pady=(15, 0), ipady=2, sticky=NSEW)

    # для bottom +--------------------------------
    labelframe_bootom = LabelFrame(frame_bottom, background='#ccc')
    label_bootom = Label(labelframe_bootom,
                         text=f"Пользователь: {current_user_avtoriz[0][1]}\\{current_user_avtoriz[0][2]}", fg='#004D40',
                         background='#ccc')
    label_bootom.grid(row=0, column=0, sticky='w')
    label_bootom_role = Label(labelframe_bootom, text=f"Роль: {current_user_avtoriz[0][3]}", fg='#004D40',
                              background='#ccc')
    label_bootom_role.grid(row=1, column=0, sticky='w')

    # -- для первого столбца
    labelframe_IPB.grid(row=1, column=0, padx=(10, 10), ipady=5, sticky='nsew')
    labelframe_Model.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), ipady=5, sticky='nsew')
    labelframe_Akb.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), ipady=5, sticky='nsew')
    labelframe_Otdelenia.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), ipady=5, sticky='nsew')
    labelframe_User.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky='nsew')
    labelframe_Raport.grid(row=6, column=0, padx=(10, 10), ipady=5, sticky='nsew')

    frame_left.grid(row=0, column=0, rowspan=3, sticky='WENS')
    frame_top.grid(row=0, column=1, sticky='WENS')
    frame_middle.grid(row=1, column=1, sticky='WENS')
    frame_bottom.grid(row=2, column=1, sticky='WENS')
    labelframe_bootom.grid(row=2, column=2, padx=(1, 0), sticky='WENS')

    try:
        result_count = ups_count_status()
        labelframe_top_left.all_ups_count.set(result_count[0])
        labelframe_top_left.all_no_work_count.set(result_count[1])
        labelframe_top_left.all_replace_element_ups_count.set(result_count[2])
        labelframe_top_left.all_repair_count.set(result_count[3])

        all_ups_count_global = labelframe_top_left.all_ups_count.get()
    except BaseException as e:
        messagebox.showwarning('Erorr', f"Ошибка данных:{e}")
