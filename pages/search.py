# 표준 라이브러리
import datetime
from io import BytesIO

# 서드파티 라이브러리
import datetime
from io import BytesIO
import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

st.header( '🔎 종목 검색하기')

def get_krx_company_list() -> pd.DataFrame:
     try:
        # 파이썬 및 인터넷의 기본 문자열 인코딩 방식- UTF-8
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        # MS 프로그램들은 cp949 / 구 몇몇 파일들의 인코딩 방식: EUC-KR
        df_listing = pd.read_html(url, header=0, flavor='bs4', encoding='EUC-KR')[0]
        
        # 필요한 컬럼만 추출 및 종목코드 6자리 포맷 맞추기
        df_listing = df_listing[['회사명', '종목코드']].copy()
        df_listing['종목코드'] = df_listing['종목코드'].apply(lambda x: f'{x:06}')
        return df_listing
     except Exception as e:
         st.error(f"상장사 명단을 불러오는 데 실패했습니다: {e}")
         return pd.DataFrame(columns=['회사명', '종목코드'])

@st.cache_data
def load_company_list():
    return pd.read_csv("kospi_list.csv")

company_df = load_company_list()

company_name = st.selectbox(
    "조회할 회사를 선택하세요",
    company_df["회사명"],
    index=None,
    placeholder="회사명을 입력하거나 선택하세요"
)

def get_stock_code_by_company(company_name: str) -> str:
    # 만약 입력값이 숫자 6자리라면 그대로 반환
    if company_name.isdigit() and len(company_name) == 6:
        return company_name
    
    company_df = get_krx_company_list()
    codes = company_df[company_df['회사명'] == company_name]['종목코드'].values
    if len(codes) > 0:
        return codes[0]
    else:
        raise ValueError(f"'{company_name}'을 찾을 수 없습니다. 종목코드 6자리를 직접 입력해보세요.")

# https://docs.streamlit.io/develop/api-reference/widgets/st.date_input

def get_start_date(period: str) -> str:
    today = datetime.date.today()

    if period == "1주일":
        start = today - datetime.timedelta(days=7)
    elif period == "1개월":
        start = today - datetime.timedelta(days=30)
    elif period == "3개월":
        start = today - datetime.timedelta(days=90)
    elif period == "1년":
        start = today - datetime.timedelta(days=365)
    elif period == "3년":
        start = today - datetime.timedelta(days=365*3)

    return start.strftime("%Y%m%d"), today.strftime("%Y%m%d")

confirm_btn = st.button('조회하기') # 클릭하면 True

period = st.radio(
    "조회 기간",
    ["1주일", "1개월", "3개월", "1년", "3년"],
    horizontal=True
)

# --- 메인 로직 ---
if confirm_btn:
    if not company_name: # '' 
        st.warning("조회할 회사 이름을 입력하세요.")
    else:
         try:
            with st.spinner('데이터를 수집하는 중...'):
                stock_code = get_stock_code_by_company(company_name)
                start_date, end_date = get_start_date(period)
                
                price_df = fdr.DataReader(stock_code, start_date, end_date)
                
            if price_df.empty:
                st.info("해당 기간의 주가 데이터가 없습니다.")
            else:
                st.subheader(f"[{company_name}] 주가 데이터")
                st.dataframe(price_df.tail(10), width="stretch")

                #Plotly 시각화
                fig = go.Figure()

                fig.add_trace(
                    go.Scatter(
                        x=price_df.index,
                        y=price_df['Close'],
                        mode='lines',
                        name='Close',
                        line=dict(color='red', width=4),
                        hovertemplate=
                            "종가: %{y:,.0f}원<br>" +
                            "거래량: %{customdata:,.0f}<extra></extra>",
                        customdata=price_df['Volume']
                    )
                )

                fig.update_layout(
                    title=f"{company_name} 종가 추이",
                    xaxis_title="날짜",
                    yaxis_title="가격",
                    template="plotly_white",
                    hovermode="x unified"
                )

                st.plotly_chart(fig, use_container_width=True)
                # 엑셀 다운로드 기능
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    price_df.to_excel(writer, index=True, sheet_name='Sheet1')
                st.download_button(
                    label="📥 엑셀 파일 다운로드",
                    data=output.getvalue(),
                    file_name=f"{company_name}_주가.xlsx",
                    mime="application/vnd.ms-excel"
                )
         except Exception as e:
             st.error(f"오류가 발생했습니다: {e}")


