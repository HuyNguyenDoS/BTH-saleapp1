from app import app
from flask import render_template, request
import utils


@app.route("/")
def home():
    cats = utils.load_categories()
    return render_template("index.html", categories=cats)

@app.route("/products")
def products_list():
    cate_id = request.args.get("category_id")

    keyword = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.load_products(cate_id=cate_id, keyword=keyword, from_price=from_price, to_price=to_price)

    return render_template("products.html", products=products)

@app.route("/products/<int:product_id>")
def product_id(product_id):
    product = utils.get_productID(product_id=product_id)
    return render_template("product_id.html", product_id=product)



if __name__ == '__main__':
    app.run(debug=True)