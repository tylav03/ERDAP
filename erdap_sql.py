import time
import datetime
import csv
import sys
import pyodbc
import pytz
import requests
from bs4 import BeautifulSoup


TIME_DELAY = 300
VERBOSE = False
WRITE = False

# Checks for verbose mode and enables it
if len(sys.argv) == 2:
    if sys.argv[1] == "-v" or sys.argv[1] == "-verbose":
        VERBOSE = True

print("----LAUNCHED----\n" if VERBOSE else "", end='')

# Create SQL connection
cnxn = pyodbc.connect('Driver={/opt/homebrew/lib/libmsodbcsql.18.dylib};'
                      'Server=tcp:tylav-data.database.windows.net,1433;'
                      'Database=Ty_Data;'
                      'Uid=tylav;Pwd=allDaData7!;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30')
cursor = cnxn.cursor()

while True:
    current_hour = datetime.datetime.now().hour
    dayOfWeek = datetime.datetime.now(pytz.timezone('America/New_York')).weekday()
    if ((current_hour >= 9 and dayOfWeek <= 4) or (current_hour >= 11 and dayOfWeek > 4)) and current_hour < 23:
        occupancy = int(BeautifulSoup(requests.get(url='https://bewell.ese.syr.edu/FacilityOccupancy').text,
                                "html.parser").find_all("strong")[2].contents[0].strip("%"))

        dayOfWeekStr = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%A'))
        date_str = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%Y-%m-%d'))
        time_str = str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S'))

        cursor.execute(f"INSERT INTO ERDAP (LogDate, LogTime, Occupancy, DayOfWeek) VALUES ('{date_str}', '{time_str}', '{occupancy}', '{dayOfWeekStr}');")
        cnxn.commit()

        print(date_str, time_str, occupancy, dayOfWeek)
    else:
        print("Gym Closed: No data retrieved")
    time.sleep(TIME_DELAY)
    driver.refresh()
