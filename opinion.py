import json

class Opinion():
  def __init__(self, id, author, recommendation, score, isPurchaseConfirmed, dateOpinionWritten, dateProductBought, votesYes, votesNo, content, upsides, downsides):
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
    self.upsides = upsides
    self.downsides = downsides
    
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
      "upsides": self.upsides,
      "downsides": self.downsides
    }
    return opinionDictionary