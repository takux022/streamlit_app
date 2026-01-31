import streamlit as st
import pandas as pd
import time


st.title("都道府県別人口推移の可視化")
st.write("e-Statの人口推移データを用いて、都道府県別の人口推移を可視化する。")


with st.spinner("データを読み込んでいます..."):
    df = pd.read_csv("last.csv")
    time.sleep(1)
st.toast("データ読み込み完了")

year_cols = ["2020年", "2021年", "2022年", "2023年", "2024年"]

for y in year_cols:
    df[y] = df[y].astype(str).str.replace(",", "").astype(int)

with st.sidebar:
    st.header("表示条件")

    population_type = st.selectbox(
        "区分を選択してください",
        df["区分"].unique()
    )

    prefecture = st.selectbox(
        "都道府県を選択してください",
        df["地域"].unique()
    )

    gender = st.radio(
        "性別を選択してください",
        ["男女計", "男", "女"]
    )

    display_type = st.radio(
        "表示形式を選択してください",
        ["グラフ", "表"]
    )

df_selected = df[
    (df["区分"] == population_type) &
    (df["地域"] == prefecture) &
    (df["性別"] == gender)
]


df_selected = df_selected.iloc[0:1]

st.header(f"{prefecture}の人口推移")
st.write(f"区分：{population_type} / 性別：{gender}")
st.write("単位：千人")


tab1, tab2 = st.tabs(["人口推移", "男女比較"])

with tab1:
    display_df = df_selected[year_cols].copy()


display_df.index = [""]

st.dataframe(
    display_df,
    use_container_width=True
)

with st.expander("注意"):
        st.write(
            "2020年10月1日現在は総務省統計局「国勢調査」。"
            "なお、日本人人口は「国勢調査（不詳補完値）」による。"
        )

with tab2:
    st.subheader("2024年 男女人口比較")

    compare_df = df[
        (df["区分"] == population_type) &
        (df["地域"] == prefecture) &
        (df["性別"].isin(["男", "女"]))
    ][["性別", "2024年"]]

    compare_df = compare_df.set_index("性別")

    st.bar_chart(compare_df)
