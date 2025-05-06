import streamlit as st
import os
import json
from components.slides.base_slide import BaseSlide
from config.app_config import COLOR_PALETTE
import streamlit.components.v1 as components

class SummarySlide(BaseSlide):
    """요약 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Overview of Key Financial Metrics")
        self.company_info = data_loader.get_all_data()
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_key_metrics()
        self._render_highlights()
    
    def _render_key_metrics(self):
        """핵심 지표 렌더링"""
        # 데이터 가져오기
        performance_data = self.data_loader.get_performance_data()
        stability_data = self.data_loader.get_stability_data()
        profitability_data = self.data_loader.get_profitability_data()
        cash_flow_data = self.data_loader.get_cash_flow_data()

        # HTML 컴포넌트 생성
        html_content = """
        <div style="
            background: linear-gradient(145deg, #f8fafc, #f1f5f9);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        ">
            <h3 style="
                color: #334155;
                font-weight: 700;
                margin-bottom: 1.5rem;
                font-size: 1.5rem;
                display: flex;
                align-items: center;
            ">
                <span style="
                    background-color: #6366f1;
                    color: white;
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 0.75rem;
                    font-size: 1rem;
                ">📊</span>
                핵심 재무 지표 (2024년)
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
        """

        # 수익성 지표
        metrics = [
            {
                'label': '매출액',
                'value': f"{performance_data['매출액'].iloc[-1]:,.0f}억원",
                'delta': f"{((performance_data['매출액'].iloc[-1] / performance_data['매출액'].iloc[-2]) - 1) * 100:.1f}%",
                'color': '#4f46e5'
            },
            {
                'label': '영업이익',
                'value': f"{performance_data['영업이익'].iloc[-1]:,.0f}억원",
                'delta': f"{((performance_data['영업이익'].iloc[-1] / performance_data['영업이익'].iloc[-2]) - 1) * 100:.1f}%",
                'color': '#0ea5e9'
            },
            {
                'label': 'ROE',
                'value': f"{profitability_data['ROE'].iloc[-1]:.1f}%",
                'delta': f"{(profitability_data['ROE'].iloc[-1] - profitability_data['ROE'].iloc[-2]):.1f}%p",
                'color': '#8b5cf6'
            }
        ]

        for metric in metrics:
            delta_color = '#16a34a' if float(metric['delta'].replace('%p', '').replace('%', '').replace(',', '')) > 0 else '#dc2626'
            html_content += f"""
                <div style="
                    background: white;
                    padding: 1.25rem;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
                    border-left: 4px solid {metric['color']};
                ">
                    <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">{metric['label']}</div>
                    <div style="color: #111827; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">{metric['value']}</div>
                    <div style="color: {delta_color}; font-size: 0.875rem; font-weight: 500;">
                        {metric['delta']} (전년비)
                    </div>
                </div>
            """

        # 안정성 지표
        metrics = [
            {
                'label': '부채비율',
                'value': f"{stability_data['부채비율'].iloc[-1]:.1f}%",
                'delta': f"{-(stability_data['부채비율'].iloc[-2] - stability_data['부채비율'].iloc[-1]):.1f}%p",
                'color': '#ec4899'
            },
            {
                'label': '유동비율',
                'value': f"{stability_data['유동비율'].iloc[-1]:.1f}%",
                'delta': f"{(stability_data['유동비율'].iloc[-1] - stability_data['유동비율'].iloc[-2]):.1f}%p",
                'color': '#f59e0b'
            },
            {
                'label': '영업현금흐름',
                'value': f"{cash_flow_data['영업활동'].iloc[-1]:,.0f}억원",
                'delta': f"{cash_flow_data['영업활동'].iloc[-1] - cash_flow_data['영업활동'].iloc[-2]:,.0f}억원",
                'color': '#10b981'
            }
        ]

        for metric in metrics:
            delta_color = '#16a34a' if float(metric['delta'].replace('%p', '').replace('억원', '').replace(',', '')) > 0 else '#dc2626'
            html_content += f"""
                <div style="
                    background: white;
                    padding: 1.25rem;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
                    border-left: 4px solid {metric['color']};
                ">
                    <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">{metric['label']}</div>
                    <div style="color: #111827; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">{metric['value']}</div>
                    <div style="color: {delta_color}; font-size: 0.875rem; font-weight: 500;">
                        {metric['delta']} (전년비)
                    </div>
                </div>
            """

        html_content += """
            </div>
        </div>
        """
        
        components.html(html_content, height=400, scrolling=False)

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

        html_content = f"""
        <div style="
            background: linear-gradient(145deg, #f0f9ff, #e0f2fe);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06);
        ">
            <h3 style="
                color: #0369a1;
                font-weight: 700;
                font-size: 1.5rem;
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
                ">💡</span>
                재무 하이라이트
            </h3>

            <div style="
                background: rgba(255, 255, 255, 0.8);
                border-radius: 8px;
                padding: 1.25rem;
            ">
                <div style="margin-bottom: 1rem;">
                    <div style="
                        display: flex;
                        align-items: center;
                        color: #0369a1;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">
                        <span style="
                            color: #0ea5e9;
                            margin-right: 0.5rem;
                        ">●</span>
                        매출 성장
                    </div>
                    <div style="
                        color: #334155;
                        padding-left: 1.25rem;
                    ">{revenue_growth:.1f}% 성장률, {'양호한' if revenue_growth > 0 else '하락하는'} 매출 추세</div>
                </div>

                <div style="margin-bottom: 1rem;">
                    <div style="
                        display: flex;
                        align-items: center;
                        color: #0369a1;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">
                        <span style="
                            color: #0ea5e9;
                            margin-right: 0.5rem;
                        ">●</span>
                        수익성
                    </div>
                    <div style="
                        color: #334155;
                        padding-left: 1.25rem;
                    ">순이익률 {profit_margin:.1f}%, ROE {roe:.1f}%로 {'우수한' if profit_margin > 5 else '보통의'} 수익성 지표</div>
                </div>

                <div style="margin-bottom: 1rem;">
                    <div style="
                        display: flex;
                        align-items: center;
                        color: #0369a1;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">
                        <span style="
                            color: #0ea5e9;
                            margin-right: 0.5rem;
                        ">●</span>
                        순이익 성장
                    </div>
                    <div style="
                        color: #334155;
                        padding-left: 1.25rem;
                    ">전년 대비 {profit_growth:.1f}% {'증가' if profit_growth > 0 else '감소'}</div>
                </div>

                <div style="margin-bottom: 1rem;">
                    <div style="
                        display: flex;
                        align-items: center;
                        color: #0369a1;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">
                        <span style="
                            color: #0ea5e9;
                            margin-right: 0.5rem;
                        ">●</span>
                        재무 안정성
                    </div>
                    <div style="
                        color: #334155;
                        padding-left: 1.25rem;
                    ">부채비율 {debt_ratio:.1f}%로 {'매우 안정적인' if debt_ratio < 50 else '적정한' if debt_ratio < 100 else '다소 높은'} 재무구조</div>
                </div>

                <div>
                    <div style="
                        display: flex;
                        align-items: center;
                        color: #0369a1;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">
                        <span style="
                            color: #0ea5e9;
                            margin-right: 0.5rem;
                        ">●</span>
                        사업 전망
                    </div>
                    <div style="
                        color: #334155;
                        padding-left: 1.25rem;
                    ">{self.company_info.get('sector', '해당 업종')}의 경쟁력 및 시장 지위 분석 필요</div>
                </div>
            </div>
        </div>
        """
        
        components.html(html_content, height=500, scrolling=False)
