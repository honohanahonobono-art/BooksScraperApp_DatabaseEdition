import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from db_setup import init_db

init_db()


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


    

# Streamlitアプリの設定
st.set_page_config(page_title="Book App",layout="wide")

st.title("📚　Books to Scrape We  管理システム　📚")

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
# 表紙ページへのリンクボタン
st.set_page_config(page_title="Book App", layout="wide")
st.title("⚙️　各機能　⚙️")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📦 在庫確認ページへ", use_container_width=True):
        st.switch_page("pages/1_stock.py")

with col2:
    if st.button("⭐ 自社人気ランキングへ", use_container_width=True):
        st.switch_page("pages/2_rank.py")
with col3:
    if st.button("📊 仕入参考へ", use_container_width=True):
        st.switch_page("pages/3_purchase.py")





