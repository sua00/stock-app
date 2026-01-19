import streamlit as st
import FinanceDataReader as fdr
import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="내 수익률 계산기", layout="wide")

# -----------------------------
# CSS (카드 스타일)
# -----------------------------
st.markdown("""
<style>
.card {
    background: linear-gradient(135deg, #1f2933, #0b1220);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
}
.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 종목 리스트 로드
# -----------------------------
@st.cache_data(ttl=60*60*24)
def load_company_list():
    df = fdr.StockListing("KOSPI")
    return df[['Name', 'Code']]

company_df = load_company_list()

# -----------------------------
# 페이지 타이틀
# -----------------------------
st.title("📈 내 수익률 계산기")
st.caption("구매 날짜만 입력하면, 구매 기준가를 자동으로 계산해줍니다.")

# -----------------------------
# 입력 영역
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🧾 매수 정보 입력</div>', unsafe_allow_html=True)

selected = st.selectbox(
    "종목 선택",
    company_df.to_dict("records"),
    format_func=lambda x: x["Name"]
)

buy_date = st.date_input(
    "구매 날짜",
    value=datetime.date.today() - datetime.timedelta(days=30)
)

quantity = st.number_input(
    "수량",
    min_value=1,
    step=1
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 데이터 조회
# -----------------------------
buy_date_str = buy_date.strftime("%Y%m%d")
today_str = datetime.date.today().strftime("%Y%m%d")

df = fdr.DataReader(
    selected["Code"],
    buy_date_str,
    today_str
)

if df.empty:
    st.warning("해당 날짜 이후의 주가 데이터가 없습니다.")
    st.stop()

# 구매 기준가 & 현재가
buy_price = df['Close'].iloc[0]      # 가장 가까운 거래일 기준
current_price = df['Close'].iloc[-1]

# -----------------------------
# 수익 계산
# -----------------------------
buy_amount = buy_price * quantity
current_amount = current_price * quantity
profit = current_amount - buy_amount
profit_rate = profit / buy_amount * 100

# -----------------------------
# 결과 표시
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📊 수익률 결과</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

c1.metric(
    "구매 기준가 (자동)",
    f"{buy_price:,.0f}원"
)

c2.metric(
    "현재 주가",
    f"{current_price:,.0f}원"
)

c3.metric(
    "손익",
    f"{profit:,.0f}원",
    f"{profit_rate:.2f}%"
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 주가 흐름 그래프
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">📉 구매 시점 이후 주가 흐름</div>', unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=df['Close'],
    name="주가",
    line=dict(width=2)
))

fig.add_hline(
    y=buy_price,
    line_dash="dot",
    annotation_text="구매 기준가",
    annotation_position="top left"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="날짜",
    yaxis_title="가격",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
