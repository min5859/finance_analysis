import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
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
        
        # Chart.js 데이터셋 준비
        labels = cash_flow_data['year'].tolist()
        datasets = [
            {
                "label": "영업활동현금흐름",
                "data": cash_flow_data['영업활동'].tolist(),
                "backgroundColor": COLOR_PALETTE["success"],
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 1
            },
            {
                "label": "투자활동현금흐름",
                "data": cash_flow_data['투자활동'].tolist(),
                "backgroundColor": COLOR_PALETTE["danger"],
                "borderColor": COLOR_PALETTE["danger"],
                "borderWidth": 1
            },
            {
                "label": "잉여현금흐름 (FCF)",
                "data": cash_flow_data['FCF'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 1
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
                    "text": "현금흐름 추이 분석 (단위: 억원)"
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
        insight_content = """
        **현금흐름 분석:**
        - 영업활동현금흐름: 155억원 → 665억원 → -146억원으로 2024년 급격히 악화
        - 투자활동현금흐름: -31억원 → -260억원 → -4억원으로 2024년 투자 감소
        - 잉여현금흐름(FCF): 124억원 → 405억원 → -150억원으로 2024년 적자 전환
        - 2024년 현금흐름 악화는 운전자본 급증(재고 317억↑, 매출채권 156억↑)에 기인
        - 운전자본 증가는 신규 사업 준비를 위한 전략적 선투자로 해석 가능하나, 단기 유동성 관리 필요
        """
        
        self.render_insight_card("현금흐름 분석", insight_content)
