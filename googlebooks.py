import sqlite3
import pandas as pd
import requests
import math
from datetime import datetime, timedelta
import streamlit as st
from db_setup import init_db

init_db()

#Google Booksの出版日フォーマットを変換する関数
def parse_published_date(s:str):
    if not s:
        return None
    try:
        if len(s)==4:
            return datetime(int(s),1,1)
        if len(s)==7:
            return datetime.strptime(s,"%Y-%m")
        return datetime.strptime(s,"%Y-%m-%d")
    except Exception:
        return None
    
#APIを1時間に1000回以上呼び出さないようにするための制御
@st.cache_data(ttl=3600)

#APIを叩く
def fetch_google_books_top10(subject, api_key=None, lang="ja", max_results=40):
    url="https://www.googleapis.com/books/v1/volumes"
    params={
        "q":f"subject:{subject}",
        "langRestrict": lang,
        "orderBy":"relevance",
        "maxResults":min(max_results,40)
    }

    if api_key:
        params["key"]=api_key

    r=requests.get(url,params=params,timeout=20)
    r.raise_for_status()
    data=r.json()

#データの整理
    rows=[]
    for item in data.get("items",[]):
        info=item.get("volumeInfo",{})
        rating=None
        count=0
        if "averageRating" in info:
            rating=info.get("averageRating")
        if "ratingsCount" in info:
            count=info.get("ratingsCount",0) or 0
        pub=parse_published_date(info.get("publishedDate"))
    
    #人気スコア（代理指標）
        if rating is None :
            pop_score=0.0
        else:
            pop_score=float(rating)*math.log1p(int(count))
        
    rows.append({
            "title": info.get("title"),
            "authors": ", ".join(info.get("authors", [])) if info.get("authors") else None,
            "publishedDate": info.get("publishedDate"),
            "published_dt": pub,
            "averageRating": rating,
            "ratingsCount": int(count),
            "pop_score": pop_score,
            "infoLink": info.get("infoLink"),
    })

#データフレームに格納
    return pd.DataFrame(rows)
    


