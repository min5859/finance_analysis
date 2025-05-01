import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class StabilitySlide(BaseSlide):
    """안정성 지표 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Financial Stability Trends")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 인사이트는 별도로 표시
        self._render_insight()
    
        # 메인 콘텐츠를 두 열로 나눕니다: 왼쪽은 차트, 오른쪽은 재무안정성 구조
        col1, col2 = st.columns([7, 5])
        with col1:
            self._render_key_metrics()
            self._render_stability_chart()
        
        with col2:
            self._render_stability_structure()
    
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
            "maintainAspectRatio": False,
            "layout": {
                "padding": {
                    "left": 10,
                    "right": 10,
                    "top": 0,
                    "bottom": 30  # 하단에 더 많은 패딩 추가
                }
            },
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": False,
                    "text": "재무안정성 지표 추이"
                },
                "tooltip": {
                    "mode": "index",
                    "intersect": False
                },
                "datalabels": {
                    "display": True,
                    "color": "black",
                    "font": {
                        "weight": "bold",
                        "size": 11
                    },
                    "formatter": "function(value) { return value.toLocaleString(); }",
                    "align": "top",
                    "offset": 10,
                    "backgroundColor": "white",
                    "borderRadius": 4,
                    "padding": 4
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
        
        # IframeChartComponent로 차트 렌더링
        IframeChartComponent.create_line_chart_in_card(
            labels=labels,
            datasets=datasets,
            options=options,
            height=400,
            title="재무안정성 지표 추이",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            },
            use_datalabels=True
        )
    
    def _render_stability_structure(self):
        """재무안정성 구조 렌더링 - 펜시한 카드 형태로"""
        stability_data = self.data_loader.get_stability_data()
        insights = self.data_loader.get_insights()
        
        # 재무안정성 메시지 동적 표시
        insight_msg = insights.get("stability", None)
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
                <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">재무안정성에 대한 메시지가 없습니다.<br>JSON의 insights.stability 항목을 추가해 주세요.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 재무안정성 지표 분석 카드
        first_year = stability_data['year'].iloc[0]
        last_year = stability_data['year'].iloc[-1]
        
        # 부채비율 변화
        start_debt_ratio = stability_data['부채비율'].iloc[0]
        end_debt_ratio = stability_data['부채비율'].iloc[-1]
        debt_ratio_change = ((end_debt_ratio / start_debt_ratio) - 1) * 100
        
        # 유동비율 변화
        start_current_ratio = stability_data['유동비율'].iloc[0]
        end_current_ratio = stability_data['유동비율'].iloc[-1]
        current_ratio_change = ((end_current_ratio / start_current_ratio) - 1) * 100
        
        # 이자보상배율 변화
        start_interest_coverage = stability_data['이자보상배율'].iloc[0]
        end_interest_coverage = stability_data['이자보상배율'].iloc[-1]
        interest_coverage_change = ((end_interest_coverage / start_interest_coverage) - 1) * 100
        
        # 변화 방향 및 색상 설정
        debt_ratio_direction = "감소" if debt_ratio_change < 0 else "증가"
        debt_ratio_color = "#10b981" if debt_ratio_change < 0 else "#ef4444"
        
        current_ratio_direction = "상승" if current_ratio_change > 0 else "하락"
        current_ratio_color = "#10b981" if current_ratio_change > 0 else "#ef4444"
        
        interest_coverage_direction = "상승" if interest_coverage_change > 0 else "하락"
        interest_coverage_color = "#10b981" if interest_coverage_change > 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">재무안정성 지표 분석</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">부채비율: {start_debt_ratio}% → {end_debt_ratio}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {debt_ratio_color};">{debt_ratio_direction} {abs(debt_ratio_change):.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">유동비율: {start_current_ratio}% → {end_current_ratio}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {current_ratio_color};">{current_ratio_direction} {abs(current_ratio_change):.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">이자보상배율: {start_interest_coverage}배 → {end_interest_coverage}배</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {interest_coverage_color};">{interest_coverage_direction} {abs(interest_coverage_change):.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 재무안정성 평가 카드
        safety_evaluation = self._evaluate_financial_safety(end_debt_ratio, end_current_ratio, end_interest_coverage)
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">재무안정성 종합 평가</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">부채비율</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {safety_evaluation['debt_ratio_color']};">{safety_evaluation['debt_ratio_status']}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">유동비율</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {safety_evaluation['current_ratio_color']};">{safety_evaluation['current_ratio_status']}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">이자보상배율</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {safety_evaluation['interest_coverage_color']};">{safety_evaluation['interest_coverage_status']}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">종합 등급</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {safety_evaluation['overall_color']};">{safety_evaluation['overall_status']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _evaluate_financial_safety(self, debt_ratio, current_ratio, interest_coverage):
        """재무안정성 평가 수행"""
        insights = self.data_loader.get_insights()
        stability_thresholds = insights.get('stability', {}).get('thresholds', {
            'debt_ratio': {
                'very_safe': 50,
                'safe': 80,
                'normal': 120,
                'caution': 200
            },
            'current_ratio': {
                'very_good': 200,
                'good': 150,
                'fair': 100,
                'caution': 80
            },
            'interest_coverage': {
                'very_good': 5,
                'good': 3,
                'fair': 1.5,
                'caution': 1
            }
        })
        
        # 부채비율 평가
        if debt_ratio < stability_thresholds['debt_ratio'].get('very_safe', 50):
            debt_ratio_status = "매우 안전 (20~40% 이내)"
            debt_ratio_color = "#10b981"
        elif debt_ratio < stability_thresholds['debt_ratio'].get('safe', 80):
            debt_ratio_status = "안전 (40~80% 이내)"
            debt_ratio_color = "#22c55e"
        elif debt_ratio < stability_thresholds['debt_ratio'].get('normal', 120):
            debt_ratio_status = "보통 (80~120% 이내)"
            debt_ratio_color = "#f59e0b"
        elif debt_ratio < stability_thresholds['debt_ratio'].get('caution', 200):
            debt_ratio_status = "주의 (120~200% 이내)"
            debt_ratio_color = "#f97316"
        else:
            debt_ratio_status = "위험 (200% 초과)"
            debt_ratio_color = "#ef4444"
        
        # 유동비율 평가
        if current_ratio > stability_thresholds['current_ratio'].get('very_good', 200):
            current_ratio_status = "매우 양호 (200% 초과)"
            current_ratio_color = "#10b981"
        elif current_ratio > stability_thresholds['current_ratio'].get('good', 150):
            current_ratio_status = "양호 (150~200% 이내)"
            current_ratio_color = "#22c55e"
        elif current_ratio > stability_thresholds['current_ratio'].get('fair', 100):
            current_ratio_status = "적정 (100~150% 이내)"
            current_ratio_color = "#f59e0b"
        elif current_ratio > stability_thresholds['current_ratio'].get('caution', 80):
            current_ratio_status = "주의 (80~100% 이내)"
            current_ratio_color = "#f97316"
        else:
            current_ratio_status = "위험 (80% 미만)"
            current_ratio_color = "#ef4444"
        
        # 이자보상배율 평가
        if interest_coverage > stability_thresholds['interest_coverage'].get('very_good', 5):
            interest_coverage_status = "매우 양호 (5배 초과)"
            interest_coverage_color = "#10b981"
        elif interest_coverage > stability_thresholds['interest_coverage'].get('good', 3):
            interest_coverage_status = "양호 (3~5배 이내)"
            interest_coverage_color = "#22c55e"
        elif interest_coverage > stability_thresholds['interest_coverage'].get('fair', 1.5):
            interest_coverage_status = "적정 (1.5~3배 이내)"
            interest_coverage_color = "#f59e0b"
        elif interest_coverage > stability_thresholds['interest_coverage'].get('caution', 1):
            interest_coverage_status = "주의 (1~1.5배 이내)"
            interest_coverage_color = "#f97316"
        else:
            interest_coverage_status = "위험 (1배 미만)"
            interest_coverage_color = "#ef4444"
        
        # 종합 등급 평가 (간단한 로직)
        # 각 지표의 색상 값에 가중치를 부여하여 종합 점수 계산
        # 녹색: 3점, 연한 녹색: 2점, 주황색: 1점, 진한 주황색: 0점, 적색: -1점
        score_map = {
            "#10b981": 3,  # 매우 양호
            "#22c55e": 2,  # 양호
            "#f59e0b": 1,  # 적정/보통
            "#f97316": 0,  # 주의
            "#ef4444": -1  # 위험
        }
        
        total_score = (
            score_map[debt_ratio_color] + 
            score_map[current_ratio_color] + 
            score_map[interest_coverage_color]
        )
        
        # 종합 점수에 따른 등급 부여
        if total_score >= 7:
            overall_status = "AAA (최상)"
            overall_color = "#10b981"
        elif total_score >= 5:
            overall_status = "AA (우수)"
            overall_color = "#22c55e"
        elif total_score >= 3:
            overall_status = "A (양호)"
            overall_color = "#3b82f6"
        elif total_score >= 1:
            overall_status = "BBB (적정)"
            overall_color = "#f59e0b"
        elif total_score >= -1:
            overall_status = "BB (주의)"
            overall_color = "#f97316"
        else:
            overall_status = "B (위험)"
            overall_color = "#ef4444"
        
        return {
            "debt_ratio_status": debt_ratio_status,
            "debt_ratio_color": debt_ratio_color,
            "current_ratio_status": current_ratio_status,
            "current_ratio_color": current_ratio_color,
            "interest_coverage_status": interest_coverage_status,
            "interest_coverage_color": interest_coverage_color,
            "overall_status": overall_status,
            "overall_color": overall_color
        }
    
    def _render_insight(self):
        """인사이트 렌더링 - 펜시한 카드 형태로"""
        insights = self.data_loader.get_insights()
        
        if "stability" in insights:
            insight_data = insights["stability"]
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">{insight_data["title"]}</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_data["content1"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 기본 인사이트 제공 (데이터가 없는 경우)
            insight_content = """
            JSON 파일에 insights.stability 항목을 추가해주세요.
            """
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">안정성 분석</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_content}</div>
            </div>
            """, unsafe_allow_html=True)