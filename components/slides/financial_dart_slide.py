import streamlit as st
import pandas as pd
from datetime import datetime
from dart.dart_api_service import DartApiService
from dart.dart_data_processor import DartDataProcessor

class FinancialDartSlide:
    """DART에서 가져온 재무 데이터를 보여주는 슬라이드 클래스"""
    
    def __init__(self, data_loader=None):
        """FinancialDartSlide 초기화
        
        Args:
            data_loader: 데이터 로더 객체 (기존 finance_analysis 프로젝트의 DataLoader)
        """
        self.data_loader = data_loader
        self.title = "DART 재무제표 데이터"
        
        # DART API 서비스 초기화
        self.dart_api = DartApiService()
        
        # 재무 데이터 프로세서 초기화
        self.data_processor = DartDataProcessor()
        
        # 세션 상태 초기화
        if 'corp_code' not in st.session_state:
            st.session_state.corp_code = None
        
        if 'selected_year' not in st.session_state:
            st.session_state.selected_year = datetime.now().year - 1
    
    def get_title(self):
        """슬라이드 제목 반환"""
        return self.title
    
    def render_header(self):
        """슬라이드 헤더 렌더링"""
        st.markdown(f'<h2 class="slide-header">{self.title}</h2>', unsafe_allow_html=True)
    
    def render(self):
        """슬라이드 내용 렌더링"""
        self.render_header()
        
        # API 키 설정 확인
        if not self.dart_api.api_key:
            st.warning("DART API 키가 설정되지 않았습니다. API 키를 설정해야 재무제표 데이터를 조회할 수 있습니다.")
            api_key = st.text_input("DART API 키 입력:", type="password")
            if api_key:
                self.dart_api = DartApiService(api_key)
                st.success("API 키가 설정되었습니다.")
            else:
                return
        
        # 기업 검색 및 선택 UI
        st.subheader("기업 검색")
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_keyword = st.text_input("기업명 검색:", value="삼성전자")
        
        with search_col2:
            search_button = st.button("검색", use_container_width=True)
        
        if search_button or search_keyword:
            # 기업 목록 조회
            with st.spinner("기업 목록을 조회 중입니다..."):
                corp_codes = self.dart_api.get_corp_codes()
            
            if corp_codes:
                # 검색어로 필터링
                filtered_corps = [corp for corp in corp_codes if search_keyword.lower() in corp['corp_name'].lower()]
                
                if filtered_corps:
                    # 선택 목록 표시
                    corp_names = [f"{corp['corp_name']} ({corp['stock_code']})" for corp in filtered_corps]
                    selected_idx = st.selectbox("조회할 기업을 선택하세요:", range(len(corp_names)), format_func=lambda i: corp_names[i])
                    selected_corp = filtered_corps[selected_idx]
                    
                    # 기업코드 저장
                    st.session_state.corp_code = selected_corp['corp_code']
                    
                    # 기업 정보 표시
                    st.info(f"선택된 기업: {selected_corp['corp_name']} (종목코드: {selected_corp['stock_code']})")
                else:
                    st.warning(f"'{search_keyword}'에 대한 검색 결과가 없습니다.")
            else:
                st.error("기업 목록을 가져오지 못했습니다. API 키를 확인하세요.")
        
        # 기업이 선택되었을 때만 재무제표 조회 부분 표시
        if st.session_state.corp_code:
            self._render_financial_statements()
    
    def _render_financial_statements(self):
        """재무제표 조회 및 표시"""
        st.subheader("재무제표 조회")
        
        # 연도 선택
        current_year = datetime.now().year
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_year = st.selectbox(
                "조회 연도:",
                list(range(current_year-10, current_year)),
                index=list(range(current_year-10, current_year)).index(st.session_state.selected_year),
                key="year_select"
            )
        
        with col2:
            query_button = st.button("조회", key="query_button", use_container_width=True)
        
        if query_button:
            st.session_state.selected_year = selected_year
        
        # 재무제표 데이터 조회
        if st.session_state.corp_code and st.session_state.selected_year:
            with st.spinner(f"{st.session_state.selected_year}년 재무제표를 조회 중입니다..."):
                financial_data = self.dart_api.get_financial_statements(
                    st.session_state.corp_code, 
                    str(st.session_state.selected_year)
                )
            
            if financial_data and 'list' in financial_data and len(financial_data['list']) > 0:
                # 데이터 처리
                processed_data = self.data_processor.extract_financial_data(financial_data)
                
                # 탭으로 재무제표 구분
                fin_tabs = st.tabs(["재무상태표", "손익계산서", "현금흐름표"])
                
                # 재무상태표 탭
                with fin_tabs[0]:
                    self._display_balance_sheet(processed_data['balance_sheet'])
                
                # 손익계산서 탭
                with fin_tabs[1]:
                    self._display_income_statement(processed_data['income_statement'])
                
                # 현금흐름표 탭
                with fin_tabs[2]:
                    self._display_cash_flow(processed_data['cash_flow'])
            else:
                st.warning(f"{st.session_state.selected_year}년 재무제표 데이터가 없습니다.")
    
    def _display_balance_sheet(self, bs_items):
        """재무상태표 표시"""
        st.subheader("재무상태표")
        
        if not bs_items:
            st.info("재무상태표 데이터가 없습니다.")
            return
        
        # 데이터프레임 생성
        bs_df = self.data_processor.create_financial_statement_df(bs_items)
        
        # 주요 항목 필터링 (선택사항)
        important_items = [
            '자산총계', '부채총계', '자본총계', '유동자산', '비유동자산', 
            '유동부채', '비유동부채', '자본금', '이익잉여금'
        ]
        
        filtered_df = bs_df[bs_df['계정과목명'].str.contains('|'.join(important_items), case=False)]
        
        if not filtered_df.empty:
            st.subheader("주요 항목")
            st.dataframe(filtered_df, hide_index=True, use_container_width=True)
        
        # 전체 데이터 표시
        st.subheader("전체 항목")
        st.dataframe(bs_df, hide_index=True, use_container_width=True)
    
    def _display_income_statement(self, is_items):
        """손익계산서 표시"""
        st.subheader("손익계산서")
        
        if not is_items:
            st.info("손익계산서 데이터가 없습니다.")
            return
        
        # 데이터프레임 생성
        is_df = self.data_processor.create_financial_statement_df(is_items)
        
        # 주요 항목 필터링 (선택사항)
        important_items = [
            '매출액', '영업이익', '영업손실', '당기순이익', '당기순손실', 
            '매출원가', '판매비와관리비', '금융수익', '금융비용'
        ]
        
        filtered_df = is_df[is_df['계정과목명'].str.contains('|'.join(important_items), case=False)]
        
        if not filtered_df.empty:
            st.subheader("주요 항목")
            st.dataframe(filtered_df, hide_index=True, use_container_width=True)
        
        # 전체 데이터 표시
        st.subheader("전체 항목")
        st.dataframe(is_df, hide_index=True, use_container_width=True)
    
    def _display_cash_flow(self, cf_items):
        """현금흐름표 표시"""
        st.subheader("현금흐름표")
        
        if not cf_items:
            st.info("현금흐름표 데이터가 없습니다.")
            return
        
        # 데이터프레임 생성
        cf_df = self.data_processor.create_financial_statement_df(cf_items)
        
        # 주요 항목 필터링 (선택사항)
        important_items = [
            '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 
            '현금및현금성자산의증가', '기초현금및현금성자산', '기말현금및현금성자산'
        ]
        
        filtered_df = cf_df[cf_df['계정과목명'].str.contains('|'.join(important_items), case=False)]
        
        if not filtered_df.empty:
            st.subheader("주요 항목")
            st.dataframe(filtered_df, hide_index=True, use_container_width=True)
        
        # 전체 데이터 표시
        st.subheader("전체 항목")
        st.dataframe(cf_df, hide_index=True, use_container_width=True)