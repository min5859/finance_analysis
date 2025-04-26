import streamlit as st
import plotly.graph_objects as go
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE

class ConclusionSlide(BaseSlide):
    """종합 결론 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "재무비율 분석 종합 결론")
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_strengths_weaknesses()
        self._render_strategic_recommendations()
        self._render_radar_chart()
    
    def _render_strengths_weaknesses(self):
        """강점과 개선 필요사항 렌더링"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="info-card" style="background: linear-gradient(to right, #eef2ff, #e0e7ff);">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: {COLOR_PALETTE["primary"]}; font-weight: bold;">강점</h3>', unsafe_allow_html=True)
            st.markdown("""
            - 업계 상위 수준의 수익성 (ROE 14.4%, 순이익률 6.4%)
            - 뛰어난 재무안정성 (부채비율 29%로 크게 개선)
            - 우수한 단기 지급능력 (유동비율 209%)
            - 효율적인 운전자본 관리 (CCC 66.9일로 단축)
            - 안정적인 그룹 계열사 시너지 (지분법이익 207억원)
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card" style="background: linear-gradient(to right, #fee2e2, #fef2f2);">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: {COLOR_PALETTE["danger"]}; font-weight: bold;">개선 필요사항</h3>', unsafe_allow_html=True)
            st.markdown("""
            - 2024년 운전자본 급증으로 현금흐름 일시 악화
            - 자산회전율 감소 추세 (2.56회 → 1.78회)
            - 매출채권 및 재고자산 관리 강화 필요
            - 원자재 가격 변동성 대응 체계 구축
            - 지분법이익 의존도 축소를 통한 수익구조 개선
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_strategic_recommendations(self):
        """전략적 제언 렌더링"""
        st.markdown('<div class="info-card" style="background: linear-gradient(to right, #ede9fe, #ddd6fe); margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: {COLOR_PALETTE["info"]}; font-weight: bold;">전략적 제언</h3>', unsafe_allow_html=True)
        st.markdown("""
        풍전비철은 탄탄한 재무구조와 우수한 수익성을 바탕으로 안정적 성장을 지속하고 있습니다. 2차전지 재활용 등 신성장 동력 확보를 위한 투자가 진행 중이며, 이에 따른 일시적 현금흐름 악화는 투자 회수 시점에 개선될 전망입니다.
        
        **단기 과제:**
        - 운전자본 관리 강화를 통한 현금흐름 개선
        - 자산효율성 제고를 위한 전략적 자산 재배치
        
        **중장기 과제:**
        - 신성장 동력 확보를 통한 매출 성장세 회복
        - 고부가가치 제품 라인업 확대로 수익성 강화 지속
        - 적정 레버리지 활용을 통한 자본효율성 개선
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_radar_chart(self):
        """레이더 차트 렌더링"""
        radar_data = self.data_loader.get_radar_data()
        
        # 플롯리 차트 생성
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=radar_data['풍전비철'],
            theta=radar_data['metric'],
            fill='toself',
            name='풍전비철',
            line_color=COLOR_PALETTE["primary"]
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=radar_data['업계평균'],
            theta=radar_data['metric'],
            fill='toself',
            name='업계평균',
            line_color=COLOR_PALETTE["success"]
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(radar_data['풍전비철'].max(), radar_data['업계평균'].max()) * 1.2]
                )
            ),
            title='재무지표 종합 비교 (2024년)',
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
