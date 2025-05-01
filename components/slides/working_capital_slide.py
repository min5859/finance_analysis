import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE

class WorkingCapitalSlide(BaseSlide):
    """운전자본 효율성 분석 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Working Capital Efficiency Analysis (CCC)")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 인사이트는 별도로 표시
        self._render_insight()
    
        # 메인 콘텐츠를 두 열로 나눕니다: 왼쪽은 차트, 오른쪽은 운전자본 효율성 분석
        col1, col2 = st.columns([7, 5])
        with col1:
            self._render_key_metrics()
            self._render_working_capital_chart()
        
        with col2:
            self._render_working_capital_analysis()
    
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
        working_capital_data = self.data_loader.get_working_capital_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        # CCC 지표
        with col1:
            st.metric(
                label="현금전환주기(CCC)", 
                value=f"{working_capital_data['CCC'].iloc[-1]}일",
                delta=f"{-((working_capital_data['CCC'].iloc[0] - working_capital_data['CCC'].iloc[-1]) / working_capital_data['CCC'].iloc[0]) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # DSO 지표
        with col2:
            st.metric(
                label="매출채권회수기간", 
                value=f"{working_capital_data['DSO'].iloc[-1]}일",
                delta=f"{-((working_capital_data['DSO'].iloc[0] - working_capital_data['DSO'].iloc[-1]) / working_capital_data['DSO'].iloc[0]) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # DIO 지표
        with col3:
            st.metric(
                label="재고자산보유기간", 
                value=f"{working_capital_data['DIO'].iloc[-1]}일",
                delta=f"{-((working_capital_data['DIO'].iloc[0] - working_capital_data['DIO'].iloc[-1]) / working_capital_data['DIO'].iloc[0]) * 100:.1f}%",
                delta_color="inverse"
            )
        
        # DPO 지표
        with col4:
            st.metric(
                label="매입채무결제기간", 
                value=f"{working_capital_data['DPO'].iloc[-1]}일",
                delta=f"{((working_capital_data['DPO'].iloc[-1] - working_capital_data['DPO'].iloc[0]) / working_capital_data['DPO'].iloc[0]) * 100:.1f}%",
                delta_color="normal"
            )
    
    def _render_working_capital_chart(self):
        """운전자본 지표 차트 렌더링"""
        working_capital_data = self.data_loader.get_working_capital_data()
        
        # Chart.js 데이터셋 준비
        labels = working_capital_data['year'].tolist()
        datasets = [
            {
                "label": "매출채권회수기간 (일)",
                "data": working_capital_data['DSO'].tolist(),
                "backgroundColor": COLOR_PALETTE["primary"],
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 1
            },
            {
                "label": "재고자산보유기간 (일)",
                "data": working_capital_data['DIO'].tolist(),
                "backgroundColor": COLOR_PALETTE["success"],
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 1
            },
            {
                "label": "매입채무결제기간 (일)",
                "data": working_capital_data['DPO'].tolist(),
                "backgroundColor": COLOR_PALETTE["warning"],
                "borderColor": COLOR_PALETTE["warning"],
                "borderWidth": 1
            },
            {
                "label": "현금전환주기 (일)",
                "data": working_capital_data['CCC'].tolist(),
                "backgroundColor": COLOR_PALETTE["danger"],
                "borderColor": COLOR_PALETTE["danger"],
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
                    "text": "운전자본 효율성 분석 (단위: 일)"
                },
                "tooltip": {
                    "mode": "index",
                    "intersect": False,
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
                    "anchor": "end",
                    "offset": 4,
                    "borderRadius": 4,
                    "padding": 4
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {
                        "display": True,
                        "text": "일수"
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
            title="운전자본 효율성 분석 (단위: 일)",
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "20px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "20px"
            },
            use_datalabels=True
        )
    
    def _render_working_capital_analysis(self):
        """운전자본 효율성 분석 렌더링 - 펜시한 카드 형태로"""
        working_capital_data = self.data_loader.get_working_capital_data()
        insights = self.data_loader.get_insights()
        
        # 운전자본 관리 메시지 동적 표시
        insight_msg = insights.get("working_capital", None)
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
                <div style="font-weight: 600; color: #b45309; font-size: 1.1rem;">운전자본 관리에 대한 메시지가 없습니다.<br>JSON의 insights.working_capital 항목을 추가해 주세요.</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 운전자본 효율성 지표 변화 카드
        first_year = working_capital_data['year'].iloc[0]
        last_year = working_capital_data['year'].iloc[-1]
        
        # CCC 변화
        start_ccc = working_capital_data['CCC'].iloc[0]
        end_ccc = working_capital_data['CCC'].iloc[-1]
        ccc_change = ((end_ccc / start_ccc) - 1) * 100
        ccc_improvement = -ccc_change  # 감소가 개선이므로 부호 변경
        
        # DSO 변화
        start_dso = working_capital_data['DSO'].iloc[0]
        end_dso = working_capital_data['DSO'].iloc[-1]
        dso_change = ((end_dso / start_dso) - 1) * 100
        dso_improvement = -dso_change  # 감소가 개선이므로 부호 변경
        
        # DIO 변화
        start_dio = working_capital_data['DIO'].iloc[0]
        end_dio = working_capital_data['DIO'].iloc[-1]
        dio_change = ((end_dio / start_dio) - 1) * 100
        dio_improvement = -dio_change  # 감소가 개선이므로 부호 변경
        
        # DPO 변화
        start_dpo = working_capital_data['DPO'].iloc[0]
        end_dpo = working_capital_data['DPO'].iloc[-1]
        dpo_change = ((end_dpo / start_dpo) - 1) * 100  # 증가가 개선이므로 부호 유지
        
        # 색상 결정 (개선되면 녹색, 악화되면 빨간색)
        ccc_color = "#10b981" if ccc_improvement > 0 else "#ef4444"
        dso_color = "#10b981" if dso_improvement > 0 else "#ef4444"
        dio_color = "#10b981" if dio_improvement > 0 else "#ef4444"
        dpo_color = "#10b981" if dpo_change > 0 else "#ef4444"
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">운전자본 효율성 지표 변화</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">현금전환주기(CCC)</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {ccc_color}">{start_ccc}일 → {end_ccc}일 ({ccc_improvement:.1f}% 개선)</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">매출채권회수기간(DSO)</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {dso_color}">{start_dso}일 → {end_dso}일 ({dso_improvement:.1f}% 개선)</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">재고자산보유기간(DIO)</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {dio_color}">{start_dio}일 → {end_dio}일 ({dio_improvement:.1f}% 개선)</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">매입채무결제기간(DPO)</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {dpo_color}">{start_dpo}일 → {end_dpo}일 ({dpo_change:.1f}% 변화)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 운전자본 효율성 요약 점수 카드
        self._render_working_capital_score_card()
        
        # 현금흐름과의 관계 분석 카드
        self._render_cash_flow_relationship_card()
    
    def _render_working_capital_score_card(self):
        """운전자본 효율성 요약 점수 카드"""
        working_capital_data = self.data_loader.get_working_capital_data()
        insights = self.data_loader.get_insights()
        
        # 최신 CCC 값 가져오기
        latest_ccc = working_capital_data['CCC'].iloc[-1]
        
        # 산업 평균 CCC를 JSON에서 가져오기
        industry_avg_ccc = insights.get('working_capital', {}).get('industry_avg_ccc', 90)  # 기본값 90
        
        # CCC 점수 계산 기준도 JSON에서 가져오기
        ccc_thresholds = insights.get('working_capital', {}).get('ccc_thresholds', {
            'very_good': 50,
            'good': 70,
            'fair': 90,
            'moderate': 110
        })
        
        # CCC 점수 계산
        if latest_ccc < ccc_thresholds.get('very_good', 50):
            ccc_score = "매우 우수"
            ccc_description = "업계 최상위 수준의 운전자본 관리 효율성"
            ccc_color = "#10b981"
        elif latest_ccc < ccc_thresholds.get('good', 70):
            ccc_score = "우수"
            ccc_description = "업계 평균보다 우수한 수준의 운전자본 관리"
            ccc_color = "#22c55e"
        elif latest_ccc < ccc_thresholds.get('fair', 90):
            ccc_score = "양호"
            ccc_description = "업계 평균 수준의 운전자본 관리"
            ccc_color = "#3b82f6"
        elif latest_ccc < ccc_thresholds.get('moderate', 110):
            ccc_score = "보통"
            ccc_description = "업계 평균과 유사한 수준의 운전자본 관리"
            ccc_color = "#f59e0b"
        else:
            ccc_score = "개선 필요"
            ccc_description = "운전자본 효율 개선을 위한 집중적인 관리 필요"
            ccc_color = "#ef4444"
        
        # 운전자본 관련 리스크 또는 기회 평가
        if latest_ccc < industry_avg_ccc:
            risk_assessment = "낮음"
            risk_color = "#10b981"
        else:
            risk_assessment = "보통"
            risk_color = "#f59e0b"
        
        st.markdown(f"""
        <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08); margin-bottom: 20px;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">운전자본 효율성 평가</div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">CCC 효율성 점수</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {ccc_color}">{ccc_score}</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">업계 평균 대비</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {ccc_color}">{industry_avg_ccc - latest_ccc:.1f}일 빠름</div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                <div style="font-size: 1rem; color: #333; font-weight: 500;">유동성 리스크</div>
                <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {risk_color}">{risk_assessment}</div>
            </div>
            <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px;">
                <div style="font-size: 0.9rem; color: #475569;">{ccc_description}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_cash_flow_relationship_card(self):
        """현금흐름과의 관계 분석 카드"""
        working_capital_data = self.data_loader.get_working_capital_data()
        
        # 현금흐름 데이터를 가져오려면 실제로는 DataLoader를 통해 가져와야 함
        # 여기서는 간단한 예시만 표시
        cash_flow_data = self.data_loader.get_cash_flow_data() if hasattr(self.data_loader, 'get_cash_flow_data') else None
        
        has_cash_flow_data = cash_flow_data is not None and not cash_flow_data.empty
        
        latest_ccc = working_capital_data['CCC'].iloc[-1]
        pre_latest_ccc = working_capital_data['CCC'].iloc[-2]
        
        if has_cash_flow_data:
            latest_fcf = cash_flow_data['FCF'].iloc[-1]
            pre_latest_fcf = cash_flow_data['FCF'].iloc[-2]
            
            ccc_change = latest_ccc - pre_latest_ccc
            fcf_change = latest_fcf - pre_latest_fcf
            
            # CCC 감소와 FCF 증가는 일반적으로 양의 상관관계
            if ccc_change < 0 and fcf_change > 0:
                relationship = "양의 상관관계"
                description = "CCC 개선으로 FCF가 증가하는 긍정적인 패턴"
                color = "#10b981"
            elif ccc_change > 0 and fcf_change < 0:
                relationship = "양의 상관관계"
                description = "CCC 악화로 FCF가 감소하는 패턴"
                color = "#ef4444"
            else:
                relationship = "역의 상관관계"
                description = "다른 요인이 FCF에 더 큰 영향을 미치고 있음"
                color = "#f59e0b"
                
            st.markdown(f"""
            <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">운전자본과 현금흐름의 관계</div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                    <div style="font-size: 1rem; color: #333; font-weight: 500;">CCC 변화</div>
                    <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {color if ccc_change < 0 else "#ef4444"}">{ccc_change:.1f}일</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding: 12px 0;">
                    <div style="font-size: 1rem; color: #333; font-weight: 500;">FCF 변화</div>
                    <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {color if fcf_change > 0 else "#ef4444"}">{fcf_change}억원</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0;">
                    <div style="font-size: 1rem; color: #333; font-weight: 500;">상관관계</div>
                    <div style="font-size: 1rem; text-align: right; font-weight: 600; color: {color}">{relationship}</div>
                </div>
                <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px;">
                    <div style="font-size: 0.9rem; color: #475569;">{description}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);">
                <div style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px;">운전자본과 현금흐름의 관계</div>
                <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px;">
                    <div style="font-size: 0.9rem; color: #475569;">현금흐름 데이터가 없습니다. 현금흐름 데이터를 로드하면 운전자본과 현금흐름 간의 관계를 확인할 수 있습니다.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_insight(self):
        """인사이트 렌더링 - 펜시한 카드 형태로"""
        insights = self.data_loader.get_insights()
        
        if "working_capital" in insights and "content1" in insights["working_capital"]:
            insight_data = insights["working_capital"]
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">{insight_data.get("title", "운전자본 효율성 분석")}</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_data["content1"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 기본 인사이트 제공 (데이터가 없는 경우)
            insight_content = """
            JSON 파일에 insights.working_capital 항목을 추가해주세요.
            """
            
            st.markdown(f"""
            <div style="background: #f0f9ff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); margin-bottom: 20px; border-left: 5px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">운전자본 효율성 분석</div>
                <div style="font-size: 0.95rem; color: #334155; line-height: 1.6;">{insight_content}</div>
            </div>
            """, unsafe_allow_html=True)