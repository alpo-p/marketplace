from db import db
from app import app
import re

# Used to render categories for the basic layout
@app.context_processor
def utility_processor():
    def get_categories():
        sql = "SELECT id, name FROM categories"
        result = db.session.execute(sql)
        categories = result.fetchall()
        return categories
    return dict(get_categories=get_categories)

def parse_price(price):
    return int(re.sub('[^0-9]','',price))
