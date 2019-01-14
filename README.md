# Theme Classification Base on Khmer Keywords Search using Naive Bayes Method

The purpose of this project is for thesis.

## Environment Requirement

* Python version >= 3.7

* MySQL

* Pycharm CE IDE

## Set up libraries and connector

* MySQL connector
```
pip search mysql-connector | grep --color mysql-connector-python
```

* In case you need to update sklearn to latest version
```
pip install -U scikit-learn
```

## Running the `demo` application

* Running `Python` as server
```
cd ROOT_DIRECTORY
python3 server.py
```

* Running web application. Open the filename `demo/index.html` with chrome browser

# Add more training data

* Insert the link from [https://www.postkhmer.com/](Phnom Penh Post Khmer Website)

__Note__: Copy the shortlink of the post from the category you want to insert

* Open the stan-alone application `standalone-app/BI Narin.zip` in order to perform Khmer word segmentation

__Note__: You can manually insert white-space, hidden space or empty space, to the document but it is not recommended.

* Upzip the file

* Setting up support library from `standalone-app/BI Narin/Setup Packages/KWSAddinSetup(x64).msi`

__Note__: Install library that support with our current operating system.

* Run the `standalone-app/BI Narin/Setup Packages/KWSAppSetup(x64).msi` file

__Note__: Run the `.exe` file that support with your current operating system.

* Running crawl
```
python3 crawler.py
```

__Note__: If there are some error, please try to re-run it because we crawl more than 1000 posts and it could some how was block.

* Go to web application to train the inserted data

# Add more cleaning character

* Edit file `clean_word_list.txt`

* Add all the characters