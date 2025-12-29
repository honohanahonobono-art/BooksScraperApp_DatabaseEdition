from bs4 import BeautifulSoup #取得したHTMLを、きれいに整形してくれるもの
from bs4 import Comment
import requests 
import re
import pandas as pd
from urllib.parse import urljoin


def get_data_book_ec():


    BASE="https://books.toscrape.com/"
    url=BASE + "index.html"


    data_ec=[]
    session = requests.Session() 
    
    page=1
    
    while True:
        print(f"==={page}ページ目：{url}===")

        res=session.get(url)
        res.encoding="utf-8"
        soup=BeautifulSoup(res.text,'html.parser')

        item=soup.find("ol",class_="row")
        lists=item.find_all("li")


        for book in lists:
            datum_ec={}
    #本のタイトル
            datum_ec["full_title"]=book.find("h3").find("a")["title"]

    #価格
            price=book.find("p",{"class":"price_color"}).text
            datum_ec["price"]=float(price.replace("£",""))

    #詳細リンク
            link=book.find("a")["href"]
            
            one_link=urljoin(url,link)
            datum_ec["link"]=one_link

    #在庫・レビュー・評価の初期値
            datum_ec["stock"]=0
            datum_ec["rating"]=0
            
            instocks=book.find("p",{"class":"instock availability"}).get_text(strip=True)
            
            
            if "In stock" in instocks :
                try:
                    res=requests.get(one_link,timeout=20)
                    res.encoding="utf-8"
                    soup_stocks=BeautifulSoup(res.text,'html.parser')
                    #在庫状況
                    stock=soup_stocks.find("p",{"class":"instock availability"})
                    if stock:
                        stock_text=stock.get_text(strip=True)
                        if "(" in stock_text :
                            num_stock=stock_text.split("(")[1].split()[0]
                            datum_ec["stock"]=int(num_stock)
                    #★★★星の数（rating）を取得★★★
                    rating_tag=soup_stocks.find("p",{"class":"star-rating"})
                    if rating_tag :
                        classes=rating_tag.get("class",[])
                        rating_word=[c for c in classes if c!="star-rating"][0]
                        rating_map={"One":1,"Two":2,"Three":3,"Four":4,"Five":5}     
                        datum_ec["rating"]=rating_map.get(rating_word,0)               
                except requests.exceptions.RequestException as e :
                    print(f"△詳細ページ取得失敗：{one_link}/{e}")            
                
    
          

            
                
            data_ec.append(datum_ec)
    #nextボタンを探し、次のURLページを探す
        botton_tag=soup.find("li",{"class":"next"})

        if botton_tag is None :
            break
        
        next_link=botton_tag.find("a")["href"]
        url= urljoin(url,next_link)
        page +=1

    df_ec=pd.DataFrame(data_ec)
    return df_ec

df_ec=get_data_book_ec()
#print(df_ec.head())
#print(df_ec.columns)

df_ec.to_csv("books.csv",index=False,encoding="utf-8-sig")

#ここからDBへの保存処理を追加
import sqlite3
df_db=df_ec.rename(columns={"full_title":"title"}).copy()

conn=sqlite3.connect("books.db")
df_db.to_sql("books",conn,if_exists="append",index=False)
print("DBへの保存が完了しました。")