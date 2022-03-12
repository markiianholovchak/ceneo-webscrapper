from flask import Flask, render_template, request, redirect, url_for
from extraction import InvalidIdError, getOpinions

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/extraction")
def extraction():
  error = request.args.get("error", None)
  return render_template('extraction.html', error=error)

@app.route("/extract", methods=["POST", "GET"])
def extract():
  if request.method == "POST":
    try:
      productId = request.form['productId']
      opinions = getOpinions(productId)
      return render_template('product.html', productId=productId, opinions=opinions)
    except InvalidIdError:
      return redirect(url_for('extraction', error="Invalid product id!"))
  else:
    return redirect("/")
  
  

if __name__ == "__main__":
  app.run(debug=True)