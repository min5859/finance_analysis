import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE
import json
from valuation.llm_valuation import ValuationAnalyzer
from valuation.display_valuation import display_valuation_results

class ValuationSlide(BaseSlide):
    """LLM 기반 기업 가치 평가 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "AI-Powered Company Valuation")
        self.company_data = data_loader.get_all_data()
        self.valuation_analyzer = ValuationAnalyzer()
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        
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
        .valuation-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            margin-bottom: 20px;
        }
        
        .valuation-info {
            background-color: #f0f7ff;
            border-left: 4px solid #3b82f6;
            padding: 12px 15px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        
        .method-card {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        
        .method-header {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #f0f0f0;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        
        .method-name {
            font-weight: 600;
            color: #333;
        }
        
        .method-value {
            font-weight: 600;
            color: #4b6cb7;
        }
        
        .method-details {
            font-size: 0.9rem;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_valuation_request_form(self):
        """가치 평가 요청 폼 렌더링"""
        st.info("AI를 활용한 기업 가치 평가를 시작하려면 아래 버튼을 클릭하세요.")
        st.caption("이 분석은 재무 데이터를 기반으로 EBITDA 방식과 DCF 방식의 기업 가치를 계산합니다.")
        
        # 가치 평가 시작 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("AI 기업 가치 평가 시작", type="primary", use_container_width=True):
                with st.spinner("AI가 기업 가치를 평가 중입니다. 잠시만 기다려주세요..."):
                    # 가치 평가 실행
                    valuation_results = self._run_valuation_analysis()
                    
                    # 세션 상태에 결과 저장
                    if valuation_results["status"] == "success":
                        st.session_state["valuation_data"] = valuation_results["valuation_data"]
                        st.success("기업 가치 평가가 완료되었습니다!")
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
        
        # 세션에서 가치 평가 결과 가져오기
        valuation_data = st.session_state.get("valuation_data", {})
        
        if valuation_data:
            # 가치 평가 결과 표시
            display_valuation_results(valuation_data)
            
            # 결과 다운로드 버튼
            company_name = valuation_data.get("company", "company")
            st.download_button(
                label="가치 평가 결과 다운로드 (JSON)",
                data=json.dumps(valuation_data, indent=2, ensure_ascii=False),
                file_name=f"{company_name}_valuation.json",
                mime="application/json"
            )
            
            # 다시 평가하기 버튼
            if st.button("가치 평가 다시하기"):
                if "valuation_data" in st.session_state:
                    del st.session_state["valuation_data"]
                st.rerun()
        else:
            st.error("가치 평가 결과가 없습니다. 다시 시도해주세요.")
            if st.button("가치 평가 다시하기"):
                if "valuation_data" in st.session_state:
                    del st.session_state["valuation_data"]
                st.rerun()