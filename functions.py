import os
import requests
from bs4 import BeautifulSoup
import databaseCon
from collections import Counter


# Initialize database object
con = databaseCon.Database()


# Create text file to HDD
def save_text_file(path_and_filename, content):
    f = open(path_and_filename, "w+")
    f.write(content)
    f.close()


# Clean crawl posts
def clean_craw_post():
    folder = 'raw_posts'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


# Check post category label
def get_compare_category_label(category):
    cat = 'sport'
    if 'car_and_technology' in category:
        cat = 'car_and_technology'
    elif 'food' in category:
        cat = 'food'
    elif 'tourism' in category:
        cat = 'tourism'
    elif 'health_and_beauty' in category:
        cat = 'health_and_beauty'
    return cat


# Check post category identifier
def get_compare_category_identifier(category):
    identifier = 1
    if 'car_and_technology' in category:
        identifier = 3
    elif 'food' in category:
        identifier = 5
    elif 'tourism' in category:
        identifier = 2
    elif 'health_and_beauty' in category:
        identifier = 4
    return identifier


# Get post identifier from post link
def get_post_identifier(post_link):
    links = post_link.split('/')
    return links[len(links) - 1]


# Generate post filename
def generate_post_filename(category, post_link, num_post):
    return 'raw_posts/' + get_compare_category_label(category) + '.' + str(num_post) + '.' + get_post_identifier(post_link) + '.txt'


# Get post data from link
def get_post_data_from_online(link_post):
    article = requests.get(link_post)
    soup_article = BeautifulSoup(article.text, 'html.parser')
    query_title = soup_article.find_all('div', class_='container-inner')
    query_content = soup_article.find_all('div', class_='paragraph-style')
    post_content = query_title[0].h2.text + '\n\n'
    for para in query_content[0].find_all('p'):
        para_text = para.text.strip()
        post_content += para_text + '\n'
    return post_content


# Create dictionary from post
def make_dict():
    data_directory = "tokenized_posts/"
    files = os.listdir(data_directory)
    posts = [data_directory + post for post in files]
    words = []

    for category in categories:
        with open(category, encoding='utf-8') as f:
            if f is not None:
                content = f.read()
                words += content.splitlines()

    for i in range(len(words)):
        words[i] = words[i].strip()

    dict = Counter(words)
    del dict['']
    return dict.most_common(3000)


# Get category array
def get_category_arr():
    return ['sport', 'tourism', 'car_and_technology', 'health_and_beauty', 'food']


# Initialize category dictionary
def init_category_keywords():
    return {'sport': [], 'tourism': [], 'car_and_technology': [], 'health_and_beauty': [], 'food': []}


# Get folder of tokonized_posts group by categories
def get_tokenized_posts_group_by_category_folders():
    tokenized_posts_folder = 'tokenized_posts'
    categories = get_category_arr()
    category_folders = [tokenized_posts_folder + '/' + category for category in categories]
    tokenized_posts = []
    for category_folder in category_folders:
        files = os.listdir(category_folder)
        tokenized_posts += [category_folder + '/' + file for file in files]
    return tokenized_posts


# Clean khmer word
def clean_word(word):
    word = word.strip()
    clean_docs = ['\n', '«', '»', '៕', '។', 'ៗ', '!', '៖', ',', '?', ')', '(', '"']
    for clean_doc in clean_docs:
        word = word.replace(clean_doc, '')
    return word


# Delete previous keywords from database
def clean_table_db(table):
    sql = 'TRUNCATE TABLE ' + table
    databaseCon.Database.execute(con, sql)


# Save keywords to database
def save_keywords_db(category, keyword_dictionary):
    category_id = get_compare_category_identifier(category)
    sql = 'INSERT INTO keywords (category_id,text,frequency) VALUES '
    has_keyword = False
    for keyword, count in keyword_dictionary.items():
        has_keyword = True
        query = ' (' + str(category_id) + ',"' + keyword + '",' + str(count) + '),'
        sql += query

    sql = sql.strip()
    sql = sql[:-1]
    print('- Saved ' + category + ' keywords to database')
    if has_keyword:
        databaseCon.Database.execute(con, sql)
