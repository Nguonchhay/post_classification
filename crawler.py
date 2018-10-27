from collections import Counter
from functions import *


# Crawl post
def craw_posts():
    print('--- Start Crawl Post from Phnom Penh Post News ----\n')
    data_directory = "20181023_posts/"
    files = os.listdir(data_directory)
    file_categories = [data_directory + category for category in files]
    for file_category in file_categories:
        with open(file_category, encoding='utf-8') as f:
            if f is not None:
                content = f.read()
                link_posts = content.splitlines()

                num_post = 1
                for link_post in link_posts:
                    link_post = link_post.strip()
                    if link_post != '':
                        post_content = get_post_data_from_online(link_post)
                        # Save post to file
                        path_and_filename = generate_post_filename(file_category, link_post, num_post)
                        save_text_file(path_and_filename, post_content)
                        message = str(num_post) + '. Load post from: ' + link_post + '\n and saved to: ' + path_and_filename + '\n'
                        num_post += 1
                        print(message)


# Find keywords for category
def find_keywords_by_posts():
    tokenized_posts = get_tokenized_posts_group_by_category_folders()
    category_keywords = init_category_keywords()
    for tokenized_post in tokenized_posts:
        obj_file = open(tokenized_post)
        if obj_file is not None:
            # Split by white space (hidden space)
            words = obj_file.read().split('​')

            # @TODO: move this logic to a proper method
            all_words = []
            for i in range(len(words)):
                words[i] = clean_word(words[i])
                if ' ' in words[i]:
                    all_words += words[i].split(' ')
                else:
                    all_words.append(words[i])

            category = get_compare_category_label(tokenized_post)
            category_keywords[category] += all_words

    # Clean keywords from database
    clean_table_db('keywords')

    # Save all categories keywords to database
    for category in category_keywords:
        keyword_dictionary = Counter(category_keywords[category])
        del keyword_dictionary['']

        # Save keywords to database
        save_keywords_db(category, keyword_dictionary)


# Clean posts
# clean_craw_post()

# Re-crawl post
# craw_posts()

# Find keywords by tokenized posts and group by category
find_keywords_by_posts()
