import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests

#日本語フォント設定
from pathlib import Path
from matplotlib import font_manager, rcParams

BASE_DIR = Path(__file__).resolve().parents[1]  
FONT_PATH = BASE_DIR / "fonts" / "NotoSansJP-Regular.ttf"

if FONT_PATH.exists():
    font_manager.fontManager.addfont(str(FONT_PATH))
    rcParams["font.family"] = "Noto Sans JP"   
else:
    rcParams["font.family"] = "DejaVu Sans"
    
    
import streamlit as st

with st.sidebar:
    st.header("⚙️ 表示設定")
    stock_only = st.checkbox("📦 在庫ありのみ表示", value=True,key="purchase_stock_only")
    

# Streamlitアプリの設定 
from db_setup import init_db

init_db()

DB_PATH="books.db"

@st.cache_data
def load_categories():
    conn=sqlite3.connect(DB_PATH)
    df=pd.read_sql_query("""
       SELECT category_name,category_link,average_rating,score
       FROM categories
       ORDER BY score DESC
    """,conn)
    conn.close()
    return df

# メイン画面の表示
st.title("📊 仕入参考データ 📊")
df=load_categories()

top_n=st.slider("上位カテゴリ数設定",5,20,10,step=5,key="purchase_top_n")
df_view=df.head(top_n)

st.subheader(f"📚 評価の高いカテゴリTOP{top_n} 📚")
st.caption("仕入スコア = 平均評価 × log(1 + 書籍数)")



#データ準備
categories = df_view["category_name"]
scores = df_view["score"]
avg_ratings = df_view["average_rating"]
fig,ax1=plt.subplots(figsize=(10,5))

# 棒グラフ（スコア）
ax1.bar(categories,scores,alpha=0.7)
ax1.set_ylabel("仕入スコア（優先度）")
ax1.set_xlabel("カテゴリ")
ax1.tick_params(axis='x', rotation=45)


#折れ線グラフ（平均評価）
ax2=ax1.twinx()
ax2.plot(categories,avg_ratings,color="orange",marker="o",linestyle="--")
ax2.set_ylabel("平均評価（★）")
ax2.set_ylim(0,5)

ax1.set_title(f"仕入参考指標　TOP{top_n}")

plt.tight_layout()
st.pyplot(fig)



df_view_disp=df_view.rename(columns={
    "category_name":"カテゴリ名",
    "category_link":"リンク",
    "average_rating":"平均評価（⭐️）",
    "score":"仕入スコア（優先度）"
})

st.data_editor(
    df_view_disp,
    column_config={
        "リンク": st.column_config.LinkColumn(
            "リンク",
            display_text="開く"
        )
    },
    hide_index=True,
    use_container_width=True
)







import os
from dotenv import load_dotenv


# API_KEY 定義 
load_dotenv()
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY") or st.secrets.get("GOOGLE_BOOKS_API_KEY")




from googlebooks import fetch_google_books_top10
from datetime import datetime, timedelta
import math



st.write("API_KEY exists:", bool(API_KEY))

st.subheader("📚 Google Books 人気本（直近1年）")




selected_cat = st.selectbox(
    "カテゴリを選択",
    df["category_name"].tolist(),key="purchase_selected_cat"
)

dfb = fetch_google_books_top10(selected_cat, API_KEY, lang="ja", max_results=40)
if dfb is None or dfb.empty:
    st.warning("Google Books データが取得できませんでした")
    st.stop()

if dfb is None or dfb.empty:
    st.warning("Google Books データが取得できませんでした")
    st.stop()


#直近1年に絞る
one_year_ago=datetime.now()-timedelta(days=365)
df_recent=dfb.dropna(subset=["published_dt"]).copy()
df_recent=df_recent[df_recent["published_dt"]>= one_year_ago]
base = df_recent if len(df_recent) >= 5 else dfb

base = base.sort_values(["pop_score", "ratingsCount"], ascending=False).head(10)



st.data_editor(base,
    column_config={
        "infoLink": st.column_config.LinkColumn(
            "リンク",
            display_text="開く"
        )
    },
    hide_index=True,
    width="stretch")

