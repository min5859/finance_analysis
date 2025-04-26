import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
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
        
        # Chart.js 데이터셋 준비
        labels = dupont_data['year'].tolist()
        datasets = [
            {
                "label": "순이익률 (%)",
                "data": dupont_data['순이익률'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 1
            },
            {
                "label": "자산회전율 (회)",
                "data": dupont_data['자산회전율'].tolist(),
                "backgroundColor": COLOR_PALETTE["success"],
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 1
            },
            {
                "label": "재무레버리지 (배)",
                "data": dupont_data['재무레버리지'].tolist(),
                "backgroundColor": COLOR_PALETTE["warning"],
                "borderColor": COLOR_PALETTE["warning"],
                "borderWidth": 1
            },
            {
                "label": "ROE (%)",
                "data": dupont_data['ROE'].tolist(),
                "type": "line",
                "borderColor": COLOR_PALETTE["danger"],
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["danger"],
                "fill": False
            }
        ]
        
        # Chart.js 옵션 설정
        options = {
            "responsive": True,
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": "ROE 분해 분석 (듀폰 분석)"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "값"
                    }
                },
                "x": {
                    "title": {
                        "display": True,
                        "text": "연도"
                    }
                }
            }
        }
        
        # Chart.js로 차트 렌더링
        ChartJSComponent.create_bar_chart(labels, datasets, options)
    
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
