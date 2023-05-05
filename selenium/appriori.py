import re
from flask.signals import Namespace
from flask import Flask,render_template, url_for,request,redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flaskext.mysql import MySQL
import requests
import time
import os
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from browsermobproxy import Server
from selenium import webdriver;
from selenium.webdriver.chrome.options import Options;
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import Curry_K8S_Mail 
import selenium_testing
import threading



login_manager = LoginManager()

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://****'
#db= SQLAlchemy(app)


###################### DataBase Connection #################
#mysql = MySQL()
#app.config['MYSQL_DATABASE_USER'] = '****'    # default user of MySQL to be replaced with appropriate username
#app.config['MYSQL_DATABASE_PASSWORD'] = '****' # default passwrod of MySQL to be replaced with appropriate password
#app.config['MYSQL_DATABASE_DB'] = '****'  # Database name to be replaced with appropriate database name
#app.config['MYSQL_DATABASE_HOST'] = '****' # default database host of MySQL to be replaced with appropriate database host

#initialise mySQL
#mysql.init_app(app)
#create connection to access data
#conn = mysql.connect()





#class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key= True)
#    content = db.Column(db.String(200), nullable=False)
#    completed = db.Column(db.Integer, default=0)
#    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#    def __repr__(self):
#        return '<Task %r>' % self.id

'''
class user(db.Model):
     id = db.Column(db.Integer, primary_key= True)
     username = db.Column(db.String(30), unique=True)
     password = db.Column(db.String(200))
     date_created = db.Column(db.DateTime, default=datetime.utcnow)

     def __repr__(self):
        return '<Task %r>' % self.id
    
class wrm_up_st(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    sys_id = db.Column(db.String(200))
    Namespace = db.Column(db.String(200), default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
'''

#@app.route('/', methods=['POST','GET'])

    

def index():
       # lista = []
        #lista =  Wrm_up_st().final_list()
        
        return render_template('index.html')



@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
       
        if username == 'admin' and password == 'admin':
                return render_template('index.html') 
        else:
                return render_template('login.html') 
    else:
     
        return render_template('login.html')





@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'POST':
        add_user_name = request.form['username']
        add_user_password = request.form['userpassword']
        new_task_username = user(username = add_user_name)
        new_task_userpassword = user(password = add_user_password)
        try:
            db.session.add(new_task_username,add_user_password)
            
            db.session.commit()    
        
            return redirect('/admin')
        except:
            return "there was an issue adding your tasks!!!!!"
    else:
        return render_template('admin.html')

@app.route('/running-test',methods=['POST','GET'])    
def redirect():
    global msisdn,header,project,url,mail,icarus_3lc,curry_3lc
    
    msisdn = request.args['msisdn']
    header = request.args['header_value']
    project = request.args['project']
    url = request.args['url']
    mail = request.args['mail']
    icarus_3lc = request.args['icarus']
    curry_3lc = request.args['curry']
    
    
    return render_template('testing.html',msisdn = request.args['msisdn'],header = request.args['header_value'],project = request.args['project']\
                           ,url = request.args['url'],mail = request.args['mail'],icarus_3lc = request.args['icarus'],curry_3lc = request.args['curry'])

  
@app. route('/run_the_script',methods=['POST','GET'])

def run_the_scripts():
    global cnt
    cnt =0 
    ############################### Call Test Function  ##########################################
    app_testing = selenium_testing.Selenium_Testing();
    #try:
        #app_testing.execute_normal_flow(header,msisdn,url);
    #except:
    cnt =25
    print(cnt)
    time.sleep(1)
        ############################### Call K8S  application  ##########################################
        #Curry_K8S_Mail.logs_db(curry_3lc,msisdn)
    cnt =50
    time.sleep(1)
    print(cnt)
        ############################### Call Curry logs application  ####################################
        #Curry_K8S_Mail.syslogs_db(icarus_3lc,msisdn)
    cnt = 75
    time.sleep(1)
    print(cnt)
        ############################### Call mail   application  ##########################################
        #Curry_K8S_Mail.recipient_mail(mail)
    time.sleep(1)
    cnt = 100
    print(cnt)
    
    return  render_template('testing.html', cnt=cnt)
   # return render_template('testing.html',code1 = request.args['msisdn'],code2 = request.args['header_value'],code3 = request.args['project'],code4 = request.args['url'],code5 = request.args['mail'])

#@app. route('/progress_bar_function',methods=['POST','GET'])

#def bar_counter():
#    print('dio')
#    while cnt < 100:
#        return cnt
    

  

if __name__ == "__main__":
        
        app.run(debug=True) 
        app.run(host='0.0.0.0', port=****)
