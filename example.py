import time
import datetime
import csv
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

TIME_DELAY = 300

# Create web driver
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)

# website that holds live occupancy data
driver.get("https://bewell.ese.syr.edu/FacilityOccupancy")

header = ["Date", "Time", "Occupancy %"]
with open("test.csv", 'w', newline="") as file:
    csvwriter = csv.writer(file) # 2. create a csvwriter object
    csvwriter.writerow(header) # 4. write the header
    #csvwriter.writerows(data) # 5. write the rest of the data

while True:
    occ = driver.find_element(By.XPATH, '//*[@id="occupancy-aa8c6536-b2ea-4b48-90e6-5df79edc5494"]/div[1]/div[2]/p[3]/strong')
    write_string = "[" + str(datetime.datetime.now()) + "] - Occupancy Rate: " + occ.text + "\n"
    file_string = str(datetime.date.today()) + "_occupancy_data.csv"
    #file1 = open(file_string, "a")
    #file1.writelines(write_string)
    #file1.close()
    data = [[datetime.date.today(), str(datetime.datetime.now()).split(" ")[1].split(".")[0], occ.text]]
    with open(file_string, 'a', newline="") as file:
        csvwriter = csv.writer(file)  # 2. create a csvwriter object
        #csvwriter.writerow(header)  # 4. write the header
        csvwriter.writerows(data) # 5. write the rest of the data

    print("[", datetime.datetime.now(), "] - Occupancy Rate:", occ.text)
    time.sleep(TIME_DELAY)
    driver.refresh()
