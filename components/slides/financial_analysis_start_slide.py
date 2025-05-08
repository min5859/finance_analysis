import streamlit as st
import json
import os
import datetime
from dart.dart_api_service import DartApiService
from data.financial_statement_processor import FinancialStatementProcessor

class FinancialAnalysisStartSlide:
    def __init__(self, api_key):
        self.api_key = api_key
        self.dart_api = DartApiService()
    
    def render(self):
        st.header("기업 재무제표 조회")
        self._render_search_section()
    
    def _render_search_section(self):
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_keyword = st.text_input("기업명 검색:", value="삼성전자")
        
        with search_col2:
            search_button = st.button("검색", use_container_width=True)
        
        if search_button or search_keyword:
            self._handle_search(search_keyword)
    
    def _handle_search(self, search_keyword):
        # 세션 상태에서 캐시된 기업 목록 확인
        if 'corp_codes_cache' not in st.session_state:
            with st.spinner("기업 목록을 조회 중입니다..."):
                corp_codes = self.dart_api.get_corp_codes()
                if corp_codes:
                    st.session_state.corp_codes_cache = corp_codes
                else:
                    st.error("기업 목록을 가져오지 못했습니다. API 키를 확인하세요.")
                    return
        else:
            corp_codes = st.session_state.corp_codes_cache
        
        # 검색어로 필터링
        filtered_corps = [corp for corp in corp_codes if search_keyword.lower() in corp['corp_name'].lower()]
        
        if not filtered_corps:
            st.warning(f"'{search_keyword}'에 대한 검색 결과가 없습니다.")
            return
        
        self._render_corp_selection(filtered_corps)
    
    def _render_corp_selection(self, filtered_corps):
        corp_names = [f"{corp['corp_name']} ({corp['stock_code']})" for corp in filtered_corps]
        selected_idx = st.selectbox("조회할 기업을 선택하세요:", range(len(corp_names)), format_func=lambda i: corp_names[i])
        selected_corp = filtered_corps[selected_idx]
        
        st.session_state.corp_code = selected_corp['corp_code']
        st.info(f"선택된 기업: {selected_corp['corp_name']} (종목코드: {selected_corp['stock_code']})")
        
        self._render_year_selection(selected_corp)
    
    def _render_year_selection(self, selected_corp):
        current_year = datetime.datetime.now().year
        selected_year = st.selectbox(
            "조회 연도:",
            list(range(current_year-10, current_year)),
            index=list(range(current_year-10, current_year)).index(current_year-1)
        )
        
        if st.button("재무제표 조회"):
            self._handle_financial_statement_request(selected_corp, selected_year)
    
    def _handle_financial_statement_request(self, selected_corp, selected_year):
        with st.spinner(f"{selected_year}년 재무제표를 조회 중입니다..."):
            financial_data = self.dart_api.get_financial_statements(
                selected_corp['corp_code'], 
                str(selected_year)
            )
        
        if not financial_data or 'list' not in financial_data or len(financial_data['list']) == 0:
            st.warning(f"{selected_year}년 재무제표 데이터가 없습니다.")
            return
        
        # 세션 상태에 기업 정보 및 DART 재무 데이터 저장
        st.session_state.corp_code = selected_corp['corp_code']
        st.session_state.selected_year = selected_year
        st.session_state.company_name = selected_corp['corp_name']
        st.session_state.stock_code = selected_corp['stock_code']
        st.session_state.dart_financial_data = financial_data # DART 원본 데이터
        
        # 기존 company_data 구조는 LLM 분석 결과 저장용으로 유지하거나, 필요시 DART 조회 정보도 포함 가능
        st.session_state['company_data'] = {
            'company_name': selected_corp['corp_name'],
            'stock_code': selected_corp['stock_code']
        }
        st.success("재무제표 데이터가 로드되었습니다.")
        
        # 재무 분석 시작 버튼
        if st.button("재무 분석 시작"):
            self._start_financial_analysis(selected_corp, selected_year, st.session_state.dart_financial_data)
    
    def _start_financial_analysis(self, selected_corp, selected_year, financial_data):
        with st.spinner("재무제표 분석 중..."):
            processor = FinancialStatementProcessor(api_key=self.api_key)
            
            analysis_data = self._prepare_analysis_data(selected_corp, selected_year, financial_data)
            json_result = processor.process_with_claude(json.dumps(analysis_data))
            
            self._process_analysis_result(selected_corp, selected_year, json_result, processor)
    
    def _prepare_analysis_data(self, selected_corp, selected_year, financial_data):
        return {
            'company_name': selected_corp['corp_name'],
            'stock_code': selected_corp['stock_code'],
            'year': selected_year,
            'financial_statements': {
                'balance_sheet': [item for item in financial_data['list'] if item.get('sj_div') == 'BS'],
                'income_statement': [item for item in financial_data['list'] if item.get('sj_div') in ['IS', 'CIS']],
                'cash_flow': [item for item in financial_data['list'] if item.get('sj_div') == 'CF']
            }
        }
    
    def _process_analysis_result(self, selected_corp, selected_year, json_result, processor):
        try:
            parsed_json = processor.parse_json_response(json_result)
            parsed_json.update({
                'company_name': selected_corp['corp_name'],
                'stock_code': selected_corp['stock_code'],
                'year': selected_year
            })
            
            st.session_state['company_data'] = parsed_json
            self._save_analysis_result(selected_corp, parsed_json)
            
        except json.JSONDecodeError as e:
            st.error(f"JSON 파싱 오류: {str(e)}")
        except Exception as e:
            st.error(f"분석 처리 오류: {str(e)}")
    
    def _save_analysis_result(self, selected_corp, parsed_json):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/companies")
        os.makedirs(data_dir, exist_ok=True)
        
        json_file = os.path.join(data_dir, f"{selected_corp['corp_name']}_{timestamp}.json")
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        
        st.success(f"재무제표 분석이 완료되었습니다. {selected_corp['corp_name']}의 데이터가 저장되었습니다.")
        
        json_str = json.dumps(parsed_json, ensure_ascii=False, indent=2)
        st.download_button(
            label="JSON 파일 다운로드",
            data=json_str,
            file_name=f"{selected_corp['corp_name']}_{timestamp}.json",
            mime="application/json"
        )
