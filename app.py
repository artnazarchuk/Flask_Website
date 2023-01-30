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
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('about.html', articles=articles)

@app.route('/article/<int:id>')
def article_detail(id):
    detail = Article.query.get(id)
    return render_template('article_detail.html', detail=detail)

@app.route('/article/<int:id>/delete')
def article_delete(id):
    detail = Article.query.get_or_404(id)
    try:
        db.session.delete(detail)
        db.session.commit()
        return redirect('/about')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/article/<int:id>/update', methods=['POST', 'GET'])
def article_update(id):
    detail = Article.query.get(id)
    if request.method == 'POST':
        detail.title = request.form['title']
        detail.intro = request.form['intro']
        detail.text = request.form['text']

        try:
            db.session.add(detail)
            db.session.commit()
            return redirect('/about')
        except:
            return 'При обновлении статьи произошла ошибка'
    else:
        detail = Article.query.get(id)
        return render_template('article_update.html', detail=detail)

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
