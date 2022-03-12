from flask import Flask, render_template, request, redirect
from extraction import getOpinions

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/extraction")
def extraction():
  return render_template('extraction.html')

@app.route("/extract", methods=["POST", "GET"])
def extract():
  if request.method == "POST":
    productId = request.form['productId']
    opinions = getOpinions(productId)
    return render_template('product.html', productId=productId, opinions=opinions)
  else:
    return redirect("/")
  
  

if __name__ == "__main__":
  app.run(debug=True)