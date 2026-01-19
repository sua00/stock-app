import streamlit as st

st.title("❓ 자주 묻는 질문 (FAQ)")
st.caption("Stock Insight 사용 중 자주 나오는 질문들을 정리했습니다.")

st.markdown("---")

with st.expander("📊 이 서비스는 어떤 기능을 제공하나요?"):
    st.write("""
    **Stock Insight**는 다음 기능을 제공합니다.
    - 종목 장바구니 기반 **수익률 비교**
    - KOSPI / KOSDAQ **시장 요약**
    - 기간별 **정규화 수익률 시각화**
    - (예정) 내 수익률 계산 기능
    """)

with st.expander("🧺 장바구니는 어떤 용도인가요?"):
    st.write("""
    관심 있는 종목을 장바구니에 담아  
    **두 종목을 선택하여 기간별 수익률을 비교**할 수 있습니다.
    
    최소 2개 이상의 종목이 필요합니다.
    """)

with st.expander("📅 수익률 비교 기준은 어떻게 계산되나요?"):
    st.write("""
    선택한 기간의 **첫 날 종가를 100으로 정규화**하여  
    상대적인 수익률 변화를 비교합니다.
    
    → 종목 간 가격 차이와 무관하게 흐름 비교가 가능합니다.
    """)

with st.expander("📈 데이터는 어디서 가져오나요?"):
    st.write("""
    주가 데이터는 **FinanceDataReader**를 통해  
    Yahoo Finance 및 KRX 데이터를 기반으로 제공됩니다.
    
    ※ 데이터 지연 또는 누락이 발생할 수 있습니다.
    """)

with st.expander("⚠️ 투자 판단에 사용해도 되나요?"):
    st.write("""
    ❗ 본 서비스는 **학습 및 참고용**입니다.  
    실제 투자 판단의 책임은 사용자 본인에게 있습니다.
    """)

with st.expander("🚀 앞으로 어떤 기능이 추가될 예정인가요?"):
    st.write("""
    - 내 매수 시점 기준 **실현/미실현 수익률 계산**
    - 포트폴리오 저장
    - 관심 종목 알림
    - 비교 결과 이미지 / CSV 저장
    """)

st.markdown("---")
st.caption("🛠 Built with Streamlit · Data by FinanceDataReader")
