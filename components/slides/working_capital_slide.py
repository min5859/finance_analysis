import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class WorkingCapitalSlide(BaseSlide):
    """운전자본 효율성 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "운전자본 효율성 분석 (CCC)")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_working_capital_chart()
        self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        working_capital_data = self.data_loader.get_working_capital_data()
        
        col1, col2 = st.columns(2)
        
        # CCC 지표
        with col1:
            st.metric(
                label="현금전환주기(CCC) (2022→2024)", 
                value=f"{working_capital_data['CCC'].iloc[-1]}일",
                delta=f"{-((working_capital_data['CCC'].iloc[0] - working_capital_data['CCC'].iloc[-1]) / working_capital_data['CCC'].iloc[0]) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 운전자본 지표 그래프 제목에 공간 확보
        with col2:
            st.write("")
            st.write("")
    
    def _render_working_capital_chart(self):
        """운전자본 지표 차트 렌더링"""
        working_capital_data = self.data_loader.get_working_capital_data()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        # DSO 막대그래프
        fig.add_trace(go.Bar(
            x=working_capital_data['year'],
            y=working_capital_data['DSO'],
            name='매출채권회수기간 (일)',
            marker_color=COLOR_PALETTE["primary"],
            text=[f"{value}일" for value in working_capital_data['DSO']],
            textposition='outside'
        ))
        
        # DIO 막대그래프
        fig.add_trace(go.Bar(
            x=working_capital_data['year'],
            y=working_capital_data['DIO'],
            name='재고자산보유기간 (일)',
            marker_color=COLOR_PALETTE["success"],
            text=[f"{value}일" for value in working_capital_data['DIO']],
            textposition='outside'
        ))
        
        # DPO 막대그래프
        fig.add_trace(go.Bar(
            x=working_capital_data['year'],
            y=working_capital_data['DPO'],
            name='매입채무결제기간 (일)',
            marker_color=COLOR_PALETTE["warning"],
            text=[f"{value}일" for value in working_capital_data['DPO']],
            textposition='outside'
        ))
        
        # CCC 막대그래프
        fig.add_trace(go.Bar(
            x=working_capital_data['year'],
            y=working_capital_data['CCC'],
            name='현금전환주기 (일)',
            marker_color=COLOR_PALETTE["danger"],
            text=[f"{value}일" for value in working_capital_data['CCC']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='운전자본 효율성 분석 (단위: 일)',
            xaxis_title='연도',
            yaxis_title='일수',
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
        **운전자본 효율성 분석:**
        - 현금전환주기(CCC): 84.2일 → 66.9일로 20.5% 개선
        - 매출채권회수기간(DSO): 36.7일 → 34.1일로 소폭 개선
        - 재고자산보유기간(DIO): 50.8일 → 41.7일로 17.9% 단축
        - 매입채무결제기간(DPO): 3.3일 → 8.9일로 170% 증가하여 공급망 협상력 강화
        - 운전자본 효율성이 전반적으로 개선되었으나, 2024년 현금흐름 악화를 고려할 때 추가적인 관리체계 강화 필요
        """
        
        self.render_insight_card("운전자본 효율성 분석", insight_content)
