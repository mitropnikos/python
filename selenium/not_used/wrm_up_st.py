# import requests module
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sys import argv
import logging
import time
import datetime
import os
import psycopg2

class Wrm_up_st():

  @staticmethod

    # Option from Chrome
  

  def final_list():
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--diasble-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options, executable_path="C:/Utility/chromedriver")
    base_url = "http://wrm.up.st/index.php"
    
    global lista 
    lista  = [[],[]]

    def login():
            driver.get(base_url)
            username = driver.find_element_by_name("username")
            username.send_keys("*****")
            password = driver.find_element_by_name("password")
            password.send_keys("******!!")
            driver.find_element_by_xpath("//button[text()='Sign In']").submit()
            time.sleep(2)
        
        
        

    def get_info():
            html_project_line= driver.find_elements_by_xpath("//table/tbody/tr")
            i = 1 
            
            while i < len(html_project_line):
                
                html_project_status = driver.find_element_by_xpath("//*[@id='example1']/tbody/tr[%s]/td[2]" % i)
                html_internal_code = driver.find_element_by_xpath("//*[@id='example1']/tbody/tr[%s]/td[3]" % i)
                html_icarus_type_code = driver.find_element_by_xpath("//*[@id='example1']/tbody/tr[%s]/td[4]" % i)
                #html_icarus_3l = driver.find_element_by_xpath("//*[@id='example1']/tbody/tr[%s]/td[7]" % i)  
                html_project_code = driver.find_element_by_xpath("//*[@id='example1']/tbody/tr[%s]/td[5]" % i)
                #print(html_project_status.text,html_internal_code.text,html_project_code.text,html_icarus_type_code.text)
                if html_project_status.text == 'ACTIVE' and html_icarus_type_code.text == 'NG':
                    lista[0].append([html_internal_code.text])
                    lista[1].append([html_project_code.text])   
                    #lista[2].append([html_icarus_3l.text])         
                i += 1
    
    
    def sql_insert():
        
    
          con = psycopg2.connect(database="*****", user="*****", password="*****",host="*****", port="*****")
          print("Connected To DB\n")
   
          
          cur = con.cursor()
          a  = lista[0]
          c = lista[1]
          for i in range(len(lista[0])):
           b = str(lista[0][i]).replace('[','').replace(']','')
           g = str(lista[1][i]).replace('[','').replace(']','')
           print (b)
           print (g)
           cur.execute("insert into public.wrm_upst (sys_id,namespace) VALUES  ({0},{1})".format(g,b))
           
       
          con.commit()
        #print(html_project_status.text,html_internal_code.text,html_project_code.text,html_icarus_type_code.text)
          con.close()
    def tearDown():
            driver.close()
        
   
    login()
    get_info()
    tearDown()
    sql_insert()
    print (lista[1])
   
    
    

    
a = Wrm_up_st().final_list()
print(a)
