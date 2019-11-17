from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_post():
    rank_receive = request.form['rank_give']
    rank_receive = int(rank_receive)

    star_receive = request.form['star_give']
    star_receive = int(star_receive)

    db.movies.update_one({'rank':rank_receive},{'$set':{'star':star_receive}})
    return jsonify({'result':'success'})

@app.route('/test', methods=['GET'])
def test_get():
    rank_receive = request.args.get('rank_give')
    rank_receive = int(rank_receive)
    movie_info = db.movies.find_one({'rank':rank_receive},{'_id':0})
    return jsonify({'result':'success', 'info':movie_info})

@app.route('/new', methods=['POST'])
def new_post():
    rank_receive = int(request.form['rank_give'])
    star_receive = request.form['star_give']
    title_receive = request.form['title_give']

    db.movies.insert_one({'rank':rank_receive, 'star':star_receive, 'title':title_receive})

    return jsonify({'result':'success'})

@app.route('/post', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    author_receive = request.form['author_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'author': author_receive, 'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result':'success'})

@app.route('/post', methods=['GET'])
def listing():
    author_receive = request.args.get('author_give')
    result = list(db.articles.find({'author':author_receive},{'_id':0}))
    return jsonify({'result':'success','articles':result})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)

