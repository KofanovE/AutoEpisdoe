"""
1. Необходимо отмечать в файлах врачей отсутствие данных фамилий
2. Необходимо нумеровать врачей, что б запуск программы происходил по - очереди для врачей.
   Это необходимо на случай возможных разрывов интернета.
3.

"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta, date
import gdown
import json


import os
import time
import wx
import threading

import sys



class Administration:
    def __init__(self):
        self.current_date = date.today()
        self.dead_time = self.current_date - timedelta(20)
        self.exit_flag = False
        self.fast = False # Флаг уменьшает время ожидания клакабельности єлемента с 60 до 10 секунд
        self.date_json = None # Дата  с json файла
        self.new_date_flag = False # Флаг показівает, что дата изменилась и нужно обновить окна врачей
        self.date_path = "date_today.json"





    def download_data(self):
        try:
            df_complete_episodes = pd.read_excel("Complete_Episodes.xlsx")
        except FileNotFoundError:
            data = {'id': [],
                    'Ready': [],
                    'Status': [],
                    'Creation': [],
                    'Surname': [],
                    'Name': [],
                    'Birthday': [],
                    'Стоматолог': [],
                    'Терапевт': [],
                    'Офтальмолог': [],
                    'Невролог': [],
                    'ЛОР': [],
                    'Дерматолог': [],
                    'Хірург': [],
                    'Психіатр': [],
                    'episode': []
                    }
            df_complete_episodes = pd.DataFrame(data)

        print(df_complete_episodes)
        self.check_exit_program()

    def download_tests(self, data):
        "Загрузка анализов по данным пациента"
        pass

    def download_browser(self):
        "Загрузка браузера"
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.service = Service(executable_path='geckodriver_64.exe')
        self.driver = webdriver.Firefox(service=self.service)
        self.driver.get("https://id.helsi.pro/")
        self.check_exit_program()

    def check_exit_program(self):
        if self.exit_flag:
            self.driver.quit()
            return

    def click_element(self, element):
        self.check_exit_program()
        if self.fast:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))
        else:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))
        self.fast = False
        self.check_exit_program()
        btn = self.driver.find_element(By.CSS_SELECTOR, element)
        time.sleep(1)
        self.check_exit_program()
        btn.click()


    def send_key_to_element(self, element, key):
        self.check_exit_program()
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))
        self.check_exit_program()
        line = self.driver.find_element(By.CSS_SELECTOR, element)
        line.click()
        line.clear()
        line.click()
        line.send_keys(key)






    def reset_element(self, element):
        self.check_exit_program()
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element)))
        self.check_exit_program()
        line = self.driver.find_element(By.CSS_SELECTOR, element)
        line.click()
        line.clear()

    def get_current_time(self, doc):
        """
        Каждьій запуск программі определяет текущую дату.
        Если есть текущая дата - она сравнивается с сегодня. Если сегодня больше текущей даті, сегодня становится новой
        текущей датой и графики всех врачей обновляются.

        """

        """
        Участок кода, которій считівает дату из json файла и сравнивает с текущей, после чего перезаписівает или 
        оставляет текущую дату в файле.
        """

        current_date_str = str(self.current_date)

        try:
            with open(self.date_path, 'r') as file:
                self.date_json = json.load(file)
                print('Дата в файле ', self.date_json['date'])
        except (FileNotFoundError, json.JSONDecodeError):
            self.date_json = {'date': None}

        if self.date_json.get('date') != current_date_str:
            print('Датьі не совпадают. Обновляем дату')
            self.date_json['date'] = current_date_str

            with open(self.date_path, 'w') as file:
                json.dump(self.date_json, file, indent=4)
            print("Файл обновлен")
            self.new_date_flag = True

















class Doctor:
    def __init__(self, profession, adm):
        from doctors import surnames
        from cred import data
        self.profession = profession
        self.surname = surnames[self.profession]
        self.email = data[self.surname]['email']
        self.key = data[self.surname]['key']
        self.link = data[self.surname]['link']
        self.num = 0    # номер пациента в списке пациентов
        self.output = self.profession + ".xlsx"
        self.adm = adm
        self.doc_today_path = 'doc_today.xlsx'
        self.df_doc_today = pd.read_excel(self.doc_today_path)


    def reset_doc_schedule(self):
        """
        Обнуление графика данного врача, если дата другая
        :return:
        """
        if self.adm.new_date_flag:
            # Обнуляем все окна докторов при новой дате
            time_columns = self.df_doc_today.select_dtypes(include=['bool']).columns
            self.df_doc_today[time_columns] = False
            self.df_doc_today.to_excel(self.doc_today_path, index=False)

    def work_with_schedule(self):
        """
        Функция осуществляет алгоритм подбора свободньіх окон докторов и пациентов.
        В последующем будет использован дневной (или недельньій) график докторов.
        :return:
        """
        pass


    def get_data(self):
        "Получение файла с данными  по всем эпизодам даного врача"
        try:
            gdown.download(url=self.link, output=self.output, fuzzy=True)
            self.df_patients = pd.read_excel(self.output)
            print(self.df_patients)
            return True
        except Exception:
            print("Patients didn't found")
            return False



    def authorization(self):
        "Регистрация даного врача"
        self.adm.send_key_to_element('#email', self.email )
        self.adm.send_key_to_element('#usercreds', self.key)
        self.adm.click_element('.btn')
        time.sleep(2)


    def exit_acc(self):
        "Выход из аккаунта"
        time.sleep(5)
        self.adm.click_element('.pull-left')
        time.sleep(2)
        self.adm.click_element('.LogOut-link')
        time.sleep(2)



    def change_patient(self):
        "Подготовка к смене пациента, если не удалось его авторизировать"
        self.adm.click_element('.tooltip-restrictions>li:nth-child(6)>a:nth-child(1)>span:nth-child(1)')
        #self.adm.click_element('.tooltip-restrictions>li:nth-child(4)>a:nth-child(1)>span:nth-child(1)')
        time.sleep(2)


    def work_with_patients(self):
        "Проработка всех пациентов по полученному списку"
        for index, row in self.df_patients.iterrows():

            self.adm.check_exit_program()
            second_name = row["Surname"]
            first_name = row["Name"]
            timestamp_str = row["Birthday"].strftime("%d-%m-%Y")
            birthday_date = timestamp_str
            diagnosis = row["Diagnosis"]
            data_patients = [second_name, first_name, birthday_date, diagnosis]
            print(data_patients)
            self.find_patients(data_patients)
            print(5)
            self.change_patient()




    def find_patients(self, data_patients):
        "Поиск и авторизация даного пациента"
        second_name = data_patients[0]
        first_name = data_patients[1]
        birthday_date = data_patients[2]

        print(data_patients)

        # Нажатие кнопки поиск пациента на боковой панели
        #self.adm.click_element('.tooltip-restrictions>li:nth-child(4)>a:nth-child(1)>span:nth-child(1)')

        self.adm.click_element('.tooltip-restrictions>li:nth-child(6)>a:nth-child(1)>span:nth-child(1)')

        # Ввод фамилии пациента в строку фамилии
        self.adm.send_key_to_element('div.col-xs-3:nth-child(1)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)', second_name)

        #  Ввод имени пациента в строку имени
        self.adm.send_key_to_element('div.form-group:nth-child(2)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)',
            first_name)

        # Ввод даты рождения пациента в строку даты рождения
        self.adm.send_key_to_element('.input__maskedDate', birthday_date)

        # Нажатие кнопки поиск пациента после ввода данных во все формы
        self.adm.click_element('.margin-left-offset-20>button:nth-child(1)')
        print(3)


        # Попытка нажать на кнопку меню управления данными пациента, если нет - стирание всех заполненных форм для поиска нового пациента
        try:
            self.adm.fast = True
            self.adm.click_element('.btn-text-lg>span:nth-child(1)>svg:nth-child(1)')

        except Exception:
            #Переход на вкладку календаря для обнуления ввода нового пациента. Операция лишняя,
            #т.к. любой ввод данніх очищает строку ввода.
            #self.adm.click_element('li.active>a:nth-child(1)>span:nth-child(1)>svg:nth-child(1)')
            self.adm.reset_element('div.col-xs-3:nth-child(1)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)')
            self.adm.reset_element('div.form-group:nth-child(2)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)')
            self.adm.reset_element('.input__maskedDate')
            self.adm.fast = False
            print("Uncorrect data")
            # write data to specil file
            return False

        # Нажатие на кнопку просмотр эпизодов менюшки управления данными пациента
        self.adm.click_element('li.ant-dropdown-menu-item:nth-child(4)>span:nth-child(1)>a:nth-child(1)')
        print(6)
        self.find_episode()
        print(8)


    def find_episode(self):
        "Поиск эпизода"
        WebDriverWait(self.adm.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-table-tbody')))
        time.sleep(2)
        episodes = self.adm.driver.find_element(By.CSS_SELECTOR, '.ant-table-tbody')

        rows_episodes = episodes.find_elements(By.TAG_NAME, 'tr')
        exit_loop = False
        for row in rows_episodes:
            if exit_loop:
                break
            cells = row.find_elements(By.TAG_NAME, 'td')
            i = 0
            open_episode = False
            for cell in cells:
                print("num  ", i)

                self.adm.check_exit_program()

                if i == 1:

                    self.adm.check_exit_program()

                    print('#', cell.text)
                    print()
                    if "Z02.3" in cell.text:
                        print(cell.text)

                        self.adm.check_exit_program()

                        selected_episode = cell
                        # doctors_list = full_doctors_list.copy()
                        # specialization_list = full_specialization_list.copy()
                        selected_episode.click()
                        print('look for all reception')
                        print()
                        WebDriverWait(self.adm.driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-table-tbody')))
                        time.sleep(3)

                        self.adm.check_exit_program()

                        status_episode = self.adm.driver.find_element(By.CSS_SELECTOR,
                                                             'div.col-md-12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
                        print('status: ', status_episode.text)
                        print()

                        self.adm.check_exit_program()

                        date = self.adm.driver.find_element(By.CSS_SELECTOR,
                                                   'div.col-md-2:nth-child(4)>div:nth-child(1)>div:nth-child(2)>div:nth-child(1)>div:nth-child(1)')
                        """
                        Time
                        div.col-md-2:nth-child(4)>div:nth-child(1)>div:nth-child(2)>div:nth-child(1)>div:nth-child(1)
                        ID of episode
                        div.col-md-12:nth-child(4)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>div:nth-child(1)>div:nth-child(1)
                        """
                        create_episode = datetime.strptime(date.text[:10], '%d.%m.%Y')
                        print('create: ', create_episode)
                        print()

                        print(status_episode.text)
                        if status_episode.text == "Завершений":
                            # В даном условии рассматривается вариант, что єпизод уже закріт.
                            # !! Необходимо добавить проверку по времени, что б понимать, открівать ли новій єпизод
                            self.exit_episodes()
                            print('okey')
                        else:
                            # При даном условии рассматривается вариант, что єпизод создан, но не закріт
                            open_episode = True

                    else:
                        # В даном условии рассматривается вариант, что єпизод не создан.
                        # Далее следует создание єпизода.
                        pass

                i = i + 1
            if self.profession == 'Терапевт':
                if open_episode:
                    print("Episode opened")
                else:
                    print("Create episode")
                    self.create_episode()


    def create_episode(self):
        "Создание нового эпизода"

        # Нажатие кноки Створити прийом зараз
        self.adm.click_element('#addEventNow')

        # Строка шаблона
        self.adm.send_key_to_element('#SearchPresetPin', 'Z02.3 Обстеження призовників під час набору на військову службу')

        # Шаблон
        self.adm.click_element('.text__hightlight')

        # Кнопка почати прийом зараз
        self.adm.click_element('#cancelEventNowButton')




    def exit_episodes(self):
        "Выход из эпизода в список всех эпизодов"

        # Нажатие на кнопку Медична Картка
        self.adm.click_element('li.ant-menu-submenu:nth-child(4)>div:nth-child(1)>span:nth-child(1)')

        time.sleep(0.5)

        # Нажатие на кнопку подменю Епізоди
        self.adm.click_element('#link_episodes')


    def enter_data(self):
        "Ввод данных по даному эпизоду"
        pass




class Terapevt(Doctor):
    def __init__(self, surname, adm):
        super().__init__(surname, adm)

    def upload_tests(self):
        "Загрузка анализов"
        pass

class Psyhyatr(Doctor):
    def __init__(self, surname, adm):
        super().__init__(surname, adm)

    def close_episode(self):
        "Закрытие эпизода после проверки на соответствия"
        pass




def main_logic():
    adm = Administration()

    # Загрузка данньіх всег пациентов из главного файла
    adm.download_data()
    # Загрузка браузера
    adm.download_browser()

    # Перебор всех врачей из списка
    #doctors = ['Терапевт', 'Стоматолог', 'Офтальмолог', 'Невролог', 'ЛОР', 'Дерматолог', 'Хірург', 'Психіатр']
    doctors = ['Терапевт', 'ЛОР', 'Хірург', 'Психіатр']
    for doctor in doctors:
        if doctor == 'Терапевт':
            doc = Terapevt(doctor, adm)
        elif doctor == 'Психіатр':
            doc = Psyhyatr(doctor, adm)
        else:
            doc = Doctor(doctor, adm)

        # Авторизация даного врача
        doc.authorization()

        # Получения данньіх по пациентов от данного врача
        doc.get_data()
        if not doc.get_data():
            doc.exit_acc()
            time.sleep(2)
            continue

        # Получение текущей датьі из файла и обновление ее
        adm.get_current_time()
        # Очистка графика врача при новой дате
        doc.reset_doc_schedule()
        print(1)
        # Работа с пациентами по списку
        doc.work_with_patients()
        print(5)
        # Вьіход из аккаунта даного врача
        doc.exit_acc()
        time.sleep(2)















if __name__ == "__main__":
    main_logic()

