from functions import *
from operator import itemgetter, attrgetter


# Read from files for more sentences
def get_search_sentences():
    search_sentences = []
    f = open('test.txt')
    if f is not None:
        content = f.read()
        search_sentences = content.splitlines()
    return search_sentences


# Do not forget to re-train in case there are new keywords
dictionary = make_keywords_dictionary()

# search_sentences = get_search_sentences()
# for sentence in search_sentences:
#     features = convert_to_features(dictionary, sentence)
#     result = predict_category(features)
#     print(result[0] + ' => ' + result[1])

ss = 'កីឡាករ​ទៅដើរលេង​រមណីយដ្ឋាន​មណ្ឌលគិរី'

features = sentence_to_features(dictionary, ss)
words = ss.split('​')
print(words)
result = predict_category(features)
print('Predict result: ' + str(result[0]) + ' => ' + result[1] + '\n')

if result[0] > 0:
    # Display related posts
    keyword_posts = []
    for keyword in words:
        posts = get_posts_by_category_and_keyword(result[0], keyword)
        keyword_posts.append([len(posts), keyword, posts])

    # sort keyword_posts
    sort_keyword_posts = sorted(keyword_posts, key=itemgetter(0), reverse=True)

    # Display posts
    for sort_keyword_post in sort_keyword_posts:
        print('* ' + sort_keyword_post[1] + ':')
        for post in sort_keyword_post[2]:
            print('\t - ' + str(post[0]) + ' | ' + post[2])

        print('---------------------------------------------------------------------------------------------------------')

    # Update keyword frequency of found category
    for keyword in words:
        print('- ' + keyword)
        update_keyword_frequency(result[0], keyword, True)
