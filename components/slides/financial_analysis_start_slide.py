import streamlit as st
import json
import os
import datetime
from dart.dart_api_service import DartApiService
from data.financial_statement_processor import FinancialStatementProcessor
from dart.dart_data_processor import DartDataProcessor

class FinancialAnalysisStartSlide:
    def __init__(self, api_key):
        self.api_key = api_key
        self.dart_api = DartApiService()
        self.data_processor = DartDataProcessor()
    
    def render(self):
        st.header("기업 재무제표 조회")
        self._render_search_section()
        if 'dart_financial_data' in st.session_state and st.session_state.dart_financial_data:
            is_analyzed = 'financial_statements' in st.session_state.get('company_data', {}) and \
                          isinstance(st.session_state.company_data['financial_statements'], dict)

            if not is_analyzed:
                self._render_dart_analysis_button_if_needed()
            elif st.session_state.get('company_data',{}).get('company_name') == st.session_state.get('company_name'):
                st.success(f"{st.session_state.get('company_name')}의 DART 데이터 기반 분석이 완료되었습니다.")

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
        
        st.session_state.current_selected_corp_for_dart = selected_corp
        
        self._render_year_selection(selected_corp)
    
    def _render_year_selection(self, selected_corp):
        current_year = datetime.datetime.now().year
        selected_year_for_dart_key = f"dart_year_select_{selected_corp['corp_code']}"
        default_dart_year_index = list(range(current_year-10, current_year)).index(current_year-1)

        selected_year = st.selectbox(
            "조회 연도:",
            list(range(current_year-10, current_year)),
            index=default_dart_year_index,
            key=selected_year_for_dart_key
        )
        
        if st.button("재무제표 조회", key=f"fetch_dart_data_{selected_corp['corp_code']}_{selected_year}"):
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
        
    def _invoke_claude_and_parse(self, data_for_claude):
        processor = FinancialStatementProcessor(api_key=self.api_key)
        try:
            json_result = processor.process_with_claude(data_for_claude)
            parsed_json = processor.parse_json_response(json_result)
            return parsed_json
        except json.JSONDecodeError as e:
            st.error(f"JSON 파싱 오류: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Claude API 처리 오류: {str(e)}")
            return None

    def _finalize_and_save_analysis(self, parsed_json_data, company_name_for_file_and_state, stock_code_for_state=None, year_for_state=None):
        if not parsed_json_data:
            st.error("분석 데이터가 없습니다.")
            return

        final_data = parsed_json_data.copy()
        final_data['company_name'] = company_name_for_file_and_state
        if stock_code_for_state:
            final_data['stock_code'] = stock_code_for_state
        if year_for_state:
            final_data['year'] = str(year_for_state)

        st.session_state['company_data'] = final_data

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/companies")
        os.makedirs(data_dir, exist_ok=True)
        
        clean_company_name = company_name_for_file_and_state.replace("/", "_").replace("\\", "_")
        file_name_base = f"{clean_company_name}_{timestamp}"
        json_file_path = os.path.join(data_dir, f"{file_name_base}.json")
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        st.success(f"재무제표 분석이 완료되었습니다. '{company_name_for_file_and_state}'의 데이터가 '{file_name_base}.json'으로 저장되었습니다.")
        
        json_str = json.dumps(final_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="JSON 파일 다운로드",
            data=json_str,
            file_name=f"{file_name_base}.json",
            mime="application/json",
            key=f"download_{file_name_base}"
        )

    def _render_dart_analysis_button_if_needed(self):
        if 'dart_financial_data' in st.session_state and st.session_state.dart_financial_data and \
           ('financial_statements' not in st.session_state.get('company_data', {})):

            corp_name = st.session_state.get('company_name')
            stock_code = st.session_state.get('stock_code')
            selected_year = st.session_state.get('selected_year')
            dart_data = st.session_state.dart_financial_data

            processed_data = self.data_processor.extract_financial_data(dart_data)
            processed_data = {
                'company_name': corp_name,
                'report_year': str(selected_year),
                **processed_data
            }

            if corp_name and selected_year and dart_data:
                if st.button("재무 분석 시작 (DART 데이터)", key="start_dart_analysis_button"):
                    with st.spinner("DART 데이터 기반 재무 분석 중..."):
                        parsed_json = self._invoke_claude_and_parse(processed_data)
                        if parsed_json:
                            self._finalize_and_save_analysis(parsed_json, corp_name, stock_code, selected_year)