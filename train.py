import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
import pickle
import codecs

# Keyword searching:
#   - https://www.enchantedlearning.com/wordlist/sports.shtml
#   - https://www.enchantedlearning.com/wordlist
#   - https://keywordtool.io/pro
#

def save(clf, name):
    pickle.dump(clf, open(name, "wb"))
    # with open(name, 'wb') as fp:
    #     pickle.dump(clf, fp)
    print("saved")


def make_dict():
    data_directory = "category/"
    files = os.listdir(data_directory)
    categories = [data_directory + category for category in files]
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


def make_dataset(dictionary):
    data_directory = "category/"
    files = os.listdir(data_directory)
    categorys = [data_directory + category for category in files]
    feature_set = []
    feature_labels = []
    for category in categorys:
        data = []
        f = open(category)
        print('Load data from: ' + category)
        if f is not None:
            words = f.read().splitlines()
            for entry in dictionary:
                data.append(words.count(entry[0]))
            feature_set.append(data)

            if 'sport' in category:
                feature_labels.append(1)
            elif 'entertainment' in category:
                feature_labels.append(2)
            elif 'technology' in category:
                feature_labels.append(3)
            elif 'life_and_social' in category:
                feature_labels.append(4)
            elif 'food' in category:
                feature_labels.append(5)
            else:
                feature_labels.append(0)

    return feature_set, feature_labels


dictionary = make_dict()
features, labels = make_dataset(dictionary)

# print(dictionary)
# print(features)
# print(labels)

x_train, x_test, y_train, y_test = tts(features, labels, test_size=0.1)

# Train with Naive Bayes
clf = MultinomialNB()
clf.fit(x_train, y_train)

preds = clf.predict(x_test)
print(accuracy_score(y_test, preds))
save(clf, "category-classifier.p")
