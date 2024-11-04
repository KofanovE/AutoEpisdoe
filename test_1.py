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

import sys
import gdown

# url1 = ''
# output1 = 'test_result.xlsx'
# gdown.download(url1, output1, quiet=False)



url = 'https://docs.google.com/spreadsheets/d/1Lwx58yCppkgGyYbD7cggbnrwHcoPbY6E/edit?usp=drive_link&ouid=107426601535608784608&rtpof=true&sd=true'

output2 = 'test_result_2.xlsx'
gdown.download(url=url, output=output2, fuzzy=True)

#df1 = pd.read_excel(output1)
df2 = pd.read_excel(output2)
# df2.loc[df2['surname'] == 'Кофанов', 'info_1'] = 1
# df2.to_excel(output2, index=False)


print(df2)
