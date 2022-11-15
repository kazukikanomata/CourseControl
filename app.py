from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
# ここでimport
# from flaski.models import Category, Subject
# from flaski.database import db_session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    

@app.route('/', methods=['GET'])
def blog():
    # DBに登録されたデータをすべて取得する
    if request.method == 'GET':
        blogarticles = BlogArticle.query.all()
        return render_template('index.html', blogarticles=blogarticles)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        # BlogArticleのインスタンスを作成
        blogarticle = BlogArticle(title=title, body=body)
        db.session.add(blogarticle)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # 引数idに一致するデータを取得する
    blogarticle = BlogArticle.query.get(id)
    if request.method == "GET":
        return render_template('update.html', blogarticle=blogarticle)
    else:
        # 上でインスタンス化したblogarticleのプロパティを更新する
        blogarticle.title = request.form.get('title')
        blogarticle.body = request.form.get('body')
        # 更新する場合は、add()は不要でcommit()だけでよい
        db.session.commit()
        return redirect('/')
    
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # 引数idに一致するデータを取得する
    blogarticle = BlogArticle.query.get(id)
    db.session.delete(blogarticle)
    db.session.commit()
    return redirect('/')



# @app.route("/", methods=['GET'])
# def websta():
#     if request.method == 'GET':
#         categories = Category.query.all()
#         subjects = Subject.query.all()
#         return render_template("index.html",categories=categories,subjects=subjects)

# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == "POST":
#         category_name = request.form.get('category_name')
#         subject_name = request.form.get('subject_name')
        
#         category = Category(name=category_name)
#         subject = Subject(name=subject_name)
#         db_session.add(subject,category)
#         db_session.commit()
#         return redirect('/')
#     else:
#         return render_template('create.html')
    
if __name__ == "__main__":
    app.run(debug=True)