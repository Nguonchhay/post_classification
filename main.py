from functions import *


# Read from files for more sentences
def get_search_sentences():
    search_sentences = []
    f = open('test.txt')
    if f is not None:
        content = f.read()
        search_sentences = content.splitlines()
    return search_sentences


# Convert word list to features for search
def sentence_to_features(dict, sentence):
    words = sentence.split('​')
    features = []
    for keyword in dict:
        features.append(words.count(keyword[1]))
    return features


# Predict sentence
def predict_category(features):
    res = clf.predict([features])
    predict = ["none", "កីឡា", "ទេសចរណ៍", "ឡាននិងបច្ចេកវិទ្យា", "សុខភាពនិងសម្រស់", "ម្ហូប"][res[0]]
    return [res[0], predict]


# Do not forget to re-train in case there are new keywords
clf = load_dataset('category-classifier.p')
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
