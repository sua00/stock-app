import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import plotly.express as px

st.title("📊 시장 요약")

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
one_week_ago = today - datetime.timedelta(days=7)

st.subheader("📈 주요 지수")

col1, col2 = st.columns(2)

with col1:
    kospi = fdr.DataReader("KS11", yesterday.strftime("%Y%m%d"), today.strftime("%Y%m%d"))
    diff = kospi['Close'].iloc[-1] - kospi['Close'].iloc[0]
    pct = diff / kospi['Close'].iloc[0] * 100
    st.metric("KOSPI", f"{kospi['Close'].iloc[-1]:,.2f}", f"{pct:.2f}%")

with col2:
    kosdaq = fdr.DataReader("KQ11", yesterday.strftime("%Y%m%d"), today.strftime("%Y%m%d"))
    diff = kosdaq['Close'].iloc[-1] - kosdaq['Close'].iloc[0]
    pct = diff / kosdaq['Close'].iloc[0] * 100
    st.metric("KOSDAQ", f"{kosdaq['Close'].iloc[-1]:,.2f}", f"{pct:.2f}%")

## 주간 상승률
@st.cache_data
def load_kospi200():
    df = fdr.StockListing("KOSPI")
    return df.head(200)[['Name', 'Code']]

kospi200 = load_kospi200()   
st.subheader("🚀 주간 상승률 TOP 10 (상위 100개)")

records = []

top100 = kospi200.head(100)

for _, row in top100.iterrows():
    try:
        df = fdr.DataReader(
            row['Code'],
            one_week_ago.strftime("%Y%m%d"),
            today.strftime("%Y%m%d")
        )
        if len(df) >= 2:
            start, end = df['Close'].iloc[0], df['Close'].iloc[-1]
            records.append({
                "회사명": row['Name'],
                "주간 상승률(%)": round((end - start) / start * 100, 2),
                "최근 종가": end   # ⭐ 추가
            })
    except:
        pass

weekly_df = pd.DataFrame(records)
top10_weekly = weekly_df.sort_values("주간 상승률(%)", ascending=False).head(10)

fig = px.bar(
    top10_weekly,
    x="주간 상승률(%)",
    y="회사명",
    orientation="h",
    text="주간 상승률(%)",
    title="🚀 주간 상승률 TOP 10 (KOSPI 상위 100)",
    custom_data=["최근 종가"]
)

fig.update_layout(
    xaxis_title="상승률 (%)",
    yaxis_title="",
    template="plotly_dark",
    height=400
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
    hovertemplate=
        "회사명: %{y}<br>" +
        "주간 상승률: %{x:.2f}%<br>" +
        "최근 종가: %{customdata[0]:,.0f}원" +
        "<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(top10_weekly, use_container_width=True)
