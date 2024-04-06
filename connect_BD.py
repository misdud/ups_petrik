import sqlite3
from sqlite3 import Error
from tkinter import messagebox

# initializing string
# pass1 = "777"
# result = (hashlib.md5('777'.encode('utf-8')).hexdigest())
# print(result)


# ----MAIN---PARAMETRS-----


# path_BD = "E:\\01_Python\pythonProject_info\my_database.db"
path_BD = "UPS_database.db"


# --END--MAIN---PARAMETRS--

def create_connection(path):
    connection_BD = None
    try:
        connection_BD = sqlite3.connect(path)
    except Error as e:
        messagebox.showerror('Error connect BD', f"The error '{e}' occurred !")

    return connection_BD


def sql_create_all_tables():
    # return Supper Admin

    connection = create_connection(path_BD)
    # для создания вторичных ключей
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    sql_user = '''
    CREATE TABLE IF NOT EXISTS users(
    user_id	INTEGER PRIMARY KEY AUTOINCREMENT,
    tab_num         INTEGER NOT NULL UNIQUE,
    pass            TEXT NOT NULL,
    fio             TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 0,
    role            TEXT NOT NULL,
    data_create	    TEXT DEFAULT CURRENT_TIMESTAMP
    );
    '''

    # --- для отделения
    sql_department = '''
    CREATE TABLE IF NOT EXISTS departments(
    depart_id	    INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,
    short_name      TEXT NOT NULL UNIQUE,
    status          INTEGER NOT NULL DEFAULT 1,
    data_create	    TEXT DEFAULT CURRENT_TIMESTAMP,
    user_id         INTEGER NOT NULL,
    CONSTRAINT users_table_fk 
    FOREIGN KEY (user_id) REFERENCES users (user_id)
     ON DELETE RESTRICT
      ON UPDATE RESTRICT
    );
    '''

    # --- для типа АКБ
    # --- UNIQUE (type_akb, capacity, volt) Дополнительный ключ, он же ограничение уникальности по столбцам type_akb, capacity, volt (чтоб дублей не было)
    sql_type_akb = '''
    CREATE TABLE IF NOT EXISTS typesakb(
    type_id	    INTEGER PRIMARY KEY AUTOINCREMENT,
    type_akb       TEXT NOT NULL,
    capacity       NUMERIC NOT NULL,
    volt           NUMERIC NOT NULL,
    type_terminal   TEXT,
    type_size       TEXT,
    dop_info        TEXT,
    status          INTEGER NOT NULL DEFAULT 1,
    data_create	    TEXT DEFAULT CURRENT_TIMESTAMP, 
    user_id         INTEGER NOT NULL,
    UNIQUE (type_akb, capacity, volt), 
    CONSTRAINT users_table_fk_akb FOREIGN KEY (user_id) REFERENCES users (user_id)  ON DELETE RESTRICT
    );
    '''

    # --- для model
    sql_model = '''
    CREATE TABLE IF NOT EXISTS models(
    model_id	    INTEGER PRIMARY KEY AUTOINCREMENT,
    type_elemt_id   INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    name            TEXT NOT NULL UNIQUE,
    short_name      TEXT NOT NULL UNIQUE,
    power           TEXT NOT NULL,
    interface       TEXT,
    info            TEXT,
    type_battery    TEXT,
    type_box        TEXT,
    count_element   INTEGER,
    is_modul        TEXT,
    name_modul        TEXT,
    type_battery_modul        TEXT,
    count_element_modul   INTEGER,
    comment         TEXT,
    status          INTEGER NOT NULL DEFAULT 1,
    data_create	    TEXT DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT model_elemt_fk FOREIGN KEY (type_elemt_id) REFERENCES typesakb (type_id) ON DELETE RESTRICT,
    CONSTRAINT model_user_fk FOREIGN KEY (user_id) REFERENCES users (user_id)  ON DELETE RESTRICT
    );
    '''

    # --- MAIN для ups
    # --- item_number  инв\номенклатурный номер
    sql_ups = '''
    CREATE TABLE IF NOT EXISTS ups(
    ups_id	        INTEGER PRIMARY KEY AUTOINCREMENT,
    depart_id       INTEGER NOT NULL,
    model_id        INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,  
    serial_number   TEXT DEFAULT 'н/д',
    room            TEXT NOT NULL DEFAULT 'н/д',
    item_number     INTEGER,
    is_work         TEXT NOT NULL DEFAULT 'Да',
    is_replace      TEXT NOT NULL DEFAULT 'Нет',
    data_replace_el TEXT NOT NULL DEFAULT 'н/д',
    is_repair       TEXT NOT NULL DEFAULT 'Нет',
    data_repair     TEXT,
    data_create	    TEXT,
    comment         TEXT,
    CONSTRAINT user_table_fk FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT depart_table_fk  FOREIGN KEY (depart_id) REFERENCES departments (depart_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT model_table_fk FOREIGN KEY (model_id) REFERENCES models (model_id) ON DELETE RESTRICT ON UPDATE RESTRICT   
    );
    '''

    # pass - 777
    sql_supper_user = '''
                INSERT INTO users(tab_num, pass,  fio, status, role, data_create)
                 VALUES(777777,'f1c1592588411002af340cbaedd6fc33','SupperAdm',1,'Supper_Admin_UPS', datetime('now', 'localtime')) '''

    try:
        cursor.execute(sql_user)
        cursor.execute(sql_department)
        cursor.execute(sql_type_akb)
        cursor.execute(sql_model)
        cursor.execute(sql_ups)
        connection.commit()

        # проверка на существование суппер админа, если нет то создаем (при первом запуске программы)
        cursor.execute("SELECT * FROM users WHERE tab_num = 777777;")
        supper_admin = cursor.fetchone()
        if supper_admin is None:
            # если  нет supper_admin то вставляем  и возвращаем
            cursor.execute(sql_supper_user)
            connection.commit()
            supper_admin = cursor.execute("SELECT * FROM users WHERE tab_num = 777777;")
            supper_admin = cursor.fetchone()

        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        if connection:
            connection.close()
            #print("The SQLite create table ALL")

    return supper_admin


def sql_get_all_users():
    # return all users

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # for test
    sql_supper_user = '''
                INSERT INTO users(tab_num, pass,  fio, status, role, data_create)
                 VALUES(445721,'f1c1592588411002af340cbaedd6fc33','Rider',1,'Bibik MM',datetime('now', 'localtime')) '''

    # cursor.execute(sql_supper_user)
    # connection.commit()

    sql = "SELECT user_id, tab_num, pass, fio, role FROM users WHERE status = 1;"
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users


def sql_get_all_status_users():
    # return all users

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT user_id, tab_num, fio, status, role, data_create FROM users WHERE tab_num NOT IN (777777) ORDER BY status DESC, fio;"
    cursor.execute(sql)
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users


def sql_insert_user(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = ''' INSERT INTO users(tab_num, pass,  fio, status, role, data_create)
                 VALUES(?,?,?,?,?,datetime('now', 'localtime')) '''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error SQL', f"The error '{e}' occurred !\n(Табельный номер должен быть уникальным)")
        res = 0
    finally:
        if connection:
            connection.close()

    return res


def sql_reset_password(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = ''' UPDATE users SET pass=? WHERE tab_num=?'''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        if connection:
            connection.close()


def sql_update_user(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = ''' UPDATE users SET fio=?, status=?, role=?  WHERE tab_num=?'''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        if connection:
            connection.close()


# ---------DEPART----------------------
def sql_insert_depart(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = ''' INSERT INTO departments(name, short_name, status, user_id, data_create)
                 VALUES(?,?,?,?,datetime('now', 'localtime')) '''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
        res = 0

    finally:
        if connection:
            connection.close()

    return res


def sql_get_all_status_depart():
    # return all users

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT departments.name, departments.short_name, departments.status,  users.fio, departments.data_create, departments.depart_id FROM departments, users WHERE departments.user_id = users.user_id ORDER BY departments.status DESC, departments.name;"
    cursor.execute(sql)
    departs = cursor.fetchall()
    cursor.close()
    connection.close()

    return departs


def sql_update_depart(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = '''UPDATE departments SET short_name=?, status=?, data_create=?, user_id=?  WHERE depart_id=?'''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        if connection:
            connection.close()


# -----------TYPE----AKB-----------------------------------------

def sql_insert_type_akb(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = ''' INSERT INTO typesakb(type_akb, capacity, volt, type_terminal, type_size, dop_info, status, data_create, user_id)
                 VALUES(?,?,?,?,?,?,?,datetime('now', 'localtime'),?) '''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showwarning('Передупреждение SQL', f"Невозможно выполнить.\n"
                                                      f"(Возможно вы патаетесь добавить уже существующие\n значения: тип АКБ, емкость, напряжение.)")
        res = 0

    finally:
        if connection:
            connection.close()

    return res


def sql_get_all_status_type():
    # return all types

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT typesakb.type_akb, typesakb.capacity, typesakb.volt, typesakb.type_terminal, typesakb.type_size," \
          "typesakb.dop_info, typesakb.status, users.fio, typesakb.data_create, typesakb.type_id " \
          "FROM typesakb, users WHERE typesakb.user_id = users.user_id ORDER BY typesakb.status DESC, typesakb.type_akb, capacity;"
    cursor.execute(sql)
    types_akb = cursor.fetchall()
    cursor.close()
    connection.close()

    return types_akb


def sql_get_status_on_type_akb():
    # return all types

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT type_id, type_akb, capacity, volt FROM typesakb WHERE status == 1 ORDER BY type_akb, capacity;"
    cursor.execute(sql)
    types_akb_on = cursor.fetchall()
    cursor.close()
    connection.close()

    return types_akb_on


# ---for edit models
def sql_get_status_type_akb():
    # return all types

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT type_id, type_akb, capacity, volt FROM typesakb  ORDER BY type_akb, capacity;"
    cursor.execute(sql)
    types_akb_on = cursor.fetchall()
    cursor.close()
    connection.close()

    return types_akb_on


def sql_update_typesakb(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = '''UPDATE typesakb SET capacity=?, volt=?, type_terminal=?, type_size=?, dop_info=?, status=?, data_create=?, user_id=?  WHERE type_id=?'''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showwarning('Передупреждение SQL', f"Невозможно выполнить.\n"
                                                      f"(Возможно вы патаетесь добавить уже существующие\nзначения: тип АКБ, емкость, напряжение.)")
        res = 0
    finally:
        if connection:
            connection.close()
    return res


def sql_select_typesakb_duble(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = '''SELECT type_id, type_akb, capacity, volt FROM typesakb WHERE type_id !=? AND type_akb=? AND capacity = ? AND volt= ?;'''

    try:
        cursor.execute(sql, params)
        dubles_types_akb = cursor.fetchall()
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        if connection:
            connection.close()
    return dubles_types_akb


# ------------MODEL---UPS----------------------

def sql_insert_model(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = ''' INSERT INTO models(type_elemt_id, user_id, name, short_name, power, interface, info, type_battery,
                type_box,count_element, is_modul, name_modul, type_battery_modul, count_element_modul, comment, 
                status, data_create)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now', 'localtime')) '''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
        res = 0

    finally:
        if connection:
            connection.close()

    return res


def sql_get_status_on_models():
    # return all types

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT models.model_id, users.fio, typesakb.type_akb, typesakb.capacity, typesakb.volt, models.name, " \
          "models.short_name, models.power, models.interface, models.info, models.type_battery, models.type_box," \
          " models.count_element, models.is_modul, models.name_modul, models.type_battery_modul,  models.count_element_modul," \
          " models.comment, models.status, models.data_create FROM models, typesakb, users " \
          "WHERE models.type_elemt_id = typesakb.type_id AND models.user_id = users.user_id " \
          "ORDER BY models.status DESC, models.name"
    try:
        cursor.execute(sql)
        types_akb_on = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    connection.close()

    return types_akb_on


def sql_update_models(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = '''UPDATE models SET type_elemt_id=?, user_id=?, short_name=?, power=?, status=?, type_battery=?, type_box=?, count_element=?, comment=?,  interface=?, info=?, is_modul=?, name_modul=?, type_battery_modul=?, count_element_modul=?, data_create=datetime('now', 'localtime') WHERE model_id=?'''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"Ошибка изменения данных:\nThe error '{e}' occurred !")
        res = 0
    finally:
        if connection:
            connection.close()
    return res


# --------------ADD---UPS-----------------------------------

def sql_get_on_status_depart():
    # return on departs

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT depart_id, short_name  FROM departments  WHERE status = 1 ORDER BY  short_name;"

    try:
        cursor.execute(sql)
        departs_on = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return departs_on


def sql_get_data(sql):
    # return all

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
    finally:
        connection.close()

    return res


def sql_get_on_status_model():
    # return on models

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT model_id, short_name FROM models  WHERE status = 1 ORDER BY  short_name;"

    try:
        cursor.execute(sql)
        models_on = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return models_on


def sql_get_all_status_model():
    # return on models

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT model_id, short_name FROM models ORDER BY  short_name;"

    try:
        cursor.execute(sql)
        models_on = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return models_on


def sql_get_duble_ups(param):
    # return on models

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = "SELECT item_number FROM ups WHERE item_number = ?;"

    try:  # ---tuple only
        cursor.execute(sql, (param,))
        duble_item_number_ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return duble_item_number_ups


def sql_insert_ups(params):
    connection = create_connection(path_BD)
    cursor = connection.cursor()
    res = 1

    sql = ''' INSERT INTO ups(depart_id, model_id, user_id, serial_number, room, item_number, data_replace_el,
                    data_repair, data_create, comment, is_work)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?) '''

    try:
        cursor.execute(sql, params)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")
        res = 0

    finally:
        if connection:
            connection.close()

    return res


# MAIN UPS -----------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# ---return all ups --------------------------------------------------------------------
def sql_get_ups_main_table():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT 1000;'''

    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_depart_main_table(param):
    # return  ups
    param = (param,)

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            ORDER BY departments.short_name, ups.room, models.short_name;'''

    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_table_param_id_depart(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #param = (param[0], param[1])

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''

    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_table_param_id_model(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #param = (param[0], param[1])

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.model_id = ?
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''

    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_table_param_id_depart_id_model(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.model_id = ?
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''

    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_table_param_like(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    param0 = param[0]
    param1 = int(param[1])

    #like_select = f"\'{param0}%\'"
    like_select_item = param0
    like_select_item +='%'

    params = (like_select_item, param1)



    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.item_number LIKE ?
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_replace_elements(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    params = (param,)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_depart_model_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.model_id = ?
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_depart_model_replace_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.model_id = ?
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_depart_model_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.model_id = ?
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    params = (param,)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_replace_and_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    params = (param,)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_depart_replace_and_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param,)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id  = ?
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_depart_and_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_depart_and_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, params)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_main_model_and_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.model_id = ? 
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_model_and_repair_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.model_id = ? 
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_main_model_and_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            typesakb.type_terminal, typesakb.type_size, models.interface, models.type_battery, models.is_modul,  ups.comment, users.fio, ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.model_id = ? 
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name
            LIMIT ?;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_update_id_depart(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''UPDATE ups
              SET user_id = ?,
                  depart_id = ?,
                  room = ?
                  WHERE ups_id = ?;'''

    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_update_status_repair_ups(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''UPDATE ups
              SET user_id = ?,
                  is_repair = ?,
                  data_repair = ?
                  WHERE ups_id = ?;'''

    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_update_status_replace_element_ups(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''UPDATE ups
              SET user_id =?,
                  is_replace = ?,
                  data_replace_el = ?
                  WHERE ups_id = ?;'''

    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_update_status_work_ups(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''UPDATE ups
              SET user_id = ?,
                  is_work = ?
                  WHERE ups_id = ?;'''

    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_save_comment(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql = '''UPDATE ups
              SET user_id = ?,
                  comment = ?
                  WHERE ups_id = ?;'''

    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_delete_ups(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    param = (param,)

    sql = '''DELETE FROM ups
                  WHERE ups_id = ?;'''
    try:
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()


def sql_ups_count():
    # return count ups on status

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    # param = (param,)

    sql1 = '''SELECT COUNT(*) FROM ups;'''

    sql2 = '''SELECT COUNT(*) FROM ups
                  WHERE is_replace = 'Да';'''

    sql3 = '''SELECT COUNT(*) FROM ups
                  WHERE is_repair = 'Да';'''

    sql4 = '''SELECT COUNT(*) FROM ups
                  WHERE is_work = 'Нет';'''
    try:
        cursor.execute(sql1)
        ups_all = cursor.fetchone()
        cursor.execute(sql2)
        ups_is_replace = cursor.fetchone()
        cursor.execute(sql3)
        ups_is_repair = cursor.fetchone()
        cursor.execute(sql4)
        ups_is_work = cursor.fetchone()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

        return (ups_all[0], ups_is_work[0], ups_is_replace[0], ups_is_repair[0])


def sql_get_ups_raport_all(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_work = 'Нет'
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_work_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_work = 'Нет'
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups



def sql_get_ups_raport_replace_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups




def sql_get_ups_raport_work(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_work = 'Нет'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_only_depart(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ? 
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_work_repair_replace():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_work = 'Нет'
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_work_repair():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_work = 'Нет'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_work_replace_repair():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_replace = 'Да'
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_only_work():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_work = 'Нет'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_only_repair():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_only_replace():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_work_replace(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.is_work = 'Нет'
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_work_replace_only():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.is_work = 'Нет'
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


def sql_get_ups_raport_depart_replace():
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.is_replace = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups

def sql_get_ups_raport_depart_repair(param):
    # return  ups

    connection = create_connection(path_BD)
    cursor = connection.cursor()

    #params = (param)

    sql = '''SELECT  departments.short_name,  ups.room, ups.serial_number, ups.item_number,  models.short_name, models.type_box, models.power, 
            typesakb.type_akb, typesakb.capacity, typesakb.volt, models.count_element, models.count_element_modul, 
            ups.is_work, ups.is_replace, ups.data_replace_el, ups.is_repair, ups.data_repair, ups.data_create,
            ups.ups_id
            FROM ups, departments, models, typesakb, users
            WHERE ups.depart_id = departments.depart_id 
            AND ups.model_id = models.model_id
            AND models.type_elemt_id = typesakb.type_id
            AND ups.user_id = users.user_id
            AND ups.depart_id = ?
            AND ups.is_repair = 'Да'
            ORDER BY departments.short_name, ups.room, models.short_name;'''
    try:
        cursor.execute(sql, param)
        ups = cursor.fetchall()
        cursor.close()
    except Error as e:
        messagebox.showerror('Error execute SQL', f"The error '{e}' occurred !")

    finally:
        connection.close()

    return ups


