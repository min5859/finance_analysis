import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
from config.app_config import COLOR_PALETTE

class IncomeStatementSlide(BaseSlide):
    """손익계산서 추이 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "손익계산서 주요 항목 추이")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # 차트와 인사이트를 나란히 배치하기 위해 columns 사용
        col1, col2 = st.columns([7, 5])  # 7:5 비율로 열 분할
        with col1:
            self._render_key_metrics()
            self._render_income_statement_chart()
        
        with col2:
            self._render_insight()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 매출액 지표
        with col1:
            st.metric(
                label="매출액 (2022→2024)", 
                value=f"{performance_data['매출액'].iloc[-1]}억원",
                delta=f"{((performance_data['매출액'].iloc[-1] / performance_data['매출액'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 영업이익 지표
        with col2:
            st.metric(
                label="영업이익 (2022→2024)", 
                value=f"{performance_data['영업이익'].iloc[-1]}억원",
                delta=f"{((performance_data['영업이익'].iloc[-1] / performance_data['영업이익'].iloc[0]) - 1) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # 순이익 지표
        with col3:
            st.metric(
                label="순이익 (2022→2024)", 
                value=f"{performance_data['순이익'].iloc[-1]}억원",
                delta=f"{((performance_data['순이익'].iloc[-1] / performance_data['순이익'].iloc[0]) - 1) * 100:.1f}%"
            )
    
    def _render_income_statement_chart(self):
        """손익계산서 차트 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        
        # Chart.js 데이터셋 준비
        labels = performance_data['year'].tolist()
        datasets = [
            {
                "label": "매출액",
                "data": performance_data['매출액'].tolist(),
                "backgroundColor": COLOR_PALETTE["secondary"],
                "borderColor": COLOR_PALETTE["secondary"],
                "borderWidth": 1
            },
            {
                "label": "영업이익",
                "data": performance_data['영업이익'].tolist(),
                "backgroundColor": COLOR_PALETTE["info"],
                "borderColor": COLOR_PALETTE["info"],
                "borderWidth": 1
            },
            {
                "label": "순이익",
                "data": performance_data['순이익'].tolist(),
                "backgroundColor": COLOR_PALETTE["warning"],
                "borderColor": COLOR_PALETTE["warning"],
                "borderWidth": 1
            },
            {
                "label": "순이익률 (%)",
                "data": performance_data['순이익률'].tolist(),
                "type": "line",
                "borderColor": COLOR_PALETTE["danger"],
                "borderWidth": 3,
                "pointRadius": 5,
                "pointBackgroundColor": COLOR_PALETTE["danger"],
                "fill": False,
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
                    "text": "손익계산서 주요 항목 추이 (단위: 억원, %)"
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
                "y1": {
                    "position": "right",
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "비율 (%)"
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
        ChartJSComponent.create_bar_chart(labels, datasets, options)
    
    def _render_insight(self):
        """인사이트 렌더링"""
        
        # 인사이트 카드의 스타일을 조정하여 차트 오른쪽에 잘 맞도록 함
        st.markdown("""
        <style>
        .insight-card {
            padding: 10px; 
            height: 100%;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #4e73df;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>손익계산서 분석</h4>
            <ul style="margin-left: 15px; padding-left: 0px;">
                <li>매출액: 3년간 28.4% 감소 (9,445억원 → 6,760억원)</li>
                <li>영업이익: 초기 하락 후 2024년 회복세 (428억원 → 362억원, -15.4%)</li>
                <li>순이익: 2024년 크게 증가 (363억원 → 430억원, +18.5%)</li>
                <li>순이익률: 3.8% → 6.4%로 크게 개선되며 수익성 체질 향상</li>
                <li>매출 감소에도 비용 효율화와 고마진 제품 확대로 수익성 방어 성공</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)