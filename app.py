from flask import Flask, Response, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import io
import json


from product import Product
from customExceptions import InvalidIdError, ProductAlreadyExists
from sortableTable import SortableTable

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

#
# Todo:
# 1. Change upsides/downsides table to string 
# 2. add productId field to each opinion
#
class CeneoProduct(db.Model):
  id = db.Column(db.String(20), nullable=False, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  averageScore = db.Column(db.String(10))
  opinions = db.Column(db.String())
  opinionsCount = db.Column(db.Integer)
  upsidesCount = db.Column(db.Integer)
  downsidesCount = db.Column(db.Integer)
  dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return "<CeneoProduct %r>" % self.id

  


@app.route("/")
def index():
  return render_template('index.html')

@app.route('/error-404')
def erro404():
  error = request.args.get("error", None)
  return render_template('404.html', error=error)
    

@app.route("/extraction")
def extraction():
  error = request.args.get("error", None)
  return render_template('extraction.html', error=error)

@app.route("/extract", methods=["POST", "GET"])
def extract():
  if request.method == "POST":
    try:
      productId = int(request.form['productId'])
      if CeneoProduct.query.get(productId):
        raise ProductAlreadyExists()
      newProduct = Product(productId)
      newProduct.extractInformation()
      newProduct.getProductDetails()
      
      newCeneoProduct = CeneoProduct(id=productId, 
                                     name=newProduct.name,
                                     opinions=newProduct.getOpinionsJson(),
                                     averageScore=newProduct.averageScore,
                                     opinionsCount=newProduct.productDetails["opinionsCount"],
                                     upsidesCount=newProduct.productDetails["upsidesCount"],
                                     downsidesCount=newProduct.productDetails["downsidesCount"],)
      try:
        db.session.add(newCeneoProduct)
        db.session.commit()
        return redirect(f"/product/{productId}")
      except:
        return redirect(url_for('error-404', error="There was an issue in commiting to DataBase"))
        
    except InvalidIdError:
      return redirect(url_for('extraction', error="Invalid product id!"))
    except ProductAlreadyExists:
      return redirect(url_for('extraction', error="Information for this product has already been extracted!"))
    except OverflowError:
      return redirect(url_for('extraction', error="Invalid product id!"))
  else:
    return redirect("/extraction")
  
@app.route("/product/<int:id>")
def product(id):
  try:
    # 1. Get all url parameters
    sortColumn = request.args.get('sort_by')
    sortDirection = request.args.get("direction")
    filterText = request.args.get('filter')
    filterColumn = request.args.get("column")
    
    # 2. Fetch product from database by id and create a product object
    dbProduct = CeneoProduct.query.get_or_404(id) 
    productToDisplay = Product(dbProduct.id, dbProduct.name)
    # 3. Create pandas dataframe to sort/filter opinions
    opinionsDf = pd.read_json(dbProduct.opinions)
    # 4. Sort and filter the opinions according to url arguments
    if sortColumn and sortDirection:
      productToDisplay.setOpinionsFromJson(opinionsDf.sort_values(sortColumn, ascending = True if sortDirection == 'asc' else False ).to_json(orient='records'))
    elif filterText and filterColumn:
      productToDisplay.setOpinionsFromJson(opinionsDf.loc[opinionsDf[filterColumn] == filterText].to_json(orient='records'))
    else:
      productToDisplay.setOpinionsFromJson(dbProduct.opinions)
    
    # 5. Create a sortable table object and render product's template
    productTable = SortableTable(productToDisplay.opinions)
    return render_template('product.html', product=productToDisplay, table=productTable)
  except:
    return redirect(url_for('error-404', error="There was an issue in loading product data!"))
  
@app.route("/products-list")
def productsList():
  try:
    products = CeneoProduct.query.order_by(CeneoProduct.dateCreated).all()
    return render_template("productList.html", products=products)
  except:
    return redirect(url_for('error-404', error="There was an issue in loading products!"))
  
@app.route("/delete/<int:id>")
def delete(id):
  try:
    productToDelete = CeneoProduct.query.get_or_404(id)
    db.session.delete(productToDelete)
    db.session.commit()
    return redirect("/products-list")
  except:
    return redirect(url_for('error-404', error="There was an issue in deleting this product!"))
  
@app.route('/download-json/<int:id>')
def downloadJson(id):
  try:
    product = CeneoProduct.query.get_or_404(id)
    return Response(product.opinions, mimetype="application/json",
                    headers={'Content-Disposition':f'attachment;filename={id}.json'})
  except:
    return redirect(url_for('error-404', error="There was an issue in downloading json!"))
    
@app.route("/download-csv/<int:id>")
def downloadCsv(id):
  try:
    product = CeneoProduct.query.get_or_404(id)
    df = pd.read_json(product.opinions)
    opinionsCsv = df.to_csv()
    return Response(opinionsCsv,
                    headers={'Content-Disposition':f'attachment;filename={id}.csv'})
  except:
    return redirect(url_for('error-404', error="There was an issue in downloading csv!"))
  
@app.route("/download-xlsx/<int:id>")
def downloadXlsx(id):
  try:
    product = CeneoProduct.query.get_or_404(id)
    df = pd.read_json(product.opinions)
    output = io.BytesIO()
    df.to_excel(output)
    xlsx_data = output.getvalue()
    return Response(xlsx_data,
                    headers={'Content-Disposition':f'attachment;filename={id}.xlsx'})
  except:
    return redirect(url_for('error-404', error="There was an issue in downloading xlsx!"))
  

@app.route("/charts/<int:id>")
def plots(id):
  try:
    product = CeneoProduct.query.get_or_404(id)
    df = pd.read_json(product.opinions)
    firstChartData = df['recommendation'].value_counts().to_dict()
    secondChartData = df['score'].value_counts().to_dict()
    return render_template('charts.html', productId=product.id, firstChartData=json.dumps(firstChartData), secondChartData=json.dumps(secondChartData))
  except:
    return redirect(url_for('error-404', error="Not found!"))
    
  
@app.route('/author')
def author():
  return render_template('author.html')


if __name__ == "__main__":
  app.run(debug=True)