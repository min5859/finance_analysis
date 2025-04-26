import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class ProfitabilitySlide(BaseSlide):
    """수익성 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "ROE 분해 분석 (듀폰 분석)")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_dupont_analysis_chart()
        self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        dupont_data = self.data_loader.get_dupont_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 순이익률 지표
        with col1:
            st.metric(
                label="순이익률 (2022→2024)", 
                value=f"{dupont_data['순이익률'].iloc[-1]}%",
                delta=f"{((dupont_data['순이익률'].iloc[-1] / dupont_data['순이익률'].iloc[0]) - 1) * 100:.1f}%"
            )
        
        # 자산회전율 지표
        with col2:
            st.metric(
                label="자산회전율 (2022→2024)", 
                value=f"{dupont_data['자산회전율'].iloc[-1]}회",
                delta=f"{((dupont_data['자산회전율'].iloc[-1] / dupont_data['자산회전율'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 재무레버리지 지표
        with col3:
            st.metric(
                label="재무레버리지 (2022→2024)", 
                value=f"{dupont_data['재무레버리지'].iloc[-1]}배",
                delta=f"{((dupont_data['재무레버리지'].iloc[-1] / dupont_data['재무레버리지'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
    
    def _render_dupont_analysis_chart(self):
        """듀폰 분석 차트 렌더링"""
        dupont_data = self.data_loader.get_dupont_data()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # 순이익률 막대그래프
        fig.add_trace(go.Bar(
            x=dupont_data['year'],
            y=dupont_data['순이익률'],
            name='순이익률 (%)',
            marker_color=COLOR_PALETTE["primary"],
            text=[f"{value}%" for value in dupont_data['순이익률']],
            textposition='outside'
        ))
        
        # 자산회전율 막대그래프
        fig.add_trace(go.Bar(
            x=dupont_data['year'],
            y=dupont_data['자산회전율'],
            name='자산회전율 (회)',
            marker_color=COLOR_PALETTE["success"],
            text=[f"{value}" for value in dupont_data['자산회전율']],
            textposition='outside'
        ))
        
        # 재무레버리지 막대그래프
        fig.add_trace(go.Bar(
            x=dupont_data['year'],
            y=dupont_data['재무레버리지'],
            name='재무레버리지 (배)',
            marker_color=COLOR_PALETTE["warning"],
            text=[f"{value}" for value in dupont_data['재무레버리지']],
            textposition='outside'
        ))
        
        # ROE 선 그래프
        fig.add_trace(go.Scatter(
            x=dupont_data['year'],
            y=dupont_data['ROE'],
            name='ROE (%)',
            mode='lines+markers',
            line=dict(color=COLOR_PALETTE["danger"], width=3),
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
    
    def _render_insight(self):
        """인사이트 렌더링"""
        insight_content = """
        **듀폰 분석 해석:**
        - 2024년 ROE가 14.4%를 유지한 것은 순이익률의 큰 폭 상승(6.36%)이 자산회전율 하락(1.78회)과 레버리지 축소(1.42배)를 상쇄했기 때문
        - 순이익률 상승: 3.84% → 6.36%로 65.6% 증가, 수익성 체질 개선 뚜렷
        - 자산회전율 하락: 2.56회 → 1.78회로 30.5% 감소, 효율성 개선 필요
        - 재무레버리지 감소: 1.72배 → 1.42배로 17.4% 감소, 재무안정성 강화
        - 효율성 개선을 통한 자산회전율 제고가 추가적인 ROE 향상의 핵심 과제
        """
        
        self.render_insight_card("듀폰 분석 해석", insight_content)
