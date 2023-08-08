import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import shutil
import traceback
from email.message import EmailMessage
import smtplib
import pandas as pd

dst_path = r"****"
download_path = r"****"
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {"download.default_directory": download_path})


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

def wait_for_download(download_path, filename, timeout=60):
    """
    We wait for 1 minute in order for one file to be downloaded to avoid an infinite loop.
    Else the program stops
    """
    file_path = os.path.join(download_path, filename)
    start_time = time.time()  # Start the timer

    while not os.path.isfile(file_path):
        time.sleep(1)
        if time.time() - start_time > timeout:  # Check if the timeout has been exceeded
            raise TimeoutError(f"Download of {filename} timed out after {timeout} seconds")

    return file_path  # This is the full path to the downloaded file

def move_file(file_path, dst_path):
    shutil.move(file_path, dst_path)

def login_actions():
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    log_screen("Trying to log in to **** portal")
    # Navigate to the page
    driver.get('****')
    # Xpath Location for username and password credentials
    username_xpath = r'//*[@id="username"]'
    password_xpath = r'//*[@id="password"]'
    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.XPATH, username_xpath)

    username_field.send_keys('****')
    password_field = driver.find_element(By.XPATH, password_xpath)
    password_field.send_keys('****')

    # Press enter/return after you're done typing in each field
    password_field.send_keys(Keys.RETURN)
    log_screen("Successfully log in")
    # Wait for the next page to load
    driver.implicitly_wait(5)

def construction_orders_ibt():
    # Click on Orders dropdown and select Order Search Option
    select_construction_orders_xpath = f'//*[@id="navbar-form"]/nav/ul/li[1]'  
    ibt_order_search_xpath = '//*[@id="navbar-form"]/nav/ul/li[1]/ul/li[1]'  

    # Click the dropdown
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, select_construction_orders_xpath)))
    dropdown.click()

    # Click the option
    option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, ibt_order_search_xpath)))
    option.click()

def ibt_order_search():
    """
    Here we are inside the IBT page, and we insert keys on form
    """
    # the keys that we insert on form to download the corresponding file report.
    asb_keys = ['56',  '69', '1', '4' ]
    # Each downloaded folder is named as ibt-orders.xls. So for each key, we move and rename the corresponding data folder
    dst_paths = [
        r'****.xls',
        r'****.xls',
        r'****.xls',
        r'****.xls'
    ]
    number_of_results_xpath = '//*[@id="searchCriteriaForm:j_idt129"]/tbody/tr[5]'  
    results_option_xpath = '//*[@id="searchCriteriaForm:nrOfResults_6"]' 
    search_button_xpath = '//*[@id="searchCriteriaForm:searchButton"]'  
    downloaded_file_xpath = '//*[@id="searchResultForm:orderSRT:exportData"]/em' 

    for key, dst_path in zip(asb_keys, dst_paths):
        time.sleep(5)

        # Try to find the clear option and click it if it exists
        try:
            clear_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, clear_asb_key)))
            clear_button.click()
            log_screen("Cleared previous ASB key")
        except:
            log_screen("No previous ASB key to clear")

        log_screen(f"Accessing Key : {key}")
        asb_gridcell_xpath = '//*[@id="searchCriteriaForm:asb_input"]'  
        clear_asb_key = '//*[@id="searchCriteriaForm:asb"]/ul/li[1]/span[1]' 
        

        # Find the key input field and enter the keys
        asb_input_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, asb_gridcell_xpath)))
        asb_input_field.click()
        asb_input_field.send_keys(key)
        driver.implicitly_wait(5)
        time.sleep(5)
        

        try:
            # Click the number of results dropdown
            dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, number_of_results_xpath)))
            dropdown.click()
            log_screen("Click on Number of results option")
            time.sleep(10)

            # Find and Click the '2500' option from the Search Dropdown
            try:

                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, results_option_xpath)))
                option = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, results_option_xpath)))
                option.click()
                log_screen("Selected 2500 results Option")
            except :
                # Here we execute a Java script click because the element is not accessible when you first enter it
                time.sleep(10)
                element = driver.find_element(By.XPATH, results_option_xpath)
                driver.execute_script("arguments[0].click();", element)
                log_screen("Selected 2500 results Option")


            # Find and Click the search button
            search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
            search_button.click()
            log_screen("Clicked on Search Option")
            time.sleep(10)


            # Find the download button and click it
            download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, downloaded_file_xpath)))
            download_button.click()
            log_screen(f"Downloaded file for ASB key : {key}")
            time.sleep(10)

            file_path = wait_for_download(download_path, 'ibt-orders.xls', timeout=60)  # get the full path to the downloaded file
            move_file(file_path, dst_path)
            log_screen(f"Moved File for Key : {key}. Destination path is : {dst_path}")
            driver.implicitly_wait(5)
            time.sleep(5)
        except Exception as e:
            log_screen("Exception occurred: " + str(e) + "\n" + traceback.format_exc())

def construction_orders_property():
    """
    We Click on Orders dropdown and select Property Search Option.
    """
    select_construction_orders_xpath = f'//*[@id="navbar-form"]/nav/ul/li[1]'  
    property_search_xpath = '//*[@id="navbar-form"]/nav/ul/li[1]/ul/li[3]/a' 
    number_of_results_dropdown = '//*[@id="searchCriteriaForm:nrOfResults"]/div[3]/span' 
    result_option = '//*[@id="searchCriteriaForm:nrOfResults_6"]' 
    search_option = '//*[@id="searchCriteriaForm:searchButton"]/span[2]' 
    downloaded_file_xpath = '//*[@id="searchResultForm:propertySearchSRT:exportPropertiesData"]/em'
    asb_keys = ['56', '69','1', '4']

    dst_paths = [
        r'****.xls',
        r'****.xls',
        r'****.xls',
        r'****.xls'
    ]

    # Click the dropdown
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, select_construction_orders_xpath)))
    dropdown.click()
    log_screen("Clicked On Orders Dropdown")

    # Click the option
    option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, property_search_xpath)))
    option.click()
    log_screen("Clicked on Property Search Option")

    for key, dst_path in zip(asb_keys, dst_paths):

        # Try to find the clear option and click it if it exists
        try:
            clear_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, clear_asb_key)))
            clear_button.click()
            log_screen("Cleared previous key")
        except:
            log_screen("No previous key to clear")

        log_screen(f"Accessing ASB Key : {key}")
        asb_gridcell_xpath = '//*[@id="searchCriteriaForm:asb_input"]'
        clear_asb_key = '//*[@id="searchCriteriaForm:asb"]/ul/li[1]/span[1]'

        # Find the input field and enter the keys
        asb_input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, asb_gridcell_xpath)))
        asb_input_field.click()
        asb_input_field.send_keys(key)
        driver.implicitly_wait(5)
        time.sleep(5)

        
        # Click the number of results dropdown
        try:
            dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, number_of_results_dropdown)))
            dropdown.click()
            log_screen("Click on Number of results option")
            time.sleep(10)

            try:
                # Find and Click the '2500' option from the Search Dropdown
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, result_option)))
                option = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, result_option)))
                option.click()
                log_screen("Selected 2500 results Option")
            except :
                # Here we execute a Java script click because the element is not accessible when you first enter it
                time.sleep(10)
                element = driver.find_element(By.XPATH, result_option)
                driver.execute_script("arguments[0].click();", element)
                log_screen("Selected 2500 results Option")
                

            # Find and Click the search button
            search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, search_option)))
            search_button.click()
            log_screen("Clicked on Search Option")
            time.sleep(10)

            # Find the download button and click it
            download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, downloaded_file_xpath)))
            download_button.click()
            log_screen(f"Downloaded file for key : {key}")
            time.sleep(10)

            file_path = wait_for_download(download_path, '****.xls', timeout=60)  # get the full path to the downloaded file
            move_file(file_path, dst_path)
            log_screen(f"Moved File for ASB Key : {key}. Destination path is : {dst_path}")
            driver.implicitly_wait(5)
            time.sleep(10)
        except Exception as e:
            log_screen("Exception occurred: " + str(e) + "\n" + traceback.format_exc())

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

def convert_files():
    # we convert the xls files to xlsx.
    files = os.listdir(dst_path)
    xls_files = [file for file in files if file.endswith('.xls')]
    if len(xls_files) == 0:
        log_screen("No xls files found to convert")
    else :
        log_screen(f"Trying to convert a total of {len(xls_files)} xls files")

    for file in xls_files:
        input_file = os.path.join(dst_path, file)
        output_file = os.path.join(dst_path, file.replace('.xls', '.xlsx'))

        #convert xls to xlsx
        df = pd.read_excel(input_file, engine='xlrd')
        df.to_excel(output_file, index=False, engine='openpyxl')
        log_screen(f"Converted {output_file}")
        os.remove(input_file)
        log_screen(f"Deleted {input_file}")
    



def main():
    try:
        login_actions()
        construction_orders_ibt()
        ibt_order_search() 
        construction_orders_property() 
        convert_files()  
    except TimeoutError as e:
        log_screen(f"Download failed: {e}")
        sent_mail("Issue with Scipt", "****", "****", f"Issue with Script. Check **** Error:\n{e}", '****')
    except Exception as e:
        log_screen(f"Download failed: {e}")
        sent_mail("Issue with Scipt", "****", "****", f"Issue with Script. Check **** Error:\n{e}", '****')

if __name__ == '__main__':
    log_screen("\n")
    main()
