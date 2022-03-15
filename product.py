from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

from opinion import Opinion
from customExceptions import InvalidIdError

class Product():
  def __init__(self, id, name=""):
    self.id = id
    self.name = name
    self.opinions = []
    self.averageScore = 0
    self.productDetails = {}
    
  @staticmethod
  def extractName(productPageSoup):
    return productPageSoup.find("h1", class_="product-top__product-info__name").text
  
  @staticmethod
  def extractAverageScore(productPageSoup):
    return productPageSoup.find("span", class_="product-review__score")['content']
  
  @staticmethod
  def extractOpinionsPages(productPageSoup):
    opinionsCount = int(productPageSoup.find('span', class_="product-review__qo").find('span').text)
    return opinionsCount // 10 + 1 if opinionsCount % 10 != 0 else opinionsCount // 10
  
  @staticmethod
  def extractOpinions(opinionsPageSoup):
    # 1. Get HTML for opinions on current page
    htmlOpinions = opinionsPageSoup.find_all('div', class_="js_product-review")
    # 2. parse html Opinions
    parsedOpinions = []
    for htmlOpinion in htmlOpinions:
      parsedOpinions.append(Opinion.parseHtmlOpinion(htmlOpinion))
    return parsedOpinions
    
  def extractInformation(self):
    # 1. Get html code for product page
    productPageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{self.id}').text, 'lxml')
    if productPageSoup.find('div', class_="error-page"):
      raise InvalidIdError("Invalid id!")
    if productPageSoup.find('li', class_="reviews_new"):
      return
    self.name = Product.extractName(productPageSoup)
    self.averageScore = Product.extractAverageScore(productPageSoup)
    opinionsPages = Product.extractOpinionsPages(productPageSoup)
    parsedOpinions = []
    for i in range(1, opinionsPages + 1):
      opinionsPageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{self.id}/opinie-{i}').text, 'lxml')
      parsedOpinions += Product.extractOpinions(opinionsPageSoup)
      
    # Create opinion objects and add them to product's opinions array
    for parsedOpinion in parsedOpinions:
      self.opinions.append(Opinion(*parsedOpinion.values()))
      
  def getOpinionsDictionaryList(self):
      opinionsDictionaryList = []
      for opinion in self.opinions:
        opinionsDictionaryList.append(opinion.getOpinionDictionary())
      return opinionsDictionaryList

  def getOpinionsJson(self):
    return json.dumps(self.getOpinionsDictionaryList(), indent=4)
  
  def setOpinionsFromJson(self, jsonOpinions):
    for opinion in json.loads(jsonOpinions):
      self.opinions.append(Opinion(*opinion.values()))
      
  def getProductDetails(self):
    df = pd.read_json(self.getOpinionsJson())
    # 1. Count number of upsides
    upsidesCount = 0
    downsidesCount = 0
    for row in df['upsides']:
      if row:
        upsidesCount += len(row.split(','))
    
          
    # 2. Count number of downsides
    for row in df['downsides']:
      if row:
        downsidesCount += len(row.split(','))
          
    productDetails = {
      "opinionsCount": len(self.opinions),
      "upsidesCount": upsidesCount,
      "downsidesCount": downsidesCount
    }
    self.productDetails = productDetails