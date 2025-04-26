import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class BalanceSheetSlide(BaseSlide):
    """재무상태표 추이 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "재무상태표 주요 항목 추이")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_balance_sheet_chart()
        self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        balance_sheet_data = self.data_loader.get_balance_sheet_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 총자산 지표
        with col1:
            st.metric(
                label="총자산 (2022→2024)", 
                value=f"{balance_sheet_data['총자산'].iloc[-1]}억원",
                delta=f"{((balance_sheet_data['총자산'].iloc[-1] / balance_sheet_data['총자산'].iloc[0]) - 1) * 100:.1f}%"
            )
        
        # 총부채 지표
        with col2:
            st.metric(
                label="총부채 (2022→2024)", 
                value=f"{balance_sheet_data['총부채'].iloc[-1]}억원",
                delta=f"{((balance_sheet_data['총부채'].iloc[-1] / balance_sheet_data['총부채'].iloc[0]) - 1) * 100:.1f}%"
            )
        
        # 자본총계 지표
        with col3:
            st.metric(
                label="자본총계 (2022→2024)", 
                value=f"{balance_sheet_data['자본총계'].iloc[-1]}억원",
                delta=f"{((balance_sheet_data['자본총계'].iloc[-1] / balance_sheet_data['자본총계'].iloc[0]) - 1) * 100:.1f}%"
            )
    
    def _render_balance_sheet_chart(self):
        """재무상태표 차트 렌더링"""
        balance_sheet_data = self.data_loader.get_balance_sheet_data()
        
        # 차트 데이터 준비 - 선형 그래프용 데이터 추가
        chart_data = balance_sheet_data.copy()
        chart_data['총자산선형'] = chart_data['총자산'] * 0.8  # 선형 그래프를 20% 아래로 조정
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # 총자산 막대그래프
        fig.add_trace(go.Bar(
            x=chart_data['year'],
            y=chart_data['총자산'],
            name='총자산',
            marker_color=COLOR_PALETTE["primary"],
            text=chart_data['총자산'],
            textposition='outside'
        ))
        
        # 총부채 막대그래프
        fig.add_trace(go.Bar(
            x=chart_data['year'],
            y=chart_data['총부채'],
            name='총부채',
            marker_color=COLOR_PALETTE["danger"],
            text=chart_data['총부채'],
            textposition='outside'
        ))
        
        # 자본총계 막대그래프
        fig.add_trace(go.Bar(
            x=chart_data['year'],
            y=chart_data['자본총계'],
            name='자본총계',
            marker_color=COLOR_PALETTE["success"],
            text=chart_data['자본총계'],
            textposition='outside'
        ))
        
        # 총자산 선형 그래프
        fig.add_trace(go.Scatter(
            x=chart_data['year'],
            y=chart_data['총자산'],
            name='총자산 추세',
            mode='lines+markers',
            line=dict(color=COLOR_PALETTE["primary"], width=3),
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
    
    def _render_insight(self):
        """인사이트 렌더링"""
        insight_content = """
        **재무상태표 분석:**
        - 총자산: 3년간 4.8% 완만한 증가 (3,683억원 → 3,859억원)
        - 자본총계: 3년간 38.5% 가파른 증가 (2,158억원 → 2,988억원)
        - 총부채: 2024년 27.5% 증가했으나 여전히 낮은 수준
        - 부채비율: 18% → 23%로 변화, 여전히 낮은 레버리지 유지
        - 전반적으로 건전한 재무 체력 구축으로 성장투자나 배당 확대가 가능한 상태
        """
        
        self.render_insight_card("재무상태표 분석", insight_content)
