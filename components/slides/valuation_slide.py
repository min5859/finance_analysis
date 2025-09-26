import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE
import json
from valuation.llm_valuation import ValuationAnalyzer
import time

class ValuationSlide(BaseSlide):
    """LLM 기반 기업 가치 평가 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "AI-Powered Company Valuation")
        self.company_data = data_loader.get_all_data()
        self.valuation_analyzer = ValuationAnalyzer()
    
    def render_content(self):
        """슬라이드 콘텐츠 렌더링"""
        # CSS 스타일 추가
        self._add_custom_styles()
        
        # 세션 상태에 가치 평가 결과가 있는지 확인
        if "valuation_data" not in st.session_state:
            # 가치 평가 시작 버튼
            self._render_valuation_request_form()
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
        
        .request-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 24px auto;
            background: #f0f9ff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            color: #3b82f6;
        }
        
        .request-title {
            font-size: 22px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 12px;
            font-family: 'Pretendard', sans-serif;
        }
        
        .request-description {
            font-size: 16px;
            line-height: 1.6;
            color: #64748b;
            margin-bottom: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            font-family: 'Pretendard', sans-serif;
        }
        
        .request-features {
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .feature-item {
            background: #f8fafc;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            width: 200px;
        }
        
        .feature-icon {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            color: white;
            font-size: 20px;
        }
        
        .feature-icon.blue {
            background: linear-gradient(135deg, #3b82f6, #60a5fa);
        }
        
        .feature-icon.purple {
            background: linear-gradient(135deg, #8b5cf6, #a78bfa);
        }
        
        .feature-icon.green {
            background: linear-gradient(135deg, #10b981, #34d399);
        }
        
        .feature-text {
            font-size: 14px;
            font-weight: 600;
            color: #334155;
            text-align: left;
            font-family: 'Pretendard', sans-serif;
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
        
        /* 결과 다운로드 버튼 스타일 */
        .download-container {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            margin: 20px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid #e5e7eb;
        }
        
        .download-text {
            font-size: 14px;
            color: #475569;
            font-family: 'Pretendard', sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_valuation_request_form(self):
        """가치 평가 요청 폼 렌더링 - 고급 디자인"""
        company_name = self.company_data.get('company_name', '기업')
        
        # 고급 컨테이너 시작
        st.markdown(f"""
        <div class="request-container">
            <div class="request-features">
                <div class="feature-item">
                    <div class="feature-icon blue">💼</div>
                    <div class="feature-text">시나리오별<br>가치 평가</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon purple">📊</div>
                    <div class="feature-text">다양한<br>평가 방법론</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon green">📝</div>
                    <div class="feature-text">상세한<br>분석 보고서</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 가치 평가 시작 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("AI 기업 가치 평가 시작", type="primary", use_container_width=True, key="start_valuation_btn"):
                with st.spinner("AI가 기업 가치를 평가 중입니다. 잠시만 기다려주세요..."):
                    
                    # 가치 평가 실행
                    valuation_results = self._run_valuation_analysis()
                    
                    # 세션 상태에 결과 저장
                    if valuation_results["status"] == "success":
                        st.session_state["valuation_data"] = valuation_results["valuation_data"]
                        st.success("기업 가치 평가가 완료되었습니다!")
                        time.sleep(2)
                        st.rerun()  # 페이지 새로고침
                    else:
                        st.error(f"분석 오류: {valuation_results.get('message', '알 수 없는 오류')}")
    
    def _run_valuation_analysis(self):
        """기업 가치 평가 분석 실행"""
        # API 키 확인
        api_key = st.secrets.get("anthropic_api_key", None) if hasattr(st, "secrets") else None
        if not api_key:
            return {
                "status": "error",
                "message": "API 키가 설정되지 않았습니다. 설정 메뉴에서 API 키를 입력해주세요."
            }
        
        # 임시 테스트용 코드 - JSON 파일 사용
        # 실제 호출 시에는 이 부분을 주석 처리하고 아래 부분을 사용
        try:
            # 응답 파싱
            json_data = json.load(open("valuation/sample_valuation.json"))
            return {
                "status": "success",
                "valuation_data": json_data
            }
        except:
            pass  # 파일이 없으면 계속 진행
        
        # 기업 정보 및 재무 데이터 준비
        company_info = {
            "corp_name": self.company_data.get('company_name', '알 수 없음'),
            "sector": self.company_data.get('sector', '알 수 없음')
        }
        
        # 재무 데이터 가져오기
        performance_data = self.data_loader.get_performance_data()
        balance_sheet_data = self.data_loader.get_balance_sheet_data()
        profitability_data = self.data_loader.get_profitability_data()
        cash_flow_data = self.data_loader.get_cash_flow_data()
        growth_rates = self.data_loader.get_growth_rates()
        
        # LLM 입력용 재무 데이터 포맷 변환
        financial_data = {
            "years": performance_data['year'].tolist() if 'year' in performance_data else [],
            "assets": balance_sheet_data['총자산'].tolist() if '총자산' in balance_sheet_data else [],
            "liabilities": balance_sheet_data['총부채'].tolist() if '총부채' in balance_sheet_data else [],
            "equity": balance_sheet_data['자본총계'].tolist() if '자본총계' in balance_sheet_data else [],
            "revenue": performance_data['매출액'].tolist() if '매출액' in performance_data else [],
            "operating_profit": performance_data['영업이익'].tolist() if '영업이익' in performance_data else [],
            "net_income": performance_data['순이익'].tolist() if '순이익' in performance_data else [],
            "fcf": cash_flow_data['FCF'].tolist() if 'FCF' in cash_flow_data else [],
            "roe": profitability_data['ROE'].tolist() if 'ROE' in profitability_data else [],
            "growth_rate": growth_rates.get('매출액성장률', []) if '매출액성장률' in growth_rates else []
        }
        
        # 업종 정보
        industry_info = {
            "sector": company_info["sector"],
            "avg_per": "15.0",  # 일반적인 PER 값 (실제로는 업종별로 다름)
            "avg_pbr": "1.8"    # 일반적인 PBR 값 (실제로는 업종별로 다름)
        }
        
        # 가치 평가 실행
        return self.valuation_analyzer.analyze_company_value(
            company_info, 
            financial_data, 
            industry_info,
            api_key
        )
    
    def _render_valuation_results(self):
        """가치 평가 결과 렌더링"""
        from valuation.display_valuation import display_valuation_results
        
        # 세션에서 가치 평가 결과 가져오기
        valuation_data = st.session_state.get("valuation_data", {})
        
        if valuation_data:
            # 가치 평가 결과 표시
            display_valuation_results(valuation_data)
            
            # 결과 다운로드 버튼 - 고급 UI로 표시
            company_name = valuation_data.get("company", "company")
            
            st.markdown("""
            <div class="download-container">
                <div class="download-text">
                    <strong>가치 평가 데이터 다운로드</strong><br>
                    JSON 형식으로 평가 결과를 저장하고 외부 도구에서 활용하세요.
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col2:
                download_button = st.download_button(
                    label="JSON 다운로드",
                    data=json.dumps(valuation_data, indent=2, ensure_ascii=False),
                    file_name=f"{company_name}_valuation.json",
                    mime="application/json",
                    key="download_valuation_btn",
                    use_container_width=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 다시 평가하기 버튼
            col1, col2, col3 = st.columns([3, 2, 3])
            with col2:
                if st.button("가치 평가 다시하기", key="restart_valuation_btn", use_container_width=True):
                    if "valuation_data" in st.session_state:
                        del st.session_state["valuation_data"]
                    st.rerun()
        else:
            st.error("가치 평가 결과가 없습니다. 다시 시도해주세요.")
            if st.button("가치 평가 다시하기", key="retry_valuation_btn"):
                if "valuation_data" in st.session_state:
                    del st.session_state["valuation_data"]
                st.rerun()