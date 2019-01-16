from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db=SQLAlchemy(app)

@app.cli.command() #注册命令
@click.option('--drop', is_flag=True, help='Create after drop.') #设置选项
def initdb(drop):
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输入提示信息
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True) # 主键
    name=db.Column(db.String(20)) #名字

class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60)) 
    year=db.Column(db.String(4))

@app.cli.command()
def forge():
    db.create_all()

    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
        ]
    user=User(name=name)
    db.session.add(user)
    for m in movies:
        movie= Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')
@app.route('/')
def index():
    user= User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)
@app.route('/user/<name>')
def user_page(name):
    return 'User: {}'.format(name)


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'