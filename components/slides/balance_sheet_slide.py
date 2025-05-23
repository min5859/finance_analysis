import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class BalanceSheetSlide(BaseSlide):
    """재무상태표 추이 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Scale and Structure Analysis")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 인사이트는 별도로 표시
        self._render_insight()
    
        # 메인 콘텐츠를 두 열로 나눕니다: 왼쪽은 차트, 오른쪽은 Scale and Structure
        col1, col2 = st.columns([7, 5])
        with col1:
            self._render_key_metrics()
            self._render_balance_sheet_chart()
        
        with col2:
            self._render_scale_and_structure()
        
    def _add_custom_styles(self):
        """커스텀 CSS 스타일 추가"""
        st.markdown("""
        <style>
        .fancy-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        
        .info-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f0f0f0;
            padding: 12px 0;
        }
        
        .metric-row:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #333;
            font-weight: 500;
        }
        
        .metric-value {
            font-size: 1rem;
            text-align: right;
            font-weight: 600;
        }
        
        .positive {
            color: #10b981;
        }
        
        .neutral {
            color: #3b82f6;
        }
        
        .negative {
            color: #ef4444;
        }
        
        .insight-card {
            background: #f0f9ff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border-left: 5px solid #3b82f6;
        }
        
        .insight-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 10px;
        }
        
        .insight-content {
            font-size: 0.95rem;
            color: #334155;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)
    
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
            "scales": {
                "y": {
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
        
        # IframeChartComponent로 차트 렌더링
        IframeChartComponent.create_bar_chart_in_card(
            labels=labels,
            datasets=datasets,
            options=options,
            height=400,
            title="재무상태표 주요 항목 추이 (단위: 억원)",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            },
            use_datalabels=True
        )
    
    def _render_scale_and_structure(self):
        """규모 및 구조 렌더링 - 펜시한 카드 형태로, 직접 컨테이너 사용"""
        balance_sheet_data = self.data_loader.get_balance_sheet_data()
        insights = self.data_loader.get_insights()
        
        # 성장투자·배당 확대 여건 메시지 동적 표시
        insight_msg = insights.get("balance_sheet", None)
        if insight_msg:
            st.markdown(f"""
            <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
                <div style="font-weight: 600; color: #1e40af; font-size: 1.1rem;">
                    {insight_msg["content2"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #fef9c3; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #f59e0b;">
                <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">성장투자·배당 확대/투자효율 모니터링 메시지가 없습니다.<br>JSON의 insights.balance_sheet_monitoring 항목을 추가해 주세요.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Scale and Structure 카드 이하 기존 코드 유지
        first_year = balance_sheet_data['year'].iloc[0]
        last_year = balance_sheet_data['year'].iloc[-1]
        start_asset = balance_sheet_data['총자산'].iloc[0]
        end_asset = balance_sheet_data['총자산'].iloc[-1]
        asset_growth = ((end_asset / start_asset) - 1) * 100
        start_equity = balance_sheet_data['자본총계'].iloc[0]
        end_equity = balance_sheet_data['자본총계'].iloc[-1]
        equity_growth = ((end_equity / start_equity) - 1) * 100
        debt_year_before = balance_sheet_data['총부채'].iloc[-2]
        end_debt = balance_sheet_data['총부채'].iloc[-1]
        debt_growth = ((end_debt / debt_year_before) - 1) * 100
        start_debt_ratio = (balance_sheet_data['총부채'].iloc[0] / balance_sheet_data['총자산'].iloc[0]) * 100
        end_debt_ratio = (balance_sheet_data['총부채'].iloc[-1] / balance_sheet_data['총자산'].iloc[-1]) * 100
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">Scale and Structure</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">총자산: {start_asset} → {end_asset}억</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {self._get_growth_color(asset_growth, 'asset')};">{self._get_growth_comment(asset_growth, 'asset')} {asset_growth:+.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">자본총계: {start_equity} → {end_equity}억</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {self._get_growth_color(equity_growth, 'equity')};">{self._get_growth_comment(equity_growth, 'equity')} {equity_growth:+.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">총부채</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {self._get_growth_color(debt_growth, 'debt')};">{self._get_growth_comment(debt_growth, 'debt')} {debt_growth:+.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">부채비율 {start_debt_ratio:.0f}% → {end_debt_ratio:.0f}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {self._get_growth_color(end_debt_ratio - start_debt_ratio, 'debt_ratio')};">{self._get_growth_comment(end_debt_ratio - start_debt_ratio, 'debt_ratio')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_insight(self):
        """인사이트 렌더링 - 펜시한 카드 형태로"""
        insights = self.data_loader.get_insights()
        
        if "balance_sheet" in insights:
            insight_data = insights["balance_sheet"]
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">{insight_data["title"]}</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_data["content1"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #f59e0b;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">재무상태표 인사이트</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">재무상태표에 대한 인사이트 정보가 없습니다. JSON 파일에 insights.balance_sheet 항목을 추가해주세요.</div>
            </div>
            """, unsafe_allow_html=True)

    def _get_growth_comment(self, growth_rate, metric_type):
        """성장률에 따른 코멘트 생성"""
        if metric_type == "asset":
            if growth_rate < 5:
                return "정체"
            elif growth_rate < 15:
                return "완만"
            elif growth_rate < 30:
                return "안정"
            else:
                return "급증"
        elif metric_type == "equity":
            if growth_rate < 5:
                return "정체"
            elif growth_rate < 15:
                return "완만"
            elif growth_rate < 30:
                return "안정"
            else:
                return "급증"
        elif metric_type == "debt":
            if growth_rate < 0:
                return "감소"
            elif growth_rate < 10:
                return "안정"
            elif growth_rate < 30:
                return "증가"
            else:
                return "급증"
        elif metric_type == "debt_ratio":
            if growth_rate < -10:
                return "대폭개선"
            elif growth_rate < 0:
                return "개선"
            elif growth_rate < 10:
                return "안정"
            else:
                return "악화"

    def _get_growth_color(self, growth_rate, metric_type):
        """성장률에 따른 색상 반환"""
        if metric_type == "debt_ratio":
            if growth_rate < 0:
                return "#10b981"  # 개선 시 초록색
            elif growth_rate < 10:
                return "#3b82f6"  # 안정 시 파란색
            else:
                return "#ef4444"  # 악화 시 빨간색
        else:
            if growth_rate < 0:
                return "#ef4444"  # 감소 시 빨간색
            elif growth_rate < 10:
                return "#3b82f6"  # 낮은 성장 시 파란색
            else:
                return "#10b981"  # 높은 성장 시 초록색