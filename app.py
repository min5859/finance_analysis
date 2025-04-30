import streamlit as st
import os
import json
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
from config.app_config import apply_custom_css
import streamlit.components.v1 as components
import base64

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

def main():
    st.set_page_config(
        page_title="기업 재무 분석 대시보드",
        page_icon="📊",
        layout="wide"
    )
    
    apply_custom_css()
    
    # 사이드바 구성
    st.sidebar.image("static/images/01.M&AIKorea_CI_transparent-(gradient).png", use_container_width=True)
    
    # 회사 선택 드롭다운을 사이드바로 이동
    companies = get_available_companies()
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
                company_name = f"{company_data.get('company_name', '기업')} 재무"
        except Exception:
            pass

    # Fancy Header 스타일의 타이틀
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
        ">{company_name} 분석</h1>
        <img src="data:image/png;base64,{img_base64}" style="max-width: 120px; margin-top: 1rem; display: block; margin-left: auto; margin-right: auto;">
    </div>
    """, height=150)

    # 구분선 추가
    st.sidebar.markdown("---")
    
    # 슬라이드 메뉴
    st.sidebar.title("목차")
    slide_names = [
        "요약",
        "손익계산서",
        "재무상태표",
        "성장성 분석",
        "수익성 분석",
        "안정성 분석",
        "현금흐름표",
        "운전자본 분석",
        "업계비교 현황",
        "종합 결론"
    ]
    selected_slide = st.sidebar.radio("분석 슬라이드 선택", slide_names)
    
    # 기업이 선택되었을 때만 슬라이드 표시
    if selected_file is not None:
        # 데이터 로더 초기화
        data_loader = DataLoader(selected_file)
        
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
    else:
        # 기업이 선택되지 않았을 때 안내 메시지 표시
        st.info("왼쪽 드롭다운에서 분석할 기업을 선택해주세요.")
        
if __name__ == "__main__":
    main()
