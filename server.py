from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from operator import itemgetter, attrgetter
import time

from functions import *
from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
# Allow cross origin request from Javascript
CORS(app)


@app.route('/training', methods=['POST'])
def training():
    dictionary = make_keywords_dictionary()
    features, labels = make_keywords_dataset(dictionary)

    x_train, x_test, y_train, y_test = tts(features, labels)

    # Train with Naive Bayes
    clf = MultinomialNB()
    clf.fit(x_train, y_train)

    filename = 'category-classifier.p'
    # delete trained file
    delete_file(filename)

    save(clf, filename)
    return jsonify({
        'statusCode': 200,
        'message': 'Save the classifier from dataset.'
    })


@app.route('/classify', methods=['POST'])
def classify():
    start_time = str(time.time())
    # Do not forget to re-train in case there are new keywords
    dictionary = make_keywords_dictionary()

    # Get POST params from request
    sentence = request.json.get('sentence')
    words = sentence.split('​')

    # Clean words
    adjust_words = []
    for i in range(0, len(words)):
        word = clean_word(words[i])
        if word != '':
            adjust_words.append(word)
    words = adjust_words

    features = sentence_to_features(dictionary, words)
    result = predict_category(features)

    if result[0] > 0:
        found_category_id = result[0]
        # Display related posts
        keyword_posts = []
        for keyword in words:
            posts = get_posts_by_category_and_keyword(found_category_id, keyword)
            keyword_posts.append([len(posts), keyword, posts])

        # sort keyword_posts
        sort_keyword_posts = sorted(keyword_posts, key=itemgetter(0), reverse=True)

        # Update new keyword frequency of found category
        news_keywords = {}
        for keyword in words:
            news_keywords[keyword] = update_keyword_frequency_for_web(found_category_id, keyword)

        end_time = str(time.time())
        return jsonify({
            'statusCode': 200,
            'data': {
                'news': sort_keyword_posts,
                'category': {
                    'id': str(found_category_id),
                    'name': result[1]
                },
                'news_keywords': news_keywords,
                'start_time': start_time,
                'end_time': end_time
            },
            'message': 'All found posts'
        })
    else:
        return jsonify({
            'statusCode': 404,
            'data': {},
            'message': 'There is no match category.'
        })


# Read from files for more sentences
def get_search_sentences():
    search_sentences = []
    f = open('test.txt')
    if f is not None:
        content = f.read()
        search_sentences = content.splitlines()
    return search_sentences


if __name__ == '__main__':
    # Enable debug mode for development
    app.run(host='0.0.0.0', port=8080, debug=True)
