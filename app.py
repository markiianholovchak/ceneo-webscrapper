from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from product import Product
from customExceptions import InvalidIdError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

#
# Todo: 
# 1. Change pluses/minuses table to string 
# 2. add productId field to each opinion
#
class CeneoProduct(db.Model):
  id = db.Column(db.String(20), nullable=False, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  opinions = db.Column(db.String())
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return "<CeneoProduct %r>" % self.id

  


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
      productId = int(request.form['productId'])
      newProduct = Product(productId)
      newProduct.extractInformation()
      
      newCeneoProduct = CeneoProduct(id=productId, name=newProduct.name, opinions=newProduct.getOpinionsJson())
      try:
        db.session.add(newCeneoProduct)
        db.session.commit()
        return redirect(f"/product/{productId}")
      except:
        return "There was an issue in commiting to database"
        
    except InvalidIdError:
      return redirect(url_for('extraction', error="Invalid product id!"))
  else:
    return redirect("/")
  
@app.route("/product/<int:id>")
def product(id):
  dbProduct = CeneoProduct.query.get_or_404(id) 
  productToDisplay = Product(dbProduct.id)
  productToDisplay.setOpinionsFromJson(dbProduct.opinions)
  print(productToDisplay.opinions)
  return render_template('product.html', product=productToDisplay)
  
@app.route("/products-list")
def productsList():
  products = CeneoProduct.query.order_by(CeneoProduct.dateCreated).all()
  
  return render_template("productList.html", products=products)
  
@app.route("/delete/<int:id>")
def delete(id):
  productToDelete = CeneoProduct.query.get_or_404(id)
  try:
    db.session.delete(productToDelete)
    db.session.commit()
    return redirect("/products-list")
  except:
    return "There was an issue deleting this product"


if __name__ == "__main__":
  app.run(debug=True)