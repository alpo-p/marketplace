from db import db
from app import app

# Used to render categories for the basic layout
@app.context_processor
def utility_processor():
    def get_categories():
        sql = "SELECT id, name FROM categories"
        result = db.session.execute(sql)
        categories = result.fetchall()
        return categories
    return dict(get_categories=get_categories)