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
from doctors import full_doctors_list

exit_flag = False

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 80))

        

        panel = wx.Panel(self)
        
        
        self.text_ctrl_global_time = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.text_ctrl_lastname = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.text_ctrl_time = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.text_ctrl_status = wx.TextCtrl(panel, style=wx.TE_READONLY)
        
        self.text_ctrl_lastname.SetMinSize((100, -1))
        self.text_ctrl_time.SetMinSize((100, -1))
        self.text_ctrl_global_time.SetMinSize((100, -1))
        self.text_ctrl_status.SetMinSize((100, -1))
        

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.text_ctrl_global_time, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.create_horizontal_sizer(self.text_ctrl_lastname, self.text_ctrl_time), 1, wx.EXPAND | wx.ALL, 5)       
        sizer.Add(self.text_ctrl_status, 1, wx.EXPAND | wx.ALL, 5)

 

        


        
        self.SetMinSize((600, 200))
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Center()

        

        self.start_time = time.time()
        self.global_time = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
        self.timer.Start(1000)
        self.surname = None

    def create_horizontal_sizer(self, ctrl1, ctrl2):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(ctrl1, 1, wx.EXPAND | wx.ALL, 5)
        hsizer.Add(ctrl2, 1, wx.EXPAND | wx.ALL, 5)
        return hsizer

    def update_display_lastname(self, lastname):
        print("!!!!!!!!!!!!!! 1")
        self.surname = lastname
        print("!!!!!!!!!!!!!! 2")
        wx.CallAfter(self.text_ctrl_lastname.SetValue, lastname)
        print("!!!!!!!!!!!!!! 3")
        self.start_time = time.time()
        print("!!!!!!!!!!!!!! 4")

    def update_display_status(self, status):
        print("!!!!!!!!!!!!!! 5")
        wx.CallAfter(self.text_ctrl_status.SetValue, status)
        print("!!!!!!!!!!!!!! 6")

    def update_time(self, event):
        current_time = time.time()
        elapsed_time = round(current_time - self.start_time)
        elapsed_time_global = round(current_time - self.global_time)
        if self.surname:
            wx.CallAfter(self.text_ctrl_time.SetValue,  f"Time for current person: {elapsed_time} seconds")
        wx.CallAfter(self.text_ctrl_global_time.SetValue,  f"Time global: {elapsed_time_global} seconds")

    def OnClose(self, event):
        global exit_flag
        exit_flag = True
        wx.GetApp().ExitMainLoop()
        

        

def main_logic(callback_lastname, callback_status):

    from cred import email, key

    global exit_flag

    app = wx.App(0)
    frame = MyFrame(None, "Program Display")
    frame.Show(True)


    threading.Thread(target=app.MainLoop).start()
    

    current_date = datetime.now()
    dead_time = current_date - timedelta(20)


    # read DF Complete episodes
    status = "Завантаження епізодів"
    callback_status(frame, status)
    try:
        df_complete_episodes = pd.read_excel("Complete_Episodes.xlsx")
    except FileNotFoundError:
        data = {'id': [],
                'Ready': [],
                'Status' : [],
                'Creation' : [],
                'Surname': [],
                'Name': [],
                'Birthday': [],
                'Прудченко О. В.': [],
                'Бабенко О. І.': [],
                'Білай-Рижова Ю. С.': [],
                'Трегуб Е. В.': [],
                'Бальченко І. С.': [],
                'Андрєєв Ю. Ф.': [],
                'Тушинський К. С.': [],
                'episode': []
                }
        df_complete_episodes = pd.DataFrame(data)

    if exit_flag:
        return

    #df_complete_episodes.set_index('id', inplace=True)
    status = "Епізоди завантажено"
    callback_status(frame, status)
    print(df_complete_episodes)
    print()

    # read DF Patients
    status = "Завантаження данних відвідувачів"
    callback_status(frame, status)
    try:
        df_patients = pd.read_excel("Patients.xlsx")
    except FileNotFoundError:
        df_patients = pd.DataFrame()

    status = "Данні відвідувачів завантажені"
    callback_status(frame, status)



    options = webdriver.FirefoxOptions()

    options.headless = True

    service = Service(executable_path='C:\\Users\\админ\\AutomMed\\geckodriver_64.exe')

    driver = webdriver.Firefox(service=service)


    driver.get("https://id.helsi.pro/")



    """ Authorization """

    if exit_flag:
        driver.quit()
        return

    status = "Авторизація: e-mail"
    callback_status(frame, status)

    print('look for email input line and send email')
    print()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#email'))).send_keys(email)

    if exit_flag:
        driver.quit()
        return

    status = "Авторизація: пароль"
    callback_status(frame, status)
    print('look for email input line and send key')
    print()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#usercreds'))).send_keys(key)



    if exit_flag:
        driver.quit()
        return

    status = "Авторизація"
    callback_status(frame, status)
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

    status = "Пошук відвідувача"
    callback_status(frame, status)
    print('look for button patient and press it')
    print()
    btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.col-xs-12:nth-child(6) > a:nth-child(1) > div:nth-child(1)')))
    time.sleep(2)
    btn.click()






    for index, row in df_patients.iterrows():

        if exit_flag:
            driver.quit()
            return
        second_name = row["Surname"]
        first_name = row["Name"]
        birthday_date = row["Birthday"]
        status = f"Відвідувач {second_name} {first_name} знайдений"
        callback_status(frame, status)
        print("#1", second_name, first_name, birthday_date)

        callback_lastname(frame, second_name)
        
        



        

        """ Cicle working with episodes """

        if exit_flag:
            driver.quit()
            return

        status = f"Введення данних відвідувача"
        callback_status(frame, status)
        
        print('look for input second name and send it')
        print()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div/div[2]/div/input'))).send_keys(second_name)

        if exit_flag:
            driver.quit()
            return
        
        print('look for line input first name')
        print()
        first_name_line = driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)')
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
        birthday_line = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/form/div[1]/div[3]/div/div[2]/div/div/input')

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
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.margin-left-offset-20 > button:nth-child(1)'))).click()

        if exit_flag:
            driver.quit()
            return

        

        print('look for button operation with patient')
        print()
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-text-lg > span:nth-child(1) > svg:nth-child(1)'))).click()
        except TimeoutException:
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.active > a:nth-child(1) > span:nth-child(1) > svg:nth-child(1)'))).click()
            print("Uncorrect data")
            # write data to specil file
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/form/div[1]/div[1]/div/div[2]/div/input'))).clear()
            driver.find_element(By.CSS_SELECTOR, 'div.form-group:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)').clear()
            driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/form/div[1]/div[3]/div/div[2]/div/div/input').clear()
            continue


        if exit_flag:
            driver.quit()
            return

        status = f"Перегляд епізодів відвідувача"
        callback_status(frame, status)
        
        print('look for button episode')
        print()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ant-dropdown-menu-item:nth-child(4) > span:nth-child(1) > a:nth-child(1)'))).click()

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

        status = f"Пошук епізоду Z02.3"
        callback_status(frame, status)

        # Check all episodes of current pacient
        for row in rows_episodes:
            if exit_loop:
                    print("!!! 4")
                    break
            cells = row.find_elements(By.TAG_NAME, 'td')
            i = 0
            for cell in cells:
                #print(i, '. ', cell.text)
                
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

                        status = f"Збір данних епізоду Z02.3"
                        callback_status(frame, status)
                        
                        if exit_flag:
                            driver.quit()
                            return
                        
                        selected_episode = cell
                        doctors_list = full_doctors_list.copy()
                        selected_episode.click()
                        print('look for all reception')
                        print()
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-table-tbody')))
                        time.sleep(3)

                        if exit_flag:
                            driver.quit()
                            return
                        
                        status_episode = driver.find_element(By.CSS_SELECTOR, 'div.col-md-12:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
                        print('status: ', status_episode.text)
                        print()

                        if exit_flag:
                            driver.quit()
                            return 

                        date = driver.find_element(By.CSS_SELECTOR, 'div.col-md-12:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
                        create_episode = datetime.strptime(date.text[:10], '%d.%m.%Y')
                        print('create: ', create_episode)
                        print()

                        if exit_flag:
                            return 


                        num_episode = driver.find_element(By.CSS_SELECTOR, '.col-md-4 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
                        print('num_episode: ', num_episode.text)
                        print()
                        

                        
                        if exit_flag:
                            driver.quit()
                            return
                        
                        receptions = driver.find_element(By.CSS_SELECTOR, '.ant-table-tbody')
                        rows_receptions = receptions.find_elements(By.TAG_NAME, 'tr')
                        # Check all punkts of current episode
                        for row in rows_receptions:
                            
                            if exit_flag:
                                driver.quit()
                                return
                            
                            cells_episode = row.find_elements(By.TAG_NAME, 'td')
                            j = 0
                            for cell_episode in cells_episode:
                                #print('#', cell_episode.text)
                                if j == 5:
                                    #print('Here!')
                                    if cell_episode.text in doctors_list:
                                        
                                        doctors_list.remove(cell_episode.text)                     
                                j = j + 1
                        if status_episode.text == 'Завершений':
                            ready_episode = "Closed"
                        elif create_episode < dead_time:
                            ready_episode = "Delay"
                        elif not doctors_list:
                            ready_episode = "Ready"
                        else:
                            ready_episode = "Not ready"
                        
                        if not df_complete_episodes['episode'].str.contains(num_episode.text).any():
                            series_index = len(df_complete_episodes) + 1
                        else:
                            series_index = df_complete_episodes.loc[df_complete_episodes['episode'] == num_episode.text].index[0]+1
                        
                        
                        
                        data_episode = {'id': series_index,
                                        'Ready': ready_episode,
                                        'Status' : status_episode.text,
                                        'Creation' : date.text[:10],
                                        'Surname': second_name,
                                        'Name': first_name,
                                        'Birthday': birthday_date,
                                        'Прудченко О. В.': True,
                                        'Бабенко О. І.': True,
                                        'Білай-Рижова Ю. С.': True,
                                        'Трегуб Е. В.': True,
                                        'Бальченко І. С.': True,
                                        'Андрєєв Ю. Ф.': True,
                                        'Тушинський К. С.': True,
                                        'episode': num_episode.text,
                                        }

                        
                        new_episode = pd.Series(data_episode)
                        print(new_episode)
                  
                                                       

                        
                        if doctors_list:
                            for doctor in doctors_list:
                                new_episode[doctor] = False


                        
                        
                        if not df_complete_episodes['episode'].str.contains(num_episode.text).any():
                            print('!!! 1')
                            df_complete_episodes = pd.concat([df_complete_episodes, new_episode.to_frame().T], ignore_index=True)
                        else:
                            row_index = df_complete_episodes.loc[df_complete_episodes['episode'] == num_episode.text].index[0]
                            for key, value in new_episode.items():
                                df_complete_episodes.at[row_index, key] = value
                            print('!!! 2')

                        exit_loop = True
                        print("!!! 3")
                        break
                                        
                        
                    else:
                        # Not episode z02.3                   
                        break
                
                
                i = i + 1

        
                 
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.active > a:nth-child(1) > span:nth-child(1) > svg:nth-child(1)'))).click()

        if index == len(df_patients) - 1:
            status = f"Завантаження данних епізода Z02.3 у файл"
            callback_status(frame, status)
            df_complete_episodes.to_excel("Complete_Episodes.xlsx", index=False)
            
    if exit_flag:
        driver.quit()
        return 

    app.MainLoop()


if __name__ == "__main__":
    main_logic(MyFrame.update_display_lastname, MyFrame.update_display_status)



