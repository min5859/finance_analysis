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
        
        # 검색 섹션
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            # 세션 상태에서 검색어 가져오기
            default_search = st.session_state.get('dart_search_keyword', '')
            search_keyword = st.text_input("기업명 검색:", value=default_search)
            # 검색어가 변경되면 세션 상태 업데이트
            if search_keyword != default_search:
                st.session_state.dart_search_keyword = search_keyword
        
        with search_col2:
            search_button = st.button("검색", use_container_width=True)
        
        if search_button or search_keyword:
            self._handle_search(search_keyword)
        
        # 분석 결과 표시
        if 'dart_financial_data' in st.session_state and st.session_state.dart_financial_data:
            is_analyzed = 'financial_statements' in st.session_state.get('company_data', {}) and \
                          isinstance(st.session_state.company_data['financial_statements'], dict)

            if not is_analyzed:
                self._render_analysis_button()
            elif st.session_state.get('company_data',{}).get('company_name') == st.session_state.get('company_name'):
                st.success(f"{st.session_state.get('company_name')}의 DART 데이터 기반 분석이 완료되었습니다.")

    def _handle_search(self, search_keyword):
        # 기업 목록 조회
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
        
        # 기업 선택 및 연도 선택 UI
        corp_names = [f"{corp['corp_name']} ({corp['stock_code']})" for corp in filtered_corps]
        
        # 세션 상태에서 이전 선택 인덱스 가져오기
        default_idx = st.session_state.get('dart_selected_corp_idx', 0)
        if default_idx >= len(corp_names):
            default_idx = 0
            
        selected_idx = st.selectbox(
            "조회할 기업을 선택하세요:", 
            range(len(corp_names)), 
            index=default_idx,
            format_func=lambda i: corp_names[i]
        )
        # 선택된 인덱스 저장
        st.session_state.dart_selected_corp_idx = selected_idx
        
        selected_corp = filtered_corps[selected_idx]
        
        current_year = datetime.datetime.now().year
        # 세션 상태에서 이전 선택 연도 가져오기
        default_year_idx = st.session_state.get('dart_selected_year_idx', 
            list(range(current_year-10, current_year)).index(current_year-1))
        
        selected_year = st.selectbox(
            "조회 연도:",
            list(range(current_year-10, current_year)),
            index=default_year_idx
        )
        # 선택된 연도 인덱스 저장
        st.session_state.dart_selected_year_idx = list(range(current_year-10, current_year)).index(selected_year)
        
        if st.button("재무제표 조회"):
            self._fetch_financial_data(selected_corp, selected_year)

    def _fetch_financial_data(self, selected_corp, selected_year):
        with st.spinner(f"{selected_year}년 재무제표를 조회 중입니다..."):
            financial_data = self.dart_api.get_financial_statements(
                selected_corp['corp_code'], 
                str(selected_year)
            )
        
        if not financial_data or 'list' not in financial_data or len(financial_data['list']) == 0:
            st.warning(f"{selected_year}년 재무제표 데이터가 없습니다.")
            return
        
        # 세션 상태에 데이터 저장
        st.session_state.corp_code = selected_corp['corp_code']
        st.session_state.selected_year = selected_year
        st.session_state.company_name = selected_corp['corp_name']
        st.session_state.stock_code = selected_corp['stock_code']
        st.session_state.dart_financial_data = financial_data
        st.success("재무제표 데이터가 로드되었습니다.")

    def _render_analysis_button(self):
        if 'dart_financial_data' in st.session_state and st.session_state.dart_financial_data:
            corp_name = st.session_state.get('company_name')
            selected_year = st.session_state.get('selected_year')
            dart_data = st.session_state.dart_financial_data

            # 토큰 최적화를 위해 핵심 재무 데이터만 추출
            optimized_data = self.data_processor.extract_optimized_financial_data(dart_data)
            
            # 기본 정보 추가
            optimized_data = {
                'company_name': corp_name,
                'report_year': str(selected_year),
                'sector': self._get_company_sector(),
                **optimized_data
            }

            if st.button("재무 분석 시작 (DART 데이터)"):
                with st.spinner("DART 데이터 기반 재무 분석 중..."):
                    processor = FinancialStatementProcessor(api_key=self.api_key)
                    try:
                        json_result = processor.process_with_claude(optimized_data)
                        parsed_json = processor.parse_json_response(json_result)
                        
                        if parsed_json:
                            self._save_analysis_results(parsed_json, corp_name, selected_year)
                    except Exception as e:
                        st.error(f"분석 중 오류가 발생했습니다: {str(e)}")

    def _get_company_sector(self):
        """회사의 업종 정보 가져오기"""
        corp_code = st.session_state.get('corp_code', '')
        if not corp_code:
            return "기타"
        
        # 회사 정보 조회
        company_info = self.dart_api.get_company_info(corp_code)
        if company_info and 'induty_code' in company_info:
            return company_info.get('induty_code', '기타')
        return "기타"

    def _save_analysis_results(self, parsed_json, company_name, year):
        final_data = parsed_json.copy()

        st.session_state['company_data'] = final_data

        # 파일 저장
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/companies")
        os.makedirs(data_dir, exist_ok=True)
        
        clean_company_name = company_name.replace("/", "_").replace("\\", "_")
        file_name_base = f"{clean_company_name}_{timestamp}"
        json_file_path = os.path.join(data_dir, f"{file_name_base}.json")
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        
        st.success(f"재무제표 분석이 완료되었습니다. '{company_name}'의 데이터가 '{file_name_base}.json'으로 저장되었습니다.")
        
        # 다운로드 버튼
        json_str = json.dumps(final_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="JSON 파일 다운로드",
            data=json_str,
            file_name=f"{file_name_base}.json",
            mime="application/json",
            key=f"download_{file_name_base}"
        )