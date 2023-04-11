import time
import datetime
import csv
import sys
import pyodbc
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

TIME_DELAY = 300
VERBOSE = False
WRITE = False

# Checks for verbose mode and enables it
if len(sys.argv) == 2:
    if sys.argv[1] == "-v" or sys.argv[1] == "-verbose":
        VERBOSE = True

print("----LAUNCHED----\n" if VERBOSE else "", end='')

# Create web driver
op = webdriver.ChromeOptions()
# launches chromium w/ no GUI
op.add_argument('headless')
# I have no idea what these do but this makes it work on Ubuntu VM
op.add_argument("--disable-dev-shm-usage")
op.add_argument("--no-sandbox")
op.add_argument("--remote-debugging-port=9222")

# Creates web driver object with enabled options
print("Creating web driver...\n" if VERBOSE else "", end='')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
print("Web driver created successfully\n" if VERBOSE else "", end='')

# Create SQL connection
cnxn = pyodbc.connect('Driver={/opt/homebrew/lib/libmsodbcsql.18.dylib};'
                      'Server=tcp:tylav-data.database.windows.net,1433;'
                      'Database=Ty_Data;'
                      'Uid=tylav;Pwd=allDaData7!;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30')
cursor = cnxn.cursor()

# website that holds live occupancy data
driver.get("https://bewell.ese.syr.edu/FacilityOccupancy")

while True:
    current_hour = datetime.datetime.now().hour
    dayOfWeek = datetime.datetime.now(pytz.timezone('America/New_York')).weekday()
    if ((current_hour >= 9 and dayOfWeek <= 4) or (current_hour >= 11 and dayOfWeek > 4)) and current_hour < 23:
        occ = driver.find_element(By.XPATH, '//*[@id="occupancy-aa8c6536-b2ea-4b48-90e6-5df79edc5494"]/div[1]/div[2]/p[3]/strong')
        dayOfWeekStr = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%A'))
        date_str = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d'))
        time_str = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S'))
        occupancy = occ.text.strip('%')

        cursor.execute(f"INSERT INTO ERDAP (LogDate, LogTime, Occupancy, DayOfWeek) VALUES ('{date_str}', '{time_str}', '{occupancy}', '{dayOfWeekStr}');")
        cnxn.commit()

        print(date_str, time_str, occupancy, dayOfWeek)
    else:
        print("Gym Closed: No data retrieved")
    time.sleep(TIME_DELAY)
    driver.refresh()
