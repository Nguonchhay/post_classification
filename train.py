from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score

from functions import *


print('Start training...')
dictionary = make_keywords_dictionary()
features, labels = make_keywords_dataset(dictionary)

x_train, x_test, y_train, y_test = tts(features, labels)

# Train with Naive Bayes
clf = MultinomialNB()
clf.fit(x_train, y_train)

preds = clf.predict(x_test)
print(accuracy_score(y_test, preds))

filename = 'category-model.classifier'
# delete trained file
delete_file(filename)

save(clf, filename)
print('Save the classifier from dataset')
