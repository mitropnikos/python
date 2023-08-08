import datetime
import os
import sys
import shutil
import smtplib
from pyotp import TOTP
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from email.message import EmailMessage
import traceback

# Global Vars 
username = "****"
password = "****"
smtpsrv = "****"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"download.default_directory": r"****"})
download_path = r"****"

def log_screen(txt):
    """
    A function that creates a log file in the below folder for monitoring purposes.
    """
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_now + ' ' + txt)
    # ensure the logs directory exists    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    with open(r"****", "a") as f:
        f.write(f"{now} {txt}" + "\n")

def sent_mail(subject, senter, to, body, cc = None):
    """
    A function that is needed to sent an email message upon failure.
    CC resipients are optional
    """
    username = "****"
    password = "****"
    smtpsrv = "****"
    smtpserver = smtplib.SMTP(smtpsrv,587)
    msg = EmailMessage()
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(username, password)
    msg['Subject'] = subject
    msg['From'] = senter
    # Check if 'to' is list, if not make it a list
    if not isinstance(to, list):
        to = [to]
    msg['To'] = ', '.join(to)

    if cc:
        # Check if 'cc' is list, if not make it a list
        if not isinstance(cc, list):
           cc = [cc]     
        msg['Cc'] = ', '.join(cc)
    msg.set_content(f"{body}")
    smtpserver.send_message (msg)


def configure_driver():
    '''Set up Chrome driver'''
    return webdriver.Chrome(r'C:\UGG_FTTF\chromedriver', options=chrome_options)

def login(driver, username, password):
    '''Log in to Power BI with given username and password'''
    log_screen("Trying to log in to Power BI")
    driver.get("https://app.powerbi.com/groups/me/list?ctid=****")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))

    uname = driver.find_element("id", "email")
    uname.send_keys(username)

    driver.find_element("id", "submitBtn").click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "passwd")))
    psword = driver.find_element("name", "passwd")
    psword.send_keys(password)
    sleep(2)
    driver.find_element("id", "idSIButton9").click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "otc")))
    log_screen("Entered Credentials for log in to Power BI")
    driver.implicitly_wait(5)
    sleep(5)

    # Confirm MFA
    totp = TOTP("rc5nylfrs6bssvqz")
    driver.find_element("name", "otc").send_keys(totp.now())
    driver.find_element("id", "idSubmit_SAOTCC_Continue").click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='tri-header ng-star-inserted']")))
    log_screen("Confirmed MFA for log in")
    sleep(10)

def download_report(driver, report_url):
    '''Download a report from a given url'''
    driver.get(report_url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='scroll-bar-div']")))
    driver.find_element(By.XPATH, "//div[@class='scroll-bar-div']").click()
    driver.find_element(By.XPATH, "//button[@class='vcMenuBtn']").click()
    driver.find_element(By.XPATH, "//button[@title='Export data']").click()

    export = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='Export']")))
    export.click()

def wait_for_download():
    '''Wait until the file is downloaded'''
    while True:
        if any(fname.endswith('data.xlsx') for fname in os.listdir(r"****")):
            break
        else:
            sleep(5)


def move_file(dst_path):
    '''Move the downloaded file to a new location'''
    shutil.move(download_path, dst_path)


def parce_actions():
    ''' Function for Selenium Automation.
    Here we log on the corresponding URLs, search Site's elements, and download the data for each report
    '''
    driver = configure_driver()

    # Login to Power BI
    login(driver, username, password)

    # URLs for the reports
    report_urls = [
        "https://app.powerbi.com/groups/****", #Report1
        "https://app.powerbi.com/groups/****", #Report2
        "https://app.powerbi.com/groups/****", #Report3
        "https://app.powerbi.com/groups/****", #Report4
    ]
    # Paths to move downloaded files
    dst_paths = [
        r"****\Report1",
        r"****\Report2",
        r"****\Report3",
        r"****\Report4",
    ]

    # Download each report and move to the corresponding path
    for url, dst_path in zip(report_urls, dst_paths):
        download_report(driver, url)
        log_screen(f"Downloaded {url}")
        wait_for_download()
        move_file(dst_path)
        log_screen(f"Successfully moved file to {dst_path}")



def main():
    try:
        parce_actions()
    except Exception as e:
        log_screen(f"{e}" + traceback.format_exc())
        sent_mail("Issue withScipt", "****", "****", f"Issue with Script. Check **** Error:\n{e}", '****, ****')


if __name__ == '__main__':
    log_screen("\n")
    main()
