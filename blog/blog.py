from flask import Flask, render_template, url_for, redirect, request, session
from flask_bootstrap import Bootstrap
from forms import ReigsterForm, LoginForm, ArticleForm, InfoForm
from exts import db
from models import User, Article, Comment, Film
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(24)  # 随机生成24个字节的字符串
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" \
                                        + os.path.join(basedir, 'blogdata.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)  # 初始化


@app.route('/')
def index():
    # db.drop_all()
    # db.create_all()
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = ReigsterForm()
    # 跳转是get,提交表单是post
    if request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        telephone = form.telephone.data
        username = form.username.data
        password = form.password.data
        confirmpassword = form.confirmpassword.data
    tel = User.query.filter(User.telephone == telephone).first()
    if tel:
        return '该手机号码已被注册，请更换手机号码重新注册！'
    elif password != confirmpassword:
        return '两次密码不相等，请重新输入！'
    else:
        date = User(telephone=telephone, username=username, password=password)
        db.session.add(date)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        telephone = form.telephone.data
        password = form.password.data
    user = User.query.filter(User.telephone == telephone).first()
    if user and user.password == password:
        session['user_id'] = user.id
        session.permanent = True  # 设置session中的数据存活周期为1个月
        return redirect(url_for('index'))
    else:
        return '用户名或密码输入错误，请重新输入！'


@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session.clear()
    if request.method == 'GET':
        return redirect(url_for('login'))


@app.route('/article/', methods=['GET', 'POST'])
def article():
    if session.get('user_id'):
        form = ArticleForm()
        if request.method == 'GET':
            return render_template('article.html', form=form)
        else:
            title = form.title.data
            content = form.content.data
            article = Article(title=title, content=content)
            article.author_id = session.get('user_id')
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/article/<article_id>/', )
def detail(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    return render_template('detail.html', article=article)


@app.route('/comment/', methods=['GET', 'POST'])
def comment():
    content = request.form.get('comment_content')
    article_id = request.form.get('article_id')
    comment = Comment(content=content, article_id=article_id)
    comment.author_id = session.get('user_id')
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', article_id=article_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    articles = Article.query.filter(Article.title.contains(q))
    return render_template('index.html', articles=articles)


@app.route('/user_detail/<user_id>')
def user_detail(user_id):
    user = User.query.filter(User.id == user_id).first()
    articles = Article.query.filter(Article.author_id == user_id).all()
    count = len(articles)
    return render_template('user_detail.html', user=user, articles=articles, count=count)


@app.route('/edit_info/<user_id>', methods=['GET', 'POST'])
def edit_info(user_id):
    form = InfoForm()
    user = User.query.filter(User.id == user_id).first()
    if request.method == 'GET':
        return render_template('edit_info.html', form=form)
    else:
        email = request.form.get('email')
        address = request.form.get('address')
        hobby = request.form.get('hobby')
        user.email = email
        user.address = address
        user.hobby = hobby
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))


@app.route('/movie/')
def movie():
    return render_template('movies_index.html')


@app.route('/movie_search/', methods=['GET', 'POST'])
def movie_search():
    kw = request.form.get('kw')
    films = Film.query.filter(Film.title.contains(kw))
    return render_template('movie_list.html', films=films)


@app.route('/movie_detail<film_id>/')
def movie_detail(film_id):
    film = Film.query.filter(Film.id == film_id).first()
    return render_template('movie_detail.html', film=film)



'''
上下文处理器，上下文处理器会返回一个字典，字典的key在所有的html页面都能作为变量使用
被上下文处理器所修饰的函数必须返回一个字典，如果为空则返回空字典
'''


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'um': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
