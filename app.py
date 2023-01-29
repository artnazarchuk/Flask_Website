from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    articles = Article.query.order_by(Article.date).all()
    return render_template('about.html', articles=articles)

@app.route('/article', methods=['POST', 'GET'])
def article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article_create = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article_create)
            db.session.commit()
            return redirect('/about')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('article.html')


if __name__ == '__main__':
    app.run(debug=True)
