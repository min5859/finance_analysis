import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
from config.app_config import COLOR_PALETTE

class StabilitySlide(BaseSlide):
    """안정성 지표 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "재무안정성 지표 추이")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_stability_chart()
        self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        stability_data = self.data_loader.get_stability_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 부채비율 지표
        with col1:
            st.metric(
                label="부채비율 (2022→2024)", 
                value=f"{stability_data['부채비율'].iloc[-1]}%",
                delta=f"{-((stability_data['부채비율'].iloc[0] - stability_data['부채비율'].iloc[-1]) / stability_data['부채비율'].iloc[0]) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 유동비율 지표
        with col2:
            st.metric(
                label="유동비율 (2022→2024)", 
                value=f"{stability_data['유동비율'].iloc[-1]}%",
                delta=f"{((stability_data['유동비율'].iloc[-1] / stability_data['유동비율'].iloc[0]) - 1) * 100:.1f}%"
            )
        
        # 이자보상배율 지표
        with col3:
            st.metric(
                label="이자보상배율 (2022→2024)", 
                value=f"{stability_data['이자보상배율'].iloc[-1]}배",
                delta=f"{((stability_data['이자보상배율'].iloc[-1] / stability_data['이자보상배율'].iloc[0]) - 1) * 100:.1f}%"
            )
    
    def _render_stability_chart(self):
        """안정성 지표 차트 렌더링"""
        stability_data = self.data_loader.get_stability_data()
        
        # Chart.js 데이터셋 준비
        labels = stability_data['year'].tolist()
        datasets = [
            {
                "label": "부채비율 (%)",
                "data": stability_data['부채비율'].tolist(),
                "borderColor": COLOR_PALETTE["danger"],
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["danger"]
            },
            {
                "label": "유동비율 (%)",
                "data": stability_data['유동비율'].tolist(),
                "borderColor": COLOR_PALETTE["success"],
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["success"]
            },
            {
                "label": "이자보상배율 (배)",
                "data": stability_data['이자보상배율'].tolist(),
                "borderColor": COLOR_PALETTE["primary"],
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["primary"],
                "yAxisID": "y1"
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
                    "text": "재무안정성 지표 추이"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "비율 (%)"
                    }
                },
                "y1": {
                    "position": "right",
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "배수"
                    },
                    "grid": {
                        "drawOnChartArea": False
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
        ChartJSComponent.create_line_chart(labels, datasets, options)
    
    def _render_insight(self):
        """인사이트 렌더링"""
        insight_content = """
        **안정성 분석:**
        - 부채비율: 71% → 29%로 크게 개선되며 재무구조 안정화
        - 유동비율: 189% → 209%로 상승하여 단기 지급능력 강화
        - 이자보상배율: 7.8배 → 7.4배로 소폭 하락했으나 여전히 우수한 수준 유지
        - 전반적으로 재무안정성이 크게 개선되어 향후 성장투자 및 배당 확대 여력 충분
        - 낮은 레버리지로 인해 경기 변동에 대한 대응력이 높고, 신규 투자에 유리한 상황
        """
        
        self.render_insight_card("안정성 분석", insight_content)
