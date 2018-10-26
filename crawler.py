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

    # for tokenized_post in tokenized_posts:
    #     print(tokenized_post)

        # if 'sport' in category:
        #     feature_labels.append(1)
        # elif 'entertainment' in category:
        #     feature_labels.append(2)
        # elif 'technology' in category:
        #     feature_labels.append(3)
        # elif 'life_and_social' in category:
        #     feature_labels.append(4)
        # elif 'food' in category:
        #     feature_labels.append(5)
        # else:
        #     feature_labels.append(0)
    #print(tokenized_posts)
    #print(len(tokenized_posts))


# Clean posts
# clean_craw_post()

# Re-crawl post
# craw_posts()

# Find keywords by tokenized posts and group by category
find_keywords_by_posts()


test = []
test[1].append('1')
#test['1'] += ['12']
#test['1'] += ['123']
print(test)

