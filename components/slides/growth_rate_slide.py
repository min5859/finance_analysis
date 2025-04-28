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
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 헤더 텍스트 추가
        st.markdown("""
        <div class="header-card">
            자산 성장 둔화, 매출 하락했지만, 2024년 순이익이 17.8% 증가하며 비용 효율화와 고마진 제품 확대를 통해 수익성 방어
        </div>
        """, unsafe_allow_html=True)
        
        # 메인 콘텐츠를 두 열로 나눕니다
        col1, col2 = st.columns([7, 5])
        
        with col1:
            self._render_growth_rate_chart()
        
        with col2:
            self._render_key_metrics()
    
    def _add_custom_styles(self):
        """커스텀 CSS 스타일 추가"""
        st.markdown("""
        <style>
        .header-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            font-size: 1.1rem;
            color: #1a1a1a;
            line-height: 1.5;
        }
        
        .growth-table-container {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
        }
        
        .growth-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .growth-table th {
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: normal;
            border-bottom: 1px solid #dee2e6;
            color: #666;
        }
        
        .growth-table td {
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }
        
        .growth-table tr:last-child td {
            border-bottom: none;
        }
        
        .positive {
            color: #228be6;
            font-weight: 500;
        }
        
        .negative {
            color: #fa5252;
            font-weight: 500;
        }
        
        .insight-message {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 12px 16px;
            color: #1a1a1a;
            font-size: 0.95rem;
            margin-top: 5px;
            border-left: 4px solid #228be6;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링 - 테이블 형태로 수정"""
        growth_rates = self.data_loader.get_growth_rates()
        
        # 테이블 HTML 생성
        st.markdown("""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">핵심 성장률 지표</div>
            <table class="growth-table">
                <tr>
                    <th>항목</th>
                    <th>2023년</th>
                    <th>2024년</th>
                </tr>
                <tr>
                    <td>총자산</td>
                    <td class="positive">+3.9%</td>
                    <td class="positive">+0.8%</td>
                </tr>
                <tr>
                    <td>매출액</td>
                    <td class="negative">-7.5%</td>
                    <td class="negative">-22.6%</td>
                </tr>
                <tr>
                    <td>당기순이익</td>
                    <td class="positive">+0.6%</td>
                    <td class="positive">+17.8%</td>
                </tr>
            </table>
        </div>
        <div class="insight-message">
            자산 성장 둔화·매출 급락에도 순이익 17.8%↑ 수익성 방어
        </div>
        """, unsafe_allow_html=True)
    
    def _render_growth_rate_chart(self):
        """성장률 차트 렌더링"""
        growth_rates = self.data_loader.get_growth_rates()
        
        # Chart.js 데이터셋 준비
        labels = growth_rates['year'].tolist()
        datasets = [
            {
                "label": "총자산성장률",
                "data": growth_rates['총자산성장률'].tolist(),
                "backgroundColor": "#4C6EF5",  # 파란색
                "borderColor": "#4C6EF5",
                "borderWidth": 1,
                "type": "bar"
            },
            {
                "label": "매출액성장률",
                "data": growth_rates['매출액성장률'].tolist(),
                "backgroundColor": "#4C6EF5",  # 파란색
                "borderColor": "#4C6EF5",
                "borderWidth": 1,
                "type": "bar"
            },
            {
                "label": "순이익성장률",
                "data": growth_rates['순이익성장률'].tolist(),
                "backgroundColor": "#FAB005",  # 노란색
                "borderColor": "#FAB005",
                "borderWidth": 1,
                "type": "bar"
            }
        ]
        
        # Chart.js 옵션 설정
        options = {
            "responsive": True,
            "plugins": {
                "legend": {
                    "position": "bottom",
                    "labels": {
                        "usePointStyle": True,
                        "padding": 20
                    }
                },
                "title": {
                    "display": True,
                    "text": "주요 항목 성장률 추이 (단위: %)",
                    "font": {
                        "size": 16
                    }
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "suggestedMin": -30,
                    "suggestedMax": 30,
                    "ticks": {
                        "stepSize": 15
                    },
                    "grid": {
                        "drawBorder": False
                    }
                },
                "x": {
                    "grid": {
                        "display": False
                    }
                }
            }
        }
        
        # Chart.js로 차트 렌더링
        ChartJSComponent.create_bar_chart(labels, datasets, options)