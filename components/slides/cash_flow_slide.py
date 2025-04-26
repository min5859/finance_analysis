import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class CashFlowSlide(BaseSlide):
    """현금흐름 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "현금흐름 추이 분석")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_cash_flow_chart()
        self._render_insight()
    
    def _render_cash_flow_chart(self):
        """현금흐름 차트 렌더링"""
        cash_flow_data = self.data_loader.get_cash_flow_data()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # 영업활동 막대그래프
        fig.add_trace(go.Bar(
            x=cash_flow_data['year'],
            y=cash_flow_data['영업활동'],
            name='영업활동현금흐름',
            marker_color=COLOR_PALETTE["success"],
            text=[f"{value}억" for value in cash_flow_data['영업활동']],
            textposition='outside'
        ))
        
        # 투자활동 막대그래프
        fig.add_trace(go.Bar(
            x=cash_flow_data['year'],
            y=cash_flow_data['투자활동'],
            name='투자활동현금흐름',
            marker_color=COLOR_PALETTE["danger"],
            text=[f"{value}억" for value in cash_flow_data['투자활동']],
            textposition='outside'
        ))
        
        # FCF 막대그래프
        fig.add_trace(go.Bar(
            x=cash_flow_data['year'],
            y=cash_flow_data['FCF'],
            name='잉여현금흐름 (FCF)',
            marker_color=COLOR_PALETTE["primary"],
            text=[f"{value}억" for value in cash_flow_data['FCF']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='현금흐름 추이 분석 (단위: 억원)',
            xaxis_title='연도',
            yaxis_title='금액 (억원)',
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
        **현금흐름 분석:**
        - 영업활동현금흐름: 155억원 → 665억원 → -146억원으로 2024년 급격히 악화
        - 투자활동현금흐름: -31억원 → -260억원 → -4억원으로 2024년 투자 감소
        - 잉여현금흐름(FCF): 124억원 → 405억원 → -150억원으로 2024년 적자 전환
        - 2024년 현금흐름 악화는 운전자본 급증(재고 317억↑, 매출채권 156억↑)에 기인
        - 운전자본 증가는 신규 사업 준비를 위한 전략적 선투자로 해석 가능하나, 단기 유동성 관리 필요
        """
        
        self.render_insight_card("현금흐름 분석", insight_content)
