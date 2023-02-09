import datetime
import time
from pytz import timezone
import pandas as pd

import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By     # Need for xpath
from selenium.webdriver.chrome.options import Options   # Need for --headless browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def utc_to_pacific_time(utc_datetime):
    # UTC timestamp in string format
    utc_timestamp = utc_datetime

    # Convert the string to a datetime object
    utc_time = datetime.datetime.strptime(utc_timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Set the timezone to UTC
    utc_time = utc_time.replace(tzinfo=timezone('UTC'))

    # Convert the UTC time to Pacific Time
    pacific = timezone('US/Pacific')
    pacific_time = utc_time.astimezone(pacific)

    print(pacific_time)
    return pacific_time

def getBearToken(username, password,token_file_path):
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)

    driver.get("https://app.traceablelive.com/auth/login")

    driver.find_element(By.XPATH, '//a[@aria-label="dismiss cookie message"]').click()

    driver.find_element("name", "email").send_keys(username)
    driver.find_element("name", "password").send_keys(password)
    driver.find_element("id", "kt_login_signin_submit").click()

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "kt_header_menu")) #This is a dummy element
        )
    finally:
        time.sleep(1)
        print("Done Loading")

    logs = driver.get_log("performance")

    for entry in logs:
        if "Bearer" in str(entry["message"]):
            token = (entry["message"].split()[3]).split('"')[0]
            print(token)
            break

    driver.close()

    with open(token_file_path, "w") as file:
        file.write(token)

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def data_request(token_file_path):
    with open(token_file_path, "r") as file:
        token = file.read()

    response = requests.get(
        'https://traceablelivefd.azurefd.net/api/device/Device_BySerialNumber?SerialNumber=221317910',
        auth=BearerAuth(token))

    thermoData = json.loads(response.content.decode(encoding='UTF-8'))
    return thermoData


if __name__ == "__main__":
    token_file_path = "traceable_live_token.txt"
    filename = "thermometer_data.csv"       # Name of save data points CSV file
    while True:
        thermoData = data_request(token_file_path)         # Request Traceable Live Data

        if thermoData['Message'] == 'Authorization has been denied for this request.':  # Error
            print('Authorization has been denied for this request - Token Expired')     # Expired Token
            print('Getting New Token')

            getBearToken(username="hellorxpharmacy@gmail.com",             # Get New Token
                         password="2268Senterrd#202",
                         token_file_path=token_file_path)

            thermoData = data_request(token_file_path)      # Request Data Again

        # with open("data.json", "w") as outfile:
        #     # Write the JSON data to the file
        #     json.dump(thermoData, outfile)
        #
        # # Serializing json
        # with open("traceable_live_data.txt", "w") as file:
        #     file.write(json.dumps(thermoData, indent=4))

        UTC_Timestamp = thermoData["Item"]["DeviceSettings"][0]["Timestamp"]
        Pacific_TimeStamp = utc_to_pacific_time(UTC_Timestamp)
        freezerTemp = thermoData["Item"]["DeviceSettings"][1]["Reading"]
        fridgeTemp = thermoData["Item"]["DeviceSettings"][0]["Reading"]
        CalibrationDueDate = thermoData["Item"]["deviceModelSerialNumberKeyMap"]["CalibrationDueDate"]
        Battery = thermoData["Item"]["Battery"]
        SerialNumber = thermoData["Item"]["deviceModelSerialNumberKeyMap"]["SerialNumber"]
        DeviceKey = thermoData["Item"]["deviceModelSerialNumberKeyMap"]["DeviceKey"]
        Model = thermoData["Item"]["deviceModelSerialNumberKeyMap"]["Model"]
        Id = thermoData["Item"]["Id"]
        AccountId = thermoData["Item"]["AccountId"]

        print('Fridge Temp: ', fridgeTemp, 'F', datetime.datetime.now())
        print('Freezer Temp: ', freezerTemp, 'F', datetime.datetime.now())

        data = {'Pacific_TimeStamp':[Pacific_TimeStamp],
                'UTC_Timestamp':[UTC_Timestamp], 'freezerTemp':[freezerTemp], 'fridgeTemp':[fridgeTemp],
                'CalibrationDueDate':[CalibrationDueDate],'Battery':[Battery],
                'SerialNumber':[SerialNumber],'DeviceKey':[DeviceKey],'Model':[Model],'Id':[Id],'AccountId':[AccountId]}

        df = pd.DataFrame(data)

        # Appending the data to the CSV file
        df.to_csv(filename, mode='a', header=False, index=False)

        time.sleep(1800)
