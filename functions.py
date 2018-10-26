import os
import requests
from bs4 import BeautifulSoup


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
    if 'technology' in category:
        cat = 'car_and_technology'
    elif 'food' in category:
        cat = 'food'
    elif 'tourism' in category:
        cat = 'tourism'
    elif 'health_and_beauty' in category:
        cat = 'health_and_beauty'
    return cat


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

# words = []
# f = open('test.txt')
# if f is not None:
#     # Split by white space
#     words += f.read().split('​')
#
# for i in range(len(words)):
#     words[i] = words[i].strip()
#
# dict = Counter(words)
# del dict['']
# print(dict.most_common())
