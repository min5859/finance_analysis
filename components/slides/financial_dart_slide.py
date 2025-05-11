import streamlit as st
import pandas as pd
from datetime import datetime
from dart.dart_data_processor import DartDataProcessor
from dart.dart_api_service import DartApiService

class FinancialDartSlide:
    """DART에서 가져온 재무 데이터를 보여주는 슬라이드 클래스"""
    
    def __init__(self):
        """FinancialDartSlide 초기화
        
        Args:
            data_loader: 데이터 로더 객체 (기존 finance_analysis 프로젝트의 DataLoader)
        """
        self.title = "DART 재무제표 데이터"
        
        # 재무 데이터 프로세서 초기화
        self.data_processor = DartDataProcessor()
        self.dart_api = DartApiService()
        
    def get_title(self):
        """슬라이드 제목 반환"""
        return self.title
    
    def render_header(self):
        """슬라이드 헤더 렌더링"""
        st.markdown(f'<h2 class="slide-header">{self.title}</h2>', unsafe_allow_html=True)
    
    def render(self):
        """슬라이드 내용 렌더링"""
        self.render_header()
        
        # dart_financial_data가 있는지 확인
        if 'dart_financial_data' in st.session_state:
            # financial_analysis_start_slide에서 조회한 연도를 가져옴
            selected_year = st.session_state.get('selected_year', datetime.now().year -1)
            st.subheader(f"{st.session_state.get('company_name','')} {selected_year}년 재무제표")
            self._render_financial_statements_display(st.session_state.dart_financial_data)
        else:
            st.info("먼저 '재무제표 분석 시작' 슬라이드에서 기업을 검색하고 재무제표를 조회해주세요.")
    
    def _render_financial_statements_display(self, financial_data):
        """세션에서 가져온 재무제표 표시"""
        if financial_data and 'list' in financial_data and len(financial_data['list']) > 0:
            # 데이터 처리
            processed_data = self.data_processor.extract_financial_data(financial_data)
            
            # 탭으로 재무제표 구분
            fin_tabs = st.tabs(["기업정보", "재무상태표", "손익계산서", "현금흐름표"])
            
            # 기업정보 탭
            with fin_tabs[0]:
                self._display_company_info()
            
            # 재무상태표 탭
            with fin_tabs[1]:
                self._display_balance_sheet(processed_data['balance_sheet'])
            
            # 손익계산서 탭
            with fin_tabs[2]:
                self._display_income_statement(processed_data['income_statement'])
            
            # 현금흐름표 탭
            with fin_tabs[3]:
                self._display_cash_flow(processed_data['cash_flow'])
        else:
            selected_year = st.session_state.get('selected_year', '해당')
            st.warning(f"{selected_year}년 재무제표 데이터가 없습니다.")
    
    def _display_company_info(self):
        """기업 정보 표시"""
        st.subheader("기업 정보")
        
        # 세션에서 기업 정보 가져오기
        company_name = st.session_state.get('company_name', '')
        stock_code = st.session_state.get('stock_code', '')
        corp_code = st.session_state.get('corp_code', '')
        selected_year = st.session_state.get('selected_year', '')
        
        # DART API를 통해 기업 상세 정보 조회
        company_info = self.dart_api.get_company_info(corp_code)
        
        if company_info and 'corp_name' in company_info:
            # 기본 정보 표시
            basic_info = {
                '항목': [
                    '기업명', '종목코드', '고유번호', '조회연도',
                    '대표자명', '설립일', '주소', '홈페이지'
                ],
                '내용': [
                    company_info.get('corp_name', ''),
                    stock_code,
                    corp_code,
                    str(selected_year),
                    company_info.get('ceo_nm', ''),
                    company_info.get('est_dt', ''),
                    company_info.get('adres', ''),
                    company_info.get('hm_url', '')
                ]
            }
            
            basic_df = pd.DataFrame(basic_info)
            st.dataframe(basic_df, hide_index=True, use_container_width=True)
            
            # 추가 정보 표시
            additional_info = {
                '항목': [
                    '업종', '주요사업', '상장일', '결산월'
                ],
                '내용': [
                    company_info.get('induty_code', ''),
                    company_info.get('main_prod', ''),
                    company_info.get('enp_ipo_dt', ''),
                    company_info.get('acc_mt', '')
                ]
            }
            
            additional_df = pd.DataFrame(additional_info)
            st.subheader("추가 정보")
            st.dataframe(additional_df, hide_index=True, use_container_width=True)
        else:
            # API 호출 실패 시 기본 정보만 표시
            basic_info = {
                '항목': ['기업명', '종목코드', '고유번호', '조회연도'],
                '내용': [company_name, stock_code, corp_code, str(selected_year)]
            }
            basic_df = pd.DataFrame(basic_info)
            st.dataframe(basic_df, hide_index=True, use_container_width=True)
            st.warning("기업 상세 정보를 가져오지 못했습니다.")
        
        # 보고서 정보 표시
        if 'dart_financial_data' in st.session_state:
            dart_data = st.session_state.dart_financial_data
            if 'list' in dart_data and len(dart_data['list']) > 0:
                report_info = dart_data['list'][0]
                
                report_data = {
                    '항목': ['보고서 종류', '보고서 코드', '보고서 명칭'],
                    '내용': [
                        report_info.get('rcept_no', ''),
                        report_info.get('reprt_code', ''),
                        report_info.get('reprt_nm', '')
                    ]
                }
                
                report_df = pd.DataFrame(report_data)
                st.subheader("보고서 정보")
                st.dataframe(report_df, hide_index=True, use_container_width=True)
    
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