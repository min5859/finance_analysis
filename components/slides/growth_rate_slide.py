import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class GrowthRateSlide(BaseSlide):
    """성장률 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Growth Rates of Key Items")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()

        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 인사이트 데이터 가져오기
        insights = self.data_loader.get_insights()
        growth_insight = insights.get('growth_rates', {})
        header_text = growth_insight.get('content1', 'JSON의 insights.growth_rates 항목을 추가해 주세요.')
        insight_message = growth_insight.get('content2', 'JSON의 insights.growth_rates 항목을 추가해 주세요.')
        
        # 헤더 텍스트 추가
        st.markdown(f"""
        <div class="header-card">
            {header_text}
        </div>
        """, unsafe_allow_html=True)
        
        # 메인 콘텐츠를 두 열로 나눕니다
        col1, col2 = st.columns([7, 5])
        
        with col1:
            growth_rates = self.data_loader.get_growth_rates()
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
                "scales": {
                    "y": {
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
            
            # iframe 방식으로 카드 내부에 차트 렌더링
            IframeChartComponent.create_bar_chart_in_card(
                labels=labels,
                datasets=datasets,
                options=options,
                height=380,
                title="주요 항목 성장률 추이 (단위: %)",
                use_datalabels=True
            )
        
        with col2:
            self._render_key_metrics(insight_message)
    
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
    
    def _render_key_metrics(self, insight_message):
        """핵심 지표 렌더링 - 테이블 형태로 수정, 인사이트 메시지 인자로 받음"""
        growth_rates = self.data_loader.get_growth_rates()
        
        # 성장률 데이터 준비
        asset_growth = growth_rates['총자산성장률'].tolist()
        revenue_growth = growth_rates['매출액성장률'].tolist()
        profit_growth = growth_rates['순이익성장률'].tolist()
        
        # CSS 클래스 결정 함수
        def get_class(value):
            return "positive" if value >= 0 else "negative"
        
        st.markdown(f"""
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
                    <td class="{get_class(asset_growth[0])}">{"+" if asset_growth[0] >= 0 else ""}{asset_growth[0]}%</td>
                    <td class="{get_class(asset_growth[1])}">{"+" if asset_growth[1] >= 0 else ""}{asset_growth[1]}%</td>
                </tr>
                <tr>
                    <td>매출액</td>
                    <td class="{get_class(revenue_growth[0])}">{"+" if revenue_growth[0] >= 0 else ""}{revenue_growth[0]}%</td>
                    <td class="{get_class(revenue_growth[1])}">{"+" if revenue_growth[1] >= 0 else ""}{revenue_growth[1]}%</td>
                </tr>
                <tr>
                    <td>당기순이익</td>
                    <td class="{get_class(profit_growth[0])}">{"+" if profit_growth[0] >= 0 else ""}{profit_growth[0]}%</td>
                    <td class="{get_class(profit_growth[1])}">{"+" if profit_growth[1] >= 0 else ""}{profit_growth[1]}%</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-message">
            {insight_message}
        </div>
        """, unsafe_allow_html=True)