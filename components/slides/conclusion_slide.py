import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
from config.app_config import COLOR_PALETTE
import os
import json

class ConclusionSlide(BaseSlide):
    """종합 결론 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "재무비율 분석 종합 결론")
        self._load_company_info()
    
    def _load_company_info(self):
        """회사 정보 로드"""
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        company_dir = os.path.join(data_dir, "data/companies")
        
        if self.data_loader.json_filename:
            json_file = os.path.join(company_dir, f"{self.data_loader.json_filename}")
        else:
            json_file = os.path.join(company_dir, "default.json")
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.company_info = json.load(f)
            except Exception:
                self.company_info = {
                    "company_name": "회사명 정보 없음",
                    "sector": "업종 정보 없음"
                }
        else:
            self.company_info = {
                "company_name": "회사명 정보 없음",
                "sector": "업종 정보 없음"
            }
    
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
            st.markdown('<div class="info-card" style="background: linear-gradient(to right, #fff1f2, #ffe4e6);">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: {COLOR_PALETTE["danger"]}; font-weight: bold;">개선 필요사항</h3>', unsafe_allow_html=True)
            st.markdown("""
            - 매출액 감소 추세 (-22.6% 성장률)
            - 자산회전율 하락 (1.78회로 감소)
            - 2024년 현금흐름 악화 (-146억원)
            - 투자활동 감소로 성장동력 약화 우려
            - 신규 사업 발굴 필요성
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def _render_strategic_recommendations(self):
        """전략적 제안 렌더링"""
        st.markdown("""
        ### 전략적 제안
        
        1. **수익성 강화**
           - 고마진 제품 포트폴리오 확대
           - 비용 효율화 프로그램 지속
           - 자산회전율 제고를 위한 운영 효율성 개선
        
        2. **성장동력 확보**
           - 신규 사업 발굴 및 투자 확대
           - R&D 투자 강화
           - M&A 기회 모니터링
        
        3. **재무건전성 유지**
           - 현금흐름 관리 강화
           - 적정 레버리지 수준 유지
           - 배당정책 검토
        """)
    
    def _render_radar_chart(self):
        """레이더 차트 렌더링"""
        radar_data = self.data_loader.get_radar_data()
        
        # 회사명 가져오기
        company_name = self.company_info.get('company_name', '회사')
        
        # Chart.js 데이터셋 준비
        labels = radar_data['metric'].tolist()
        
        # 데이터셋의 첫 번째 회사명(컬럼명) 가져오기
        company_columns = [col for col in radar_data.columns if col != 'metric']
        company_column = company_columns[0] if company_columns else '회사'
        
        datasets = [
            {
                "label": company_name,
                "data": radar_data[company_column].tolist(),
                "backgroundColor": f"{COLOR_PALETTE['primary']}40",
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 2,
                "pointBackgroundColor": COLOR_PALETTE["primary"]
            },
            {
                "label": "업계평균",
                "data": radar_data['업계평균'].tolist(),
                "backgroundColor": f"{COLOR_PALETTE['success']}40",
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 2,
                "pointBackgroundColor": COLOR_PALETTE["success"]
            }
        ]
        
        # Chart.js 옵션 설정
        options = {
            "responsive": True,
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": f"재무지표 종합 비교 (2024년)"
                }
            },
            "scales": {
                "r": {
                    "beginAtZero": True,
                    "max": max(radar_data[company_column].max(), radar_data['업계평균'].max()) * 1.2
                }
            }
        }
        
        # Chart.js로 차트 렌더링
        ChartJSComponent.create_radar_chart(labels, datasets, options)
