import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class GrowthRateSlide(BaseSlide):
    """성장률 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "주요 항목 성장률 추이")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_growth_rate_chart()
        self._render_insight()
    
    def _render_growth_rate_chart(self):
        """성장률 차트 렌더링"""
        growth_rates = self.data_loader.get_growth_rates()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # 총자산성장률 막대그래프
        fig.add_trace(go.Bar(
            x=growth_rates['year'],
            y=growth_rates['총자산성장률'],
            name='총자산성장률',
            marker_color=COLOR_PALETTE["primary"],
            text=[f"{value:.1f}%" for value in growth_rates['총자산성장률']],
            textposition='outside'
        ))
        
        # 매출액성장률 막대그래프
        fig.add_trace(go.Bar(
            x=growth_rates['year'],
            y=growth_rates['매출액성장률'],
            name='매출액성장률',
            marker_color=COLOR_PALETTE["secondary"],
            text=[f"{value:.1f}%" for value in growth_rates['매출액성장률']],
            textposition='outside'
        ))
        
        # 순이익성장률 막대그래프
        fig.add_trace(go.Bar(
            x=growth_rates['year'],
            y=growth_rates['순이익성장률'],
            name='순이익성장률',
            marker_color=COLOR_PALETTE["warning"],
            text=[f"{value:.1f}%" for value in growth_rates['순이익성장률']],
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
    
    def _render_insight(self):
        """인사이트 렌더링"""
        insight_content = """
        **성장률 분석:**
        - 총자산 성장: 3.9% → 0.8%로 둔화되며 자산 확대 속도 감소
        - 매출액 성장: -7.5% → -22.6%로 큰 폭 하락
        - 순이익 성장: 0.6% → 17.8%로 급증하며 수익성 개선 뚜렷
        - 매출 감소에도 불구하고 순이익 성장률이 크게 상승한 것은 고부가가치 제품으로의 포트폴리오 전환과 비용 효율화에 기인
        - 자산 성장 둔화와 매출 하락 추세에 대응하기 위한 신성장 동력 발굴 필요성 제기
        """
        
        self.render_insight_card("성장률 분석", insight_content)
