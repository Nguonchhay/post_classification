from functions import *


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

ss = 'រមណីយដ្ឋាន​មណ្ឌលគិរី​បឹងយក្សឡោម​ដើរលេង'

features = sentence_to_features(dictionary, ss)
words = ss.split('​')
result = predict_category(features)
print(str(result[0]) + ' => ' + result[1] + '\n')

# Update keyword frequency of found category
if result[0] > 0:
    for keyword in words:
        print('- ' + keyword)
        update_keyword_frequency(result[0], keyword, True)
