import time
import datetime
import csv
import sys
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

TIME_DELAY = 5
VERBOSE = False

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
print("Web driver created successfully!\n" if VERBOSE else "", end='')


# website that holds live occupancy data
print("Opening webpage...\n" if VERBOSE else "", end='')
driver.get("https://bewell.ese.syr.edu/FacilityOccupancy")
print("Webpage opened successfully!\n" if VERBOSE else "", end='')

# determines the file name of the csv file on the date of creation
file_string = str(datetime.date.today()) + "_occupancy_data.csv"

# writes header to csv file
header = ["Date", "Time", "Occupancy %"]
with open(file_string, 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(header)

while True:
    # assigns occ with the HTML element object that contains the occupancy number using XPath
    print("Finding element...\n" if VERBOSE else "", end='')
    occ = driver.find_element(By.XPATH, '//*[@id="occupancy-aa8c6536-b2ea-4b48-90e6-5df79edc5494"]/div[1]/div[2]/p[3]/strong')
    print("HTML element found!\n" if VERBOSE else "", end='')

    # constructs 2D data array to be passed into the csv writer in format (date, time, occupancy)
    data = [[datetime.date.today(), str(datetime.datetime.now()).split(" ")[1].split(".")[0], occ.text]]

    # opens the csv file according to the date, if no file exists then one is created
    print("Opening CSV file...\n" if VERBOSE else "", end='')
    with open(file_string, 'a', newline="") as file:
        csvwriter = csv.writer(file)  # create the csvwriter object
        print("Writing to file...\n" if VERBOSE else "", end='')
        csvwriter.writerows(data) # write the data
    print("File written and closed successfully!\n" if VERBOSE else "", end='')

    # Prints out the occupancy data to the terminal when logged
    print("[", datetime.datetime.now(), "] - Occupancy Rate:", occ.text)

    # time to wait before next data point based on global variable TIME_DELAY
    time.sleep(TIME_DELAY)
    driver.refresh()
