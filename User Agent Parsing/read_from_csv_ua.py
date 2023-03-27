import csv
import pandas as pd
from user_agents import parse

"""
    A script that reads the useragents for the corresponding files and finds the common values
    Tested with  Python 3.8.10

"""



c44_ua = []
c44_new = []

with open('c44_user_agents.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            c44_ua.append(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

for row in c44_ua:
    row = ''.join(row)
    ua_string = row
    user_agent = parse(ua_string)
    os = user_agent.os.family
    family = user_agent.browser.family
    shortcut = str(user_agent)
    browser_version = user_agent.browser.version

    if not browser_version :
        browser_version = ['null']
        a = browser_version[0]
    if browser_version:
        a = browser_version[0]

    touches = user_agent.is_touch_capable
    bot = user_agent.is_bot


    information = str(os) + ',' + (str(family) + ' ' + str(a)) + ',' + str(touches) + ',' +  str(bot) + ',' + str(shortcut)
    c44_new.append(information)


c65_ua = []
c65_ua_new = []



with open('c65_user_agents.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            c65_ua.append(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

for row in c65_ua:
    row = ''.join(row)
    ua_string = row
    user_agent = parse(ua_string)
    os = user_agent.os.family
    family = user_agent.browser.family
    shortcut = str(user_agent)
    browser_version = user_agent.browser.version

    if not browser_version :
        browser_version = ['null']
        a = browser_version[0]
    if browser_version:
        a = browser_version[0]

    touches = user_agent.is_touch_capable
    bot = user_agent.is_bot


    information = str(os) + ',' + (str(family) + ' ' + str(a)) + ',' + str(touches) + ',' +  str(bot) + ',' + str(shortcut)
    c65_ua_new.append(information)

common_list = set(c44_new).intersection(c65_ua_new)
print(common_list)
