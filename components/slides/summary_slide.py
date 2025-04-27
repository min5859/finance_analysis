import streamlit as st
import os
import json
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class SummarySlide(BaseSlide):
    """요약 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "기업 개요 및 핵심 지표")
        self._load_company_info()
    
    def _load_company_info(self):
        """회사 정보 로드"""
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        company_dir = os.path.join(data_dir, "data/companies")
        
        if self.data_loader.company_code:
            json_file = os.path.join(company_dir, f"{self.data_loader.company_code}.json")
        else:
            json_file = os.path.join(company_dir, "default.json")
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.company_info = json.load(f)
            except Exception:
                self.company_info = {
                    "company_name": "회사명 정보 없음",
                    "company_code": "000000",
                    "sector": "업종 정보 없음"
                }
        else:
            self.company_info = {
                "company_name": "회사명 정보 없음",
                "company_code": "000000",
                "sector": "업종 정보 없음"
            }
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_highlights()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        st.markdown("### 핵심 재무 지표 (2024년)")
        
        # 데이터 가져오기
        performance_data = self.data_loader.get_performance_data()
        stability_data = self.data_loader.get_stability_data()
        profitability_data = self.data_loader.get_profitability_data()
        
        # 1행: 수익성 지표
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="매출액", 
                value=f"{performance_data['매출액'].iloc[-1]}억원",
                delta=f"{((performance_data['매출액'].iloc[-1] / performance_data['매출액'].iloc[-2]) - 1) * 100:.1f}% (전년비)",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                label="영업이익", 
                value=f"{performance_data['영업이익'].iloc[-1]}억원",
                delta=f"{((performance_data['영업이익'].iloc[-1] / performance_data['영업이익'].iloc[-2]) - 1) * 100:.1f}% (전년비)",
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                label="ROE", 
                value=f"{profitability_data['ROE'].iloc[-1]}%",
                delta=f"{(profitability_data['ROE'].iloc[-1] - profitability_data['ROE'].iloc[-2]):.1f}%p (전년비)",
                delta_color="normal"
            )
        
        # 2행: 안정성 지표
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="부채비율", 
                value=f"{stability_data['부채비율'].iloc[-1]}%",
                delta=f"{-(stability_data['부채비율'].iloc[-2] - stability_data['부채비율'].iloc[-1]):.1f}%p (전년비)",
                delta_color="inverse"
            )
        
        with col2:
            st.metric(
                label="유동비율", 
                value=f"{stability_data['유동비율'].iloc[-1]}%",
                delta=f"{(stability_data['유동비율'].iloc[-1] - stability_data['유동비율'].iloc[-2]):.1f}%p (전년비)",
                delta_color="normal"
            )
        
        cash_flow_data = self.data_loader.get_cash_flow_data()
        with col3:
            st.metric(
                label="영업현금흐름", 
                value=f"{cash_flow_data['영업활동'].iloc[-1]}억원",
                delta=f"{cash_flow_data['영업활동'].iloc[-1] - cash_flow_data['영업활동'].iloc[-2]}억원 (전년비)",
                delta_color="normal"
            )
    
    def _render_highlights(self):
        """주요 하이라이트 렌더링"""
        performance_data = self.data_loader.get_performance_data()
        profitability_data = self.data_loader.get_profitability_data()
        stability_data = self.data_loader.get_stability_data()
        growth_rates = self.data_loader.get_growth_rates()
        
        # 주요 특징 계산
        revenue_growth = growth_rates['매출액성장률'].iloc[-1]
        profit_growth = growth_rates['순이익성장률'].iloc[-1]
        profit_margin = performance_data['순이익률'].iloc[-1]
        roe = profitability_data['ROE'].iloc[-1]
        debt_ratio = stability_data['부채비율'].iloc[-1]
        
        insight_content = f"""
        **재무 하이라이트:**
        
        1. **매출 성장**: {revenue_growth:.1f}% 성장률, {'양호한' if revenue_growth > 0 else '하락하는'} 매출 추세
        2. **수익성**: 순이익률 {profit_margin:.1f}%, ROE {roe:.1f}%로 {'우수한' if profit_margin > 5 else '보통의'} 수익성 지표
        3. **순이익 성장**: 전년 대비 {profit_growth:.1f}% {'증가' if profit_growth > 0 else '감소'}
        4. **재무 안정성**: 부채비율 {debt_ratio:.1f}%로 {'매우 안정적인' if debt_ratio < 50 else '적정한' if debt_ratio < 100 else '다소 높은'} 재무구조
        5. **사업 전망**: {self.company_info.get('sector', '해당 업종')}의 경쟁력 및 시장 지위 분석 필요
        """
        
        self.render_insight_card("재무 하이라이트", insight_content)
