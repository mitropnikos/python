import google_play_scraper as gps
import requests
from google_play_scraper import app, Sort, reviews
import pandas as pd
import time
import openpyxl

"""
This Script scans the provided applications and distinguishes them based on some criteria. Brief explanation : 

1. Code line 9 → Insert hardcoded the applications for investigation. 
2. Line 173 → Change the desired criteria. Note : If applications fullfil these criteria they will be marked as "undesired".
3. Line 189 → Apply the desired Rating. Applications with <= {Rating} will be marked as "undesired"
4. Line 190 → parse_apps_comments(scan_comments_count = 100) This line scans the last 100 comments for each app. Apply a new number if you want. 
Tested with Python 3.8
"""

#provide the desired applications
apps = [

]

##############################################################################
# define global vars
url = 'https://play.google.com/store/apps/details?id={app_name}'
app_not_on_playstore = [] #apps that does not exists on playstore
app_found_on_playstore = [] #apps that exists on playstore
app_with_score = []

app_with_with_no_rating = [] #apps with no rating
words_of_interest = {"fake", "scam", "ads"}
app_reviews = {} # need this dictionary to insert app reviews
filtered_apps = [] #insert apps that fullfil certain criterias



##############################################################################


def sort_applications():
    """
    This function distinguishes all aplications from the apps list
    and inserts them on two new lists.
    1. app_not_on_playstore -> applications that can not be found or have been removed on playstore
    2. app_found_on_playstore -> applications that are present on playstore
    """
    for app in apps:
        r = requests.get(url.format(app_name = app))

        if r.status_code == 200 :
            app_found_on_playstore.append(app)
        else :
            app_not_on_playstore.append(app)

def playstore_app_parse(rating):
    """
    This function loops over applications that exists on playstore and retrieves only the ones
    having a score -rating- less than the provided.
    """
    global low_scored_applications
    low_scored_applications = []  # low scored applications.

    for app in app_found_on_playstore:
        app_info = gps.app(app)
        stars = app_info['score']

        if stars is None:
            app_with_with_no_rating.append(app)

        if stars is not None and stars <= rating :
            low_scored_applications.append(app)
            print(f"Application with a score less or equal to {rating} are {low_scored_applications} ")


def parse_apps_comments(scan_comments_count):
    """
    This function searches the last `scan_comments_count` comments for every application that exists on playstore
    and tries to find the words of interest that is defined on global vars.
    """
    app_reviews = {}
    for app in app_found_on_playstore:
        result, continuation_token = reviews(app, lang='en', sort='newest', count=scan_comments_count)
        cnt_fake = 0
        cnt_scam = 0
        cnt_ads = 0
        num_comments = len(result)
        #print(f'{app} has a length of {num_comments} comments')

        for review in result:
            words = review['content'].lower().split()
            for word in words:
                if word in words_of_interest:
                    if word == "fake":
                        cnt_fake += 1
                    elif word == "scam":
                        cnt_scam += 1
                    else:
                        cnt_ads += 1

        app_reviews[app] = {"fake_count": cnt_fake, "scam_count": cnt_scam, "ads_count": cnt_ads, "comments_scanned": num_comments}

    print_dict = {}
    print_dict["headers"] = ["app", "fake_count", "fake_count_percentage", "scam_count", "scam_count_percentage", "ads_count", "ads_count_percentage", "comments_scanned"]

    rows = []

    for app, counts in app_reviews.items():
        #handle applications with zero comments
        if counts['comments_scanned'] == 0:
            fake_count_percentage = 0

        else:
            fake_count_percentage = (counts['fake_count']/counts['comments_scanned']) * 100
            scam_count_percentage = (counts['scam_count']/counts['comments_scanned']) * 100
            ads_count_percentage = (counts['ads_count']/counts['comments_scanned']) * 100
            #collect applications that fullfil certain criteria
            if fake_count_percentage >= 40 or scam_count_percentage >= 10 or ads_count_percentage >= 50:
                row = [app, counts['fake_count'], fake_count_percentage, counts['scam_count'], scam_count_percentage, counts['ads_count'], ads_count_percentage, counts['comments_scanned']]
                rows.append(row)
                filtered_apps.append(app)

    print_dict["rows"] = rows
    return print_dict

def main() :
    start_time = time.time()

    sort_applications()
    print(f"Applications that can not be found on Playstore are : {app_not_on_playstore}")
    print(f"Applications that exists on Playstore are : {app_found_on_playstore}")
    print(f"Applications that have no Rating on Playstore are: {app_with_with_no_rating}\n")

    playstore_app_parse(rating = 3.5) #provide the desired rating
    print_dict = parse_apps_comments(scan_comments_count = 100) # store the returned value in a var
    print(f"Filtered applications With High Scam-Ads-Fake comments are : {filtered_apps}\n")

    app_for_blacklist = filtered_apps + app_not_on_playstore + low_scored_applications
    print(f"Applications for blacklist are : {app_for_blacklist}")


    df1 = pd.DataFrame(print_dict["rows"], columns=print_dict["headers"]) # Dataframe for filtered apps
    df2 = pd.DataFrame(app_not_on_playstore, columns=["App Not Found on Playstore"]) #Dataframe for applications that does not exists on playstore
    df3 = pd.DataFrame(low_scored_applications, columns=['Low Scored Apps']) # Dataframe for low scored applications
    df4 = pd.DataFrame(app_for_blacklist, columns=['Apps For Blacklist']) # Unified Dataframe

    #pandas to excel
    with pd.ExcelWriter('app_reviews.xlsx') as writer:
        df1.to_excel(writer, sheet_name='App Reviews', index=False)
        df2.to_excel(writer, sheet_name='App Not Found on Playstore', index=False)
        df3.to_excel(writer, sheet_name='Low Scored Apps', index=False)
        df4.to_excel(writer, sheet_name='Apps For Blacklist', index=False)


    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.4f} seconds")

if __name__ == '__main__':
    main()
