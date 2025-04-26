import streamlit as st
from components.slides.summary_slide import SummarySlide
from components.slides.balance_sheet_slide import BalanceSheetSlide
from components.slides.income_statement_slide import IncomeStatementSlide
from components.slides.growth_rate_slide import GrowthRateSlide
from components.slides.profitability_slide import ProfitabilitySlide
from components.slides.stability_slide import StabilitySlide
from components.slides.cash_flow_slide import CashFlowSlide
from components.slides.working_capital_slide import WorkingCapitalSlide
from components.slides.conclusion_slide import ConclusionSlide

class Dashboard:
    """메인 대시보드 클래스"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.tabs = None
        self.slides = []
        self._setup_header()
        self._setup_slides()
    
    def _setup_header(self):
        """대시보드 헤더 설정"""
        st.markdown(
            '<div class="main-header">풍전비철 재무 분석<br>'
            '<span style="font-size: 1.5rem; font-weight: 400;">2022-2024년 재무성과 종합 분석</span></div>', 
            unsafe_allow_html=True
        )
    
    def _setup_slides(self):
        """모든 슬라이드 인스턴스 생성"""
        self.slides = [
            SummarySlide(self.data_loader),
            BalanceSheetSlide(self.data_loader),
            IncomeStatementSlide(self.data_loader),
            GrowthRateSlide(self.data_loader),
            ProfitabilitySlide(self.data_loader),
            StabilitySlide(self.data_loader),
            CashFlowSlide(self.data_loader),
            WorkingCapitalSlide(self.data_loader),
            ConclusionSlide(self.data_loader)
        ]
    
    def render(self):
        """대시보드 전체 렌더링"""
        # 탭 제목 가져오기
        tab_titles = [slide.get_title() for slide in self.slides]
        
        # 탭 생성
        self.tabs = st.tabs(tab_titles)
        
        # 각 탭에 슬라이드 렌더링
        for i, slide in enumerate(self.slides):
            with self.tabs[i]:
                slide.render()
