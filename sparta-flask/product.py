from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

@app.route('/')
def home():
    return render_template('product.html')

@app.route('/order', methods=['GET'])
def listing():
    item_receive = request.args.get('item_give')
    result = list(db.orderlists.find({'item':item_receive},{'_id':0}))
    return jsonify({'result':'success', 'orderlists':result})

@app.route('/order', methods=['POST'])
def saving():
    name_give = request.form['name_give']
    count_give = request.form['count_give']
    address_give = request.form['address_give']
    phone_give = request.form['phone_give']
    item_give = request.form['item_give']

    orderlist = {
        'name': name_give,
        'count': count_give,
        'address': address_give,
        'phone': phone_give,
        'item': item_give
    }

    db.orderlists.insert_one(orderlist)

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('127.0.0.1',port=5000,debug=True)