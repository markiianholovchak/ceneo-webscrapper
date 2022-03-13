import json

class Opinion():
  def __init__(self, id, author, recommendation, score, isPurchaseConfirmed, dateOpinionWritten, dateProductBought, votesYes, votesNo, content, pluses, minuses):
    self.id = id
    self.author = author
    self.recommendation = recommendation
    self.score = score
    self.isPurchaseConfirmed = isPurchaseConfirmed
    self.dateOpinionWritten = dateOpinionWritten
    self.dateProductBought = dateProductBought
    self.votesYes = votesYes
    self.votesNo = votesNo
    self.content = content
    self.pluses = pluses
    self.minuses = minuses
    
  def getOpinionDictionary(self):
    opinionDictionary = {
      "id": self.id,
      "author": self.author,
      "recommendation": self.recommendation,
      "score": self.score,
      "isPurchaseConfirmed": self.isPurchaseConfirmed,
      "dateOpinionWritten": self.dateOpinionWritten,
      "dateProductBought": self.dateProductBought,
      "votesYes": self.votesYes,
      "votesNo": self.votesNo,
      "content": self.content,
      "pluses": self.pluses,
      "minuses": self.minuses
    }
    return opinionDictionary