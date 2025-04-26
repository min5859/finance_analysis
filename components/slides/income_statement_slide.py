import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class IncomeStatementSlide(BaseSlide):
    """손익계산서 추이 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "손익계산서 주요 항목 추이")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_income_statement_chart()
        self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 매출액 지표
        with col1:
            st.metric(
                label="매출액 (2022→2024)", 
                value=f"{performance_data['매출액'].iloc[-1]}억원",
                delta=f"{((performance_data['매출액'].iloc[-1] / performance_data['매출액'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 영업이익 지표
        with col2:
            st.metric(
                label="영업이익 (2022→2024)", 
                value=f"{performance_data['영업이익'].iloc[-1]}억원",
                delta=f"{((performance_data['영업이익'].iloc[-1] / performance_data['영업이익'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 순이익 지표
        with col3:
            st.metric(
                label="순이익 (2022→2024)", 
                value=f"{performance_data['순이익'].iloc[-1]}억원",
                delta=f"{((performance_data['순이익'].iloc[-1] / performance_data['순이익'].iloc[0]) - 1) * 100:.1f}%"
            )
    
    def _render_income_statement_chart(self):
        """손익계산서 차트 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # 매출액 막대그래프
        fig.add_trace(go.Bar(
            x=performance_data['year'],
            y=performance_data['매출액'],
            name='매출액',
            marker_color=COLOR_PALETTE["secondary"],
            text=performance_data['매출액'],
            textposition='outside'
        ))
        
        # 영업이익 막대그래프
        fig.add_trace(go.Bar(
            x=performance_data['year'],
            y=performance_data['영업이익'],
            name='영업이익',
            marker_color=COLOR_PALETTE["info"],
            text=performance_data['영업이익'],
            textposition='outside'
        ))
        
        # 순이익 막대그래프
        fig.add_trace(go.Bar(
            x=performance_data['year'],
            y=performance_data['순이익'],
            name='순이익',
            marker_color=COLOR_PALETTE["warning"],
            text=performance_data['순이익'],
            textposition='outside'
        ))
        
        # 순이익률 선형 그래프 (보조 y축)
        fig.add_trace(go.Scatter(
            x=performance_data['year'],
            y=performance_data['순이익률'],
            name='순이익률 (%)',
            mode='lines+markers',
            line=dict(color=COLOR_PALETTE["danger"], width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='손익계산서 주요 항목 추이 (단위: 억원, %)',
            xaxis_title='연도',
            yaxis_title='금액 (억원)',
            yaxis2=dict(
                title='비율 (%)',
                title_font=dict(color=COLOR_PALETTE["danger"]),
                tickfont=dict(color=COLOR_PALETTE["danger"]),
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
    
    def _render_insight(self):
        """인사이트 렌더링"""
        insight_content = """
        **손익계산서 분석:**
        - 매출액: 3년간 28.4% 감소 (9,445억원 → 6,760억원)
        - 영업이익: 초기 하락 후 2024년 회복세 (428억원 → 362억원, -15.4%)
        - 순이익: 2024년 크게 증가 (363억원 → 430억원, +18.5%)
        - 순이익률: 3.8% → 6.4%로 크게 개선되며 수익성 체질 향상
        - 매출 감소에도 비용 효율화와 고마진 제품 확대로 수익성 방어 성공
        """
        
        self.render_insight_card("손익계산서 분석", insight_content)
