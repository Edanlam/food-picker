import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="小羊宝宝今天吃什么", layout="centered")

# 初始化会话状态
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "brand_list_in_cat" not in st.session_state:
    st.session_state.brand_list_in_cat = []
if "final_pick" not in st.session_state:
    st.session_state.final_pick = None

@st.cache_data
def load_data():
    df = pd.read_excel("Ymmme.xlsx")
    return df

df = load_data()

st.markdown("# 🥘 小羊宝宝今天吃什么")
st.divider()

if st.button("🎲 第一步：先随机一个美食品类", use_container_width=True, type="primary"):
    all_categories = df["美食品类"].unique().tolist()
    rand_cat = random.choice(all_categories)
    st.session_state.selected_category = rand_cat
    cat_df = df[df["美食品类"] == rand_cat].copy()
    st.session_state.brand_list_in_cat = cat_df.to_dict("records")
    st.session_state.final_pick = None

if st.session_state.selected_category is not None:
    st.subheader(f"✅ 抽到品类：{st.session_state.selected_category}")
    st.markdown("**该品类下面可选品牌：**")
    for item in st.session_state.brand_list_in_cat:
        st.markdown(f"- {item['品牌名称']}（人均{item['参考人均(元)']}元）")
    st.divider()

    if st.button("🍽️ 第二步：从该品类抽一家吃饭", use_container_width=True, type="primary"):
        st.session_state.final_pick = random.choice(st.session_state.brand_list_in_cat)

    if st.session_state.final_pick is not None:
        item = st.session_state.final_pick
        st.subheader("🎉今天就吃这家！")
        st.markdown(f"""
**品牌名称**：{item['品牌名称']}
**美食品类**：{item['美食品类']}
**参考人均**：{item['参考人均(元)']}元
**口味**：{item['口味']}
**是否含辣**：{item['是否含辣']}
**食材**：{item['食材']}
**适合场景**：{item['适合场景']}
**特色备注**：{item['特色备注']}
""")

st.divider()
st.caption("文件放在同一目录，访问 http://localhost:8501")
