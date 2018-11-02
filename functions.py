import os
import requests
from bs4 import BeautifulSoup
import databaseCon
import pickle
from collections import Counter


# Initialize database object
con = databaseCon.Database()

# Frequency of keyword
keyword_frequency = 9


# Create text file to HDD
def save_text_file(path_and_filename, content):
    f = open(path_and_filename, "w+")
    f.write(content)
    f.close()


# Create classifier file from dataset
def save(clf, name):
    pickle.dump(clf, open(name, "wb"))


# Delete file
def delete_file(path_and_filename):
    try:
        if os.path.isfile(path_and_filename):
            os.unlink(path_and_filename)
    except Exception as e:
        print(e)


# Load classifier from file
def load_dataset(clf_file):
    return pickle.load(open(clf_file, "rb"))


# Clean crawl posts
def clean_craw_post():
    folder = 'raw_posts'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        delete_file(file_path)


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
    post_content = ''
    if query_title is not None and query_content is not None:
        post_content = query_title[0].h2.text + '\n\n'
        for para in query_content[0].find_all('p'):
            para_text = para.text.strip()
            post_content += para_text + '\n'
    return post_content


# Check whether keyword is exist
def check_trained_keyword_exist(category, keyword):
    query = 'SELECT * FROM keywords WHERE category_id=' + str(category) + ' AND text="' + keyword + '" LIMIT 1'
    query_keyword = databaseCon.Database.select_one(con, query)
    return query_keyword


# Save new keywords to the found category
def update_keyword_frequency(category, keyword, enable_msg = False):
    query_keyword = check_trained_keyword_exist(category, keyword)
    if query_keyword is None:
        update_query = 'INSERT INTO keywords(category_id,text,frequency) VALUES('
        update_query += str(category) + ',"' + keyword + '",1)'
        databaseCon.Database.execute(con, update_query)
        if enable_msg:
            print('==> Keyword: "' + keyword + '" was added to category: ' + str(category))
    else:
        frequency = int(query_keyword[3])
        if frequency < (keyword_frequency + 1):
            update_query = 'UPDATE keywords SET frequency=' + str(frequency + 1)
            update_query += ' WHERE id=' + str(query_keyword[0])
            databaseCon.Database.execute(con, update_query)
            if enable_msg:
                print('==> Keyword: "' + keyword + '" was updated frequency from ' + str(frequency) + ' to : ' + str(frequency + 1))


# Generate sample for none category keywords
def generate_none_category_keywords():
    return [[0, 'none'], [0, 'n/a'], [0, 'no'], [0, 'nothing']]


# Create keywords dictionary from database
def make_keywords_dictionary():
    # Select all keyword that happen more than 9 times
    query = 'SELECT category_id, text FROM keywords WHERE frequency > ' + str(keyword_frequency) + ' ORDER BY category_id;'
    query_result = databaseCon.Database.execute_query(con, query)
    # keywords = generate_none_category_keywords()
    keywords = []
    for result in query_result:
        keywords.append([result[0], result[1]])

    return keywords


# Create dictionary from post
def make_keywords_dataset(dictionary):
    features_set = []
    labels_set = []

    categories = [0, 1, 2, 3, 4, 5]
    for category in categories:
        data = []
        for entry in dictionary:
            if entry[0] == category:
                data.append(1)
            else:
                data.append(0)
        features_set.append(data)
        labels_set.append(category)

    return features_set, labels_set


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


# Find keywords by post
def find_keywords_by_post(post_content):
    words = post_content.split('​')

    # @TODO: move this logic to a proper method
    all_words = []
    for i in range(len(words)):
        words[i] = clean_word(words[i])
        if ' ' in words[i]:
            all_words += words[i].split(' ')
        else:
            all_words.append(words[i])
    return all_words


# Save tokenized posts and its keywords to databases
def save_posts_and_keywords():
    # Clean posts from database
    clean_table_db('posts')

    tokenized_posts = get_tokenized_posts_group_by_category_folders()
    num = 0
    for tokenized_post in tokenized_posts:
        obj_file = open(tokenized_post)
        if obj_file is not None:
            post_data = obj_file.read().splitlines()
            post_title = post_data[1].strip()
            post_content = ''
            for i in range(3, len(post_data)):
                post_content += post_data[i].replace('"', "'") + '\n'

            post_content = post_content.strip()
            if post_title is not '' and post_content is not '':
                dict = Counter(find_keywords_by_post(post_content))
                del dict['']
                keywords = ','.join(dict)
                sql = 'INSERT INTO posts (title,content,keywords) VALUES("' + post_title + '","' + post_content + '","' + keywords + '")'
                databaseCon.Database.execute(con, sql)
                num += 1
    print(str(num) + ' posts were saved to database')

# Loop predict by enable user to input the sentence
def loop_predict(dictionary):
    # Loop input
    while True:
        features = []
        inp = input("Enter test keyword: ")
        words = inp.split('​')
        if inp[0] == "exit":
            break
        for word in dictionary:
            features.append(words.count(word[1]))

        res = clf.predict([features])
        predict = ["none", "កីឡា", "ទេសចរណ៍", "ឡាននិងបច្ចេកវិទ្យា", "សុខភាពនិងសម្រស់", "ម្ហូប"][res[0]]
        print(inp + ' => ' + predict)


# Convert word list to features for search
def sentence_to_features(dict, sentence):
    words = sentence.split('​')
    features = []
    for keyword in dict:
        features.append(words.count(keyword[1]))
    return features


# Predict sentence
def predict_category(features):
    clf = load_dataset('category-classifier.p')
    res = clf.predict([features])
    predict = ["none", "កីឡា", "ទេសចរណ៍", "ឡាននិងបច្ចេកវិទ្យា", "សុខភាពនិងសម្រស់", "ម្ហូប"][res[0]]
    return [res[0], predict]