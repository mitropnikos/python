import requests
import time
import os
import js2py
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from browsermobproxy import Server
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from bs4 import BeautifulSoup  
from urllib.request import urlopen
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from browsermobproxy import Server
from selenium import webdriver;



class Selenium_Testing():
  
  def execute_normal_flow(self,header,msisdn,url):
    
    #########################select proxy and chromedrive ###################################################
    dict={'port':****}
    server = Server("C:/Utility/browsermob-proxy-2.1.4/bin/browsermob-proxy",options=dict)
    server.start()
    proxy = server.create_proxy()

    #########################star chromedrive ###################################################
    opt = webdriver.ChromeOptions()
    opt.add_argument("--proxy-server={0}".format(proxy.proxy))
    #opt.add_argument('headless')
    browser = webdriver.Chrome("C:/Utility/chromedriver",chrome_options=opt)
      
    ############################### Execute Normal Flow #########################################
    proxy.headers({ header : msisdn })
    url = url
    browser.get(url);

    ############################### Find the elements of the 1st button  #########################################
    time.sleep(2)
    browser.save_screenshot('1st_page.png')
    time.sleep(2)
    browser.find_element_by_xpath("//input[contains(@class, 'button')]").click();
    browser.save_screenshot('2ond_page.png')
    time.sleep(2)
    

  
    divs_parent = browser.find_element_by_css_selector(".secured-button")
    divs_child = divs_parent.find_elements_by_css_selector("div")
    print(divs_child)
    
      
    for x_div in divs_child:
      time.sleep(0.1)
      css_opacity =  x_div.value_of_css_property('opacity')
      css_display=  x_div.value_of_css_property('display')
      css_height=  x_div.value_of_css_property('height')
      css_visibility= x_div.value_of_css_property('visibility')
      css_transform=  x_div.value_of_css_property('transform')
      css_position =  x_div.value_of_css_property('position')
      css_PropertyValue = x_div.value_of_css_property('getPropertyValue("z-index")')
      class_name = x_div.get_attribute("class")
      print(class_name," ",css_opacity," ",css_display," ",css_height," ",css_visibility," ",css_position," ",css_transform) 
      if (css_opacity == '1') and (css_display != 'none') and (css_height != '0px')  and ( css_visibility != 'hidden') and (css_position != 'absolute') \
      and (css_transform != 'matrix(1, 0, 0, 1, 9999, 0)'):
            
        print('in the condition_3_sdssssss' , "   ",class_name )
        a = str(class_name)
        browser.find_element_by_xpath("//*/div[@class='{}']/form[@method='post']/button[@type='submit']".format(str(a))).click();
        time.sleep(2)
        browser.save_screenshot('3rd_page.png')
        time.sleep(2)
       
      ############################### Close driver and testing app ####################################
    server.stop()
    browser.quit()
