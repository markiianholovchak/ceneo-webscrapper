from bs4 import BeautifulSoup
import requests


class InvalidIdError(Exception):
  pass

def parseHtmlOpinions(htmlOpinions):
  '''
    Parses html code for each opinion into a dictionary
    Returns a list of dictionaries
  '''
  opinions = []
  for htmlOpinion in htmlOpinions:
    upsides = []
    downsides = []
    # extract all upsides and downsides
    for featuresColumn in htmlOpinion.find_all("div", class_="review-feature__col"):
      if featuresColumn.find('div', class_="review-feature__title").text == "Zalety":
        for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
          upsides.append(feature.text)
      elif featuresColumn.find('div', class_="review-feature__title").text == "Wady":
         for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
          downsides.append(feature.text)
    # extract recommendation
    recommendation = ""
    if htmlOpinion.find('span', class_="user-post__author-recomendation") and htmlOpinion.find('span', class_="user-post__author-recomendation").text.replace("\n", "") == "Polecam":
        recommendation="Positive"
    else:
        recommendation="Negative"
    # extract review date and purchase date
    dateWritten = ""
    datePurchased = ""
    if len(htmlOpinion.find("span", class_="user-post__published").find_all("time")) == 2:
      dateWritten = htmlOpinion.find("span", class_="user-post__published").find_all("time")[0]['datetime']
      datePurchased = htmlOpinion.find("span", class_="user-post__published").find_all("time")[1]['datetime']
    elif len(htmlOpinion.find("span", class_="user-post__published").find_all("time")) == 1:
      dateWritten = htmlOpinion.find("span", class_="user-post__published").find_all("time")[0]['datetime']
      
    opinion = {
      "id": htmlOpinion['data-entry-id'],
      "author": htmlOpinion.find("span", class_="user-post__author-name").text.replace("\n", ""),
      "recommendation": recommendation,
      "stars": htmlOpinion.find("span", class_='user-post__score-count').text,
      "confirmedPurchase": True if htmlOpinion.find('div', class_="review-pz") else False,
      "dateWritten": dateWritten,
      "dateBought": datePurchased,
      "votesYes": htmlOpinion.find('button', class_="vote-yes")['data-total-vote'],
      "votesNo": htmlOpinion.find('button', class_="vote-no")['data-total-vote'],
      "content": htmlOpinion.find('div', class_="user-post__text").text,
      "upsides": upsides,
      "downsides": downsides
    }
    opinions.append(opinion)
  return opinions

def getOpinions(productId): 
  '''
    Returns a list containing all opinions for product with id passesd as productId param
    Returns an error message if the productId is invalid
  '''
  pageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{productId}/opinie-1').text, 'lxml')
  if pageSoup.find('div', class_="error-page"):
    raise InvalidIdError("Invalid id!")
  if pageSoup.find('li', class_="reviews_new"):
    return "There are no opinions for this product"
  
  opinions = []
  totalOpinions = int(pageSoup.find('span', class_="product-review__qo").find('span').text)
  opinionPages = totalOpinions // 10 + 1
  opinions += parseHtmlOpinions(pageSoup.find_all('div', class_="js_product-review"))
  for i in range(2, opinionPages + 1):
    pageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{productId}/opinie-{i}').text, 'lxml')
    opinions += parseHtmlOpinions(pageSoup.find_all('div', class_="js_product-review"))
  return opinions 