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
from components.slides.financial_dart_slide import FinancialDartSlide
from config.app_config import apply_custom_css
import streamlit.components.v1 as components
from data.financial_statement_processor import FinancialStatementProcessor
from pdf_extractor_app import FinancialStatementDetector, PDFViewer
import pdfplumber

def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_path = "static/images/04.M&AIKorea_CI_hor_transparent-04(white).png"
img_base64 = get_image_as_base64(img_path)

def get_available_companies():
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

def main():
    st.set_page_config(page_title="Financial Analysis System", page_icon="📊", layout="wide")
    apply_custom_css()
    
    st.sidebar.image("static/images/01.M&AIKorea_CI_transparent-(gradient).png", use_container_width=True)
    
    api_key = st.secrets.get("anthropic_api_key", None) if hasattr(st, "secrets") else None
    if not api_key:
        api_key = st.sidebar.text_input("Anthropic API 키를 입력하세요", type="password")
        if not api_key:
            st.warning("API 키를 입력해주세요.")
            return

    st.sidebar.markdown("---")
    # ... (file uploader and processing logic remains the same) ...

    companies = get_available_companies()
    companies.sort(key=lambda x: x['name'])
    company_names = ["기업을 선택하세요"] + [f"{c['name']} ({c['sector']})" for c in companies]
    company_files = [None] + [c['filename'] for c in companies]
    
    selected_index = st.sidebar.selectbox(
        "분석할 기업 선택",
        range(len(company_names)),
        format_func=lambda i: company_names[i]
    )
    
    selected_file = company_files[selected_index]

    if selected_file is not None:
        data_dir = os.path.dirname(os.path.abspath(__file__))
        company_dir = os.path.join(data_dir, "data/companies")
        json_file = os.path.join(company_dir, selected_file)
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                company_data = json.load(f)
                st.session_state['company_data'] = company_data
                st.sidebar.success(f"{company_data.get('company_name', '기업')}의 데이터가 로드되었습니다.")
        except Exception as e:
            st.sidebar.error(f"파일 로드 오류: {str(e)}")
    
    company_name = "기업 재무"
    if st.session_state.get('company_data'):
        company_name = f"{st.session_state['company_data'].get('company_name', '기업')}"

    components.html(f"""
    <div style="background: linear-gradient(90deg, #0a1172, #1a237e, #283593); padding: 1.5rem; border-radius: 0.8rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-weight: 800; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);">{company_name} 재무 분석</h1>
        <img src="data:image/png;base64,{img_base64}" style="max-width: 120px; margin-top: 1rem; display: block; margin-left: auto; margin-right: auto;">
    </div>
    """, height=150)

    st.sidebar.markdown("---")
    st.sidebar.title("목차")
    slide_names = [
        "재무제표 분석 시작", "DART 재무제표 데이터", "요약", "손익계산서", "재무상태표",
        "성장성 분석", "수익성 분석", "안정성 분석", "현금흐름표", "운전자본 분석",
        "업계비교 현황", "종합 결론", "가치 평가", "가치 평가(검증)", "전체 슬라이드 보기",
    ]
    selected_slide = st.sidebar.radio("분석 슬라이드 선택", slide_names)

    st.sidebar.markdown("---")
    if st.sidebar.button("PDF로 인쇄", use_container_width=True):
        st.markdown("<script>window.print();</script>", unsafe_allow_html=True)

    slide_mapping = {
        "DART 재무제표 데이터": FinancialDartSlide, "요약": SummarySlide, "손익계산서": IncomeStatementSlide,
        "재무상태표": BalanceSheetSlide, "성장성 분석": GrowthRateSlide, "수익성 분석": ProfitabilitySlide,
        "안정성 분석": StabilitySlide, "현금흐름표": CashFlowSlide, "운전자본 분석": WorkingCapitalSlide,
        "업계비교 현황": IndustryComparisonSlide, "종합 결론": ConclusionSlide, "가치 평가": ValuationSlide,
        "가치 평가(검증)": ValuationManualSlide,
    }

    if selected_slide == "재무제표 분석 시작":
        FinancialAnalysisStartSlide(api_key).render()
    elif selected_slide == "전체 슬라이드 보기":
        if 'company_data' in st.session_state:
            data_loader = DataLoader(st.session_state.get('company_data'))
            for slide_name, slide_class in slide_mapping.items():
                st.markdown(f'<div class="slide-container" style="page-break-after: always;">', unsafe_allow_html=True)
                try:
                    instance = slide_class(data_loader=data_loader)
                except TypeError:
                    instance = slide_class()
                instance.render()
                st.markdown(f'</div>', unsafe_allow_html=True)
        else:
            st.warning("먼저 기업 데이터를 로드해주세요.")
    elif 'company_data' in st.session_state or selected_slide == "DART 재무제표 데이터":
        data_loader = DataLoader(st.session_state.get('company_data')) if 'company_data' in st.session_state else None
        slide_class = slide_mapping.get(selected_slide)
        if slide_class:
            try:
                slide_instance = slide_class(data_loader=data_loader)
            except TypeError:
                slide_instance = slide_class()
            slide_instance.render()
        else:
            st.warning("선택한 슬라이드를 찾을 수 없습니다.")
    else:
        st.info("왼쪽 사이드바에서 재무제표를 업로드하거나 DART API를 통해 기업 정보를 조회해주세요.")

if __name__ == "__main__":
    main()