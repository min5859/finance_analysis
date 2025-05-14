import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
from datetime import datetime

class ValuationManualSlide(BaseSlide):
    """LLM 기반 기업 가치 평가 슬라이드 - 향상된 버전"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Advanced Company Valuation")
        self.company_data = data_loader.get_all_data()
        self.performance_data = data_loader.get_performance_data() if hasattr(data_loader, 'get_performance_data') else None
        self.balance_sheet_data = data_loader.get_balance_sheet_data() if hasattr(data_loader, 'get_balance_sheet_data') else None
        self.cash_flow_data = data_loader.get_cash_flow_data() if hasattr(data_loader, 'get_cash_flow_data') else None
        self.growth_rates = data_loader.get_growth_rates() if hasattr(data_loader, 'get_growth_rates') else None
        self.profitability_data = data_loader.get_profitability_data() if hasattr(data_loader, 'get_profitability_data') else None
        self.stability_data = data_loader.get_stability_data() if hasattr(data_loader, 'get_stability_data') else None
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 세션 상태 초기화
        if "valuation_method" not in st.session_state:
            st.session_state.valuation_method = "dcf"
        if "valuation_params" not in st.session_state:
            st.session_state.valuation_params = {}
        
        # 가치평가 방법 선택
        self._render_method_selector()
        
        # 세션 상태에 가치 평가 결과가 있는지 확인
        if "valuation_results" not in st.session_state:
            # 가치 평가 시작 폼
            self._render_valuation_form()
        else:
            # 가치 평가 결과 표시
            self._render_valuation_results()
    
    def _add_custom_styles(self):
        """커스텀 CSS 스타일 추가"""
        st.markdown("""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        /* 분석 요청 폼 스타일 */
        .request-container {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
            text-align: center;
            margin: 30px 0;
            border: 1px solid #e5e7eb;
        }
        
        .method-selector {
            padding: 10px;
            margin-bottom: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .parameter-group {
            padding: 15px;
            margin-bottom: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .parameter-title {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 10px;
            color: #4F46E5;
        }
        
        .info-box {
            padding: 10px 15px;
            margin: 10px 0;
            background: #F3F4F6;
            border-left: 3px solid #4F46E5;
            border-radius: 5px;
        }
        
        .scenario-tabs > div[role="tablist"] {
            gap: 5px;
        }
        
        .scenario-tabs > div[role="tablist"] > button {
            border-radius: 5px;
            border: none;
            padding: 5px 15px;
            background: #E5E7EB;
            color: #4B5563;
            font-weight: 500;
        }
        
        .scenario-tabs > div[role="tablist"] > button[aria-selected="true"] {
            background: #4F46E5;
            color: white;
        }
        
        /* 결과 카드 스타일 */
        .result-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        
        .result-title {
            font-size: 18px;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #E5E7EB;
        }
        
        .result-subtitle {
            font-size: 16px;
            font-weight: 500;
            color: #4B5563;
            margin: 10px 0;
        }
        
        .result-metric {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
        }
        
        .metric-label {
            color: #6B7280;
        }
        
        .metric-value {
            font-weight: 600;
            color: #111827;
        }
        
        /* 로딩 스피너 스타일 */
        @keyframes spinner {
            to {transform: rotate(360deg);}
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: spinner 0.8s linear infinite;
            margin: 20px auto;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_method_selector(self):
        """가치평가 방법 선택기 렌더링"""
        st.markdown('<div class="method-selector">', unsafe_allow_html=True)
        method_options = {
            "dcf": "DCF (Discounted Cash Flow)",
            "multiples": "상대가치법 (Multiples)",
            "asset": "자산가치법 (Asset-based)",
            "combined": "복합 가치평가법"
        }
        cols = st.columns(len(method_options))
        
        for i, (key, label) in enumerate(method_options.items()):
            with cols[i]:
                if st.button(
                    label, 
                    key=f"method_{key}",
                    use_container_width=True,
                    type="primary" if st.session_state.valuation_method == key else "secondary"
                ):
                    st.session_state.valuation_method = key
                    # 기존 결과를 초기화합니다
                    if "valuation_results" in st.session_state:
                        del st.session_state.valuation_results
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_valuation_form(self):
        """가치평가 파라미터 입력 폼 렌더링"""
        method = st.session_state.valuation_method
        company_name = self.company_data.get('company_name', '기업')
        
        st.markdown(f"## {company_name} 가치평가 - {method_options[method]}")

        # 메소드별 필요한 파라미터 폼 렌더링
        if method == "dcf":
            self._render_dcf_form()
        elif method == "multiples":
            self._render_multiples_form()
        elif method == "asset":
            self._render_asset_based_form()
        elif method == "combined":
            self._render_combined_form()
        
        # 가치평가 시작 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("가치평가 계산 시작", type="primary", use_container_width=True):
                with st.spinner("가치평가 계산 중..."):
                    valuation_results = self._run_valuation_calculation()
                    st.session_state.valuation_results = valuation_results
                    st.rerun()
    
    def _render_dcf_form(self):
        """DCF 가치평가 파라미터 입력 폼"""
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">예측 기간 설정</div>', unsafe_allow_html=True)
        
        # 예측 기간 설정
        forecast_period = st.slider("예측 기간 (년)", min_value=3, max_value=10, value=5, 
                                   help="미래 현금흐름을 예측할 기간을 선택하세요")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 할인율 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">할인율 (WACC) 설정</div>', unsafe_allow_html=True)
        
        # 간단한 WACC 계산기 제공
        col1, col2 = st.columns(2)
        with col1:
            risk_free_rate = st.number_input("무위험수익률 (%)", value=2.5, min_value=0.0, max_value=10.0, step=0.1,
                                          help="국고채 수익률 등 안전 자산의 수익률")
            market_risk_premium = st.number_input("시장위험프리미엄 (%)", value=5.5, min_value=0.0, max_value=20.0, step=0.1,
                                               help="시장수익률과 무위험수익률의 차이")
            debt_ratio = 0
            if self.balance_sheet_data is not None:
                try:
                    latest_assets = self.balance_sheet_data["총자산"].iloc[-1]
                    latest_debt = self.balance_sheet_data["총부채"].iloc[-1]
                    if latest_assets > 0:
                        debt_ratio = (latest_debt / latest_assets) * 100
                except (KeyError, IndexError):
                    debt_ratio = 30  # 기본값
            else:
                debt_ratio = 30
            
            debt_weight = st.slider("부채 비중 (%)", min_value=0, max_value=100, value=int(debt_ratio),
                                help="기업의 총자본 중 부채가 차지하는 비중")
            
        with col2:
            beta = st.number_input("베타 (β)", value=1.1, min_value=0.0, max_value=3.0, step=0.05,
                               help="기업의 시장 변동성 대비 주가 변동성")
            cost_of_debt = st.number_input("부채비용 (%)", value=4.0, min_value=0.0, max_value=20.0, step=0.1,
                                       help="기업이 부담하는 차입금리")
            tax_rate = st.number_input("법인세율 (%)", value=22.0, min_value=0.0, max_value=40.0, step=0.5,
                                   help="적용되는 법인세율")
        
        # WACC 계산
        equity_weight = 100 - debt_weight
        cost_of_equity = risk_free_rate + beta * market_risk_premium
        wacc = (cost_of_equity * equity_weight / 100) + (cost_of_debt * (1 - tax_rate / 100) * debt_weight / 100)
        
        st.markdown(f'<div class="info-box">계산된 WACC (가중평균자본비용): <b>{wacc:.2f}%</b></div>', unsafe_allow_html=True)
        
        # 고급 사용자를 위한 직접 입력 옵션
        use_calculated_wacc = st.checkbox("계산된 WACC 사용", value=True)
        if not use_calculated_wacc:
            wacc = st.number_input("직접 입력 WACC (%)", value=wacc, min_value=0.0, max_value=30.0, step=0.1)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 성장률 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">성장률 설정</div>', unsafe_allow_html=True)
        
        # 과거 데이터 기반 성장률 계산
        historic_growth_rate = self._calculate_historical_growth_rate()
        
        st.markdown(f'<div class="info-box">과거 3년 평균 성장률: <b>{historic_growth_rate:.2f}%</b></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            growth_years = st.slider("성장 예측 기간 (년)", min_value=1, max_value=forecast_period, value=min(3, forecast_period),
                                  help="고성장이 지속될 것으로 예상되는 기간")
            initial_growth_rate = st.number_input("초기 성장률 (%)", value=max(-10.0, min(historic_growth_rate, 15.0)), 
                                               min_value=-20.0, max_value=50.0, step=0.5,
                                               help="첫 해 예상 성장률")
        
        with col2:
            terminal_growth_rate = st.number_input("영구 성장률 (%)", value=min(2.0, max(0.0, historic_growth_rate / 3)), 
                                                min_value=0.0, max_value=5.0, step=0.1,
                                                help="장기적으로 지속 가능한 성장률")
            growth_decay = st.checkbox("성장률 점진적 감소", value=True, 
                                    help="초기 성장률에서 영구 성장률로 점진적으로 감소")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 현금흐름 조정 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">현금흐름 조정</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # 최근 3년 현금흐름 표시
            if self.cash_flow_data is not None:
                try:
                    recent_fcfs = []
                    for year in range(3):
                        if year < len(self.cash_flow_data):
                            recent_fcfs.append(self.cash_flow_data['FCF'].iloc[-(year+1)])
                    
                    years_str = ", ".join([str(datetime.now().year - i - 1) for i in range(len(recent_fcfs))][::-1])
                    fcf_str = ", ".join([f"{fcf}억원" for fcf in recent_fcfs[::-1]])
                    st.markdown(f'<div class="info-box">최근 FCF ({years_str}): <b>{fcf_str}</b></div>', unsafe_allow_html=True)
                except (KeyError, IndexError, AttributeError):
                    st.markdown('<div class="info-box">최근 FCF 데이터를 가져올 수 없습니다.</div>', unsafe_allow_html=True)
            
            # FCF 계산 방식 선택
            fcf_calc_method = st.radio("FCF 기준값 계산 방식", 
                                     ["최근 연도 FCF 사용", "최근 3년 평균 FCF 사용", "영업이익 기반 FCF 추정"],
                                     horizontal=True)
            
            # FCF 기준값 계산
            base_fcf = self._calculate_base_fcf(fcf_calc_method)
            
            # FCF 기준값 조정
            fcf_adjustment = st.slider(f"FCF 기준값 조정 (기본: {base_fcf}억원)", 
                                     min_value=-50, max_value=50, value=0, step=5,
                                     help="기준 FCF에 대한 추가적인 조정 비율 (%)")
            
            adjusted_base_fcf = base_fcf * (1 + fcf_adjustment / 100)
            st.markdown(f'<div class="info-box">조정된 FCF 기준값: <b>{adjusted_base_fcf:.2f}억원</b></div>', unsafe_allow_html=True)
        
        with col2:
            # 감가상각비 및 자본적 지출
            capex_percent = st.slider("자본적 지출 (매출액 대비 %)", 
                                   min_value=0, max_value=30, value=5, step=1,
                                   help="매출액 대비 시설투자 비율")
            
            working_capital_percent = st.slider("운전자본 증가 (매출 증가액 대비 %)", 
                                            min_value=0, max_value=40, value=10, step=1,
                                            help="매출 증가액 대비 운전자본 증가 비율")
            
            # 부채 증가 비율
            debt_increase_percent = st.slider("부채 증가 (자본적 지출 대비 %)", 
                                          min_value=0, max_value=100, value=20, step=5,
                                          help="자본적 지출 대비 부채 증가 비율")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 민감도 분석 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">민감도 분석 설정</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            sensitivity_wacc = st.checkbox("WACC 민감도 분석", value=True)
            wacc_min = st.number_input("WACC 최소값 (%)", value=max(wacc-3, 0.0), min_value=0.0, max_value=wacc, step=0.5)
            wacc_max = st.number_input("WACC 최대값 (%)", value=min(wacc+3, 30.0), min_value=wacc, max_value=30.0, step=0.5)
        
        with col2:
            sensitivity_growth = st.checkbox("성장률 민감도 분석", value=True)
            growth_min = st.number_input("성장률 최소값 (%)", value=max(terminal_growth_rate-2, 0.0), min_value=-10.0, max_value=terminal_growth_rate, step=0.5)
            growth_max = st.number_input("성장률 최대값 (%)", value=min(terminal_growth_rate+2, 10.0), min_value=terminal_growth_rate, max_value=10.0, step=0.5)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 폼 제출을 위한 파라미터 저장
        st.session_state.valuation_params = {
            "method": "dcf",
            "forecast_period": forecast_period,
            "wacc": wacc,
            "initial_growth_rate": initial_growth_rate,
            "terminal_growth_rate": terminal_growth_rate,
            "growth_years": growth_years,
            "growth_decay": growth_decay,
            "base_fcf": adjusted_base_fcf,
            "capex_percent": capex_percent,
            "working_capital_percent": working_capital_percent,
            "debt_increase_percent": debt_increase_percent,
            "sensitivity_wacc": sensitivity_wacc,
            "wacc_min": wacc_min,
            "wacc_max": wacc_max,
            "sensitivity_growth": sensitivity_growth,
            "growth_min": growth_min,
            "growth_max": growth_max
        }
    
    def _render_multiples_form(self):
        """상대가치법 입력 폼"""
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">상대가치 배수 선택</div>', unsafe_allow_html=True)
        
        selected_multiples = []
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.checkbox("PER (주가수익비율)", value=True):
                selected_multiples.append("PER")
            if st.checkbox("PBR (주가장부가치비율)", value=True):
                selected_multiples.append("PBR")
        
        with col2:
            if st.checkbox("PSR (주가매출액비율)", value=False):
                selected_multiples.append("PSR")
            if st.checkbox("EV/EBITDA", value=True):
                selected_multiples.append("EV/EBITDA")
        
        with col3:
            if st.checkbox("EV/Sales", value=False):
                selected_multiples.append("EV/Sales")
            if st.checkbox("P/FCF (주가현금흐름비율)", value=False):
                selected_multiples.append("P/FCF")
        
        if not selected_multiples:
            st.warning("최소한 하나 이상의 가치평가 배수를 선택해주세요.")
            selected_multiples = ["PER"]
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 산업 평균 배수 입력
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">산업 평균 배수 입력</div>', unsafe_allow_html=True)
        
        industry_multiples = {}
        col1, col2 = st.columns(2)
        
        with col1:
            if "PER" in selected_multiples:
                industry_multiples["PER"] = st.number_input("산업 평균 PER", value=12.0, min_value=0.0, max_value=50.0, step=0.5)
            if "PBR" in selected_multiples:
                industry_multiples["PBR"] = st.number_input("산업 평균 PBR", value=1.5, min_value=0.0, max_value=20.0, step=0.1)
            if "PSR" in selected_multiples:
                industry_multiples["PSR"] = st.number_input("산업 평균 PSR", value=1.0, min_value=0.0, max_value=10.0, step=0.1)
        
        with col2:
            if "EV/EBITDA" in selected_multiples:
                industry_multiples["EV/EBITDA"] = st.number_input("산업 평균 EV/EBITDA", value=8.0, min_value=0.0, max_value=25.0, step=0.5)
            if "EV/Sales" in selected_multiples:
                industry_multiples["EV/Sales"] = st.number_input("산업 평균 EV/Sales", value=2.0, min_value=0.0, max_value=15.0, step=0.1)
            if "P/FCF" in selected_multiples:
                industry_multiples["P/FCF"] = st.number_input("산업 평균 P/FCF", value=15.0, min_value=0.0, max_value=50.0, step=0.5)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 적정 할인율 / 할증율 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">적정 할인/할증률 설정</div>', unsafe_allow_html=True)
        
        discount_premium = st.slider("할인/할증률 (%)", min_value=-50, max_value=50, value=0, step=5,
                                  help="산업 평균 대비 회사의 경쟁력, 성장성 등을 고려한 할인/할증률")
        
        rationale = st.text_area("할인/할증 근거", 
                               placeholder="회사의 경쟁력, 시장 점유율, 성장성 등을 고려하여 할인/할증 근거를 입력하세요.",
                               height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 각 가치평가 배수별 가중치 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">가치평가 배수별 가중치 설정</div>', unsafe_allow_html=True)
        
        # 기본 가중치 계산 (동일 비중)
        default_weight = 100 // len(selected_multiples)
        remaining_weight = 100
        multiple_weights = {}
        
        cols = st.columns(len(selected_multiples))
        for i, multiple in enumerate(selected_multiples[:-1]):  # 마지막 항목은 나머지 가중치로 계산
            with cols[i]:
                weight = st.slider(f"{multiple} 가중치 (%)", 
                                 min_value=0, max_value=remaining_weight, 
                                 value=min(default_weight, remaining_weight), 
                                 step=5)
                multiple_weights[multiple] = weight
                remaining_weight -= weight
        
        # 마지막 항목 가중치 설정
        if selected_multiples:
            last_multiple = selected_multiples[-1]
            with cols[-1]:
                st.markdown(f"**{last_multiple} 가중치 (%)**")
                st.markdown(f"<div style='text-align: center; font-size: 1.5rem; font-weight: 600;'>{remaining_weight}%</div>", unsafe_allow_html=True)
                multiple_weights[last_multiple] = remaining_weight
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 폼 제출을 위한 파라미터 저장
        st.session_state.valuation_params = {
            "method": "multiples",
            "selected_multiples": selected_multiples,
            "industry_multiples": industry_multiples,
            "discount_premium": discount_premium,
            "rationale": rationale,
            "multiple_weights": multiple_weights
        }
    
    def _render_asset_based_form(self):
        """자산가치법 입력 폼"""
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">자산가치 조정</div>', unsafe_allow_html=True)
        
        # 최근 자산 가치 표시
        assets_value = 0
        liabilities_value = 0
        if self.balance_sheet_data is not None:
            try:
                assets_value = self.balance_sheet_data['총자산'].iloc[-1]
                liabilities_value = self.balance_sheet_data['총부채'].iloc[-1]
                equity_value = self.balance_sheet_data['자본총계'].iloc[-1]
                
                st.markdown(f"""
                <div class="info-box">
                    최근 재무상태표 기준:<br>
                    <b>총자산:</b> {assets_value}억원<br>
                    <b>총부채:</b> {liabilities_value}억원<br>
                    <b>자본총계:</b> {equity_value}억원
                </div>
                """, unsafe_allow_html=True)
            except (KeyError, IndexError):
                st.markdown('<div class="info-box">재무상태표 데이터를 가져올 수 없습니다.</div>', unsafe_allow_html=True)
        
        # 자산별 가치 조정
        st.markdown("### 자산 가치 조정")
        
        # 토지 및 건물 가치 조정
        col1, col2 = st.columns(2)
        with col1:
            real_estate_percent = st.slider("토지 및 건물 비중 (%)", min_value=0, max_value=70, value=30, step=5,
                                          help="총자산 중 토지 및 건물이 차지하는 비중")
            real_estate_adjustment = st.slider("토지 및 건물 가치 조정 (%)", min_value=-50, max_value=100, value=20, step=5,
                                             help="장부가 대비 실제 시장가치 조정률")
        
        # 설비 및 재고자산 가치 조정
        with col2:
            equipment_percent = st.slider("설비 및 기계장치 비중 (%)", min_value=0, max_value=70, value=20, step=5,
                                       help="총자산 중 설비 및 기계장치가 차지하는 비중")
            equipment_adjustment = st.slider("설비 및 기계장치 가치 조정 (%)", min_value=-80, max_value=50, value=-30, step=5,
                                          help="장부가 대비 실제 시장가치 조정률")
            
        col1, col2 = st.columns(2)
        with col1:
            inventory_percent = st.slider("재고자산 비중 (%)", min_value=0, max_value=50, value=15, step=5,
                                       help="총자산 중 재고자산이 차지하는 비중")
            inventory_adjustment = st.slider("재고자산 가치 조정 (%)", min_value=-50, max_value=30, value=-10, step=5,
                                          help="장부가 대비 실제 시장가치 조정률")
        
        # 무형자산 및 금융자산 가치 조정
        with col2:
            intangible_percent = st.slider("무형자산 비중 (%)", min_value=0, max_value=50, value=10, step=5,
                                        help="총자산 중 무형자산이 차지하는 비중")
            intangible_adjustment = st.slider("무형자산 가치 조정 (%)", min_value=-80, max_value=200, value=50, step=10,
                                           help="장부가 대비 실제 시장가치 조정률")
        
        # 기타 자산 비중 및 조정
        other_percent = 100 - real_estate_percent - equipment_percent - inventory_percent - intangible_percent
        st.markdown(f'<div class="info-box">기타 자산 비중: <b>{other_percent}%</b></div>', unsafe_allow_html=True)
        other_adjustment = st.slider("기타 자산 가치 조정 (%)", min_value=-50, max_value=50, value=0, step=5,
                                  help="장부가 대비 실제 시장가치 조정률")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 부채 가치 조정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">부채 가치 조정</div>', unsafe_allow_html=True)
        
        liability_adjustment = st.slider("부채 가치 조정 (%)", min_value=-20, max_value=30, value=0, step=5,
                                      help="장부가 대비 실제 부채가치 조정률")
        
        # 우발채무 추가
        contingent_liability = st.number_input("우발채무 추가 (억원)", min_value=0, max_value=1000, value=0, step=10,
                                            help="재무제표에 반영되지 않은 우발채무나 잠재적 리스크")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 청산 비용 설정
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">청산 비용 설정</div>', unsafe_allow_html=True)
        
        liquidation_cost_percent = st.slider("청산 비용 (자산 대비 %)", min_value=0, max_value=30, value=10, step=1,
                                          help="자산을 처분할 때 발생하는 비용(중개 수수료, 세금 등)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 폼 제출을 위한 파라미터 저장
        st.session_state.valuation_params = {
            "method": "asset",
            "assets_value": assets_value,
            "liabilities_value": liabilities_value,
            "real_estate_percent": real_estate_percent,
            "real_estate_adjustment": real_estate_adjustment,
            "equipment_percent": equipment_percent,
            "equipment_adjustment": equipment_adjustment,
            "inventory_percent": inventory_percent,
            "inventory_adjustment": inventory_adjustment,
            "intangible_percent": intangible_percent,
            "intangible_adjustment": intangible_adjustment,
            "other_percent": other_percent,
            "other_adjustment": other_adjustment,
            "liability_adjustment": liability_adjustment,
            "contingent_liability": contingent_liability,
            "liquidation_cost_percent": liquidation_cost_percent
        }
    
    def _render_combined_form(self):
        """복합 가치평가법 입력 폼"""
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        st.markdown('<div class="parameter-title">가치평가 방법 선택 및 가중치 설정</div>', unsafe_allow_html=True)
        
        # 사용할 가치평가 방법 선택
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            use_dcf = st.checkbox("DCF 방법 사용", value=True)
        with col2:
            use_multiples = st.checkbox("상대가치법 사용", value=True)
        with col3:
            use_asset = st.checkbox("자산가치법 사용", value=True)
        
        # 가중치 설정 (동적으로 표시)
        selected_methods = []
        if use_dcf:
            selected_methods.append("DCF")
        if use_multiples:
            selected_methods.append("상대가치법")
        if use_asset:
            selected_methods.append("자산가치법")
        
        if not selected_methods:
            st.warning("최소한 하나 이상의 가치평가 방법을 선택해주세요.")
            selected_methods = ["DCF"]
            use_dcf = True
        
        # 기본 가중치 계산 (동일 비중)
        default_weight = 100 // len(selected_methods)
        remaining_weight = 100
        method_weights = {}
        
        st.markdown("### 각 방법별 가중치 설정")
        
        cols = st.columns(len(selected_methods))
        for i, method in enumerate(selected_methods[:-1]):  # 마지막 항목은 나머지 가중치로 계산
            with cols[i]:
                weight = st.slider(f"{method} 가중치 (%)", 
                                 min_value=0, max_value=remaining_weight, 
                                 value=min(default_weight, remaining_weight), 
                                 step=5)
                method_weights[method] = weight
                remaining_weight -= weight
        
        # 마지막 항목 가중치 설정
        if selected_methods:
            last_method = selected_methods[-1]
            with cols[-1]:
                st.markdown(f"**{last_method} 가중치 (%)**")
                st.markdown(f"<div style='text-align: center; font-size: 1.5rem; font-weight: 600;'>{remaining_weight}%</div>", unsafe_allow_html=True)
                method_weights[last_method] = remaining_weight
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 각 방법별 간소화된 파라미터 설정
        if use_dcf:
            st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
            st.markdown('<div class="parameter-title">DCF 방법 기본 파라미터</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                dcf_wacc = st.number_input("할인율 (WACC, %)", value=10.0, min_value=0.0, max_value=30.0, step=0.5)
                dcf_terminal_growth = st.number_input("영구 성장률 (%)", value=2.0, min_value=0.0, max_value=5.0, step=0.1)
            
            with col2:
                # FCF 계산 방식 선택
                fcf_calc_method = st.radio("FCF 기준값 계산 방식", 
                                         ["최근 연도 FCF 사용", "최근 3년 평균 FCF 사용"],
                                         horizontal=True)
                
                # FCF 기준값 계산
                dcf_base_fcf = self._calculate_base_fcf(fcf_calc_method)
                
                # FCF 기준값 조정
                dcf_fcf_adjustment = st.slider(f"FCF 기준값 조정 (기본: {dcf_base_fcf}억원)", 
                                            min_value=-50, max_value=50, value=0, step=5)
                
            dcf_adjusted_base_fcf = dcf_base_fcf * (1 + dcf_fcf_adjustment / 100)
            st.markdown(f'<div class="info-box">조정된 FCF 기준값: <b>{dcf_adjusted_base_fcf:.2f}억원</b></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if use_multiples:
            st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
            st.markdown('<div class="parameter-title">상대가치법 기본 파라미터</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                per_multiple = st.number_input("PER 배수", value=12.0, min_value=0.0, max_value=50.0, step=0.5)
            with col2:
                pbr_multiple = st.number_input("PBR 배수", value=1.5, min_value=0.0, max_value=20.0, step=0.1)
            with col3:
                evebitda_multiple = st.number_input("EV/EBITDA 배수", value=8.0, min_value=0.0, max_value=25.0, step=0.5)
            
            multiples_discount = st.slider("할인/할증률 (%)", min_value=-50, max_value=50, value=0, step=5)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        if use_asset:
            st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
            st.markdown('<div class="parameter-title">자산가치법 기본 파라미터</div>', unsafe_allow_html=True)
            
            assets_value = 0
            liabilities_value = 0
            if self.balance_sheet_data is not None:
                try:
                    assets_value = self.balance_sheet_data['총자산'].iloc[-1]
                    liabilities_value = self.balance_sheet_data['총부채'].iloc[-1]
                except (KeyError, IndexError):
                    pass
            
            col1, col2 = st.columns(2)
            with col1:
                asset_adjustment = st.slider("자산 가치 조정 (%)", min_value=-50, max_value=100, value=10, step=5)
            
            with col2:
                liability_adjustment = st.slider("부채 가치 조정 (%)", min_value=-20, max_value=30, value=0, step=5)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 폼 제출을 위한 파라미터 저장
        combined_params = {
            "method": "combined",
            "selected_methods": selected_methods,
            "method_weights": method_weights
        }
        
        if use_dcf:
            combined_params.update({
                "dcf_wacc": dcf_wacc,
                "dcf_terminal_growth": dcf_terminal_growth,
                "dcf_base_fcf": dcf_adjusted_base_fcf
            })
        
        if use_multiples:
            combined_params.update({
                "per_multiple": per_multiple,
                "pbr_multiple": pbr_multiple,
                "evebitda_multiple": evebitda_multiple,
                "multiples_discount": multiples_discount
            })
        
        if use_asset:
            combined_params.update({
                "assets_value": assets_value,
                "liabilities_value": liabilities_value,
                "asset_adjustment": asset_adjustment,
                "liability_adjustment": liability_adjustment
            })
        
        st.session_state.valuation_params = combined_params
    
    def _calculate_historical_growth_rate(self):
        """과거 데이터를 기반으로 성장률 계산"""
        # 수익 데이터에서 성장률 계산
        if self.performance_data is not None and 'growth_rates' in st.session_state and self.growth_rates is not None:
            try:
                # 매출액 성장률 기반 계산
                growth_rates = []
                
                # 최근 2-3년 매출액 성장률 사용
                if '매출액성장률' in self.growth_rates:
                    growth_values = self.growth_rates['매출액성장률'].values
                    if len(growth_values) > 0:
                        # 마이너스 성장률은 0으로 대체하거나 더 낮은 가중치 부여
                        growth_rates = [max(0, rate) if rate < -15 else rate for rate in growth_values]
                
                # 순이익 성장률도 고려
                if '순이익성장률' in self.growth_rates:
                    net_income_growth = self.growth_rates['순이익성장률'].values
                    if len(net_income_growth) > 0:
                        # 순이익 성장률이 있으면 평균에 포함
                        growth_rates.extend([rate for rate in net_income_growth if rate > -50])  # 극단적인 값 제외
                
                if growth_rates:
                    # 최근 데이터에 더 높은 가중치 부여
                    weighted_avg = sum(growth_rates) / len(growth_rates)
                    return weighted_avg
                
                return 3.0  # 기본값
                
            except (KeyError, IndexError, AttributeError, ValueError):
                pass
        
        # 직접적인 성장률 데이터가 없는 경우 영업이익으로부터 추정
        if self.performance_data is not None:
            try:
                recent_years = min(3, len(self.performance_data))
                if recent_years > 1:
                    operating_profits = self.performance_data['영업이익'].iloc[-recent_years:].values
                    revenues = self.performance_data['매출액'].iloc[-recent_years:].values
                    
                    growth_rates = []
                    for i in range(1, len(operating_profits)):
                        if operating_profits[i-1] > 0:
                            growth_rate = ((operating_profits[i] / operating_profits[i-1]) - 1) * 100
                            growth_rates.append(growth_rate)
                    
                    if growth_rates:
                        weighted_avg = sum(growth_rates) / len(growth_rates)
                        # 극단적인 성장률 제한
                        return max(-10, min(weighted_avg, 20))
            except (KeyError, IndexError, AttributeError, ValueError):
                pass
        
        # 기본값
        return 3.0
    
    def _calculate_base_fcf(self, method):
        """FCF 기준값 계산"""
        if self.cash_flow_data is not None:
            try:
                if method == "최근 연도 FCF 사용":
                    return float(self.cash_flow_data['FCF'].iloc[-1])
                elif method == "최근 3년 평균 FCF 사용":
                    recent_years = min(3, len(self.cash_flow_data))
                    recent_fcfs = self.cash_flow_data['FCF'].iloc[-recent_years:].values
                    # 음수 FCF는 낮은 가중치 부여
                    weighted_fcfs = []
                    for fcf in recent_fcfs:
                        if fcf < 0:
                            weighted_fcfs.append(fcf * 0.5)  # 음수는 절반만 반영
                        else:
                            weighted_fcfs.append(fcf)
                    
                    return sum(weighted_fcfs) / len(weighted_fcfs)
                elif method == "영업이익 기반 FCF 추정":
                    if self.performance_data is not None:
                        latest_op_profit = self.performance_data['영업이익'].iloc[-1]
                        # 영업이익의 70%를 FCF로 추정
                        return latest_op_profit * 0.7
            except (KeyError, IndexError, AttributeError, ValueError):
                pass
        
        # 영업이익 기반 대체 계산
        if self.performance_data is not None:
            try:
                latest_op_profit = self.performance_data['영업이익'].iloc[-1]
                # 영업이익의 70%를 FCF로 추정
                return latest_op_profit * 0.7
            except (KeyError, IndexError, AttributeError):
                pass
            
            try:
                latest_net_income = self.performance_data['순이익'].iloc[-1]
                # 순이익의 80%를 FCF로 추정
                return latest_net_income * 0.8
            except (KeyError, IndexError, AttributeError):
                pass
        
        # 데이터가 없는 경우 기본값 반환
        return 100.0
    
    def _run_valuation_calculation(self):
        """가치평가 계산 실행"""
        params = st.session_state.valuation_params
        method = params.get("method")
        
        if method == "dcf":
            return self._calculate_dcf_valuation(params)
        elif method == "multiples":
            return self._calculate_multiples_valuation(params)
        elif method == "asset":
            return self._calculate_asset_based_valuation(params)
        elif method == "combined":
            return self._calculate_combined_valuation(params)
        else:
            return {"error": "지원되지 않는 가치평가 방법입니다."}
    
    def _calculate_dcf_valuation(self, params):
        """DCF 가치평가 계산"""
        forecast_period = params.get("forecast_period", 5)
        wacc = params.get("wacc", 10.0) / 100
        initial_growth_rate = params.get("initial_growth_rate", 3.0) / 100
        terminal_growth_rate = params.get("terminal_growth_rate", 2.0) / 100
        growth_years = params.get("growth_years", 3)
        growth_decay = params.get("growth_decay", True)
        base_fcf = params.get("base_fcf", 100.0)
        
        # 부채 정보 조회
        net_debt = 0
        if self.balance_sheet_data is not None:
            try:
                latest_debt = self.balance_sheet_data['총부채'].iloc[-1]
                net_debt = latest_debt
            except (KeyError, IndexError):
                net_debt = 0
        
        # 미래 FCF 예측
        fcfs = []
        
        # 성장률 패턴 계산
        growth_rates = []
        
        if growth_decay:
            # 점진적 감소 시나리오
            for year in range(forecast_period):
                if year < growth_years:
                    # 초기 성장 기간: 점진적으로 감소
                    decay_factor = (growth_years - year) / growth_years
                    year_growth = initial_growth_rate * decay_factor + terminal_growth_rate * (1 - decay_factor)
                else:
                    # 이후: 영구 성장률
                    year_growth = terminal_growth_rate
                growth_rates.append(year_growth)
        else:
            # 단순 패턴: 초기 성장률 → 영구 성장률
            for year in range(forecast_period):
                if year < growth_years:
                    growth_rates.append(initial_growth_rate)
                else:
                    growth_rates.append(terminal_growth_rate)
        
        # FCF 예측
        current_fcf = base_fcf
        for i, growth_rate in enumerate(growth_rates):
            fcfs.append(current_fcf)
            current_fcf *= (1 + growth_rate)
        
        # 현재가치 계산
        present_values = []
        for i, fcf in enumerate(fcfs):
            present_values.append(fcf / ((1 + wacc) ** (i + 1)))
        
        # 잔존가치 계산
        terminal_value = fcfs[-1] * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)
        present_terminal_value = terminal_value / ((1 + wacc) ** forecast_period)
        
        # 기업가치 계산
        enterprise_value = sum(present_values) + present_terminal_value
        equity_value = enterprise_value - net_debt
        
        # 민감도 분석
        sensitivity_results = {}
        if params.get("sensitivity_wacc", False):
            wacc_min = params.get("wacc_min", 7.0) / 100
            wacc_max = params.get("wacc_max", 13.0) / 100
            wacc_step = (wacc_max - wacc_min) / 4
            
            wacc_sensitivity = {}
            for test_wacc in np.arange(wacc_min, wacc_max + wacc_step, wacc_step):
                test_pvs = [fcf / ((1 + test_wacc) ** (i + 1)) for i, fcf in enumerate(fcfs)]
                test_ptv = (fcfs[-1] * (1 + terminal_growth_rate) / (test_wacc - terminal_growth_rate)) / ((1 + test_wacc) ** forecast_period)
                test_ev = sum(test_pvs) + test_ptv
                test_equity = test_ev - net_debt
                wacc_sensitivity[f"{test_wacc*100:.1f}%"] = round(test_equity, 1)
            
            sensitivity_results["wacc_sensitivity"] = wacc_sensitivity
        
        if params.get("sensitivity_growth", False):
            growth_min = params.get("growth_min", 0.0) / 100
            growth_max = params.get("growth_max", 4.0) / 100
            growth_step = (growth_max - growth_min) / 4
            
            growth_sensitivity = {}
            for test_growth in np.arange(growth_min, growth_max + growth_step, growth_step):
                test_ptv = (fcfs[-1] * (1 + test_growth) / (wacc - test_growth)) / ((1 + wacc) ** forecast_period)
                test_ev = sum(present_values) + test_ptv
                test_equity = test_ev - net_debt
                growth_sensitivity[f"{test_growth*100:.1f}%"] = round(test_equity, 1)
            
            sensitivity_results["growth_sensitivity"] = growth_sensitivity
        
        # 결과 반환
        return {
            "method": "DCF",
            "enterprise_value": round(enterprise_value, 1),
            "equity_value": round(equity_value, 1),
            "details": {
                "forecast_period": forecast_period,
                "wacc": wacc * 100,
                "initial_growth_rate": initial_growth_rate * 100,
                "terminal_growth_rate": terminal_growth_rate * 100,
                "base_fcf": base_fcf,
                "net_debt": net_debt,
                "fcfs": [round(fcf, 1) for fcf in fcfs],
                "growth_rates": [round(gr * 100, 1) for gr in growth_rates],
                "present_values": [round(pv, 1) for pv in present_values],
                "terminal_value": round(terminal_value, 1),
                "present_terminal_value": round(present_terminal_value, 1),
                "terminal_value_percent": round((present_terminal_value / enterprise_value) * 100, 1)
            },
            "sensitivity": sensitivity_results
        }
    
    def _calculate_multiples_valuation(self, params):
        """상대가치법 가치평가 계산"""
        selected_multiples = params.get("selected_multiples", ["PER"])
        industry_multiples = params.get("industry_multiples", {})
        discount_premium = params.get("discount_premium", 0) / 100
        multiple_weights = params.get("multiple_weights", {})
        
        # 각 배수별 가치평가 계산
        valuations = {}
        
        # 필요한 재무 데이터 추출
        net_income = 0
        equity = 0
        revenue = 0
        operating_profit = 0
        ebitda = 0
        fcf = 0
        
        # 당기순이익
        if self.performance_data is not None:
            try:
                net_income = self.performance_data['순이익'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # 자기자본
        if self.balance_sheet_data is not None:
            try:
                equity = self.balance_sheet_data['자본총계'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # 매출액
        if self.performance_data is not None:
            try:
                revenue = self.performance_data['매출액'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # 영업이익
        if self.performance_data is not None:
            try:
                operating_profit = self.performance_data['영업이익'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # EBITDA 추정 (영업이익의 1.25배로 가정)
        ebitda = operating_profit * 1.25
        
        # FCF
        if self.cash_flow_data is not None:
            try:
                fcf = self.cash_flow_data['FCF'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # 부채
        debt = 0
        if self.balance_sheet_data is not None:
            try:
                debt = self.balance_sheet_data['총부채'].iloc[-1]
            except (KeyError, IndexError):
                pass
        
        # PER 가치평가
        if "PER" in selected_multiples:
            per = industry_multiples.get("PER", 12.0)
            per_adjusted = per * (1 + discount_premium)
            per_valuation = net_income * per_adjusted
            valuations["PER"] = {
                "multiple": per,
                "adjusted_multiple": per_adjusted,
                "base_value": net_income,
                "valuation": per_valuation
            }
        
        # PBR 가치평가
        if "PBR" in selected_multiples:
            pbr = industry_multiples.get("PBR", 1.5)
            pbr_adjusted = pbr * (1 + discount_premium)
            pbr_valuation = equity * pbr_adjusted
            valuations["PBR"] = {
                "multiple": pbr,
                "adjusted_multiple": pbr_adjusted,
                "base_value": equity,
                "valuation": pbr_valuation
            }
        
        # PSR 가치평가
        if "PSR" in selected_multiples:
            psr = industry_multiples.get("PSR", 1.0)
            psr_adjusted = psr * (1 + discount_premium)
            psr_valuation = revenue * psr_adjusted
            valuations["PSR"] = {
                "multiple": psr,
                "adjusted_multiple": psr_adjusted,
                "base_value": revenue,
                "valuation": psr_valuation
            }
        
        # EV/EBITDA 가치평가
        if "EV/EBITDA" in selected_multiples:
            ev_ebitda = industry_multiples.get("EV/EBITDA", 8.0)
            ev_ebitda_adjusted = ev_ebitda * (1 + discount_premium)
            ev_valuation = ebitda * ev_ebitda_adjusted
            equity_valuation = ev_valuation - debt
            valuations["EV/EBITDA"] = {
                "multiple": ev_ebitda,
                "adjusted_multiple": ev_ebitda_adjusted,
                "base_value": ebitda,
                "ev_valuation": ev_valuation,
                "valuation": equity_valuation
            }
        
        # EV/Sales 가치평가
        if "EV/Sales" in selected_multiples:
            ev_sales = industry_multiples.get("EV/Sales", 2.0)
            ev_sales_adjusted = ev_sales * (1 + discount_premium)
            ev_valuation = revenue * ev_sales_adjusted
            equity_valuation = ev_valuation - debt
            valuations["EV/Sales"] = {
                "multiple": ev_sales,
                "adjusted_multiple": ev_sales_adjusted,
                "base_value": revenue,
                "ev_valuation": ev_valuation,
                "valuation": equity_valuation
            }
        
        # P/FCF 가치평가
        if "P/FCF" in selected_multiples:
            p_fcf = industry_multiples.get("P/FCF", 15.0)
            p_fcf_adjusted = p_fcf * (1 + discount_premium)
            # FCF가 음수인 경우 조정 (최근 3년 평균 사용)
            fcf_base = fcf
            if fcf_base <= 0 and self.cash_flow_data is not None:
                try:
                    recent_years = min(3, len(self.cash_flow_data))
                    fcf_values = self.cash_flow_data['FCF'].iloc[-recent_years:].values
                    positive_fcfs = [f for f in fcf_values if f > 0]
                    if positive_fcfs:
                        fcf_base = sum(positive_fcfs) / len(positive_fcfs)
                    else:
                        fcf_base = operating_profit * 0.7  # 영업이익 기반 추정
                except (KeyError, IndexError):
                    fcf_base = operating_profit * 0.7
            
            p_fcf_valuation = fcf_base * p_fcf_adjusted
            valuations["P/FCF"] = {
                "multiple": p_fcf,
                "adjusted_multiple": p_fcf_adjusted,
                "base_value": fcf_base,
                "valuation": p_fcf_valuation
            }
        
        # 가중 평균 가치 계산
        weighted_value = 0
        total_weight = 0
        
        for multiple, weight in multiple_weights.items():
            if multiple in valuations:
                weighted_value += valuations[multiple]["valuation"] * weight / 100
                total_weight += weight
        
        # 가중치 합이 0이면 단순 평균
        if total_weight == 0:
            values = [v["valuation"] for k, v in valuations.items()]
            if values:
                weighted_value = sum(values) / len(values)
        
        # 결과 반환
        return {
            "method": "상대가치법",
            "weighted_value": round(weighted_value, 1),
            "valuations": {k: {**v, "valuation": round(v["valuation"], 1)} for k, v in valuations.items()},
            "weights": multiple_weights,
            "discount_premium": discount_premium * 100,
            "financial_data": {
                "net_income": net_income,
                "equity": equity,
                "revenue": revenue,
                "operating_profit": operating_profit,
                "ebitda": ebitda,
                "fcf": fcf,
                "debt": debt
            }
        }
    
    def _calculate_asset_based_valuation(self, params):
        """자산가치법 가치평가 계산"""
        assets_value = params.get("assets_value", 0)
        liabilities_value = params.get("liabilities_value", 0)
        
        real_estate_percent = params.get("real_estate_percent", 30) / 100
        real_estate_adjustment = params.get("real_estate_adjustment", 20) / 100
        
        equipment_percent = params.get("equipment_percent", 20) / 100
        equipment_adjustment = params.get("equipment_adjustment", -30) / 100
        
        inventory_percent = params.get("inventory_percent", 15) / 100
        inventory_adjustment = params.get("inventory_adjustment", -10) / 100
        
        intangible_percent = params.get("intangible_percent", 10) / 100
        intangible_adjustment = params.get("intangible_adjustment", 50) / 100
        
        other_percent = params.get("other_percent", 25) / 100
        other_adjustment = params.get("other_adjustment", 0) / 100
        
        liability_adjustment = params.get("liability_adjustment", 0) / 100
        contingent_liability = params.get("contingent_liability", 0)
        
        liquidation_cost_percent = params.get("liquidation_cost_percent", 10) / 100
        
        # 자산 가치 조정
        real_estate_value = assets_value * real_estate_percent
        real_estate_adjusted = real_estate_value * (1 + real_estate_adjustment)
        
        equipment_value = assets_value * equipment_percent
        equipment_adjusted = equipment_value * (1 + equipment_adjustment)
        
        inventory_value = assets_value * inventory_percent
        inventory_adjusted = inventory_value * (1 + inventory_adjustment)
        
        intangible_value = assets_value * intangible_percent
        intangible_adjusted = intangible_value * (1 + intangible_adjustment)
        
        other_value = assets_value * other_percent
        other_adjusted = other_value * (1 + other_adjustment)
        
        # 조정된 자산 가치 합계
        adjusted_assets = real_estate_adjusted + equipment_adjusted + inventory_adjusted + intangible_adjusted + other_adjusted
        
        # 부채 가치 조정
        adjusted_liabilities = liabilities_value * (1 + liability_adjustment) + contingent_liability
        
        # 청산 비용 계산
        liquidation_cost = adjusted_assets * liquidation_cost_percent
        
        # 순자산 가치 계산
        net_asset_value = adjusted_assets - adjusted_liabilities - liquidation_cost
        
        # 결과 반환
        return {
            "method": "자산가치법",
            "book_value": {
                "assets": assets_value,
                "liabilities": liabilities_value,
                "equity": assets_value - liabilities_value
            },
            "adjusted_assets": {
                "real_estate": {
                    "original": round(real_estate_value, 1),
                    "adjusted": round(real_estate_adjusted, 1),
                    "adjustment_percent": real_estate_adjustment * 100
                },
                "equipment": {
                    "original": round(equipment_value, 1),
                    "adjusted": round(equipment_adjusted, 1),
                    "adjustment_percent": equipment_adjustment * 100
                },
                "inventory": {
                    "original": round(inventory_value, 1),
                    "adjusted": round(inventory_adjusted, 1),
                    "adjustment_percent": inventory_adjustment * 100
                },
                "intangible": {
                    "original": round(intangible_value, 1),
                    "adjusted": round(intangible_adjusted, 1),
                    "adjustment_percent": intangible_adjustment * 100
                },
                "other": {
                    "original": round(other_value, 1),
                    "adjusted": round(other_adjusted, 1),
                    "adjustment_percent": other_adjustment * 100
                },
                "total": {
                    "original": round(assets_value, 1),
                    "adjusted": round(adjusted_assets, 1)
                }
            },
            "adjusted_liabilities": {
                "original": round(liabilities_value, 1),
                "adjusted": round(adjusted_liabilities, 1),
                "contingent_liability": contingent_liability
            },
            "liquidation_cost": round(liquidation_cost, 1),
            "net_asset_value": round(net_asset_value, 1)
        }
    
    def _calculate_combined_valuation(self, params):
        """복합 가치평가법 계산"""
        selected_methods = params.get("selected_methods", ["DCF"])
        method_weights = params.get("method_weights", {"DCF": 100})
        
        valuations = {}
        
        # DCF 가치평가
        if "DCF" in selected_methods:
            dcf_params = {
                "method": "dcf",
                "forecast_period": 5,
                "wacc": params.get("dcf_wacc", 10.0),
                "initial_growth_rate": 5.0,
                "terminal_growth_rate": params.get("dcf_terminal_growth", 2.0),
                "growth_years": 3,
                "growth_decay": True,
                "base_fcf": params.get("dcf_base_fcf", 100.0)
            }
            
            dcf_results = self._calculate_dcf_valuation(dcf_params)
            valuations["DCF"] = dcf_results["equity_value"]
        
        # 상대가치법 계산
        if "상대가치법" in selected_methods:
            # PER, PBR, EV/EBITDA 배수 적용한 간소화된 상대가치 계산
            net_income = 0
            equity = 0
            ebitda = 0
            debt = 0
            
            # 당기순이익
            if self.performance_data is not None:
                try:
                    net_income = self.performance_data['순이익'].iloc[-1]
                except (KeyError, IndexError):
                    pass
            
            # 자기자본
            if self.balance_sheet_data is not None:
                try:
                    equity = self.balance_sheet_data['자본총계'].iloc[-1]
                except (KeyError, IndexError):
                    pass
            
            # 영업이익
            if self.performance_data is not None:
                try:
                    operating_profit = self.performance_data['영업이익'].iloc[-1]
                    # EBITDA 추정 (영업이익의 1.25배로 가정)
                    ebitda = operating_profit * 1.25
                except (KeyError, IndexError):
                    pass
            
            # 부채
            if self.balance_sheet_data is not None:
                try:
                    debt = self.balance_sheet_data['총부채'].iloc[-1]
                except (KeyError, IndexError):
                    pass
            
            # 배수 값 가져오기
            per_multiple = params.get("per_multiple", 12.0)
            pbr_multiple = params.get("pbr_multiple", 1.5)
            evebitda_multiple = params.get("evebitda_multiple", 8.0)
            
            # 할인/할증률 적용
            discount_premium = params.get("multiples_discount", 0) / 100
            
            # 각 배수별 가치 계산
            per_valuation = net_income * per_multiple * (1 + discount_premium)
            pbr_valuation = equity * pbr_multiple * (1 + discount_premium)
            ev_valuation = ebitda * evebitda_multiple * (1 + discount_premium)
            evebitda_valuation = ev_valuation - debt
            
            # 세 가지 방법의 평균값을 상대가치법 결과로 사용
            multiples_valuation = (per_valuation + pbr_valuation + evebitda_valuation) / 3
            valuations["상대가치법"] = multiples_valuation
        
        # 자산가치법 계산
        if "자산가치법" in selected_methods:
            assets_value = params.get("assets_value", 0)
            liabilities_value = params.get("liabilities_value", 0)
            asset_adjustment = params.get("asset_adjustment", 10) / 100
            liability_adjustment = params.get("liability_adjustment", 0) / 100
            
            # 간소화된 자산가치 계산
            adjusted_assets = assets_value * (1 + asset_adjustment)
            adjusted_liabilities = liabilities_value * (1 + liability_adjustment)
            
            asset_based_valuation = adjusted_assets - adjusted_liabilities
            valuations["자산가치법"] = asset_based_valuation
        
        # 가중 평균 가치 계산
        weighted_value = 0
        for method, value in valuations.items():
            weight = method_weights.get(method, 0)
            weighted_value += value * weight / 100
        
        # 결과 반환
        return {
            "method": "복합 가치평가법",
            "weighted_value": round(weighted_value, 1),
            "valuations": {k: round(v, 1) for k, v in valuations.items()},
            "weights": method_weights
        }
    
    def _render_valuation_results(self):
        """가치평가 결과 표시"""
        company_name = self.company_data.get('company_name', '기업')
        valuation_results = st.session_state.valuation_results
        
        method = valuation_results.get("method", "알 수 없음")
        
        # 결과 헤더 표시
        st.markdown(f"## {company_name} 가치평가 결과 - {method}")
        
        # 결과 요약 표시
        self._render_valuation_summary(valuation_results)
        
        # 세부 결과 표시
        if method == "DCF":
            self._render_dcf_results(valuation_results)
        elif method == "상대가치법":
            self._render_multiples_results(valuation_results)
        elif method == "자산가치법":
            self._render_asset_based_results(valuation_results)
        elif method == "복합 가치평가법":
            self._render_combined_results(valuation_results)
        
        # 다시 계산하기 버튼
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("가치평가 다시하기", key="recalculate_btn", use_container_width=True):
                if "valuation_results" in st.session_state:
                    del st.session_state.valuation_results
                st.rerun()
    
    def _render_valuation_summary(self, results):
        """가치평가 결과 요약 표시"""
        method = results.get("method", "알 수 없음")
        
        # 방법별 결과값 추출
        if method == "DCF":
            enterprise_value = results.get("enterprise_value", 0)
            equity_value = results.get("equity_value", 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<div class="result-title">기업가치 (Enterprise Value)</div>', unsafe_allow_html=True)
                
                # 트릴리온 단위 처리 (1조 이상)
                if enterprise_value >= 10000:
                    ev_display = f"{enterprise_value/10000:.2f}조원"
                else:
                    ev_display = f"{enterprise_value}억원"
                
                st.markdown(f'<div style="font-size: 2rem; font-weight: 700; text-align: center; color: #3b82f6;">{ev_display}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<div class="result-title">주주가치 (Equity Value)</div>', unsafe_allow_html=True)
                
                # 트릴리온 단위 처리 (1조 이상)
                if equity_value >= 10000:
                    eq_display = f"{equity_value/10000:.2f}조원"
                else:
                    eq_display = f"{equity_value}억원"
                
                st.markdown(f'<div style="font-size: 2rem; font-weight: 700; text-align: center; color: #10b981;">{eq_display}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
        elif method == "상대가치법":
            weighted_value = results.get("weighted_value", 0)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">가중평균 주주가치 (Weighted Equity Value)</div>', unsafe_allow_html=True)
            
            # 트릴리온 단위 처리 (1조 이상)
            if weighted_value >= 10000:
                wv_display = f"{weighted_value/10000:.2f}조원"
            else:
                wv_display = f"{weighted_value}억원"
            
            st.markdown(f'<div style="font-size: 2rem; font-weight: 700; text-align: center; color: #8b5cf6;">{wv_display}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif method == "자산가치법":
            net_asset_value = results.get("net_asset_value", 0)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">조정순자산가치 (Adjusted Net Asset Value)</div>', unsafe_allow_html=True)
            
            # 트릴리온 단위 처리 (1조 이상)
            if net_asset_value >= 10000:
                nav_display = f"{net_asset_value/10000:.2f}조원"
            else:
                nav_display = f"{net_asset_value}억원"
            
            st.markdown(f'<div style="font-size: 2rem; font-weight: 700; text-align: center; color: #f59e0b;">{nav_display}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        elif method == "복합 가치평가법":
            weighted_value = results.get("weighted_value", 0)
            
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">종합 기업가치 (Combined Value)</div>', unsafe_allow_html=True)
            
            # 트릴리온 단위 처리 (1조 이상)
            if weighted_value >= 10000:
                wv_display = f"{weighted_value/10000:.2f}조원"
            else:
                wv_display = f"{weighted_value}억원"
            
            st.markdown(f'<div style="font-size: 2rem; font-weight: 700; text-align: center; color: #6366f1;">{wv_display}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_dcf_results(self, results):
        """DCF 가치평가 결과 상세 표시"""
        details = results.get("details", {})
        sensitivity = results.get("sensitivity", {})
        
        # DCF 상세 결과 표시
        st.markdown("### DCF 분석 세부 결과")
        
        # DCF 가정 표시
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">주요 가정</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            assumptions = [
                ("예측 기간", f"{details.get('forecast_period', 5)}년"),
                ("할인율 (WACC)", f"{details.get('wacc', 10.0):.1f}%"),
                ("초기 성장률", f"{details.get('initial_growth_rate', 3.0):.1f}%"),
                ("영구 성장률", f"{details.get('terminal_growth_rate', 2.0):.1f}%")
            ]
            
            for label, value in assumptions:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            assumptions2 = [
                ("FCF 기준값", f"{details.get('base_fcf', 0):.1f}억원"),
                ("순부채", f"{details.get('net_debt', 0):.1f}억원"),
                ("터미널 가치 비중", f"{details.get('terminal_value_percent', 0):.1f}%"),
                ("종합 위험 평가", "중간" if details.get('wacc', 10) > 8 else "낮음")
            ]
            
            for label, value in assumptions2:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # FCF 예측 데이터 표시
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">미래 현금흐름 예측</div>', unsafe_allow_html=True)
        
        fcfs = details.get("fcfs", [])
        growth_rates = details.get("growth_rates", [])
        present_values = details.get("present_values", [])
        forecast_period = details.get("forecast_period", 5)
        terminal_value = details.get("terminal_value", 0)
        present_terminal_value = details.get("present_terminal_value", 0)
        
        # 현재 연도 계산
        current_year = datetime.now().year
        forecast_years = [current_year + i for i in range(1, forecast_period + 1)]
        
        # 데이터프레임 생성
        df_forecast = pd.DataFrame({
            "연도": forecast_years,
            "FCF 예측치 (억원)": fcfs,
            "성장률 (%)": growth_rates,
            "현재가치 (억원)": present_values
        })
        
        # 터미널 가치 행 추가
        terminal_row = pd.DataFrame({
            "연도": ["영구가치"],
            "FCF 예측치 (억원)": [terminal_value],
            "성장률 (%)": [details.get("terminal_growth_rate", 2.0)],
            "현재가치 (억원)": [present_terminal_value]
        })
        
        df_forecast = pd.concat([df_forecast, terminal_row], ignore_index=True)
        
        # 데이터프레임 표시
        st.dataframe(df_forecast, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # FCF 및 현재가치 차트
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">미래 현금흐름 및 현재가치 추이</div>', unsafe_allow_html=True)
        
        # FCF와 현재가치를 함께 표시하는 차트
        fig = go.Figure()
        
        # FCF 예측치 표시
        fig.add_trace(go.Bar(
            x=[str(year) for year in forecast_years],
            y=fcfs,
            name="FCF 예측치",
            marker_color="#3b82f6"
        ))
        
        # 현재가치 표시
        fig.add_trace(go.Bar(
            x=[str(year) for year in forecast_years],
            y=present_values,
            name="현재가치",
            marker_color="#10b981"
        ))
        
        # 터미널 가치 표시 (마지막 항목)
        fig.add_trace(go.Bar(
            x=["영구가치"],
            y=[present_terminal_value],
            name="영구가치의 현재가치",
            marker_color="#f59e0b"
        ))
        
        # 차트 레이아웃 설정
        fig.update_layout(
            barmode='group',
            xaxis_title="연도",
            yaxis_title="금액 (억원)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 민감도 분석 표시
        if sensitivity:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-title">민감도 분석</div>', unsafe_allow_html=True)
            
            # 민감도 분석 탭
            tabs = []
            if "wacc_sensitivity" in sensitivity:
                tabs.append("할인율(WACC) 민감도")
            if "growth_sensitivity" in sensitivity:
                tabs.append("영구성장률 민감도")
            
            if tabs:
                sensitivity_tabs = st.tabs(tabs)
                
                tab_index = 0
                if "wacc_sensitivity" in sensitivity and tab_index < len(sensitivity_tabs):
                    with sensitivity_tabs[tab_index]:
                        wacc_sensitivity = sensitivity["wacc_sensitivity"]
                        
                        # 데이터프레임으로 변환
                        wacc_values = list(wacc_sensitivity.keys())
                        equity_values = list(wacc_sensitivity.values())
                        
                        # 막대 차트로 표시
                        fig = go.Figure(data=[
                            go.Bar(
                                x=wacc_values,
                                y=equity_values,
                                marker_color="#3b82f6",
                                text=equity_values,
                                textposition="auto"
                            )
                        ])
                        
                        fig.update_layout(
                            title="할인율(WACC) 변화에 따른 주주가치 변화",
                            xaxis_title="할인율 (WACC)",
                            yaxis_title="주주가치 (억원)"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    tab_index += 1
                
                if "growth_sensitivity" in sensitivity and tab_index < len(sensitivity_tabs):
                    with sensitivity_tabs[tab_index]:
                        growth_sensitivity = sensitivity["growth_sensitivity"]
                        
                        # 데이터프레임으로 변환
                        growth_values = list(growth_sensitivity.keys())
                        equity_values = list(growth_sensitivity.values())
                        
                        # 막대 차트로 표시
                        fig = go.Figure(data=[
                            go.Bar(
                                x=growth_values,
                                y=equity_values,
                                marker_color="#10b981",
                                text=equity_values,
                                textposition="auto"
                            )
                        ])
                        
                        fig.update_layout(
                            title="영구성장률 변화에 따른 주주가치 변화",
                            xaxis_title="영구성장률",
                            yaxis_title="주주가치 (억원)"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_multiples_results(self, results):
        """상대가치법 결과 상세 표시"""
        valuations = results.get("valuations", {})
        weights = results.get("weights", {})
        discount_premium = results.get("discount_premium", 0)
        financial_data = results.get("financial_data", {})
        
        # 각 배수별 가치평가 결과 표시
        st.markdown("### 상대가치법 분석 세부 결과")
        
        # 기본 재무 정보 표시
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">주요 재무 지표</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            financials1 = [
                ("당기순이익", f"{financial_data.get('net_income', 0):.1f}억원"),
                ("자기자본", f"{financial_data.get('equity', 0):.1f}억원"),
                ("매출액", f"{financial_data.get('revenue', 0):.1f}억원")
            ]
            
            for label, value in financials1:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            financials2 = [
                ("영업이익", f"{financial_data.get('operating_profit', 0):.1f}억원"),
                ("EBITDA", f"{financial_data.get('ebitda', 0):.1f}억원"),
                ("FCF", f"{financial_data.get('fcf', 0):.1f}억원")
            ]
            
            for label, value in financials2:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 각 배수별 가치평가 결과 테이블
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">배수별 가치평가 결과</div>', unsafe_allow_html=True)
        
        # 배수별 가치평가 표시
        multiple_data = []
        for multiple, value_info in valuations.items():
            if multiple in ["EV/EBITDA", "EV/Sales"]:
                multiple_data.append({
                    "배수": multiple,
                    "산업 평균 배수": f"{value_info.get('multiple', 0):.1f}x",
                    "적용 배수": f"{value_info.get('adjusted_multiple', 0):.1f}x",
                    "기준값": f"{value_info.get('base_value', 0):.1f}억원",
                    "기업가치(EV)": f"{value_info.get('ev_valuation', 0):.1f}억원",
                    "주주가치(EQ)": f"{value_info.get('valuation', 0):.1f}억원",
                    "가중치": f"{weights.get(multiple, 0)}%"
                })
            else:
                multiple_data.append({
                    "배수": multiple,
                    "산업 평균 배수": f"{value_info.get('multiple', 0):.1f}x",
                    "적용 배수": f"{value_info.get('adjusted_multiple', 0):.1f}x",
                    "기준값": f"{value_info.get('base_value', 0):.1f}억원",
                    "기업가치(EV)": "-",
                    "주주가치(EQ)": f"{value_info.get('valuation', 0):.1f}억원",
                    "가중치": f"{weights.get(multiple, 0)}%"
                })
        
        if multiple_data:
            df_multiples = pd.DataFrame(multiple_data)
            st.dataframe(df_multiples, use_container_width=True)
        
        # 할인/할증 정보
        st.markdown(f"""
        <div style="margin-top: 15px; padding: 10px; background-color: #f8fafc; border-radius: 8px;">
            <div style="font-size: 0.9rem; color: #475569; font-weight: 500;">
                적용된 할인/할증률: {discount_premium:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 배수별 가치평가 결과 시각화
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">배수별 가치평가 결과 비교</div>', unsafe_allow_html=True)
        
        # 배수별 가치 데이터
        multiples = []
        values = []
        for multiple, value_info in valuations.items():
            multiples.append(multiple)
            values.append(value_info.get("valuation", 0))
        
        # 가중평균값 추가
        multiples.append("가중평균")
        values.append(results.get("weighted_value", 0))
        
        # 막대 차트로 표시
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#ec4899", "#6366f1"]
        fig = go.Figure(data=[
            go.Bar(
                x=multiples,
                y=values,
                marker_color=[colors[i % len(colors)] for i in range(len(multiples))],
                text=[f"{value:.1f}억원" for value in values],
                textposition="auto"
            )
        ])
        
        fig.update_layout(
            xaxis_title="평가 방법",
            yaxis_title="주주가치 (억원)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_asset_based_results(self, results):
        """자산가치법 결과 상세 표시"""
        book_value = results.get("book_value", {})
        adjusted_assets = results.get("adjusted_assets", {})
        adjusted_liabilities = results.get("adjusted_liabilities", {})
        liquidation_cost = results.get("liquidation_cost", 0)
        net_asset_value = results.get("net_asset_value", 0)
        
        # 자산가치법 상세 결과 표시
        st.markdown("### 자산가치법 분석 세부 결과")
        
        # 장부가치 vs 조정가치 비교
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">장부가치 vs 조정가치</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="result-subtitle">장부가치</div>', unsafe_allow_html=True)
            
            book_items = [
                ("총자산", f"{book_value.get('assets', 0):.1f}억원"),
                ("총부채", f"{book_value.get('liabilities', 0):.1f}억원"),
                ("자기자본", f"{book_value.get('equity', 0):.1f}억원")
            ]
            
            for label, value in book_items:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="result-subtitle">조정가치</div>', unsafe_allow_html=True)
            
            adjusted_items = [
                ("조정 자산", f"{adjusted_assets.get('total', {}).get('adjusted', 0):.1f}억원"),
                ("조정 부채", f"{adjusted_liabilities.get('adjusted', 0):.1f}억원"),
                ("청산 비용", f"{liquidation_cost:.1f}억원")
            ]
            
            for label, value in adjusted_items:
                st.markdown(f"""
                <div class="result-metric">
                    <span class="metric-label">{label}</span>
                    <span class="metric-value">{value}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 자산 항목별 조정 내역
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">자산 항목별 조정 내역</div>', unsafe_allow_html=True)
        
        # 자산 항목별 조정 테이블 데이터
        asset_items = [
            {
                "항목": "토지 및 건물",
                "원래 가치": f"{adjusted_assets.get('real_estate', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{adjusted_assets.get('real_estate', {}).get('adjustment_percent', 0):.1f}%",
                "조정 가치": f"{adjusted_assets.get('real_estate', {}).get('adjusted', 0):.1f}억원"
            },
            {
                "항목": "설비 및 기계장치",
                "원래 가치": f"{adjusted_assets.get('equipment', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{adjusted_assets.get('equipment', {}).get('adjustment_percent', 0):.1f}%",
                "조정 가치": f"{adjusted_assets.get('equipment', {}).get('adjusted', 0):.1f}억원"
            },
            {
                "항목": "재고자산",
                "원래 가치": f"{adjusted_assets.get('inventory', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{adjusted_assets.get('inventory', {}).get('adjustment_percent', 0):.1f}%",
                "조정 가치": f"{adjusted_assets.get('inventory', {}).get('adjusted', 0):.1f}억원"
            },
            {
                "항목": "무형자산",
                "원래 가치": f"{adjusted_assets.get('intangible', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{adjusted_assets.get('intangible', {}).get('adjustment_percent', 0):.1f}%",
                "조정 가치": f"{adjusted_assets.get('intangible', {}).get('adjusted', 0):.1f}억원"
            },
            {
                "항목": "기타 자산",
                "원래 가치": f"{adjusted_assets.get('other', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{adjusted_assets.get('other', {}).get('adjustment_percent', 0):.1f}%",
                "조정 가치": f"{adjusted_assets.get('other', {}).get('adjusted', 0):.1f}억원"
            },
            {
                "항목": "자산 합계",
                "원래 가치": f"{adjusted_assets.get('total', {}).get('original', 0):.1f}억원",
                "조정 비율": f"{(adjusted_assets.get('total', {}).get('adjusted', 0) / adjusted_assets.get('total', {}).get('original', 1) - 1) * 100:.1f}%",
                "조정 가치": f"{adjusted_assets.get('total', {}).get('adjusted', 0):.1f}억원"
            }
        ]
        
        # 데이터프레임으로 변환하여 표시
        df_assets = pd.DataFrame(asset_items)
        st.dataframe(df_assets, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 순자산가치 계산 결과
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">순자산가치 계산 결과</div>', unsafe_allow_html=True)
        
        # 순자산가치 계산 과정 표시
        calculation_items = [
            ("총자산 (조정 후)", f"{adjusted_assets.get('total', {}).get('adjusted', 0):.1f}억원"),
            ("총부채 (조정 후)", f"{adjusted_liabilities.get('adjusted', 0):.1f}억원"),
            ("우발부채", f"{adjusted_liabilities.get('contingent_liability', 0):.1f}억원"),
            ("청산 비용", f"{liquidation_cost:.1f}억원"),
            ("순자산 가치", f"{net_asset_value:.1f}억원")
        ]
        
        for label, value in calculation_items:
            st.markdown(f"""
            <div class="result-metric">
                <span class="metric-label">{label}</span>
                <span class="metric-value">{value}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # 자산가치법 결과 시각화
        fig = go.Figure()
        
        # 장부가치 vs 조정가치 막대 차트
        fig.add_trace(go.Bar(
            x=["장부가치", "조정가치"],
            y=[book_value.get('equity', 0), net_asset_value],
            marker_color=["#3b82f6", "#f59e0b"],
            text=[f"{book_value.get('equity', 0):.1f}억원", f"{net_asset_value:.1f}억원"],
            textposition="auto"
        ))
        
        fig.update_layout(
            title="장부가치 vs 조정 순자산가치 비교",
            xaxis_title="가치 유형",
            yaxis_title="가치 (억원)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_combined_results(self, results):
        """복합 가치평가법 결과 상세 표시"""
        valuations = results.get("valuations", {})
        weights = results.get("weights", {})
        weighted_value = results.get("weighted_value", 0)
        
        # 복합 가치평가법 상세 결과 표시
        st.markdown("### 복합 가치평가법 분석 세부 결과")
        
        # 각 방법별 가치평가 결과
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">각 방법별 가치평가 결과</div>', unsafe_allow_html=True)
        
        # 방법별 가치평가 표시
        method_data = []
        for method, value in valuations.items():
            method_data.append({
                "평가 방법": method,
                "가치평가 결과": f"{value:.1f}억원",
                "가중치": f"{weights.get(method, 0)}%",
                "가중 가치": f"{value * weights.get(method, 0) / 100:.1f}억원"
            })
        
        # 가중평균 행 추가
        method_data.append({
            "평가 방법": "최종 가중평균",
            "가치평가 결과": f"{weighted_value:.1f}억원",
            "가중치": "100%",
            "가중 가치": f"{weighted_value:.1f}억원"
        })
        
        # 데이터프레임으로 변환하여 표시
        df_methods = pd.DataFrame(method_data)
        st.dataframe(df_methods, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 방법별 가치평가 결과 시각화
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">방법별 가치평가 결과 비교</div>', unsafe_allow_html=True)
        
        # 막대 차트로 표시
        methods = list(valuations.keys()) + ["가중평균"]
        values = list(valuations.values()) + [weighted_value]
        
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#6366f1"]
        fig = go.Figure(data=[
            go.Bar(
                x=methods,
                y=values,
                marker_color=[colors[i % len(colors)] for i in range(len(methods))],
                text=[f"{value:.1f}억원" for value in values],
                textposition="auto"
            )
        ])
        
        fig.update_layout(
            xaxis_title="평가 방법",
            yaxis_title="가치 (억원)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 가중치 파이 차트 표시
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">각 방법별 가중치 비율</div>', unsafe_allow_html=True)
        
        # 파이 차트로 표시
        fig = go.Figure(data=[
            go.Pie(
                labels=list(weights.keys()),
                values=list(weights.values()),
                marker_colors=colors[:len(weights)],
                textinfo="label+percent",
                insidetextorientation="radial"
            )
        ])
        
        fig.update_layout(
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


# 가치평가 방법 옵션 매핑
method_options = {
    "dcf": "DCF (Discounted Cash Flow)",
    "multiples": "상대가치법 (Multiples)",
    "asset": "자산가치법 (Asset-based)",
    "combined": "복합 가치평가법"
}