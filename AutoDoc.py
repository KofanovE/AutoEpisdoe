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


import os
import time
import wx
import threading
from doctors import full_doctors_list, full_specialization_list
import sys

from cred import email, key

current_date = datetime.now()

try:
    df_patients = pd.read_excel("Patients_Oftalmolog.xlsx")
except FileNotFoundError:
    df_patients = pd.DataFrame()


options = webdriver.FirefoxOptions()
options.headless = True
service = Service(executable_path='geckodriver_64.exe')
driver = webdriver.Firefox(service=service)
driver.get("https://id.helsi.pro/")



""" Authorization """

if exit_flag:
    driver.quit()
    return



print('look for email input line and send email')
print()
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email'))).send_keys(email)

if exit_flag:
    driver.quit()
    return

print('look for email input line and send key')
print()
WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#usercreds'))).send_keys(key)



if exit_flag:
    driver.quit()
    return

print('look for key button enter')
print()
enter_btn = driver.find_element(By.CSS_SELECTOR, '.btn')

if exit_flag:
    driver.quit()
    return

print('press enter')
print()
enter_btn.click()

time.sleep(2)

if exit_flag:
    driver.quit()
    return


print('look for button patient and press it')
print()
btn = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.col-xs-12:nth-child(6) > a:nth-child(1) > div:nth-child(1)')))
time.sleep(2)
btn.click()

for index, row in df_patients.iterrows():

    if exit_flag:
        driver.quit()
        return

    second_name = row["Surname"]
    first_name = row["Name"]
    birthday_date = row["Birthday"]
    appoint = row["Appointment"]

    if appoint:
        print(appoint, second_name, first_name, birthday_date)
        continue

    print("#1", second_name, first_name, birthday_date)



    """ Cicle working with episodes """

    if exit_flag:
        driver.quit()
        return



    print('look for input second name and send it')
    print()

    print('a')
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[1]/form/div[1]/div[1]/div/div[2]/div/input')))
    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.has-error > div:nth-child(2) > div:nth-child(1)')))
    # time.sleep(5)
    print('b')
    """
    .has-error > div:nth-child(2) > div:nth-child(1)
    .has - error > div: nth - child(2) > div:nth - child(1) > input: nth - child(1)
    .has-error > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)
    /html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[1]/form/div[1]/div[1]/div/div[2]/div/input
    / html / body / div[1] / div / div / div[2] / div[2] / div[2] / div / div / div[3] / div[1] / form / div[1] / \
      div[1] / div / div[2] / div / input
    """

    second_name_line = driver.find_element(By.XPATH,
                                           '/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div[3]/div[1]/form/div[1]/div[1]/div/div[2]/div/input')
    print('c')
    second_name_line.click()
    if exit_flag:
        driver.quit()
        return

    print('send second name')
    print()
    second_name_line.send_keys(second_name)

    print('look for line input first name')
    print()
    first_name_line = driver.find_element(By.CSS_SELECTOR,
                                          'div.form-group:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)')
    first_name_line.click()
    if exit_flag:
        driver.quit()
        return

    print('send first name')
    print()
    first_name_line.send_keys(first_name)

    if exit_flag:
        driver.quit()
        return

    print('look for key line input birthday date')
    print()
    birthday_line = driver.find_element(By.CSS_SELECTOR, '.input__maskedDate')
    """
    .form - control_maskedDate
    .input__maskedDate
    """
    if exit_flag:
        driver.quit()
        return

    print('click on line input birthday')
    print()
    birthday_line.click()

    if exit_flag:
        driver.quit()
        return

    print('send birthday date')
    print()
    birthday_line.send_keys(birthday_date)

    if exit_flag:
        driver.quit()
        return

    print('look for button find a patient and press it')
    print()
    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-left-offset-20 > button:nth-child(1)'))).click()

    if exit_flag:
        driver.quit()
        return

    print('look for button episode')
    print()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'li.ant-dropdown-menu-item:nth-child(4) > span:nth-child(1) > a:nth-child(1)'))).click()

    if exit_flag:
        driver.quit()
        return

    print('look for all episodes')
    print()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-table-content')))



    time.sleep(3)
    episodes = driver.find_element(By.CSS_SELECTOR, '.ant-table-content')
    rows_episodes = episodes.find_elements(By.TAG_NAME, 'tr')

    if exit_flag:
        driver.quit()
        return

    exit_loop = False



    # Check all episodes of current pacient
    for row in rows_episodes:
        if exit_loop:
            print("!!! 4")
            break
        cells = row.find_elements(By.TAG_NAME, 'td')
        i = 0
        for cell in cells:
            # print(i, '. ', cell.text)

            if exit_flag:
                driver.quit()
                return

            if i == 1:

                if exit_flag:
                    driver.quit()
                    return

                print('#', cell.text)
                print()
                if "Z02.3" in cell.text:



                    exit_loop = True
                    print("!!! 3")
                    break

                else:
                     # Not episode z02.3
                     break


"""

В епизодах
#addEventNow
#addEventNow

Строка в диалоговом окне "Выбор шаблона"
#SearchPresetPin

Выбор шаблона
.ant-table-small > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(1)
td.word__break_word:nth-child(1)
td.word__break_word:nth-child(1) > span:nth-child(1) > span:nth-child(1)
td.word__break_word:nth-child(1) > span:nth-child(1) > span:nth-child(1)
в этих шаблонах нужно найти z02.3

Кнопка почати прийом
#createEhealthEventNowButton

Открывается список активных эпизодов и ищем вариант с z02.3
Кнопка продовжити епізод и кнопка продовження следующего епизода

div.margin-top-offset-30:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(2) > td:nth-child(5) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)
div.margin-top-offset-30:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(3) > td:nth-child(5) > div:nth-child(1) > span:nth-child(1) > button:nth-child(1)

В открывшемся диалоговом окне кнопка Залишити
#Cancel
#Cancel

Кнопка завершити
.btn-success


"""

