import streamlit as st

st.set_page_config(
    page_title="Stock Insight",
    page_icon="📈",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.hero {
    padding: 80px 20px 60px 20px;
    text-align: center;
}
.hero-title {
    font-size: 56px;
    font-weight: 800;
    color: #e6edf3;
}
.hero-sub {
    font-size: 20px;
    color: #9da7b1;
    margin-top: 16px;
}
.hero-btn {
    margin-top: 40px;
}
.hero-btn button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 14px;
    padding: 16px 28px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}
.hero-btn button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
}

.feature-card {
    background: linear-gradient(135deg, #1f2933, #0b1220);
    border-radius: 20px;
    padding: 30px;
    height: 100%;
    border: 1px solid #30363d;
}
.feature-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 12px;
}
.feature-desc {
    color: #9da7b1;
    font-size: 16px;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="hero-title">📊 Stock Insight</div>
    <div class="hero-sub">
        종목 비교 · 시장 요약 · 나의 수익률을 한눈에
    </div>
</div>
""", unsafe_allow_html=True)

# CTA 버튼
c1, c2 = st.columns([1, 1])

with c1:
    if st.button("🚀 종목 비교 시작하기", use_container_width=True):
        st.switch_page("pages/Cart.py")

with c2:
    if st.button("📈 시장 요약 보기", use_container_width=True):
        st.switch_page("pages/Market Summary.py")

# ---------------- FEATURES ----------------
st.markdown("## ✨ 주요 기능")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 종목 비교</div>
        <div class="feature-desc">
            관심 종목을 장바구니에 담아<br>
            기간별 수익률을 한눈에 비교하세요.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🚀 시장 요약</div>
        <div class="feature-desc">
            KOSPI · KOSDAQ 지수와<br>
            주간 상승률 TOP 종목을 빠르게 확인합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">💰 내 수익률 계산</div>
        <div class="feature-desc">
            내가 산 종목의 현재 수익률을<br>
            자동으로 계산해보세요.
        </div>
    </div>
    """, unsafe_allow_html=True)
    # ---------------- HELP / CONTACT ----------------
st.markdown("""
<div style="
    margin-top: 60px;
    padding: 30px;
    background: linear-gradient(135deg, #111827, #0b1220);
    border-radius: 20px;
    border: 1px solid #30363d;
    text-align: center;
">
    <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px;">
        🤔 더 궁금한 점이 있으신가요?
    </div>
    <div style="color: #9da7b1; font-size: 16px; line-height: 1.6;">
        서비스 사용 중 궁금한 점은 <b>FAQ</b> 페이지에서 먼저 확인해 주세요.<br>
        그 외 문의 사항은 아래 이메일로 연락 주시면 답변드리겠습니다.
    </div>
    <div style="margin-top: 16px; font-size: 17px; font-weight: 600;">
        📩 suasua0105@gmail.com
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("📌 Data Source: FinanceDataReader · Yahoo Finance")
st.caption("🛠 Built with Streamlit · Dark Finance UI")
