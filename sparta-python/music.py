import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

genie = soup.select('#body-content > div > div > table > tbody > tr')


rank = 1
for music in genie:
    a_tag = music.select_one('td.info > a.title.ellipsis')
    b_tag = music.select_one('td.info > a.artist.ellipsis')
    c_tag = music.select_one('td.info > a.')
        if a_tag is not None:

        title = a_tag.text
        singer = b_tag.text
        print(rank, title.strip(), singer.strip())

        doc = {
            'rank' : rank,
            'title' : title,
            'singer' : singer
        }
    #    db.musics.insert_one(doc)
    #    rank += 1