def parseHtmlOpinions(htmlOpinions):
  '''
    Parses html code for each opinion into a dictionary
    Returns a list of dictionaries
  '''
  opinions = []
  for htmlOpinion in htmlOpinions:
    pluses = []
    minuses = []
    # extract all pluses and minuses
    for featuresColumn in htmlOpinion.find_all("div", class_="review-feature__col"):
      if featuresColumn.find('div', class_="review-feature__title").text == "Zalety":
        for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
          pluses.append(feature.text)
      elif featuresColumn.find('div', class_="review-feature__title").text == "Wady":
         for feature in  featuresColumn.find_all("div", class_="review-feature__item"):
          minuses.append(feature.text)
    # extract recommendation
    recommendation = ""
    if htmlOpinion.find('span', class_="user-post__author-recomendation") and htmlOpinion.find('span', class_="user-post__author-recomendation").text.replace("\n", "") == "Polecam":
        recommendation="Positive"
    else:
        recommendation="Negative"
    # extract review date and purchase date
    dateOpinionWritten = ""
    dateProductBought = ""
    if len(htmlOpinion.find("span", class_="user-post__published").find_all("time")) == 2:
      dateOpinionWritten = htmlOpinion.find("span", class_="user-post__published").find_all("time")[0]['datetime']
      dateProductBought = htmlOpinion.find("span", class_="user-post__published").find_all("time")[1]['datetime']
    elif len(htmlOpinion.find("span", class_="user-post__published").find_all("time")) == 1:
      dateOpinionWritten = htmlOpinion.find("span", class_="user-post__published").find_all("time")[0]['datetime']
      
    opinion = {
      "id": htmlOpinion['data-entry-id'],
      "author": htmlOpinion.find("span", class_="user-post__author-name").text.replace("\n", ""),
      "recommendation": recommendation,
      "score": htmlOpinion.find("span", class_='user-post__score-count').text,
      "isPurchaseConfirmed": True if htmlOpinion.find('div', class_="review-pz") else False,
      "dateOpinionWritten": dateOpinionWritten,
      "dateProductBought": dateProductBought,
      "votesYes": htmlOpinion.find('button', class_="vote-yes")['data-total-vote'],
      "votesNo": htmlOpinion.find('button', class_="vote-no")['data-total-vote'],
      "content": htmlOpinion.find('div', class_="user-post__text").text,
      "pluses": (",").join(pluses),
      "minuses": (",").join(minuses)
    }
    opinions.append(opinion)
  return opinions

