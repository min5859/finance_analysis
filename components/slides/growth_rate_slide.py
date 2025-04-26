import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
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
        
        # Chart.js 데이터셋 준비
        labels = growth_rates['year'].tolist()
        datasets = [
            {
                "label": "총자산성장률",
                "data": growth_rates['총자산성장률'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 1
            },
            {
                "label": "매출액성장률",
                "data": growth_rates['매출액성장률'].tolist(),
                "backgroundColor": COLOR_PALETTE["secondary"],
                "borderColor": COLOR_PALETTE["secondary"],
                "borderWidth": 1
            },
            {
                "label": "순이익성장률",
                "data": growth_rates['순이익성장률'].tolist(),
                "backgroundColor": COLOR_PALETTE["warning"],
                "borderColor": COLOR_PALETTE["warning"],
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
                    "text": "주요 항목 성장률 추이 (단위: %)"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "성장률 (%)"
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
        **성장률 분석:**
        - 총자산 성장: 3.9% → 0.8%로 둔화되며 자산 확대 속도 감소
        - 매출액 성장: -7.5% → -22.6%로 큰 폭 하락
        - 순이익 성장: 0.6% → 17.8%로 급증하며 수익성 개선 뚜렷
        - 매출 감소에도 불구하고 순이익 성장률이 크게 상승한 것은 고부가가치 제품으로의 포트폴리오 전환과 비용 효율화에 기인
        - 자산 성장 둔화와 매출 하락 추세에 대응하기 위한 신성장 동력 발굴 필요성 제기
        """
        
        self.render_insight_card("성장률 분석", insight_content)
