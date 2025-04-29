import streamlit as st
from components.slides.base_slide import BaseSlide
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
        self._render_fancy_header()
        self._render_strengths_weaknesses()
        self._render_strategic_recommendations()
    
    def _render_fancy_header(self):
        """향상된 헤더 렌더링"""
        company_name = self.company_info.get('company_name', '회사')
        
        # 화려한 그라데이션 헤더
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #4338ca, #3b82f6, #0ea5e9); 
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
            ">{company_name} 재무비율 분석 종합 결론</h1>
            <p style="
                color: rgba(255, 255, 255, 0.9); 
                font-size: 1.1rem; 
                margin-top: 0.5rem;
                margin-bottom: 0;
                font-weight: 500;
            ">2022-2024년 재무성과 및 전략 방향성</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_strengths_weaknesses(self):
        """강점과 개선 필요사항 렌더링"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #eef2ff, #e0e7ff);
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(66, 71, 184, 0.1), 0 2px 4px -1px rgba(66, 71, 184, 0.06);
                padding: 1.5rem;
                border-left: 6px solid #4f46e5;
                height: 100%;
            ">
                <h3 style="
                    color: #4338ca;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                    display: flex;
                    align-items: center;
                ">
                    <span style="
                        background-color: #4f46e5;
                        color: white;
                        width: 32px;
                        height: 32px;
                        border-radius: 50%;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 0.75rem;
                        font-size: 1rem;
                    ">✓</span>
                    강점
                </h3>
                <ul style="
                    list-style-type: none;
                    padding-left: 0;
                    margin-bottom: 0;
                ">
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #4f46e5;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #4338ca;">업계 상위 수준의 수익성</strong> (ROE 14.4%, 순이익률 6.4%)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #4f46e5;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #4338ca;">뛰어난 재무안정성</strong> (부채비율 29%로 크게 개선)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #4f46e5;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #4338ca;">우수한 단기 지급능력</strong> (유동비율 209%)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #4f46e5;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #4338ca;">효율적인 운전자본 관리</strong> (CCC 66.9일로 단축)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #4f46e5;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #4338ca;">안정적인 그룹 계열사 시너지</strong> (지분법이익 207억원)
                        </span>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(145deg, #fff1f2, #ffe4e6);
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06);
                padding: 1.5rem;
                border-left: 6px solid #ef4444;
                height: 100%;
            ">
                <h3 style="
                    color: #b91c1c;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    font-size: 1.5rem;
                    display: flex;
                    align-items: center;
                ">
                    <span style="
                        background-color: #ef4444;
                        color: white;
                        width: 32px;
                        height: 32px;
                        border-radius: 50%;
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        margin-right: 0.75rem;
                        font-size: 1rem;
                    ">!</span>
                    개선 필요사항
                </h3>
                <ul style="
                    list-style-type: none;
                    padding-left: 0;
                    margin-bottom: 0;
                ">
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #ef4444;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #b91c1c;">매출액 감소 추세</strong> (-22.6% 성장률)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #ef4444;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #b91c1c;">자산회전율 하락</strong> (1.78회로 감소)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #ef4444;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #b91c1c;">2024년 현금흐름 악화</strong> (-146억원)
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #ef4444;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #b91c1c;">투자활동 감소로 성장동력 약화 우려</strong>
                        </span>
                    </li>
                    <li style="
                        margin-bottom: 0;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            color: #ef4444;
                            font-weight: bold;
                            margin-right: 0.5rem;
                        ">⬤</span>
                        <span style="line-height: 1.5;">
                            <strong style="color: #b91c1c;">신규 사업 발굴 필요성</strong>
                        </span>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_strategic_recommendations(self):
        """전략적 제안 렌더링"""
        import streamlit.components.v1 as components

        html_content = """
        <div style="
            background: linear-gradient(145deg, #f0f9ff, #e0f2fe);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06);
            padding: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        ">
            <h3 style="
                color: #0369a1;
                font-weight: 700;
                font-size: 1.5rem;
                border-bottom: 2px solid rgba(14, 165, 233, 0.2);
                padding-bottom: 0.75rem;
                margin-top: 0;
                margin-bottom: 1.25rem;
                display: flex;
                align-items: center;
            ">
                <span style="
                    background-color: #0ea5e9;
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 0.75rem;
                ">🚀</span>
                전략적 제안
            </h3>

            <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
                <div style="
                    flex: 1;
                    min-width: 250px;
                    background: rgba(14, 165, 233, 0.05);
                    border-radius: 8px;
                    padding: 1rem;
                    border-left: 4px solid #0ea5e9;
                ">
                    <h4 style="
                        color: #0369a1;
                        font-weight: 700;
                        margin-top: 0;
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            background-color: #0ea5e9;
                            color: white;
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            margin-right: 0.5rem;
                            font-size: 0.85rem;
                        ">1</span>
                        수익성 강화
                    </h4>
                    <ul style="
                        padding-left: 1.5rem;
                        margin-bottom: 0;
                    ">
                        <li style="margin-bottom: 0.5rem;">고마진 제품 포트폴리오 확대</li>
                        <li style="margin-bottom: 0.5rem;">비용 효율화 프로그램 지속</li>
                        <li>자산회전율 제고를 위한 운영 효율성 개선</li>
                    </ul>
                </div>

                <div style="
                    flex: 1;
                    min-width: 250px;
                    background: rgba(14, 165, 233, 0.05);
                    border-radius: 8px;
                    padding: 1rem;
                    border-left: 4px solid #0ea5e9;
                ">
                    <h4 style="
                        color: #0369a1;
                        font-weight: 700;
                        margin-top: 0;
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            background-color: #0ea5e9;
                            color: white;
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            margin-right: 0.5rem;
                            font-size: 0.85rem;
                        ">2</span>
                        성장동력 확보
                    </h4>
                    <ul style="
                        padding-left: 1.5rem;
                        margin-bottom: 0;
                    ">
                        <li style="margin-bottom: 0.5rem;">신규 사업 발굴 및 투자 확대</li>
                        <li style="margin-bottom: 0.5rem;">R&D 투자 강화</li>
                        <li>M&A 기회 모니터링</li>
                    </ul>
                </div>

                <div style="
                    flex: 1;
                    min-width: 250px;
                    background: rgba(14, 165, 233, 0.05);
                    border-radius: 8px;
                    padding: 1rem;
                    border-left: 4px solid #0ea5e9;
                ">
                    <h4 style="
                        color: #0369a1;
                        font-weight: 700;
                        margin-top: 0;
                        margin-bottom: 0.75rem;
                        display: flex;
                        align-items: center;
                    ">
                        <span style="
                            background-color: #0ea5e9;
                            color: white;
                            width: 24px;
                            height: 24px;
                            border-radius: 50%;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            margin-right: 0.5rem;
                            font-size: 0.85rem;
                        ">3</span>
                        재무건전성 유지
                    </h4>
                    <ul style="
                        padding-left: 1.5rem;
                        margin-bottom: 0;
                    ">
                        <li style="margin-bottom: 0.5rem;">현금흐름 관리 강화</li>
                        <li style="margin-bottom: 0.5rem;">적정 레버리지 수준 유지</li>
                        <li>배당정책 검토</li>
                    </ul>
                </div>
            </div>
        </div>
        """

        # components.html을 사용하여 HTML 콘텐츠 렌더링
        # 높이 값은 콘텐츠 크기에 맞게 조정하세요
        components.html(html_content, height=500, scrolling=False)
