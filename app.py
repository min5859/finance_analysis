import streamlit as st
import os
import json
import base64
import datetime
import tempfile
from data.data_loader import DataLoader
from components.slides.summary_slide import SummarySlide
from components.slides.income_statement_slide import IncomeStatementSlide
from components.slides.balance_sheet_slide import BalanceSheetSlide
from components.slides.cash_flow_slide import CashFlowSlide
from components.slides.profitability_slide import ProfitabilitySlide
from components.slides.growth_rate_slide import GrowthRateSlide
from components.slides.stability_slide import StabilitySlide
from components.slides.working_capital_slide import WorkingCapitalSlide
from components.slides.conclusion_slide import ConclusionSlide
from components.slides.industry_comparison_slide import IndustryComparisonSlide
from components.slides.valuation_slide import ValuationSlide
from components.slides.financial_analysis_start_slide import FinancialAnalysisStartSlide
from components.slides.valuation_manual_slide import ValuationManualSlide
# 새로 추가한 DART 슬라이드 임포트
from components.slides.financial_dart_slide import FinancialDartSlide
from config.app_config import apply_custom_css
import streamlit.components.v1 as components
from data.financial_statement_processor import FinancialStatementProcessor

# PDF 재무제표 추출기 임포트
from pdf_extractor_app import FinancialStatementDetector, PDFViewer
import pdfplumber

def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 이미지를 Base64로 변환
img_path = "static/images/04.M&AIKorea_CI_hor_transparent-04(white).png"
img_base64 = get_image_as_base64(img_path)

def get_available_companies():
    """사용 가능한 회사 목록 가져오기"""
    companies = []
    data_dir = os.path.dirname(os.path.abspath(__file__))
    company_dir = os.path.join(data_dir, "data/companies")
    
    if os.path.exists(company_dir):
        for file in os.listdir(company_dir):
            if file.endswith('.json'):
                try:
                    with open(os.path.join(company_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        companies.append({
                            'filename': file,
                            'name': data.get('company_name', file.replace('.json', '')),
                            'sector': data.get('sector', '기타')
                        })
                except Exception:
                    pass
    
    return companies

def extract_text_from_pdf_pages(pdf_path, pages):
    """선택된 페이지들에서만 텍스트 추출"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for page_num in pages:
                # 0-인덱스로 변환 및 범위 확인
                idx = page_num - 1
                if 0 <= idx < total_pages:
                    page = pdf.pages[idx]
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- 페이지 {page_num} ---\n"
                        text += page_text
    except Exception as e:
        st.error(f"PDF 텍스트 추출 오류: {str(e)}")
    
    return {
        "text": text,
        "pages": len(pages)
    }

def extract_financial_statement_pages(pdf_path):
    """PDF에서 재무제표 페이지만 추출"""
    detector = FinancialStatementDetector()
    try:
        # 재무제표 페이지 탐지
        financial_pages, statement_types = detector.detect_financial_statements(pdf_path)
        return financial_pages, statement_types
    except Exception as e:
        st.error(f"재무제표 페이지 탐지 오류: {str(e)}")
        return [], {}

def main():
    st.set_page_config(
        page_title="Financial Analysis System",
        page_icon="📊",
        layout="wide"
    )
    
    apply_custom_css()
    
    # 사이드바 구성
    st.sidebar.image("static/images/01.M&AIKorea_CI_transparent-(gradient).png", use_container_width=True)
    
    # API 키 설정
    api_key = st.secrets.get("anthropic_api_key", None) if hasattr(st, "secrets") else None
    if not api_key:
        api_key = st.sidebar.text_input("Anthropic API 키를 입력하세요", type="password")
        if not api_key:
            st.warning("API 키를 입력해주세요.")
            return
    
    # 파일 업로드 섹션
    st.sidebar.markdown("---")
    uploaded_files = st.sidebar.file_uploader(
        "Upload Financial Data",
        type=["pdf", "png", "jpg", "jpeg", "json"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        # 파일 타입에 따라 처리
        json_files = [f for f in uploaded_files if f.type == "application/json"]
        other_files = [f for f in uploaded_files if f.type != "application/json"]
        
        if json_files and other_files:
            st.error("JSON 파일과 다른 형식의 파일을 동시에 업로드할 수 없습니다.")
            return
        
        if json_files:
            # JSON 파일 처리
            if len(json_files) > 1:
                st.error("JSON 파일은 한 번에 하나만 업로드할 수 있습니다.")
                return
                
            try:
                # JSON 파일 로드
                json_data = json.load(json_files[0])
                
                # 결과를 session_state에 저장
                st.session_state['company_data'] = json_data
                
                company_name = json_data.get('company_name', '알 수 없는 기업')
                st.sidebar.success(f"{company_name}의 데이터가 로드되었습니다.")
                
            except json.JSONDecodeError as e:
                st.error(f"JSON 파일 파싱 오류: {str(e)}")
            except Exception as e:
                st.error(f"파일 처리 오류: {str(e)}")
                
        elif other_files:
            # PDF/이미지 파일 처리
            processor = FinancialStatementProcessor(api_key=api_key)
            
            # PDF 파일과 이미지 파일 분리
            pdf_files = [f for f in other_files if f.type == "application/pdf"]
            image_files = [f for f in other_files if f.type != "application/pdf"]
            
            # 재무제표 분석 설정
            st.sidebar.markdown("### PDF 분석 설정")
            auto_detect = st.sidebar.checkbox("재무제표 페이지 자동 탐지", value=True)
            
            # 민감도 설정 (자동 탐지 활성화된 경우만)
            detection_sensitivity = 5
            #if auto_detect:
            #    detection_sensitivity = st.sidebar.slider(
            #        "탐지 민감도",
            #        min_value=1,
            #        max_value=10,
            #        value=5,
            #        help="낮을수록 더 많은 페이지가 검출됩니다. 높을수록 확실한 재무제표만 검출됩니다."
            #    )
            
            if st.sidebar.button("재무제표 분석 시작"):
                with st.spinner("재무제표 분석 중..."):
                    results = []
                    
                    # PDF 파일 처리
                    if pdf_files:
                        try:
                            # 진행 상태 표시
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            # PDF 파일 병합
                            status_text.text("PDF 파일 병합 중...")
                            progress_bar.progress(25)
                            
                            merged_pdf = processor.merge_pdfs(pdf_files)
                            
                            # 임시 파일로 저장
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                                tmp_file.write(merged_pdf)
                                pdf_path = tmp_file.name
                            
                            # 자동 탐지 활성화된 경우에만 재무제표 페이지 탐지
                            detected_pages = []
                            statement_types = {}
                            
                            if auto_detect:
                                status_text.text("재무제표 페이지 탐지 중...")
                                progress_bar.progress(40)
                                
                                # 탐지기 인스턴스 생성 및 민감도 설정
                                detector = FinancialStatementDetector()
                                if detection_sensitivity != 5:  # 기본값과 다른 경우만 조정
                                    detector.min_score_threshold = 5 + (detection_sensitivity - 5) * 1  # 5~15 범위
                                    detector.min_accounts_required = max(2, int(3 + (detection_sensitivity - 5) * 0.5))  # 2~5 범위
                                    detector.numeric_content_ratio = 0.15 + (detection_sensitivity - 5) * 0.03  # 0.15~0.3 범위
                                
                                detected_pages, statement_types = detector.detect_financial_statements(pdf_path)
                                
                                # 탐지 결과 표시
                                if detected_pages:
                                    # 재무제표 유형별 페이지 정보 표시
                                    st.subheader("📋 탐지된 재무제표 페이지")

                                    # 페이지 번호 표시
                                    page_numbers = [str(page) for page in detected_pages]
                                    st.write(f"**재무제표 페이지**: {', '.join(page_numbers)}")
                                    
                                    # 유형별 페이지 수 표시
                                    type_counts = {}
                                    for page, page_type in statement_types.items():
                                        if page_type not in type_counts:
                                            type_counts[page_type] = 0
                                        type_counts[page_type] += 1
                                    
                                    type_summary = ", ".join([f"{type}: {count}페이지" for type, count in type_counts.items()])
                                    st.write(f"**유형별 페이지 수**: {type_summary}")
                                    
                                    # 재무제표 유형별 페이지 표시
                                    for page_type in set(statement_types.values()):
                                        pages_of_type = [page for page, t in statement_types.items() if t == page_type]
                                        if pages_of_type:
                                            pages_str = ", ".join([str(p) for p in sorted(pages_of_type)])
                                            st.write(f"**{page_type}**: {pages_str}페이지")
                                else:
                                    st.warning("재무제표 페이지를 찾을 수 없습니다. 전체 PDF 내용을 분석합니다.")
                            
                            # 데이터 추출 부분
                            progress_bar.progress(60)
                            status_text.text("텍스트 추출 중...")
                            
                            # 탐지된 페이지만 처리하거나 전체 PDF 처리
                            if auto_detect and detected_pages:
                                # 탐지된 페이지에서만 텍스트 추출
                                file_data = extract_text_from_pdf_pages(pdf_path, detected_pages)
                                status_text.text(f"탐지된 {len(detected_pages)}개 재무제표 페이지 분석 중...")
                            else:
                                # 전체 PDF에서 텍스트 추출
                                file_data = processor.extract_text_from_pdf(merged_pdf)
                                status_text.text("전체 PDF 내용 분석 중...")
                            
                            progress_bar.progress(75)

                            # Claude API 호출
                            json_result = processor.process_with_claude(file_data)

                            progress_bar.progress(90)
                            
                            # JSON 결과 정리
                            try:
                                parsed_json = processor.parse_json_response(json_result)
                                results.append(parsed_json)
                                progress_bar.progress(100)
                                status_text.text("분석 완료!")
                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 오류: {str(e)}")
                                st.error("디버깅을 위한 LLM 출력 결과:")
                                st.code(json_result, language="json")
                                return
                            
                            # 임시 파일 삭제
                            try:
                                os.unlink(pdf_path)
                            except:
                                pass
                        
                        except Exception as e:
                            st.error(f"PDF 처리 오류: {str(e)}")
                            return
                    
                    # 이미지 파일 처리
                    for image_file in image_files:
                        try:
                            file_data = processor.process_image(image_file)
                            json_result = processor.process_with_claude(file_data)
                            
                            try:
                                parsed_json = processor.parse_json_response(json_result)
                                results.append(parsed_json)
                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 오류: {str(e)}")
                                st.error("디버깅을 위한 LLM 출력 결과:")
                                st.code(json_result, language="json")
                                return
                        
                        except Exception as e:
                            st.error(f"이미지 처리 오류: {str(e)}")
                            return
                    
                    if results:
                        # 결과를 session_state에 저장
                        st.session_state['company_data'] = results[0]

                        # 타임스탬프 생성
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

                        # JSON 파일로 저장
                        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/companies")
                        os.makedirs(data_dir, exist_ok=True)

                        company_name = results[0].get('company_name', 'unknown_company')
                        json_file = os.path.join(data_dir, f"{company_name}_{timestamp}.json")
                        
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(results[0], f, ensure_ascii=False, indent=2)
                        
                        st.sidebar.success(f"재무제표 분석이 완료되었습니다. {company_name}의 데이터가 저장되었습니다.")
                        
                        # JSON 파일 다운로드 버튼 추가 (사이드바)
                        json_str = json.dumps(results[0], ensure_ascii=False, indent=2)
                        st.sidebar.download_button(
                            label="JSON 파일 다운로드",
                            data=json_str,
                            file_name=f"{company_name}_{timestamp}.json",
                            mime="application/json"
                        )
    
    # 회사 선택 드롭다운을 사이드바로 이동
    companies = get_available_companies()
    # 회사 이름 기준으로 오름차순 정렬
    companies.sort(key=lambda x: x['name'])
    company_names = ["기업을 선택하세요"] + [f"{c['name']} ({c['sector']})" for c in companies]
    company_files = [None] + [c['filename'] for c in companies]
    
    selected_index = st.sidebar.selectbox(
        "분석할 기업 선택",
        range(len(company_names)),
        format_func=lambda i: company_names[i]
    )
    
    selected_file = company_files[selected_index]

    # 선택된 기업 정보 가져오기
    company_name = "기업 재무"
    if selected_file is not None:
        data_dir = os.path.dirname(os.path.abspath(__file__))
        company_dir = os.path.join(data_dir, "data/companies")
        json_file = os.path.join(company_dir, selected_file)
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                company_data = json.load(f)
                company_name = f"{company_data.get('company_name', '기업')}"
                st.session_state['company_data'] = company_data
                st.sidebar.success(f"{company_data.get('company_name', '기업')}의 데이터가 로드되었습니다.")
        except Exception as e:
            st.sidebar.error(f"파일 로드 오류: {str(e)}")
    
    # Fancy Header 스타일의 타이틀
    if st.session_state.get('company_data'):
        company_name = f"{st.session_state['company_data'].get('company_name', '기업')}"

    components.html(f"""
    <div style="
        background: linear-gradient(90deg, #0a1172, #1a237e, #283593);
        padding: 1.5rem; 
        border-radius: 0.8rem; 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        text-align: center;
    ">
        <h1 style="
            color: white; 
            font-weight: 800; 
            margin: 0; 
            font-size: 2.2rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        ">{company_name} 재무 분석</h1>
        <img src="data:image/png;base64,{img_base64}" style="max-width: 120px; margin-top: 1rem; display: block; margin-left: auto; margin-right: auto;">
    </div>
    """, height=150)

    # 구분선 추가
    st.sidebar.markdown("---")
    
    # 슬라이드 메뉴
    st.sidebar.title("목차")
    slide_names = [
        "재무제표 분석 시작",
        "DART 재무제표 데이터",  # 새로 추가한 DART 슬라이드
        "요약",
        "손익계산서",
        "재무상태표",
        "성장성 분석",
        "수익성 분석",
        "안정성 분석",
        "현금흐름표",
        "운전자본 분석",
        "업계비교 현황",
        "종합 결론",
        "가치 평가",
        "가치 평가(검증)",
    ]
    selected_slide = st.sidebar.radio("분석 슬라이드 선택", slide_names)
    
    # 선택된 슬라이드 표시
    if selected_slide == "재무제표 분석 시작":
        FinancialAnalysisStartSlide(api_key).render()
    elif selected_slide == "DART 재무제표 데이터":
        # DART API를 사용한 새로운 슬라이드 표시
        FinancialDartSlide().render()

    # 기업이 선택되었을 때만 다른 슬라이드 표시
    elif 'company_data' in st.session_state:
        # 데이터 로더 초기화
        data_loader = DataLoader(st.session_state['company_data'])

        # 선택된 슬라이드 표시
        if selected_slide == "요약":
            SummarySlide(data_loader).render()
        elif selected_slide == "손익계산서":
            IncomeStatementSlide(data_loader).render()
        elif selected_slide == "재무상태표":
            BalanceSheetSlide(data_loader).render()
        elif selected_slide == "성장성 분석":
            GrowthRateSlide(data_loader).render()
        elif selected_slide == "수익성 분석":
            ProfitabilitySlide(data_loader).render()
        elif selected_slide == "안정성 분석":
            StabilitySlide(data_loader).render()
        elif selected_slide == "현금흐름표":
            CashFlowSlide(data_loader).render()
        elif selected_slide == "운전자본 분석":
            WorkingCapitalSlide(data_loader).render()
        elif selected_slide == "업계비교 현황":
            IndustryComparisonSlide(data_loader).render()
        elif selected_slide == "종합 결론":
            ConclusionSlide(data_loader).render()
        elif selected_slide == "가치 평가":
            ValuationSlide(data_loader).render()
        elif selected_slide == "가치 평가(검증)":
            ValuationManualSlide(data_loader).render()
    else:
        # 기업이 선택되지 않았을 때 안내 메시지 표시
        st.info("왼쪽 사이드바에서 재무제표를 업로드하거나 DART API를 통해 기업 정보를 조회해주세요.")
        
if __name__ == "__main__":
    main()
