import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pyodbc
import os

mydir = os.getcwd()
filename = f'{mydir}\movies.csv'
topic_url ='https://www.imdb.com/search/title/?genres=crime&explore=title_type,genres&ref_=adv_prv'



drop1 = """
drop table if exists public.movies_list
"""
create1 = """
create table public.movies_list 
(
	name text,
	year text,
	certificate text,
	duration text,
	rating text 
)
"""
copy_query = f"COPY public.movies_list FROM '{filename}' DELIMITER ',' CSV HEADER;"

def run_sql(dsn, query):
    conn = pyodbc.connect(f'DSN={dsn}', autocommit=True)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.close()


def get_topics_page():
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception(f'Failed to load page {topic_url}')
    # Save the entire page's contents for reference.
    with open('webpage.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    # Parse the entire response text.
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

def get_movie_name(doc):
    selection_class = "lister-item-header"
    movie_name_tags = doc.find_all('h3', {'class': selection_class})
    movie_names = [tag.find('a').text if tag.find('a') else 'N/A' for tag in movie_name_tags]
    return movie_names

def get_movie_year(doc):
    year_selector = "lister-item-year text-muted unbold"
    movie_year_tags = doc.find_all('span', {'class': year_selector})
    movie_year = [tag.get_text().strip() for tag in movie_year_tags]
    return movie_year

def get_certificate(doc):
    selection_class = "certificate"
    movie_certificate_tags = doc.find_all('span', {'class': selection_class})
    movie_certificate = [tag.text[:10] for tag in movie_certificate_tags]
    return movie_certificate

def get_duration(doc):
    selection_class = "runtime"
    movie_duration_tags = doc.find_all('span', {'class': selection_class})
    movie_duration = [tag.text[:10] for tag in movie_duration_tags]
    return movie_duration


def get_rating(doc):
    rating_selector = "inline-block ratings-imdb-rating"
    movie_rating_tags = doc.find_all('div', {'class': rating_selector})
    movie_rating = [tag.get_text().strip() for tag in movie_rating_tags]
    return movie_rating

def get_director(doc):
    # Find the directors using more precise selection
    movie_director_tags = doc.select(".lister-item-content p:has(.director) a")
    movie_directors = [tag.text for tag in movie_director_tags]
    return movie_directors


def imdb_dict():
    movies_dictionary = {
        'Name': [],
        'Year': [],
        'Certificate': [],
        'Duration': [],
        'Rating': [],
        #'Director': [],
    }

    # Loop through the paginated URLs
    for i in range(1, 2000, 100):
        time.sleep(5)
        url = 'https://www.imdb.com/search/title/?genres=crime&start=' + str(
            i) + '&explore=title_type,genres&ref_=adv_nxt'

        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to load page {url}")
                continue

            # Parse using BeautifulSoup
            doc = BeautifulSoup(response.text, 'html.parser')
            name = get_movie_name(doc)
            year = get_movie_year(doc)
            certificate = get_certificate(doc)
            duration = get_duration(doc)
            rating = get_rating(doc)
            #director = get_director(doc)

            # Ensure consistency for this specific page
            max_len = max(len(name), len(year), len(certificate), len(duration), len(rating)) #, len(director))
            while len(name) < max_len: name.append('N/A')
            while len(year) < max_len: year.append('N/A')
            while len(certificate) < max_len: certificate.append('N/A')
            while len(duration) < max_len: duration.append('N/A')
            while len(rating) < max_len: rating.append('N/A')
            #while len(director) < max_len: director.append('N/A')

            # Add movie data to dictionary
            movies_dictionary['Name'].extend(name)
            movies_dictionary['Year'].extend(year)
            movies_dictionary['Certificate'].extend(certificate)
            movies_dictionary['Duration'].extend(duration)
            movies_dictionary['Rating'].extend(rating)
            #movies_dictionary['Director'].extend(director)

            # Add movie data to dictionary
            movies_dictionary['Name'].extend(name)
            movies_dictionary['Year'].extend(year)
            movies_dictionary['Certificate'].extend(certificate)
            movies_dictionary['Duration'].extend(duration)
            movies_dictionary['Rating'].extend(rating)
            #movies_dictionary['Director'].extend(director)
        except Exception as e:
            print(f"Error processing page {url}: {e}")

    return pd.DataFrame(movies_dictionary)


def main():
    start_time = time.time()
    try:
        final_df = imdb_dict()
        final_df.to_csv('movies.csv',index=None, encoding='utf-8-sig')
	final_df = final_df.drop_duplicates()
        run_sql('postgresys', drop1)
        run_sql('postgresys', create1)
        run_sql('postgresys', copy_query)
    except Exception as e:
        print(e)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == '__main__':
    main()
