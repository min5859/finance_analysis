import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
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
        
        # Chart.js 데이터셋 준비
        labels = balance_sheet_data['year'].tolist()
        datasets = [
            {
                "label": "총자산",
                "data": balance_sheet_data['총자산'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 1
            },
            {
                "label": "총부채",
                "data": balance_sheet_data['총부채'].tolist(),
                "backgroundColor": COLOR_PALETTE["danger"],
                "borderColor": COLOR_PALETTE["danger"],
                "borderWidth": 1
            },
            {
                "label": "자본총계",
                "data": balance_sheet_data['자본총계'].tolist(),
                "backgroundColor": COLOR_PALETTE["success"],
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 1
            },
            {
                "label": "총자산 추세",
                "data": balance_sheet_data['총자산'].tolist(),
                "type": "line",
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["primary"],
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
                    "text": "재무상태표 주요 항목 추이 (단위: 억원)"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "금액 (억원)"
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
        insight_data = self.data_loader.get_insights()["balance_sheet"]
        self.render_insight_card(insight_data["title"], insight_data["content"])
