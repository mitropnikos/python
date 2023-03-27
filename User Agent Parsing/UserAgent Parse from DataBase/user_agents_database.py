from user_agents import parse
import os
import pandas as pd
import csv
import pyodbc

"""
    A simple script that parses useragent from DB and appends the results to csv files.
    Tested with  Python 3.8.10

"""


##############################################################################################################################

# define vars

query1 = """
with v1 as
(
....
"""

query2 = """
with v1 as 
(....
"""

def get_sql_data (dsn, query) :
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    print(f"Connected to {dsn}")
    db = conn.cursor()
    db.execute(query)
    results = db.fetchall()
    return results
    db.close()
    cursor.close()

a = 'OS :'
b = 'Family : '
c = 'Touchable : '
d = 'BOT : '
e = 'PC : '
f = 'MOBILE : '
g = 'TABLET : '
aa = 'UA : '

c44_information = []
c65_information = []

def user_agent_parse (dataset, lst) :

    print("Begin Parsing")
    for i in dataset :
        os = ''
        family = ''
        shortcut = ''
        browser_version = ''
        touches = ''
        bot = ''
        pc = ''
        mobile = ''
        tablet = ''
        i = ''.join(i)
        ua_string = i
        user_agent = parse(ua_string)
        os = user_agent.os.family
        family = user_agent.browser.family
        shortcut = str(user_agent)
        browser_version = user_agent.browser.version

        if not browser_version:
            browser_version = ['null']
            a = browser_version[0]
        if browser_version:
            a = browser_version[0]

        touches = user_agent.is_touch_capable
        bot = user_agent.is_bot
        pc = user_agent.is_pc
        mobile = user_agent.is_mobile
        tablet = user_agent.is_tablet
        information = str(os) + ',' + (str(family) + ' ' + str(a) )+ ',' +  str(touches) + ',' + str(bot) + ',' + str(pc) + ',' + str(mobile) + ',' + str(tablet) + ',' + str(shortcut)
        lst.append(information)
###################################################################################################################################################


try :
    #Execute the programm for c44 key
    ua_c44key = get_sql_data('impalasys', query1)
    print("Query1 Finished")
    #parse the key as designed above
    user_agent_parse(ua_c44key, c44_information)
    #list to dataframe
    df = pd.DataFrame(c44_information)
    df.columns = ['OS,Family,Touchable,Bot,PC,Mobile,Tablet,Shortcut']
    #export to csv
    df.to_csv('c44_information_final.csv', header = True, index=False, sep='\t')
    print('Dataset has been exported to csv')

except Exception as e:
    print(e)


try :
    ua_c65key = get_sql_data('impalasys', query2)
    print("Query2 finished")
    user_agent_parse(ua_c65key, c65_information)
    df = pd.DataFrame(c65_information)
    df.columns = ['OS,Family,Touchable,Bot,PC,Mobile,Tablet,Shortcut']
    #export to csv
    df.to_csv('c65_information_final.csv', header = True, index=False, sep='\t')
    print('Dataset has been exported to csv')

except Exception as e:
    print(e)
