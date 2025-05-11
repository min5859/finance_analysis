import streamlit as st
import pandas as pd
import json
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
            
            # 최적화된 데이터 처리 (LLM용)
            optimized_data = self.data_processor.extract_optimized_financial_data(financial_data)
            
            # 기업 정보 추가
            corp_name = st.session_state.get('company_name', '')
            selected_year = st.session_state.get('selected_year', '')
            sector = self._get_company_sector()
            
            optimized_data = {
                'company_name': corp_name,
                'report_year': str(selected_year),
                'sector': sector,
                **optimized_data
            }
            
            # 탭으로 재무제표 구분
            fin_tabs = st.tabs(["기업정보", "재무상태표", "손익계산서", "현금흐름표", "LLM 최적화 데이터", "감사보고서"])
            
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
                
            # LLM 최적화 데이터 탭 (새로 추가)
            with fin_tabs[4]:
                self._display_optimized_data(optimized_data)
            
            # 감사보고서 탭
            with fin_tabs[5]:
                self._display_audit_report()
        else:
            selected_year = st.session_state.get('selected_year', '해당')
            st.warning(f"{selected_year}년 재무제표 데이터가 없습니다.")
    
    def _display_optimized_data(self, optimized_data):
        """LLM 최적화 데이터 표시"""
        st.subheader("LLM 분석용 최적화 데이터")
        
        # 최적화 데이터에 대한 설명
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 0.25rem solid #4f46e5;">
        이 데이터는 LLM(Claude)에 전송되는 최적화된 형태의 재무 데이터입니다. 모든 금액은 <b>억원 단위</b>로 변환되었으며, 
        재무분석에 필요한 핵심 계정과목만 추출하여 토큰 수를 최적화하였습니다.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 기본 정보 카드
            st.markdown("""
            <div style="background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
                <h4 style="color: #4338ca; margin-bottom: 0.75rem;">기업 기본 정보</h4>
            """, unsafe_allow_html=True)
            
            info_df = pd.DataFrame({
                '항목': ['기업명', '보고서 연도', '업종 코드'],
                '값': [
                    optimized_data.get('company_name', ''), 
                    optimized_data.get('report_year', ''), 
                    optimized_data.get('sector', '')
                ]
            })
            st.dataframe(info_df, hide_index=True, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # LLM 최적화 데이터 전체 (JSON)
            st.markdown("<h4 style='margin-top: 1.5rem;'>전체 최적화 데이터 (JSON)</h4>", unsafe_allow_html=True)
            # JSON 문자열로 변환하고 들여쓰기 적용
            optimized_json = json.dumps(optimized_data, indent=2, ensure_ascii=False)
            st.code(optimized_json, language="json")
            
            # 다운로드 버튼
            st.download_button(
                label="JSON 다운로드",
                data=optimized_json,
                file_name=f"{optimized_data.get('company_name', 'company')}_optimized.json",
                mime="application/json"
            )
            
        with col2:
            # 재무비율 데이터 카드 (3년치)
            st.markdown("""
            <div style="background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12);">
                <h4 style="color: #4338ca; margin-bottom: 0.75rem;">재무비율 (3년치)</h4>
            """, unsafe_allow_html=True)
            
            # 재무비율 데이터가 있는지 확인
            if 'financial_ratios' in optimized_data and optimized_data['financial_ratios']:
                ratios = optimized_data['financial_ratios']
                years = ratios.get('year', [])
                
                # 각 재무비율에 대한 테이블 작성
                ratio_data = []
                
                for i, year in enumerate(years):
                    row = {'연도': year}
                    
                    for key in ratios:
                        if key != 'year' and isinstance(ratios[key], list) and len(ratios[key]) > i:
                            row[key] = f"{ratios[key][i]}%"
                    
                    ratio_data.append(row)
                
                # 재무비율 데이터프레임 생성 및 표시
                ratio_df = pd.DataFrame(ratio_data)
                st.dataframe(ratio_df, hide_index=True, use_container_width=True)
            else:
                st.info("재무비율 데이터가 없습니다.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 핵심 재무제표 항목 수 표시
            st.markdown("""
            <div style="background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12); margin-top: 1rem;">
                <h4 style="color: #4338ca; margin-bottom: 0.75rem;">데이터 최적화 요약</h4>
            """, unsafe_allow_html=True)
            
            # 각 재무제표 항목 수 계산
            bs_count = len(optimized_data.get('balance_sheet', []))
            is_count = len(optimized_data.get('income_statement', []))
            cf_count = len(optimized_data.get('cash_flow', []))
            ratio_count = len([k for k in optimized_data.get('financial_ratios', {}).keys() if k != 'year'])
            
            # 요약 정보 데이터프레임
            summary_df = pd.DataFrame({
                '항목': ['재무상태표 계정 수', '손익계산서 계정 수', '현금흐름표 계정 수', '재무비율 지표 수', '총 데이터 항목 수'],
                '개수': [
                    bs_count,
                    is_count, 
                    cf_count,
                    ratio_count,
                    bs_count + is_count + cf_count + ratio_count
                ]
            })
            st.dataframe(summary_df, hide_index=True, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 토큰 분석
            st.markdown("""
            <div style="background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.12); margin-top: 1rem;">
                <h4 style="color: #4338ca; margin-bottom: 0.75rem;">대략적인 토큰 분석</h4>
            """, unsafe_allow_html=True)
            
            # JSON 문자열 길이로 대략적인 토큰 수 추정
            json_chars = len(optimized_json)
            estimated_tokens = json_chars // 4  # 대략적인 추정 (4자당 1토큰)
            
            token_df = pd.DataFrame({
                '항목': ['JSON 문자 수', '추정 토큰 수', '약 토큰 비용 (USD)'],
                '값': [
                    f"{json_chars:,}자",
                    f"{estimated_tokens:,}토큰",
                    f"${(estimated_tokens * 0.00025):.4f}"  # Claude 토큰 비용 추정 (입력 토큰)
                ]
            })
            st.dataframe(token_df, hide_index=True, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _display_audit_report(self):
        """감사 보고서 표시"""
        st.subheader("감사 보고서")
        
        # 세션에서 필요한 정보 가져오기
        corp_code = st.session_state.get('corp_code', '')
        selected_year = st.session_state.get('selected_year', '')
        
        if not corp_code or not selected_year:
            st.warning("기업 정보가 없습니다.")
            return
        
        # 감사 보고서 정보 조회
        audit_data = self.dart_api.get_audit_report(corp_code, str(selected_year))
        
        if audit_data and 'list' in audit_data and len(audit_data['list']) > 0:
            # 외부감사 정보 표시
            audit_info = audit_data['list'][0]
            
            # 감사인 정보
            auditor_info = {
                '항목': [
                    '감사인', '감사인 주소', '감사인 전화번호',
                    '감사인 이메일', '감사인 홈페이지'
                ],
                '내용': [
                    audit_info.get('auditor_nm', ''),
                    audit_info.get('auditor_adres', ''),
                    audit_info.get('auditor_telno', ''),
                    audit_info.get('auditor_email', ''),
                    audit_info.get('auditor_hmpg', '')
                ]
            }
            
            auditor_df = pd.DataFrame(auditor_info)
            st.subheader("감사인 정보")
            st.dataframe(auditor_df, hide_index=True, use_container_width=True)
            
            # 감사의견 정보
            opinion_info = {
                '항목': [
                    '감사의견', '감사보고서 일자', '감사보고서 번호',
                    '감사보고서 제출일', '감사보고서 접수일'
                ],
                '내용': [
                    audit_info.get('opnion_cd', ''),
                    audit_info.get('audit_report_dt', ''),
                    audit_info.get('audit_report_no', ''),
                    audit_info.get('submission_dt', ''),
                    audit_info.get('rcept_dt', '')
                ]
            }
            
            opinion_df = pd.DataFrame(opinion_info)
            st.subheader("감사의견 정보")
            st.dataframe(opinion_df, hide_index=True, use_container_width=True)
            
            # 감사보고서 원문 정보 표시
            if 'audit_reports' in audit_data and audit_data['audit_reports']:
                st.subheader("감사보고서 원문")
                for report in audit_data['audit_reports']:
                    disclosure_info = report['disclosure_info']
                    document_info = report['document_info']
                    
                    # 공시 정보 표시
                    disclosure_data = {
                        '항목': ['보고서명', '접수번호', '접수일자', '공시일자'],
                        '내용': [
                            disclosure_info.get('report_nm', ''),
                            disclosure_info.get('rcept_no', ''),
                            disclosure_info.get('rcept_dt', ''),
                            disclosure_info.get('flr_nm', '')
                        ]
                    }
                    
                    disclosure_df = pd.DataFrame(disclosure_data)
                    st.dataframe(disclosure_df, hide_index=True, use_container_width=True)
                    
                    # 문서 정보 표시
                    if 'document' in document_info:
                        st.text_area("감사보고서 전문", document_info['document'], height=300)
        else:
            st.warning(f"{selected_year}년 감사 보고서 데이터가 없습니다.")
    
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