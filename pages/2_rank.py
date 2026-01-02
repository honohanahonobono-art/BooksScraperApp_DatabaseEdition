import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


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
    stock_only = st.checkbox("📦 在庫ありのみ表示", value=True)



# ここにDBからデータを取得して表示する処理を追加
DB_PATH="books.db"

def load_top5(stock_only:bool):
    conn=sqlite3.connect(DB_PATH)
    where="WHERE stock>0" if stock_only else ""
    query=f"""
    SELECT title,price,link,stock,rating
    FROM books
    {where}
    ORDER BY rating DESC,STOCK DESC,price ASC
    LIMIT 5
    """
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df

df_top5=load_top5(stock_only)


st.subheader("⭐️人気ランキングTOP5")
#st.bar_chart(df_top5.set_index("title")["rating"])
#横棒グラフに変更
df_plot=df_top5.sort_values("rating")

fig,ax=plt.subplots(figsize=(8,4))
ax.barh(df_plot["title"],df_plot["rating"])

ax.set_xlabel("Rating (★マーク)")
ax.set_ylabel("タイトル")
ax.set_title("人気ランキングTOP5")

st.pyplot(fig)


# データフレームを表示
st.subheader("⭐️人気ランキングTOP5（詳細）在庫あり" if stock_only else "⭐️人気ランキングTOP5（詳細）全て")
#詳細リンクをクリック可能にする
#df_top5["link"]=df_top5["link"].apply(lambda x:f"[詳細ページ]({x})")
#st.dataframe(df_top5,use_container_width=True)
st.data_editor(
    df_top5,
    column_config={"link":st.column_config.LinkColumn("詳細ページ",display_text="詳細ページ")},
    hide_index=True,
    use_container_width=True
    
    
)


