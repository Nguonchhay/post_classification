from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
# from sklearn.metrics import accuracy_score

from functions import *


dictionary = make_keywords_dictionary()
features, labels = make_keywords_dataset(dictionary)

x_train, x_test, y_train, y_test = tts(features, labels)

# Train with Naive Bayes
clf = MultinomialNB()
clf.fit(x_train, y_train)

# preds = clf.predict(x_test)
# print(accuracy_score(y_test, preds))

# delete trained file
delete_file('category-classifier.p')

save(clf, 'category-classifier.p')
print('Save the classifier from dataset')
