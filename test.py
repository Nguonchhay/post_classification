import os
import pickle
from sklearn import *
from collections import Counter


def load_dataset(clf_file):
    return pickle.load(open(clf_file, "rb"))
    # with open(clf_file) as fp:
    #     clf = pickle.load(fp)
    # return clf


def make_dict():
    direc = "category/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    words = []

    for email in emails:
        # f = open(email)
        with open(email, encoding='utf-8') as f:
            if f is not None:
                content = f.read()
                words += content.splitlines()

    dictionary = Counter(words)
    del dictionary['']
    return dictionary.most_common(3000)


clf = load_dataset("category-classifier.p")
d = make_dict()

# print(d)

# None
# inp = 'testing'

# ​កីឡា
inp = 'កីឡាករ ស្រុកខ្មែរ មាន ការហ្វឹកហាត់'

# កំសាន្ត
# inp = 'ប្រកួតប្រជែង ភាពយន្ត ខ្នាតធំ'

features = []
for word in d:
    features.append(inp.count(word[0]))


res = clf.predict([features])
print(res)
print(["none", "កីឡា", "កំសាន្ត", "បច្ចេកវិទ្យា", "ជីវិតនិងសង្គម", "ម្ហូប"][res[0]])

# # Loop input
# while True:
#     features = []
#     inp = input("Enter test keyword: ").split(' ')
#     if inp[0] == "exit":
#         break
#     for word in d:
#         features.append(inp.count(word[0]))
#     res = clf.predict([features])
#     print(["កីឡា", "កំសាន្ត", "បច្ចេកវិទ្យា", "ជីវិតនិងសង្គម", "ម្ហូប"][res[0]])
