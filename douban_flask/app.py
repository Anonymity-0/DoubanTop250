import json

import jieba
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    conn = sqlite3.connect('douban.db')
    cursor = conn.cursor()
    sql = '''
    select sum(rated) from movie;
    '''

    data = cursor.execute(sql)
    for item in data:
        count = item[0]
        break
    sql = '''
    select sum(rated) from book;
    '''
    data = cursor.execute(sql)
    for item in data:
        count += item[0]
        break


    sql = '''
        select inp from book
    '''
    data = cursor.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]
    sql = '''
        select inp from movie
    '''
    data = cursor.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]

    cursor.close()
    cursor.close()

    cut = jieba.cut(text)
    string = ' '.join(cut)
    words = len(string)
    cursor.close()
    conn.close()
    return render_template("index.html",count = count,words = words)


@app.route('/index')
def home():
    return index()


@app.route('/movie')
def movie():
    datalist = []
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    sql = '''
    select * from movie
    '''
    data = cur.execute(sql)

    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return render_template("movie.html", movies=datalist)

@app.route('/score')
def score():
    scores = []
    counts = []
    conn = sqlite3.connect("douban.db")
    cursor = conn.cursor()
    sql = '''
    select score,count(score) from movie group by score
    '''
    data = cursor.execute(sql)
    for item in data:
        scores.append(item[0])
        counts.append(item[1])
    sql1 = '''
    select score,count(score),sum(rated) from book group by score
    '''
    data = cursor.execute(sql1)
    book_socre = []
    book_count = []
    book_rated = []
    for item in data:
        book_socre.append(item[0])
        book_count.append(item[1])
        book_rated.append(item[2])
    cursor.close()
    conn.close()
    return render_template("score.html", scores=scores, counts=counts,book_socre=book_socre,book_count=book_count,book_rated=book_rated)


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/book')
def book():
    datalist = []
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    sql = '''
    select * from book
    '''
    data = cur.execute(sql)
    print(data)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()

    return render_template("book.html",books = datalist)


if __name__ == '__main__':
    app.run()
