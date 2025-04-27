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
        
        # 메인 콘텐츠를 두 열로 나눕니다: 왼쪽은 차트, 오른쪽은 Scale and Structure
        col1, col2 = st.columns([7, 5])
        
        with col1:
            self._render_key_metrics()
            self._render_balance_sheet_chart()
        
        with col2:
            self._render_scale_and_structure()
        
        # 인사이트는 별도로 표시
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
    
    def _render_scale_and_structure(self):
        """규모 및 구조 렌더링"""
        balance_sheet_data = self.data_loader.get_balance_sheet_data()
        
        # 카드 스타일 적용
        st.markdown("""
        <style>
        .scale-card {
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 카드: 모니터링 필요 항목
        st.markdown('<div class="scale-card">', unsafe_allow_html=True)
        st.markdown("### 성장투자·배당 확대 여건 양호, 투자효율 모니터링 필요", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
        st.markdown('<div class="scale-card">', unsafe_allow_html=True)
        
        # 타이틀
        st.markdown("### Scale and Structure", unsafe_allow_html=True)
        
        # 첫 번째 연도와 마지막 연도의 값 가져오기
        first_year = balance_sheet_data['year'].iloc[0]
        last_year = balance_sheet_data['year'].iloc[-1]
        
        # 총자산 변화
        start_asset = balance_sheet_data['총자산'].iloc[0]
        end_asset = balance_sheet_data['총자산'].iloc[-1]
        asset_growth = ((end_asset / start_asset) - 1) * 100
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span>총자산: {start_asset} → {end_asset}억</span>
            <span style="text-align: right; font-weight: bold;">완만 +{asset_growth:.1f} %</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 자본총계 변화
        start_equity = balance_sheet_data['자본총계'].iloc[0]
        end_equity = balance_sheet_data['자본총계'].iloc[-1]
        equity_growth = ((end_equity / start_equity) - 1) * 100
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span>자본총계: {start_equity} → {end_equity}억</span>
            <span style="text-align: right; font-weight: bold;">가파른 +{equity_growth:.1f} %</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 총부채 변화
        debt_year_before = balance_sheet_data['총부채'].iloc[-2]
        end_debt = balance_sheet_data['총부채'].iloc[-1]
        debt_growth = ((end_debt / debt_year_before) - 1) * 100
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span>총부채</span>
            <span style="text-align: right; font-weight: bold;">점프 +{debt_growth:.1f} %</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 부채비율 변화
        start_debt_ratio = (balance_sheet_data['총부채'].iloc[0] / balance_sheet_data['총자산'].iloc[0]) * 100
        end_debt_ratio = (balance_sheet_data['총부채'].iloc[-1] / balance_sheet_data['총자산'].iloc[-1]) * 100
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span>부채비율 {start_debt_ratio:.0f} % → {end_debt_ratio:.0f} %</span>
            <span style="text-align: right; font-weight: bold;">저레버리지</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    def _render_insight(self):
        """인사이트 렌더링"""
        insights = self.data_loader.get_insights()
        if "balance_sheet" in insights:
            insight_data = insights["balance_sheet"]
            self.render_insight_card(insight_data["title"], insight_data["content"])
        else:
            st.info("재무상태표에 대한 인사이트 정보가 없습니다. JSON 파일에 insights.balance_sheet 항목을 추가해주세요.")
