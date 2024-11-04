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
from datetime import datetime, timedelta
import gdown


import os
import time
import wx
import threading

import sys



class Administration:
    def __init__(self):
        self.current_date = datetime.now()
        self.dead_time = self.current_date - timedelta(20)
        self.exit_flag = False

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
        service = Service(executable_path='geckodriver_64.exe')
        self.driver = webdriver.Firefox(service=service)
        self.driver.get("https://id.helsi.pro/")
        self.check_exit_program()

    def check_exit_program(self):
        if self.exit_flag:
            self.driver.quit()
            return

    def click_element(self, element):
        pass

    def send_key_to_element(self, element, key):
        self.check_exit_program()
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element))).send_keys(key)

    def reset_element(self, element):
        pass









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

        if exit_flag:
            self.adm.driver.quit()
            return

        WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email'))).send_keys(self.email)

        if exit_flag:
            self.adm.driver.quit()
            return

        WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#usercreds'))).send_keys(self.key)

        if exit_flag:
            self.adm.driver.quit()
            return

        enter_btn = self.adm.driver.find_element(By.CSS_SELECTOR, '.btn')

        if exit_flag:
            self.adm.driver.quit()
            return

        enter_btn.click()
        time.sleep(2)

        if exit_flag:
            self.adm.driver.quit()
            return

        btn = WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.col-xs-12:nth-child(6)>a:nth-child(1)>div:nth-child(1)')))


    def exit_acc(self):
        "Выход из аккаунта"

        time.sleep(5)
        ava_btn = WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pull-left')))

        if exit_flag:
            self.adm.driver.quit()
            return

        ava_btn.click()
        time.sleep(2)

        if exit_flag:
            self.adm.driver.quit()
            return

        exit_btn = self.adm.driver.find_element(By.CSS_SELECTOR, '.LogOut-link')

        if exit_flag:
            self.adm.driver.quit()
            return

        exit_btn.click()
        time.sleep(2)



    def change_patient(self):
        "Подготовка к смене пациента, если не удалось его авторизировать"

        # time.sleep(1)
        # btn_1 = WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.tooltip-restrictions>li:nth-child(2)>a:nth-child(1)>span:nth-child(1)')))
        # btn_1.click()
        #
        # if exit_flag:
        #     self.adm.driver.quit()
        #     return
        #
        # time.sleep(1)


        btn_2 = WebDriverWait(self.adm.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.tooltip-restrictions>li:nth-child(4)>a:nth-child(1)>span:nth-child(1)')))
        time.sleep(2)
        btn_2.click()
        """
        .tooltip - restrictions > li: nth - child(4)
        .tooltip - restrictions > li: nth - child(4) > a:nth - child(1)
        .tooltip - restrictions > li: nth - child(4) > a:nth - child(1) > span: nth - child(1)
        """

        if exit_flag:
            self.adm.driver.quit()
            return
        time.sleep(2)


    def work_with_patients(self):
        "Проработка всех пациентов по полученному списку"
        for index, row in self.df_patients.iterrows():
            print(0)
            if exit_flag:
                self.adm.driver.quit()
                return

            second_name = row["Surname"]
            first_name = row["Name"]
            timestamp_str = row["Birthday"].strftime("%dd-%mm-%YYYY")
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
        btn = WebDriverWait(self.adm.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.tooltip-restrictions>li:nth-child(4)>a:nth-child(1)>span:nth-child(1)')))
        #btn = WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.col-xs-12:nth-child(6)>a:nth-child(1)>div:nth-child(1)')))
        time.sleep(2)
        btn.click()

        if exit_flag:
            self.adm.driver.quit()
            return



        # Ввод фамилии пациента в строку фамилии
        second_name_line = self.adm.driver.find_element(By.CSS_SELECTOR,
                                               'div.col-xs-3:nth-child(1)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)')
        second_name_line.clear()
        second_name_line.click()
        if exit_flag:
            self.adm.driver.quit()
            return
        second_name_line.send_keys(second_name)

        #  Ввод имени пациента в строку имени
        first_name_line = self.adm.driver.find_element(By.CSS_SELECTOR,
                                              'div.form-group:nth-child(2)>div:nth-child(1)>div:nth-child(1)>div:nth-child(2)>input:nth-child(1)')
        # div.form-group:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)
        first_name_line.clear()
        first_name_line.click()
        if exit_flag:
            self.adm.driver.quit()
            return
        first_name_line.send_keys(first_name)

        if exit_flag:
            self.adm.driver.quit()
            return

        # Ввод даты рождения пациента в строку даты рождения
        birthday_line = self.adm.driver.find_element(By.CSS_SELECTOR, '.input__maskedDate')

        if exit_flag:
            self.adm.driver.quit()
            return

        birthday_line.clear()
        birthday_line.click()

        if exit_flag:
            self.adm.driver.quit()
            return

        birthday_line.send_keys(birthday_date)

        print(2)
        if exit_flag:
            self.adm.driver.quit()
            return

        # Нажатие кнопки поиск пациента после ввода данных во все формы
        WebDriverWait(self.adm.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-left-offset-20>button:nth-child(1)'))).click()

        print(3)



        if exit_flag:
            self.adm.driver.quit()
            return


        # Попытка нажать на кнопку меню управления данными пациента, если нет - стирание всех заполненных форм для поиска нового пациента
        try:
            WebDriverWait(self.adm.driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.btn-text-lg>span:nth-child(1)>svg:nth-child(1)'))).click()
        except Exception:


            WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'li.active>a:nth-child(1)>span:nth-child(1)>svg:nth-child(1)'))).click()
            print("Uncorrect data")
            # write data to specil file

            second_name_line.clear()
            first_name_line.clear()
            birthday_line.clear()

            if exit_flag:
                self.adm.driver.quit()
                return
            return False

        # Нажатие на кнопку просмотр эпизодов менюшки управления данными пациента
        WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'li.ant-dropdown-menu-item:nth-child(4)>span:nth-child(1)>a:nth-child(1)'))).click()
        print(6)
        self.find_episode()
        print(8)

        if exit_flag:
            self.adm.driver.quit()
            return

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
            for cell in cells:
                print("num  ", i)

                if exit_flag:
                    self.adm.driver.quit()
                    return

                if i == 1:

                    if exit_flag:
                        self.adm.driver.quit()
                        return

                    print('#', cell.text)
                    print()
                    if "Z02.3" in cell.text:
                        print(cell.text)

                        if exit_flag:
                            self.adm.driver.quit()
                            return

                        selected_episode = cell
                        # doctors_list = full_doctors_list.copy()
                        # specialization_list = full_specialization_list.copy()
                        selected_episode.click()
                        print('look for all reception')
                        print()
                        WebDriverWait(self.adm.driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-table-tbody')))
                        time.sleep(3)

                        if exit_flag:
                            self.adm.driver.quit()
                            return

                        status_episode = self.adm.driver.find_element(By.CSS_SELECTOR,
                                                             'div.col-md-12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
                        print('status: ', status_episode.text)
                        print()

                        if exit_flag:
                            self.adm.driver.quit()
                            return

                        date = self.adm.driver.find_element(By.CSS_SELECTOR,
                                                   'div.col-md-12:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
                        create_episode = datetime.strptime(date.text[:10], '%d.%m.%Y')
                        print('create: ', create_episode)
                        print()

                        if status_episode.text is "Завершений":
                            self.exit_episodes()

                i = i + 1




    def exit_episodes(self):
        "Выход из эпизода в список всех эпизодов"
        # Кнопка Медична картка
        # .ant - menu - root > li: nth - child(3)
        # li.ant - menu - submenu: nth - child(4)
        # li.ant - menu - submenu: nth - child(4) > div:nth - child(1) > span: nth - child(1)
        # li.ant - menu - submenu: nth - child(4) > div:nth - child(1) > i: nth - child(2)
        #
        # Кнопка в подменю История Захворювань: Епизоды
        # # rc-menu-uuid-29781-1-submenu\.\/emk\/page\/85b67624-79a3-4c56-af2e-b368d01e8edd\/signalMark-popup > li:nth-child(3) > span:nth-child(1)
        # # rc-menu-uuid-29781-1-submenu\.\/emk\/page\/85b67624-79a3-4c56-af2e-b368d01e8edd\/signalMark-popup > li:nth-child(3) > span:nth-child(1) > span:nth-child(1)
        # # link_episodes

        # Нажатие на кнопку Медична Картка
        WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'li.ant - menu - submenu: nth - child(4)'))).click()

        time.sleep(0.5)

        # Нажатие на кнопку подменю Епізоди
        WebDriverWait(self.adm.driver, 60).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '# link_episodes'))).click()


    def enter_data(self):
        "Ввод данных по даному эпизоду"
        pass

    def close_sesion(self):
        "Выход из сесии даного врача"


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


class Actions:
    def __init__(self, name):
        self.name = name


    def find_adr(self):
        "Перебор словаря адресов и поиск рабочего для даного элемента"

    def press_but(self):
        "Нажатие кнопки"
        pass

    def enter_text(self):
        "Ввод текста в заданное поле"
        pass

    def choise_menu(self):
        "Выбор пункта подменю"
        pass


def main_logic():
    adm = Administration()
    adm.download_data()
    adm.download_browser()

    current_date = datetime.now()
    dead_time = current_date - timedelta(20)


    #doctors = ['Терапевт', 'Стоматолог', 'Офтальмолог', 'Невролог', 'ЛОР', 'Дерматолог', 'Хірург', 'Психіатр']
    doctors = ['Терапевт', 'ЛОР', 'Хірург', 'Психіатр']
    for doctor in doctors:
        if doctor == 'Терапевт':
            doc = Terapevt(doctor, adm)
        elif doctor == 'Психіатр':
            doc = Psyhyatr(doctor, adm)
        else:
            doc = Doctor(doctor, adm)

        doc.authorization()

        doc.get_data()
        if not doc.get_data():
            doc.exit_acc()
            time.sleep(2)
            continue
        print(1)
        doc.work_with_patients()
        print(5)

        doc.exit_acc()
        time.sleep(2)















if __name__ == "__main__":
    main_logic()