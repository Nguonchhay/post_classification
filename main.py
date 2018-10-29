from functions import *


# Do not forget to re-train in case there are new keywords
clf = load_dataset("category-classifier.p")
dictionary = make_keywords_dictionary()

# Read from files for more sentences
search_sentences = []
f = open('test.txt')
if f is not None:
    content = f.read()
    search_sentences = content.splitlines()

for sentence in search_sentences:
    # Split by white space
    words = sentence.split('​')
    features = []
    for keyword in dictionary:
        features.append(words.count(keyword[1]))

    res = clf.predict([features])
    predict = ["none", "កីឡា", "ទេសចរណ៍", "ឡាននិងបច្ចេកវិទ្យា", "សុខភាពនិងសម្រស់", "ម្ហូប"][res[0]]
    print(sentence + ' => ' + predict)
