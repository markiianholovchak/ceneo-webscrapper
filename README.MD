# Scrapify - extract opinions from Ceneo.pl

Scrapify - project based on Flask framework that allows you to extract opinions about different products from ceneo.pl webpage

![Homepage](https://github.com/markiianholovchak/ceneo-webscrapper/blob/media/home.png)

## Extracting opinions

Enter product's id and press "Extract"

![Extraction](https://github.com/markiianholovchak/ceneo-webscrapper/blob/media/extraction.png)

## Presenting opinions

Opinions are presented in a sortable and filterable table

You can download opinions in json, csv and xls formats

![Product](https://github.com/markiianholovchak/ceneo-webscrapper/blob/media/product.png)

## Extracted opinions

All extracted opinions are stored in a local SQLite database.

![ProductList](https://github.com/markiianholovchak/ceneo-webscrapper/blob/media/productList.png)

## Used frameworks and libraries

1. Flask
2. TailwindCSS
3. Chart.js
4. Pandas
5. Beautiful Soup
6. SQLAlchemy

## Data

Scrapify uses a local SQLite database to store all the data about extracted products

## Installation

To install and run the app:

1. Clone the git repository
2. Install virtualenv `pip install virtualenv` if you dont't have it installed yet
3. Create and activate virtual environment:
   1. `virtualenv environment_name`
   2. `source environment_name/bin/activate`
4. Install needed packages: `pip3 install -r requirements.txt`
5. `flask run`

Happy coding!
