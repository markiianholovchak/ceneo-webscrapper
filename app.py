# from bs4 import BeautifulSoup
# import requests

# def parseHtmlOpinions(htmlOpinions):
#   '''
#     Parses html code for each opinion into a dictionary
#     Returns a list of dictionaries
#   '''
#   opinions = []
#   for htmlOpinion in htmlOpinions:
#     pluses = []
#     minuses = []
#     for featuresColumn in htmlOpinion.find_all("div", class_="review-feature__col"):
#       if featuresColumn.find('div', class_="review-feature__title").text == "Zalety":
#         for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
#           pluses.append(feature.text)
#       elif featuresColumn.find('div', class_="review-feature__title").text == "Wady":
#          for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
#           minuses.append(feature.text)
#     opinion = {
#       "id": htmlOpinion['data-entry-id'],
#       "author": htmlOpinion.find("span", class_="user-post__author-name").text.replace("\n", ""),
#       "recomendation": htmlOpinion.find('span', class_="user-post__author-recomendation").text.replace("\n", "") if htmlOpinion.find('span', class_="user-post__author-recomendation") else "", 
#       "stars": htmlOpinion.find("span", class_='user-post__score-count').text,
#       "confirmedPurchase": True if htmlOpinion.find('div', class_="review-pz") else False,
#       "dateWritten": htmlOpinion.find_all("time")[0]['datetime'] if len(htmlOpinion.find_all("time")) > 0 else "",
#       "dateBought": htmlOpinion.find_all("time")[1]['datetime'] if len(htmlOpinion.find_all("time")) == 2 else "",
#       "votesYes": htmlOpinion.find('button', class_="vote-yes")['data-total-vote'],
#       "votesNo": htmlOpinion.find('button', class_="vote-no")['data-total-vote'],
#       "content": htmlOpinion.find('div', class_="user-post__text").text,
#       "pluses": pluses,
#       "minuses": minuses
#     }
#     opinions.append(opinion)
#   return opinions

# def getOpinions(productId): 
#   '''
#     Returns a list containing all opinions for product with id passesd as productId param
#     Returns an error message if the productId is invalid
#   '''
#   pageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{productId}/opinie-1').text, 'lxml')
#   if pageSoup.find('div', class_="error-page"):
#     return "Invalid product id!"
#   if pageSoup.find('li', class_="reviews_new"):
#     return "There are no opinions for this product"
  
#   opinions = []
#   totalOpinions = int(pageSoup.find('span', class_="product-review__qo").find('span').text)
#   opinionPages = totalOpinions // 10 + 1
#   opinions += parseHtmlOpinions(pageSoup.find_all('div', class_="js_product-review"))
#   for i in range(2, opinionPages + 1):
#     pageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{productId}/opinie-{i}').text, 'lxml')
#     opinions += parseHtmlOpinions(pageSoup.find_all('div', class_="js_product-review"))
#   return opinions 

# opinions = getOpinions(57276002)

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)