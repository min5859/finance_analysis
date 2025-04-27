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
from config.app_config import apply_custom_css

def get_available_companies():
    """사용 가능한 회사 목록 가져오기"""
    companies = []
    data_dir = os.path.dirname(os.path.abspath(__file__))
    company_dir = os.path.join(data_dir, "data/companies")
    
    if os.path.exists(company_dir):
        # 먼저 default.json 파일 처리
        default_file = os.path.join(company_dir, "default.json")
        if os.path.exists(default_file):
            try:
                with open(default_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    companies.append({
                        'code': "default",  # 실제 파일 이름 사용
                        'name': f"(예시) {data.get('company_name', 'default')}",
                        'sector': data.get('sector', '기타')
                    })
            except Exception:
                pass
        
        # 나머지 json 파일 처리
        for file in os.listdir(company_dir):
            if file.endswith('.json') and file != 'default.json':
                try:
                    with open(os.path.join(company_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        companies.append({
                            'code': data.get('company_code', file.replace('.json', '')),
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
    
    st.title("기업 재무 분석 대시보드")
    
    # 회사 선택 드롭다운
    companies = get_available_companies()
    
    # 빈 선택 옵션 추가
    company_names = ["기업을 선택하세요"] + [f"{c['name']} ({c['sector']})" for c in companies]
    company_codes = [None] + [c['code'] for c in companies]
    
    selected_index = st.selectbox(
        "분석할 기업 선택",
        range(len(company_names)),
        format_func=lambda i: company_names[i]
    )
    
    selected_company_code = company_codes[selected_index]
    
    # 슬라이드 메뉴
    st.sidebar.title("목차")
    slide_names = [
        "요약", 
        "손익계산서", 
        "재무상태표", 
        "현금흐름표", 
        "수익성 분석", 
        "성장성 분석", 
        "안정성 분석", 
        "운전자본 분석", 
        "종합 결론"
    ]
    selected_slide = st.sidebar.radio("분석 슬라이드 선택", slide_names)
    
    # 기업이 선택되었을 때만 슬라이드 표시
    if selected_company_code is not None:
        # 데이터 로더 초기화
        data_loader = DataLoader(selected_company_code)
        
        # 선택된 슬라이드 표시
        if selected_slide == "요약":
            SummarySlide(data_loader).render()
        elif selected_slide == "손익계산서":
            IncomeStatementSlide(data_loader).render()
        elif selected_slide == "재무상태표":
            BalanceSheetSlide(data_loader).render()
        elif selected_slide == "현금흐름표":
            CashFlowSlide(data_loader).render()
        elif selected_slide == "수익성 분석":
            ProfitabilitySlide(data_loader).render()
        elif selected_slide == "성장성 분석":
            GrowthRateSlide(data_loader).render()
        elif selected_slide == "안정성 분석":
            StabilitySlide(data_loader).render()
        elif selected_slide == "운전자본 분석":
            WorkingCapitalSlide(data_loader).render()
        elif selected_slide == "종합 결론":
            ConclusionSlide(data_loader).render()
    else:
        # 기업이 선택되지 않았을 때 안내 메시지 표시
        st.info("왼쪽 드롭다운에서 분석할 기업을 선택해주세요.")
        
if __name__ == "__main__":
    main()
