import streamlit as st
import FinanceDataReader as fdr
import datetime
import plotly.graph_objects as go
import pandas as pd

# 1. CSS 수정: 카드 스타일 및 간격 설정
st.markdown("""
<style>
    /* 카드 전체 컨테이너 사이의 여백 */
    .stColumn {
        margin-bottom: 10px;
    }
    
    /* 카드 스타일 */
    .cart-card {
        background: linear-gradient(135deg, #1f2933, #0b1220);
        border-radius: 12px;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        height: 60px; /* 버튼과 높이 맞춤 */
        border: 1px solid #30363d;
    }
    
    .cart-name {
        font-size: 18px;
        font-weight: 600;
        color: #e6edf3;
    }

    /* Streamlit 버튼 스타일 커스텀 (쓰레기통 버튼) */
    div[data-testid="stButton"] button {
        height: 60px;
        width: 100%;
        border-radius: 12px;
        background-color: #1f2933;
        border: 1px solid #30363d;
        color: white;  
        transition: 0.3s;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #ff4b4b;
        color: white;
        border-color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)


if "cart" not in st.session_state:
    st.session_state.cart = []

@st.cache_data
def load_company_list():
    return pd.read_csv("kospi_list.csv")

company_df = load_company_list()

st.title("📊 종목 비교")
st.subheader("🧺 비교할 종목 담기")

selected = st.selectbox(
    "종목 검색",
    company_df.to_dict("records"),
    format_func=lambda x: x["Name"]
)

if st.button("장바구니에 담기"):
    if selected not in st.session_state.cart:
        st.session_state.cart.append(selected)
        st.success(f"{selected['Name']} 추가됨")
    else:
        st.info("이미 담긴 종목입니다.")

st.markdown("---")
st.markdown("### 🛒 현재 장바구니")

# 2. 장바구니 렌더링 부분 수정
for i, item in enumerate(st.session_state.cart):
    # gap='small'을 사용하고 배율을 조정하여 버튼이 카드 옆에 붙게 함
    col_card, col_btn = st.columns([0.85, 0.15], gap="small")

    with col_card:
        st.markdown(
            f"""
            <div class="cart-card">
                <span class="cart-name">{item['Name']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_btn:
        # 삭제 버튼 (CSS로 카드와 높이를 맞춤)
        if st.button("🗑️", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()
      
cart = st.session_state.get("cart", [])

if len(cart) < 2:
    st.warning("장바구니에 최소 2개 종목이 필요합니다.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    stock1 = st.selectbox("종목 1", cart, key="stock1")

with col2:
    stock2 = st.selectbox(
        "종목 2",
        [s for s in cart if s != stock1],
        key="stock2"
    )

period = st.radio(
    "비교 기간",
    ["1개월", "3개월", "6개월", "1년"],
    horizontal=True
)

def get_start_date(period):
    today = datetime.date.today()
    days = {"1개월":30, "3개월":90, "6개월":180, "1년":365}[period]
    return (today - datetime.timedelta(days=days)).strftime("%Y%m%d"), today.strftime("%Y%m%d")

start, end = get_start_date(period)

df1 = fdr.DataReader(stock1["Code"], start, end)
df2 = fdr.DataReader(stock2["Code"], start, end)

df1['norm'] = df1['Close'] / df1['Close'].iloc[0] * 100
df2['norm'] = df2['Close'] / df2['Close'].iloc[0] * 100

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df1.index,
    y=df1['norm'],
    name=stock1["Name"]   # ⭐ 문자열로
))
fig.add_trace(go.Scatter(
    x=df2.index,
    y=df2['norm'],
    name=stock2["Name"]
))

fig.update_layout(
    title="📈 수익률 비교 (100 기준 정규화)",
    template="plotly_dark",
    yaxis_title="지수화 수익률"
)

st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    st.metric(
        stock1["Name"],
        f"{df1['Close'].iloc[-1]:,.0f}원",
        f"{(df1['Close'].iloc[-1]/df1['Close'].iloc[0]-1)*100:.2f}%"
    )

with c2:
    st.metric(
        stock2["Name"],
        f"{df2['Close'].iloc[-1]:,.0f}원",
        f"{(df2['Close'].iloc[-1]/df2['Close'].iloc[0]-1)*100:.2f}%"
    )
