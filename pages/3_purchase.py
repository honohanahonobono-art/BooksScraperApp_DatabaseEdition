import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


#日本語フォント設定
from pathlib import Path
from matplotlib import font_manager, rcParams

FONT_PATH = Path(__file__).parent / "fonts" / "NotoSansJP-Regular.ttf"

# デフォルト
rcParams["font.family"] = "DejaVu Sans"

# フォントがあれば、それを“直接使う”設定にする（登録しない）
if FONT_PATH.exists():
    jp_font = font_manager.FontProperties(fname=str(FONT_PATH))
else:
    jp_font = None
    
import streamlit as st

with st.sidebar:
    st.header("⚙️ 表示設定")
    stock_only = st.checkbox("📦 在庫ありのみ表示", value=True)
    

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

top_n=st.slider("上位カテゴリ数設定",5,20,10,step=5)
df_view=df.head(top_n)

st.subheader(f"📚 評価の高いカテゴリTOP{top_n} 📚")






#データ準備
categories = df_view["category_name"]
scores = df_view["score"]
avg_ratings = df_view["average_rating"]
fig,ax1=plt.subplots(figsize=(10,5))

# 棒グラフ（スコア）
ax1.bar(categories,scores,alpha=0.7)
ax1.set_ylabel("仕入スコア（優先度）",fontproperties=jp_font)
ax1.set_xlabel("カテゴリ",fontproperties=jp_font)
ax1.tick_params(axis='x', rotation=45)


#折れ線グラフ（平均評価）
ax2=ax1.twinx()
ax2.plot(categories,avg_ratings,color="orange",marker="o",linestyle="--")
ax2.set_ylabel("平均評価（⭐️）",fontproperties=jp_font)
ax2.set_ylim(0,5)

ax1.set_title(f"仕入参考指標　TOP{top_n}",fontproperties=jp_font)

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




