from collections import Counter
from functions import *


# Crawl post
def craw_posts():
    print('--- Start Crawl Post from Phnom Penh Post News ----\n')
    data_directory = "post_links/"
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
                    if not link_post.startswith('#') and link_post != '':
                        post_content = get_post_data_from_online(link_post)
                        if post_content is not '':
                            # Save post to file
                            path_and_filename = generate_post_filename(file_category, link_post, num_post)
                            save_text_file(path_and_filename, post_content)
                            message = str(num_post) + '. Load post from: ' + link_post + '\n and saved to: ' + path_and_filename + '\n'
                            num_post += 1
                            print(message)
                        else:
                            print('There is no post data from ' + link_post)


# Clean posts
# clean_craw_post()

# Re-crawl post
# craw_posts()

# Save tokenized post to data

# Find keywords by tokenized posts and group by category
find_keywords_by_posts()

# Save tokenized posts and its keywords
save_posts_and_keywords()
