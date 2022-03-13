from bs4 import BeautifulSoup
import requests
import json
import pandas as pd


from helper import parseHtmlOpinions
from opinion import Opinion

from customExceptions import InvalidIdError

class Product():
  def __init__(self, id):
    self.id = id
    self.name = ""
    self.opinions = []
    
  def extractInformation(self):
    # 1. Get html code for product page
    productPageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{self.id}').text, 'lxml')
    if productPageSoup.find('div', class_="error-page"):
      raise InvalidIdError("Invalid id!")
    if productPageSoup.find('li', class_="reviews_new"):
      return
    self.name = productPageSoup.find("h1", class_="product-top__product-info__name").text
    temporaryOpinions = []
    opinionsCount = int(productPageSoup.find('span', class_="product-review__qo").find('span').text)
    opinionsPages = opinionsCount // 10 + 1
    for i in range(1, opinionsPages + 1):
      opinionsPageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{self.id}/opinie-{i}').text, 'lxml')
      temporaryOpinions += parseHtmlOpinions(opinionsPageSoup.find_all('div', class_="js_product-review"))
      
    # Create opinion objects and add them to product's opinions array
    for temporaryOpinion in temporaryOpinions:
      self.opinions.append(Opinion(*temporaryOpinion.values()))
      
  def getOpinionsDictionaryList(self):
      opinionsDictionaryList = []
      for opinion in self.opinions:
        opinionsDictionaryList.append(opinion.getOpinionDictionary())
      return opinionsDictionaryList

  def getOpinionsJson(self):
    return json.dumps(self.getOpinionsDictionaryList())
  
  def setOpinionsFromJson(self, jsonOpinions):
    for opinion in json.loads(jsonOpinions):
      self.opinions.append(Opinion(*opinion.values()))
      
  def getProductDetails(self):
    df = pd.read_json(self.getOpinionsJson())
    print(df)
    productDetails = {
      "opinionsNumber": len(self.opinions)
      
    }