# для копмиляции использовать
# pyinstaller --hidden-import babel.numbers --noconsole  --windowed --onefile  --name=UPS --icon='G:\python_progect\pythonProject_UPS1\ups.ico' 'G:\python_progect\pythonProject_UPS1\main.py'
# ----MAIN---PARAMETRS-----
# импортируем библиотеку tkinter
import tkinter
import tkinter.ttk
from tkinter import messagebox

# --END--MAIN---PARAMETRS--
# data
from datetime import date

# подключение к БД
import connect_BD

# подключение авторизации
import avtorizacia



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # cоздание таблицы Users -> Otdels ->  Ups -> Revisions + user SupperAdmin и поличение supper admina
    supper_admin = connect_BD.sql_create_all_tables()
    #print(supper_admin)


    # создание главного окна
    root = tkinter.Tk()

    # запуск авторизации и главного окна
    avtorizacia.form_avtoriz(root)


    root.mainloop()
