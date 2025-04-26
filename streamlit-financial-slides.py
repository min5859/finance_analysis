import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide", page_title="풍전비철 재무 분석")

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: white !important;
        background: linear-gradient(to right, #4f46e5, #3b82f6);
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .slide-header {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
        margin-bottom: 1rem;
    }
    .info-card {
        background-color: #f9fafb;
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    .insight-card {
        background: linear-gradient(to right, #f3f4f6, #f9fafb);
        border-radius: 0.5rem;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        margin-top: 1rem;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .highlight {
        color: #4f46e5;
        font-weight: 600;
    }
    .negative {
        color: #ef4444;
        font-weight: 600;
    }
    .positive {
        color: #10b981;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown('<div class="main-header">풍전비철 재무 분석<br><span style="font-size: 1.5rem; font-weight: 400;">2022-2024년 재무성과 종합 분석</span></div>', unsafe_allow_html=True)

# 데이터 준비
# 매출 및 수익성 데이터
performance_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    '매출액': [9470, 8730, 6760],
    '영업이익': [430, 330, 360],
    '순이익': [360, 360, 430],
    '영업이익률': [4.5, 3.8, 5.4],
    '순이익률': [3.8, 4.2, 6.4]
})

# 재무상태표 항목 데이터
balance_sheet_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    '총자산': [3683, 3827, 3859],
    '총부채': [683, 683, 871],
    '자본총계': [2158, 2498, 2988]
})

# 안정성 지표
stability_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    '부채비율': [71, 53, 29],
    '유동비율': [189, 208, 209],
    '이자보상배율': [7.8, 4.4, 7.4]
})

# 현금흐름 데이터
cash_flow_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    '영업활동': [155, 665, -146],
    '투자활동': [-31, -260, -4],
    '재무활동': [0, 0, 0],
    'FCF': [124, 405, -150]
})

# 운전자본 데이터 (CCC)
working_capital_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    'DSO': [36.7, 32.2, 34.1],
    'DIO': [50.8, 43.2, 41.7],
    'DPO': [3.3, 3.3, 8.9],
    'CCC': [84.2, 72.1, 66.9]
})

# ROE 및 수익성 지표
profitability_data = pd.DataFrame({
    'year': ['2022', '2023', '2024'],
    'ROE': [16.8, 14.6, 14.4],
    'ROA': [9.8, 9.5, 11.2],
    '영업이익률': [4.5, 3.8, 5.4],
    '순이익률': [3.8, 4.2, 6.4]
})

# 성장률 계산 데이터
growth_rates = pd.DataFrame({
    'year': ['2023', '2024'],
    '총자산성장률': [3.9, 0.8],
    '매출액성장률': [-7.5, -22.6],
    '순이익성장률': [0.6, 17.8]
})

# 탭 생성
tabs = st.tabs([
    "핵심 요약", 
    "재무상태표 추이", 
    "손익계산서 추이", 
    "성장률 분석", 
    "수익성 분석", 
    "안정성 지표", 
    "현금흐름",
    "운전자본",
    "종합 결론"
])

# 탭 1: 핵심 요약
with tabs[0]:
    st.markdown('<h2 class="slide-header">풍전비철 핵심 재무비율 요약</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # ROE
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #4f46e5;">ROE (자기자본이익률)</h3>', unsafe_allow_html=True)
        
        metrics = profitability_data[['year', 'ROE']].copy()
        for _, row in metrics.iterrows():
            st.markdown(f'<div class="metric-container"><span>{row["year"]}년</span><span class="highlight">{row["ROE"]}%</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: right; font-size: 0.8rem; margin-top: 0.5rem;">업계평균 8.5% 대비 1.7배↑</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 순이익률
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #10b981;">순이익률</h3>', unsafe_allow_html=True)
        
        metrics = profitability_data[['year', '순이익률']].copy()
        for _, row in metrics.iterrows():
            st.markdown(f'<div class="metric-container"><span>{row["year"]}년</span><span class="highlight">{row["순이익률"]}%</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: right; font-size: 0.8rem; margin-top: 0.5rem;">지속적 수익성 개선↑</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 부채비율
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #f59e0b;">부채비율</h3>', unsafe_allow_html=True)
        
        metrics = stability_data[['year', '부채비율']].copy()
        for _, row in metrics.iterrows():
            st.markdown(f'<div class="metric-container"><span>{row["year"]}년</span><span class="highlight">{row["부채비율"]}%</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: right; font-size: 0.8rem; margin-top: 0.5rem;">재무구조 개선 중↓</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # FCF
    with col4:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #3b82f6;">현금창출력 (FCF)</h3>', unsafe_allow_html=True)
        
        metrics = cash_flow_data[['year', 'FCF']].copy()
        for _, row in metrics.iterrows():
            value_class = "negative" if row["FCF"] < 0 else "highlight"
            st.markdown(f'<div class="metric-container"><span>{row["year"]}년</span><span class="{value_class}">{row["FCF"]}억</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div style="text-align: right; font-size: 0.8rem; margin-top: 0.5rem;">운전자본 급증 주의↓</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 핵심 지표 소개
    st.markdown('<h3 class="sub-header">핵심 인사이트</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #4f46e5;">강점</h4>', unsafe_allow_html=True)
        st.markdown("""
        - 업계 상위 수준의 수익성 (ROE 14.4%, 순이익률 6.4%)
        - 뛰어난 재무안정성 (부채비율 29%로 크게 개선)
        - 우수한 단기 지급능력 (유동비율 209%)
        - 효율적인 운전자본 관리 (CCC 66.9일로 단축)
        - 안정적인 그룹 계열사 시너지 (지분법이익 207억원)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #ef4444;">개선 필요사항</h4>', unsafe_allow_html=True)
        st.markdown("""
        - 2024년 운전자본 급증으로 현금흐름 일시 악화
        - 자산회전율 감소 추세 (2.56회 → 1.78회)
        - 매출채권 및 재고자산 관리 강화 필요
        - 원자재 가격 변동성 대응 체계 구축
        - 지분법이익 의존도 축소를 통한 수익구조 개선
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# 탭 2: 재무상태표 추이
with tabs[1]:
    st.markdown('<h2 class="slide-header">재무상태표 주요 항목 추이</h2>', unsafe_allow_html=True)
    
    # 재무상태표 수치 요약
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="총자산 (2022→2024)", 
            value=f"{balance_sheet_data['총자산'].iloc[-1]}억원",
            delta=f"{((balance_sheet_data['총자산'].iloc[-1] / balance_sheet_data['총자산'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    with col2:
        st.metric(
            label="총부채 (2022→2024)", 
            value=f"{balance_sheet_data['총부채'].iloc[-1]}억원",
            delta=f"{((balance_sheet_data['총부채'].iloc[-1] / balance_sheet_data['총부채'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="자본총계 (2022→2024)", 
            value=f"{balance_sheet_data['자본총계'].iloc[-1]}억원",
            delta=f"{((balance_sheet_data['자본총계'].iloc[-1] / balance_sheet_data['자본총계'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    # 재무상태표 그래프
    fig = go.Figure()
    
    # 총자산 막대그래프
    fig.add_trace(go.Bar(
        x=balance_sheet_data['year'],
        y=balance_sheet_data['총자산'],
        name='총자산',
        marker_color='#4f46e5',
        text=balance_sheet_data['총자산'],
        textposition='outside'
    ))
    
    # 총부채 막대그래프
    fig.add_trace(go.Bar(
        x=balance_sheet_data['year'],
        y=balance_sheet_data['총부채'],
        name='총부채',
        marker_color='#ef4444',
        text=balance_sheet_data['총부채'],
        textposition='outside'
    ))
    
    # 자본총계 막대그래프
    fig.add_trace(go.Bar(
        x=balance_sheet_data['year'],
        y=balance_sheet_data['자본총계'],
        name='자본총계',
        marker_color='#10b981',
        text=balance_sheet_data['자본총계'],
        textposition='outside'
    ))
    
    # 총자산 선형 그래프
    fig.add_trace(go.Scatter(
        x=balance_sheet_data['year'],
        y=balance_sheet_data['총자산'],
        name='총자산 추세',
        mode='lines+markers',
        line=dict(color='#4f46e5', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title='재무상태표 주요 항목 추이 (단위: 억원)',
        xaxis_title='연도',
        yaxis_title='금액 (억원)',
        barmode='group',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("""
    **재무상태표 분석:**
    - 총자산: 3년간 4.8% 완만한 증가 (3,683억원 → 3,859억원)
    - 자본총계: 3년간 38.5% 가파른 증가 (2,158억원 → 2,988억원)
    - 총부채: 2024년 27.5% 증가했으나 여전히 낮은 수준
    - 부채비율: 18% → 23%로 변화, 여전히 낮은 레버리지 유지
    - 전반적으로 건전한 재무 체력 구축으로 성장투자나 배당 확대가 가능한 상태
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 탭 3: 손익계산서 추이
with tabs[2]:
    st.markdown('<h2 class="slide-header">손익계산서 주요 항목 추이</h2>', unsafe_allow_html=True)
    
    # 손익계산서 수치 요약
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="매출액 (2022→2024)", 
            value=f"{performance_data['매출액'].iloc[-1]}억원",
            delta=f"{((performance_data['매출액'].iloc[-1] / performance_data['매출액'].iloc[0]) - 1) * 100:.1f}%",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="영업이익 (2022→2024)", 
            value=f"{performance_data['영업이익'].iloc[-1]}억원",
            delta=f"{((performance_data['영업이익'].iloc[-1] / performance_data['영업이익'].iloc[0]) - 1) * 100:.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="순이익 (2022→2024)", 
            value=f"{performance_data['순이익'].iloc[-1]}억원",
            delta=f"{((performance_data['순이익'].iloc[-1] / performance_data['순이익'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    # 손익계산서 그래프
    fig = go.Figure()
    
    # 매출액 막대그래프
    fig.add_trace(go.Bar(
        x=performance_data['year'],
        y=performance_data['매출액'],
        name='매출액',
        marker_color='#3b82f6',
        text=performance_data['매출액'],
        textposition='outside'
    ))
    
    # 영업이익 막대그래프
    fig.add_trace(go.Bar(
        x=performance_data['year'],
        y=performance_data['영업이익'],
        name='영업이익',
        marker_color='#8b5cf6',
        text=performance_data['영업이익'],
        textposition='outside'
    ))
    
    # 순이익 막대그래프
    fig.add_trace(go.Bar(
        x=performance_data['year'],
        y=performance_data['순이익'],
        name='순이익',
        marker_color='#f59e0b',
        text=performance_data['순이익'],
        textposition='outside'
    ))
    
    # 순이익률 선형 그래프 (보조 y축)
    fig.add_trace(go.Scatter(
        x=performance_data['year'],
        y=performance_data['순이익률'],
        name='순이익률 (%)',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='손익계산서 주요 항목 추이 (단위: 억원, %)',
        xaxis_title='연도',
        yaxis_title='금액 (억원)',
        yaxis2=dict(
            title='비율 (%)',
            title_font=dict(color='#ef4444'),
            tickfont=dict(color='#ef4444'),
            overlaying='y',
            side='right'
        ),
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("""
    **손익계산서 분석:**
    - 매출액: 3년간 28.4% 감소 (9,445억원 → 6,760억원)
    - 영업이익: 초기 하락 후 2024년 회복세 (428억원 → 362억원, -15.4%)
    - 순이익: 2024년 크게 증가 (363억원 → 430억원, +18.5%)
    - 순이익률: 3.8% → 6.4%로 크게 개선되며 수익성 체질 향상
    - 매출 감소에도 비용 효율화와 고마진 제품 확대로 수익성 방어 성공
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 탭 4: 성장률 분석
with tabs[3]:
    st.markdown('<h2 class="slide-header">주요 항목 성장률 추이</h2>', unsafe_allow_html=True)
    
    # 성장률 그래프
    fig = go.Figure()
    
    # 총자산성장률 막대그래프
    fig.add_trace(go.Bar(
        x=growth_rates['year'],
        y=growth_rates['총자산성장률'],
        name='총자산성장률',
        marker_color='#4f46e5',
        text=[f"{value}%" for value in growth_rates['총자산성장률']],
        textposition='outside'
    ))
    
    # 매출액성장률 막대그래프
    fig.add_trace(go.Bar(
        x=growth_rates['year'],
        y=growth_rates['매출액성장률'],
        name='매출액성장률',
        marker_color='#3b82f6',
        text=[f"{value}%" for value in growth_rates['매출액성장률']],
        textposition='outside'
    ))
    
    # 순이익성장률 막대그래프
    fig.add_trace(go.Bar(
        x=growth_rates['year'],
        y=growth_rates['순이익성장률'],
        name='순이익성장률',
        marker_color='#f59e0b',
        text=[f"{value}%" for value in growth_rates['순이익성장률']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='주요 항목 성장률 추이 (단위: %)',
        xaxis_title='연도',
        yaxis_title='성장률 (%)',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("""
    **성장률 분석:**
    - 총자산 성장: 3.9% → 0.8%로 둔화되며 자산 확대 속도 감소
    - 매출액 성장: -7.5% → -22.6%로 큰 폭 하락
    - 순이익 성장: 0.6% → 17.8%로 급증하며 수익성 개선 뚜렷
    - 매출 감소에도 불구하고 순이익 성장률이 크게 상승한 것은 고부가가치 제품으로의 포트폴리오 전환과 비용 효율화에 기인
    - 자산 성장 둔화와 매출 하락 추세에 대응하기 위한 신성장 동력 발굴 필요성 제기
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# 탭 5: 수익성 분석
with tabs[4]:
    st.markdown('<h2 class="slide-header">ROE 분해 분석 (듀폰 분석)</h2>', unsafe_allow_html=True)
    
    # 듀폰 분석 데이터 준비
    dupont_data = pd.DataFrame({
        'year': ['2022', '2023', '2024'],
        '순이익률': [3.84, 4.18, 6.36],
        '자산회전율': [2.56, 2.33, 1.78],
        '재무레버리지': [1.72, 1.64, 1.42],
        'ROE': [16.8, 15.7, 15.7]
    })
    
    # 측정 지표 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="순이익률 (2022→2024)", 
            value=f"{dupont_data['순이익률'].iloc[-1]}%",
            delta=f"{((dupont_data['순이익률'].iloc[-1] / dupont_data['순이익률'].iloc[0]) - 1) * 100:.1f}%"
        )
    
    with col2:
        st.metric(
            label="자산회전율 (2022→2024)", 
            value=f"{dupont_data['자산회전율'].iloc[-1]}회",
            delta=f"{((dupont_data['자산회전율'].iloc[-1] / dupont_data['자산회전율'].iloc[0]) - 1) * 100:.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="재무레버리지 (2022→2024)", 
            value=f"{dupont_data['재무레버리지'].iloc[-1]}배",
            delta=f"{((dupont_data['재무레버리지'].iloc[-1] / dupont_data['재무레버리지'].iloc[0]) - 1) * 100:.1f}%",
            delta_color="inverse"
        )
    
    # 듀폰 분석 그래프
    fig = go.Figure()
    
    # 순이익률 막대그래프
    fig.add_trace(go.Bar(
        x=dupont_data['year'],
        y=dupont_data['순이익률'],
        name='순이익률 (%)',
        marker_color='#4f46e5',
        text=[f"{value}%" for value in dupont_data['순이익률']],
        textposition='outside'
    ))
    
    # 자산회전율 막대그래프
    fig.add_trace(go.Bar(
        x=dupont_data['year'],
        y=dupont_data['자산회전율'],
        name='자산회전율 (회)',
        marker_color='#10b981',
        text=[f"{value}" for value in dupont_data['자산회전율']],
        textposition='outside'
    ))
    
    # 재무레버리지 막대그래프
    fig.add_trace(go.Bar(
        x=dupont_data['year'],
        y=dupont_data['재무레버리지'],
        name='재무레버리지 (배)',
        marker_color='#f59e0b',
        text=[f"{value}" for value in dupont_data['재무레버리지']],
        textposition='outside'
    ))
    
    # ROE 선 그래프
    fig.add_trace(go.Scatter(
        x=dupont_data['year'],
        y=dupont_data['ROE'],
        name='ROE (%)',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title='ROE 분해 분석 (듀폰 분석)',
        xaxis_title='연도',
        yaxis_title='값',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 인사이트
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown("""
    **듀폰 분석 해석:**
    - 2024년 ROE가 14.4%를 유지한 것은 순이익률의 큰 폭 상승(6.36%)이 자산회전율 하락(1.78회)과 레버리지 축소(1.42배)를 상쇄했기 때문
    - 순이익률 상승: 3.84% → 6.36%로 65.6% 증가, 수익성 체질 개선 뚜렷
    - 자산회전율 하락: 2.56회 → 1.78회로 30.5% 감소, 효율성 개선 필요
    - 재무레버리지 감소: 1.72배 → 1.42배로 17.4% 감소, 재무안정성 강화
    - 효율성 개선을 통한 자산회전율 제고가 추가적인 ROE 향상의 핵심 과제
    """)
    st.markdown('</div>', unsafe_allow_html=True)