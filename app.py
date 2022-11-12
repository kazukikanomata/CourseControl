from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///websta.db"
db = SQLAlchemy(app)

# 1
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    subjects = relationship("Subject")

# 多
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    categories = relationship("Category")

with app.app_context():
    db.create_all()    

@app.route("/")
def websta():
    categories = Category.query.all()
    subjects = Subject.query.all()
    return render_template("index.html",categories=categories, subjects=subjects)

if __name__ == "__main__":
    app.run(debug=True)