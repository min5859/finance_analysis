import streamlit as st
import pandas as pd
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class SummarySlide(BaseSlide):
    """핵심 요약 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "핵심 요약")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_summary_cards()
        self._render_key_insights()
    
    def _render_summary_cards(self):
        """핵심 지표 요약 카드 렌더링"""
        col1, col2, col3, col4 = st.columns(4)
        
        # ROE 카드
        with col1:
            roe_data = self.data_loader.get_profitability_data()[['year', 'ROE']].copy()
            roe_data.columns = ['year', 'value']
            self.render_info_card(
                "ROE (자기자본이익률)",
                COLOR_PALETTE["primary"],
                roe_data,
                "업계평균 8.5% 대비 1.7배↑"
            )
        
        # 순이익률 카드
        with col2:
            profit_margin_data = self.data_loader.get_profitability_data()[['year', '순이익률']].copy()
            profit_margin_data.columns = ['year', 'value']
            self.render_info_card(
                "순이익률",
                COLOR_PALETTE["success"],
                profit_margin_data,
                "지속적 수익성 개선↑"
            )
        
        # 부채비율 카드
        with col3:
            debt_ratio_data = self.data_loader.get_stability_data()[['year', '부채비율']].copy()
            debt_ratio_data.columns = ['year', 'value']
            self.render_info_card(
                "부채비율",
                COLOR_PALETTE["warning"],
                debt_ratio_data,
                "재무구조 개선 중↓"
            )
        
        # FCF 카드
        with col4:
            fcf_data = self.data_loader.get_cash_flow_data()[['year', 'FCF']].copy()
            fcf_data.columns = ['year', 'value']
            self.render_info_card(
                "현금창출력 (FCF)",
                COLOR_PALETTE["secondary"],
                fcf_data,
                "운전자본 급증 주의↓"
            )
    
    def _render_key_insights(self):
        """핵심 인사이트 렌더링"""
        st.markdown('<h3 class="sub-header">핵심 인사이트</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_strengths()
        
        with col2:
            self._render_weaknesses()
    
    def _render_strengths(self):
        """강점 섹션 렌더링"""
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color: {COLOR_PALETTE["primary"]};">강점</h4>', unsafe_allow_html=True)
        st.markdown("""
        - 업계 상위 수준의 수익성 (ROE 14.4%, 순이익률 6.4%)
        - 뛰어난 재무안정성 (부채비율 29%로 크게 개선)
        - 우수한 단기 지급능력 (유동비율 209%)
        - 효율적인 운전자본 관리 (CCC 66.9일로 단축)
        - 안정적인 그룹 계열사 시너지 (지분법이익 207억원)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_weaknesses(self):
        """개선 필요사항 섹션 렌더링"""
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color: {COLOR_PALETTE["danger"]};">개선 필요사항</h4>', unsafe_allow_html=True)
        st.markdown("""
        - 2024년 운전자본 급증으로 현금흐름 일시 악화
        - 자산회전율 감소 추세 (2.56회 → 1.78회)
        - 매출채권 및 재고자산 관리 강화 필요
        - 원자재 가격 변동성 대응 체계 구축
        - 지분법이익 의존도 축소를 통한 수익구조 개선
        """)
        st.markdown('</div>', unsafe_allow_html=True)
