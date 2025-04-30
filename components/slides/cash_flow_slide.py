import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE
import streamlit.components.v1 as components

class CashFlowSlide(BaseSlide):
    """현금흐름 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Operating, Investing, and Free Cash Flow Trends")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 인사이트는 별도로 표시
        self._render_insight()
    
        # 메인 콘텐츠를 두 열로 나눕니다: 왼쪽은 차트, 오른쪽은 현금흐름 분석
        col1, col2 = st.columns([7, 5])
        with col1:
            self._render_key_metrics()
            self._render_cash_flow_chart()
        
        with col2:
            self._render_cash_flow_analysis()
    
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
        cash_flow_data = self.data_loader.get_cash_flow_data()
        
        col1, col2, col3 = st.columns(3)
        
        # 영업활동현금흐름 지표
        latest_op_cf = cash_flow_data['영업활동'].iloc[-1]
        delta_color = "normal" if latest_op_cf >= 0 else "inverse"
        with col1:
            st.metric(
                label="영업활동현금흐름 (2024)", 
                value=f"{latest_op_cf}억원",
                delta=f"{((latest_op_cf / cash_flow_data['영업활동'].iloc[-2]) - 1) * 100:.1f}%" if cash_flow_data['영업활동'].iloc[-2] != 0 else "N/A",
                delta_color=delta_color
            )
        
        # 투자활동현금흐름 지표
        latest_inv_cf = cash_flow_data['투자활동'].iloc[-1]
        delta_color = "inverse" if latest_inv_cf < 0 else "normal"
        with col2:
            st.metric(
                label="투자활동현금흐름 (2024)", 
                value=f"{latest_inv_cf}억원",
                delta=f"{((latest_inv_cf / cash_flow_data['투자활동'].iloc[-2]) - 1) * 100:.1f}%" if cash_flow_data['투자활동'].iloc[-2] != 0 else "N/A",
                delta_color=delta_color
            )
        
        # 잉여현금흐름(FCF) 지표
        latest_fcf = cash_flow_data['FCF'].iloc[-1]
        delta_color = "normal" if latest_fcf >= 0 else "inverse"
        with col3:
            st.metric(
                label="잉여현금흐름(FCF) (2024)", 
                value=f"{latest_fcf}억원",
                delta=f"{((latest_fcf / cash_flow_data['FCF'].iloc[-2]) - 1) * 100:.1f}%" if cash_flow_data['FCF'].iloc[-2] != 0 else "N/A",
                delta_color=delta_color
            )
    
    def _render_cash_flow_chart(self):
        """현금흐름 차트 렌더링"""
        cash_flow_data = self.data_loader.get_cash_flow_data()
        
        # Chart.js 데이터셋 준비
        labels = cash_flow_data['year'].tolist()
        datasets = [
            {
                "label": "영업활동현금흐름",
                "data": cash_flow_data['영업활동'].tolist(),
                "backgroundColor": COLOR_PALETTE["success"],
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 1
            },
            {
                "label": "투자활동현금흐름",
                "data": cash_flow_data['투자활동'].tolist(),
                "backgroundColor": COLOR_PALETTE["danger"],
                "borderColor": COLOR_PALETTE["danger"],
                "borderWidth": 1
            },
            {
                "label": "잉여현금흐름 (FCF)",
                "data": cash_flow_data['FCF'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
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
                    "display": False,
                    "text": "현금흐름 추이 분석 (단위: 억원)"
                },
                "tooltip": {
                    "mode": "index",
                    "intersect": False
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": False,
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
            title="현금흐름 추이 분석 (단위: 억원)",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "10px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            }
        )
    
    def _render_cash_flow_analysis(self):
        """현금흐름 분석 렌더링 - 펜시한 카드 형태로"""
        cash_flow_data = self.data_loader.get_cash_flow_data()
        insights = self.data_loader.get_insights()
        
        # 현금흐름 모니터링 필요성 메시지 동적 표시
        insight_msg = insights.get("cash_flow", None)
        if insight_msg and "content2" in insight_msg:
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
                <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">현금흐름 모니터링에 대한 메시지가 없습니다.<br>JSON의 insights.cash_flow 항목을 추가해 주세요.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 현금흐름 추이 분석 카드
        first_year = cash_flow_data['year'].iloc[0]
        last_year = cash_flow_data['year'].iloc[-1]
        
        # 영업활동현금흐름 변화
        op_cf_values = [f"{val}억원" for val in cash_flow_data['영업활동'].tolist()]
        op_cf_latest = cash_flow_data['영업활동'].iloc[-1]
        op_cf_prev = cash_flow_data['영업활동'].iloc[-2]
        op_cf_first = cash_flow_data['영업활동'].iloc[0]
        
        # 투자활동현금흐름 변화
        inv_cf_values = [f"{val}억원" for val in cash_flow_data['투자활동'].tolist()]
        inv_cf_latest = cash_flow_data['투자활동'].iloc[-1]
        inv_cf_prev = cash_flow_data['투자활동'].iloc[-2]
        
        # FCF 변화
        fcf_values = [f"{val}억원" for val in cash_flow_data['FCF'].tolist()]
        fcf_latest = cash_flow_data['FCF'].iloc[-1]
        fcf_prev = cash_flow_data['FCF'].iloc[-2]
        
        # 색상 결정
        op_cf_color = "#10b981" if op_cf_latest >= 0 else "#ef4444"
        inv_cf_color = "#ef4444" if inv_cf_latest < 0 else "#10b981"
        fcf_color = "#10b981" if fcf_latest >= 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">현금흐름 추이 변화</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">영업활동현금흐름</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {op_cf_color};">{op_cf_values[0]} → {op_cf_values[1]} → {op_cf_values[2]}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">투자활동현금흐름</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {inv_cf_color};">{inv_cf_values[0]} → {inv_cf_values[1]} → {inv_cf_values[2]}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">잉여현금흐름(FCF)</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {fcf_color};">{fcf_values[0]} → {fcf_values[1]} → {fcf_values[2]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 현금흐름 변동 원인 분석 카드
        self._render_cash_flow_causes_card()
        
        # 현금흐름 진단 및 예측 카드
        self._render_cash_flow_diagnosis()
    
    def _render_cash_flow_causes_card(self):
        """현금흐름 변동 원인 분석 카드"""
        insights = self.data_loader.get_insights()
        
        causes = []
        if "cash_flow_causes" in insights:
            causes = insights["cash_flow_causes"]
        else:
            # 기본 원인 분석 (데이터가 없는 경우)
            causes = [
                {"factor": "운전자본 증가", "impact": "부정적", "description": "재고 317억원, 매출채권 156억원 증가"},
                {"factor": "신규 투자", "impact": "부정적", "description": "4억원 투자 지출 발생"},
                {"factor": "매출 감소", "impact": "부정적", "description": "매출 하락으로 영업활동현금 유입 감소"}
            ]
        
        causes_html = ""
        for cause in causes:
            impact_color = "#ef4444" if cause["impact"] == "부정적" else "#10b981"
            causes_html += f"""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">{cause["factor"]}</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {impact_color};">{cause["description"]}</div>
            </div>
            """
        
        html_content = f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">2024년 현금흐름 변동 요인</div>
            {causes_html}
        </div>
        """
        
        components.html(html_content, height=250, scrolling=False)
    
    def _render_cash_flow_diagnosis(self):
        """현금흐름 진단 및 예측 카드"""
        cash_flow_data = self.data_loader.get_cash_flow_data()
        insights = self.data_loader.get_insights()
        
        # 현금흐름이 양수인지 음수인지에 따라 다른 진단
        latest_fcf = cash_flow_data['FCF'].iloc[-1]
        
        if latest_fcf >= 0:
            diagnosis_title = "현금창출 양호"
            diagnosis_color = "#10b981"
            diagnosis_icon = "✅"
        else:
            diagnosis_title = "현금창출 개선 필요"
            diagnosis_color = "#f97316"
            diagnosis_icon = "⚠️"
        
        # 진단 내용
        if "cash_flow_diagnosis" in insights:
            diagnosis = insights["cash_flow_diagnosis"]
        else:
            # 기본 진단 (데이터가 없는 경우)
            if latest_fcf >= 0:
                diagnosis = "안정적인 현금 창출 능력 보유 중입니다. 지속적인 모니터링이 필요합니다."
            else:
                diagnosis = """
                현재 현금흐름이 악화된 상태입니다. 주요 원인은 운전자본의 급격한 증가로 판단됩니다.
                이는 신규 사업 준비를 위한 전략적 선투자로 해석할 수 있으나, 단기 유동성 관리가 필요합니다.
                재고 및 매출채권 회전율 개선을 통해 현금 회수 기간을 단축하는 것이 중요합니다.
                """
        
        html_content = f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);">
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 1.8rem; margin-right: 10px;">{diagnosis_icon}</div>
                <div style="font-size: 1.5rem; font-weight: 600; color: {diagnosis_color};">{diagnosis_title}</div>
            </div>
            <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">
                {diagnosis}
            </div>
        </div>
        """
        
        components.html(html_content, height=250, scrolling=False)
    
    def _render_insight(self):
        """인사이트 렌더링 - 펜시한 카드 형태로"""
        insights = self.data_loader.get_insights()
        
        if "cash_flow" in insights and "content1" in insights["cash_flow"]:
            insight_data = insights["cash_flow"]
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">{insight_data.get("title", "현금흐름 분석")}</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_data["content1"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 기본 인사이트 제공 (데이터가 없는 경우)
            insight_content = """
            JSON 파일에 insights.cash_flow 항목을 추가해주세요.
            """
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">현금흐름 분석</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_content}</div>
            </div>
            """, unsafe_allow_html=True)