from bs4 import BeautifulSoup #取得したHTMLを、きれいに整形してくれるもの
from bs4 import Comment
import requests 
import re
import pandas as pd
from urllib.parse import urljoin
from datetime import datetime

url="https://books.toscrape.com/catalogue/category/books_1/index.html"
    
session=requests.Session()

#最初のページを取得
    
res=session.get(url)
res.encoding="utf-8"
soup=BeautifulSoup(res.text,'html.parser')

item=soup.find("ul",class_="nav nav-list")

#カテゴリ名とリンクを取得
categories = item.find_all("a")
category_linklist = []
category_namelist=[]
for category in categories:
    category_name = category.get_text(strip=True)
    category_link = urljoin(url, category['href'])
    category_namelist.append(category_name)
    category_linklist.append(category_link)


#rating取得
RATING_MAP={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

session=requests.Session()

def get_category_avg_ratings(category_linklist:list[str])->list[dict]:
    
    """
        カテゴリごとの平均評価を取得する関数
    """
    category_ratings = []
    
    for category_link in category_linklist:
        print(f"===カテゴリページ：{category_link}===")
        ratings=[]
        next_link=category_link
        
        while next_link:
            res=session.get(next_link)
            res.encoding="utf-8"
            soup=BeautifulSoup(res.text,'html.parser')
            
            items=soup.find_all("article",class_="product_pod")
            
            for item in items :
                rating_class=item.find("p",class_="star-rating")["class"][1]
                rating=RATING_MAP.get(rating_class,0)
                ratings.append(rating)
            
            #次のページのリンクを取得
            next_page = soup.find("li",class_="next")
            if next_page:
                next_link = urljoin(url, next_page.find("a")['href'])
            else:
                next_link = None

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        count_books=len(ratings)
        category_ratings.append({
            "category_link": category_link,
            "average_rating": avg_rating,
            "count_books": count_books
        })

    return category_ratings

#取得したデータをDataFrameにまとめる
results = get_category_avg_ratings(category_linklist)
df_avg=pd.DataFrame(results)
df_cat=pd.DataFrame({
    "category_name":category_namelist,
    "category_link":category_linklist
})
df=pd.merge(df_cat,df_avg,on="category_link",how="left")
df=df[df["category_name"]!="Books"]
#書籍数が一定以上のカテゴリに絞る
MIN_COUNT=10
df=df[df["count_books"]>=MIN_COUNT]
df=df.sort_values("average_rating",ascending=False).reset_index(drop=True)

#信頼スコア
import numpy as np
df["score"]=df["average_rating"]*np.log1p(df["count_books"])
df=df.sort_values("score",ascending=False)

         

#books.dbに保存　
import sqlite3
conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS categories;")

cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_name TEXT,
    category_link TEXT PRIMARY KEY,
    score REAL,
    average_rating REAL,
    created_at TEXT
);
""")
rows=[]
now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for _,r in df.iterrows():
        rows.append((
            r["category_name"],
            r["category_link"],
            r["average_rating"],
            r["score"],
            now
        ))
        

cur.executemany("""
    INSERT INTO categories (category_name,category_link,average_rating,score,created_at)
    VALUES (?,?,?,?,?)
    ON CONFLICT(category_link) DO UPDATE SET
        category_name=excluded.category_name,
        average_rating=excluded.average_rating,
        score=excluded.score,
        created_at=excluded.created_at
    """,rows)

conn.commit()
conn.close()
print("DBへの保存が完了しました。")