from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import io

from opinion import Opinion
from customExceptions import InvalidIdError

class Product():
  def __init__(self, id, name="", averageScore=0):
    self.id = id
    self.name = name
    self.opinions = []
    self.averageScore = averageScore
    
  @staticmethod
  def extractName(productPageSoup):
    return productPageSoup.find("h1", class_="product-top__product-info__name").text
  
  @staticmethod
  def extractAverageScore(productPageSoup):
    return float(productPageSoup.find("span", class_="product-review__score")['content'])
  
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
  
  @staticmethod    
  def convertJson(jsonContent, dataFormat):
    '''Convert json format to csv or xlsx'''
    df = pd.read_json(jsonContent)
    if dataFormat == "csv":
      return df.to_csv()
    elif dataFormat == "xlsx":
      output = io.BytesIO()
      df.to_excel(output)
      return output.getvalue()
    
  def extractInformation(self):
    '''
    Extracts all product's opinions
    '''
    
    # 1. Get html code for product page
    productPageSoup = BeautifulSoup(requests.get(f'https://www.ceneo.pl/{self.id}').text, 'lxml')
    if productPageSoup.find('div', class_="error-page"):
      raise InvalidIdError("Invalid id!")
    self.name = Product.extractName(productPageSoup)
    if productPageSoup.find('li', class_="reviews_new"):
      return
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
      '''
      Returns opinions as dictionaries in a list
      '''
      opinionsDictionaryList = []
      for opinion in self.opinions:
        opinionsDictionaryList.append(opinion.getOpinionDictionary())
      return opinionsDictionaryList

  def getOpinionsJson(self):
    '''
    Return json-formatted opinions
    '''
    return json.dumps(self.getOpinionsDictionaryList(), indent=4)
  
  def setOpinionsFromJson(self, jsonOpinions):
    '''
    Converts opinions from json format to Opinion object format
    '''
    opinions = []
    for opinion in json.loads(jsonOpinions):
      opinions.append(Opinion(*opinion.values()))
    self.opinions = opinions
    
  def getProductDetails(self):
    '''
    Returns product's details: id, name, average score, opinions' count, upsides and downisides count
    '''
    if self.opinions:
      
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
            
      return {
        "id": self.id,
        "name": self.name,
        "averageScore": self.averageScore,
        "opinionsCount": len(self.opinions),
        "upsidesCount": upsidesCount,
        "downsidesCount": downsidesCount
      }
    else:
      return {
        "id": self.id,
        "name": self.name,
        "averageScore": 0,
        "opinionsCount": 0,
        "upsidesCount": 0,
        "downsidesCount": 0
      }
    
  def sortOpinions(self, sortColumn, sortDirection):
    '''
    Sorts opinions depending on column and direction
    '''
    opinionsDf = pd.read_json(self.getOpinionsJson())
    sortedOpinions = opinionsDf.sort_values(sortColumn, ascending = False if sortDirection == 'asc' else True ).to_json(orient='records')
    self.setOpinionsFromJson(sortedOpinions)
    
  def filterOpinions(self, filterColumn, filterText):
    '''
    Filters opinions depending on column and text
    '''
    opinionsDf = pd.read_json(self.getOpinionsJson())
    filteredOpinions = opinionsDf.loc[opinionsDf[filterColumn].astype(str).str.contains(filterText)].to_json(orient='records')
    self.setOpinionsFromJson(filteredOpinions)
    
  def getCountedColumnValuesDict(self, column):
     '''
     Counts how many of different values there are in column
     Return dictionary with different values as keys and their count as values
     '''
     df = pd.read_json(self.getOpinionsJson())
     return df[column].value_counts().to_dict()
   
 
   
      
      