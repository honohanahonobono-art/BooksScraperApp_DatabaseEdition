import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
#日本語フォント設定
import matplotlib.pyplot as plt
from matplotlib import font_manager,rcParams

from pathlib import Path
from matplotlib import font_manager, rcParams

FONT_PATH = Path(__file__).parent / "fonts" / "NotoSansCJKjp-VF.otf"

if FONT_PATH.exists():
    font_prop = font_manager.FontProperties(fname=str(FONT_PATH))
    rcParams["font.family"] = font_prop.get_name()
else:
    rcParams["font.family"] = "DejaVu Sans"  # 最後の保険
    

# Streamlitアプリの設定
st.set_page_config(page_title="Book App",layout="wide")

st.title("📚　在庫確認ページ　📚")

#サイドバー設定

with st.sidebar:
    st.header("⚙️　表示設定　⚙️")
        
        
    stock_only= st.checkbox("📦 在庫ありのみ表示",value=True)
        
    st.subheader("📦 在庫アラート設定")

    threshold = st.number_input(
        "在庫アラートの値（この数以下で警告）",
        min_value=0,
        max_value=100,
        value=5,
        step=1
    )
    
    
#在庫不足データの取得と表示
from stock_alert import load_stock_alert
df_alert = load_stock_alert(threshold)
#アラート件数を見出しに表示
alert_count = len(df_alert)

with st.expander(f"🔺在庫アラート({alert_count}件)を表示",expanded=False):
                if df_alert.empty:
                     st.success("在庫不足は発生していません🙌")
                else:
                    st.warning(f"在庫不足が{alert_count}件発生しています⚠️")

                    st.data_editor(
                        df_alert,
                        column_config={"link":st.column_config.LinkColumn("詳細ページ",display_text="詳細ページ")},
                        hide_index=True,
                        use_container_width=True
                    )

# 在庫検索　

from stock_search import search_books
st.subheader("🔍　在庫検索　🔍")

with st.form("search_form"):
    col1,col2,col3=st.columns([2,2,1])
    with col1:
        keyword=st.text_input("キーワード検索（タイトルに含む）",value="")
    with col2:
        min_stock_raw=st.text_input("最低在庫数絞込（未入力OK）",value="")
    with col3:
        submitted=st.form_submit_button("検索")
    min_stock=None
    input_error=False
    if min_stock_raw.strip():
        try:
            min_stock_val=int(min_stock_raw)
            if min_stock_val<0:
                st.warning("最低在庫数は0以上で入力してください")
                input_error=True
            else:
                min_stock=min_stock_val
        except ValueError:
            st.error("最低在庫数は数字で入力してください")
            input_error=True

if submitted and not input_error:
    df_search=search_books(keyword,min_stock,stock_only)
    st.caption(f"検索結果：{len(df_search)}件")
    st.data_editor(
        df_search,
        column_config={"link":st.column_config.LinkColumn("詳細ページ",display_text="詳細ページ")},
        hide_index=True,
        use_container_width=True
    )
elif not submitted:
    st.info("検索条件を入力して「検索」を押してください")



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


