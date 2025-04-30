import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class ProfitabilitySlide(BaseSlide):
    """수익성 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Comprehensive Analysis of ROE Drivers")
    
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
            self._render_dupont_analysis_chart()
        
        with col2:
            self._render_profitability_structure()
        
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
                    "display": False,
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
        
        # IframeChartComponent로 차트 렌더링
        IframeChartComponent.create_bar_chart_in_card(
            labels=labels,
            datasets=datasets,
            options=options,
            height=400,
            title="ROE 분해 분석 (듀폰 분석)",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            }
        )
    
    def _render_profitability_structure(self):
        """수익성 구조 렌더링 - 펜시한 카드 형태로, 직접 컨테이너 사용"""
        dupont_data = self.data_loader.get_dupont_data()
        insights = self.data_loader.get_insights()
        
        # 수익성 체질 개선 메시지 동적 표시
        insight_msg = insights.get("profitability", None)
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
                <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">수익성 체질 개선에 대한 메시지가 없습니다.<br>JSON의 insights.profitability 항목을 추가해 주세요.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # ROE 구성요소 분석 카드
        first_year = dupont_data['year'].iloc[0]
        last_year = dupont_data['year'].iloc[-1]
        start_roe = dupont_data['ROE'].iloc[0]
        end_roe = dupont_data['ROE'].iloc[-1]
        roe_change = ((end_roe / start_roe) - 1) * 100
        
        start_npm = dupont_data['순이익률'].iloc[0]
        end_npm = dupont_data['순이익률'].iloc[-1]
        npm_change = ((end_npm / start_npm) - 1) * 100
        
        start_at = dupont_data['자산회전율'].iloc[0]
        end_at = dupont_data['자산회전율'].iloc[-1]
        at_change = ((end_at / start_at) - 1) * 100
        
        start_fl = dupont_data['재무레버리지'].iloc[0]
        end_fl = dupont_data['재무레버리지'].iloc[-1]
        fl_change = ((end_fl / start_fl) - 1) * 100
        
        # ROE 변화 방향
        roe_direction = "상승" if roe_change > 0 else "하락"
        roe_color = "#10b981" if roe_change > 0 else "#ef4444"
        
        # 순이익률 변화 방향
        npm_direction = "상승" if npm_change > 0 else "하락"
        npm_color = "#10b981" if npm_change > 0 else "#ef4444"
        
        # 자산회전율 변화 방향
        at_direction = "상승" if at_change > 0 else "하락"
        at_color = "#10b981" if at_change > 0 else "#ef4444"
        
        # 재무레버리지 변화 방향
        fl_direction = "상승" if fl_change > 0 else "하락"
        fl_color = "#10b981" if fl_change > 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">ROE 구성요소 분석</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">ROE: {start_roe:.1f}% → {end_roe:.1f}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {roe_color};">{roe_direction} {abs(roe_change):.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">순이익률: {start_npm:.2f}% → {end_npm:.2f}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {npm_color};">{npm_direction} {abs(npm_change):.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">자산회전율: {start_at:.2f}회 → {end_at:.2f}회</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {at_color};">{at_direction} {abs(at_change):.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">재무레버리지: {start_fl:.2f}배 → {end_fl:.2f}배</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {fl_color};">{fl_direction} {abs(fl_change):.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        ## 업계 평균 비교 카드
        #if "industry_comparison" in insights:
        #    industry_data = insights["industry_comparison"]
        #    st.markdown(f"""
        #    <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
        #        <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">업계 평균 비교</div>
        #        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
        #            <div style="font-size: 1rem; color: #333; font-weight: 500;">ROE</div>
        #            <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #10b981;">업계평균 {industry_data["ROE"]}% 대비 {end_roe/industry_data["ROE"]:.1f}배</div>
        #        </div>
        #        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
        #            <div style="font-size: 1rem; color: #333; font-weight: 500;">순이익률</div>
        #            <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #10b981;">업계평균 {industry_data["순이익률"]}% 대비 {end_npm/industry_data["순이익률"]:.1f}배</div>
        #        </div>
        #        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
        #            <div style="font-size: 1rem; color: #333; font-weight: 500;">영업이익률</div>
        #            <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #10b981;">업계평균 {industry_data["영업이익률"]}% 대비 {dupont_data["영업이익률"].iloc[-1]/industry_data["영업이익률"]:.1f}배</div>
        #        </div>
        #    </div>
        #    """, unsafe_allow_html=True)
        #else:
        #    st.markdown("""
        #    <div style="background-color: #fef9c3; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #f59e0b;">
        #        <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">업계 평균 비교 데이터가 없습니다.<br>JSON의 insights.industry_comparison 항목을 추가해 주세요.</div>
        #    </div>
        #    """, unsafe_allow_html=True)
    
    def _render_insight(self):
        """인사이트 렌더링 - 펜시한 카드 형태로"""
        insights = self.data_loader.get_insights()
        
        if "profitability" in insights:
            insight_data = insights["profitability"]
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">{insight_data["title"]}</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_data["content1"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #f59e0b;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">수익성 분석 인사이트</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">수익성 분석에 대한 인사이트 정보가 없습니다. JSON 파일에 insights.profitability 항목을 추가해주세요.</div>
            </div>
            """, unsafe_allow_html=True)