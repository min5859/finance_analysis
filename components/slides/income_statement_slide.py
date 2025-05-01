import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class IncomeStatementSlide(BaseSlide):
    """손익계산서 추이 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Income Statement Analysis")
    
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
        
        # Chart.js 옵션 설정 - datalabels 플러그인 추가
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
                    "text": "손익계산서 주요 항목 추이 (단위: 억원, %)"
                },
                # datalabels 플러그인 설정 추가 - 항상 데이터 라벨 표시
                "datalabels": {
                    "display": True,
                    "color": "black",
                    "font": {
                        "weight": "bold",
                        "size": 11
                    },
                    "formatter": """function(value, context) {
                        // 순이익률(%) 라인 차트에는 % 추가
                        if (context.datasetIndex === 3) {
                            return value + '%';
                        }
                        // 다른 데이터셋에는 숫자만 표시
                        return value.toLocaleString();
                    }""",
                    "align": "top",
                    "anchor": "end",
                    "offset": 4,
                    "borderRadius": 4,
                    "padding": 4
                },
                # 기존 tooltip 설정도 유지
                "tooltip": {
                    "mode": "index",
                    "intersect": False
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
        
        # IframeChartComponent로 차트 렌더링 (datalabels 플러그인 사용)
        IframeChartComponent.create_bar_chart_in_card(
            labels=labels,
            datasets=datasets,
            options=options,
            height=400,
            title="손익계산서 주요 항목 추이 (단위: 억원, %)",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            },
            use_datalabels=True  # datalabels 플러그인 사용 설정
        )
    
    def _render_insight(self):
        """인사이트 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        insights = self.data_loader.get_insights()
        
        # 데이터 계산
        start_revenue = performance_data['매출액'].iloc[0]
        end_revenue = performance_data['매출액'].iloc[-1]
        revenue_change = ((end_revenue / start_revenue) - 1) * 100
        
        start_op_profit = performance_data['영업이익'].iloc[0]
        end_op_profit = performance_data['영업이익'].iloc[-1]
        op_profit_change = ((end_op_profit / start_op_profit) - 1) * 100
        
        start_net_profit = performance_data['순이익'].iloc[0]
        end_net_profit = performance_data['순이익'].iloc[-1]
        net_profit_change = ((end_net_profit / start_net_profit) - 1) * 100
        
        start_net_margin = performance_data['순이익률'].iloc[0]
        end_net_margin = performance_data['순이익률'].iloc[-1]
        
        # 인사이트 메시지를 JSON에서 가져오기
        insight_msg = insights.get('income_statement', {}).get('summary_message', 'JSON 파일에 insights.income_statement 항목을 추가해주세요')
        
        # 새로운 스타일로 인사이트 렌더링
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px; height: 100%;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">Key Insight</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">매출액: {start_revenue} → {end_revenue}억원</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #ef4444;">3년간 {revenue_change:.1f}% 감소</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">영업이익: {start_op_profit} → {end_op_profit}억원</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #ef4444;">감소 후 회복 {op_profit_change:.1f}%</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">순이익: {start_net_profit} → {end_net_profit}억원</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #10b981;">+{net_profit_change:.1f}% 성장</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">순이익률: {start_net_margin}% → {end_net_margin}%</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #10b981;">수익성 체질 개선</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500; line-height: 1.4;">{insight_msg}</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: #8b5cf6;">⭐</div>
            </div>
        </div>
        """, unsafe_allow_html=True)