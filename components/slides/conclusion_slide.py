import streamlit as st
from components.slides.base_slide import BaseSlide
import os
import json
import streamlit.components.v1 as components

class ConclusionSlide(BaseSlide):
    """종합 결론 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Comprehensive Assessment & Strategic Recommendations")
        self.company_info = data_loader.get_all_data()
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_strengths_weaknesses()
        self._render_strategic_recommendations()
   
    def _render_strengths_weaknesses(self):
        """강점과 개선 필요사항 렌더링"""
        html_content = """
        <div style="display: flex; gap: 1rem; margin-bottom: 0rem;">
            <div style="
                flex: 1;
                background: linear-gradient(145deg, #eef2ff, #e0e7ff);
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(66, 71, 184, 0.1), 0 2px 4px -1px rgba(66, 71, 184, 0.06);
                padding: 1.5rem;
                border-left: 6px solid #4f46e5;
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
        """

        for strength in self.company_info.get('conclusion', {}).get('strengths', []):
            html_content += f"""
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
                        <strong style="color: #4338ca;">{strength['title']}</strong> {strength['description']}
                    </span>
                </li>
            """

        html_content += """
                </ul>
            </div>

            <div style="
                flex: 1;
                background: linear-gradient(145deg, #fff1f2, #ffe4e6);
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.1), 0 2px 4px -1px rgba(239, 68, 68, 0.06);
                padding: 1.5rem;
                border-left: 6px solid #ef4444;
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
        """

        for weakness in self.company_info.get('conclusion', {}).get('weaknesses', []):
            html_content += f"""
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
                        <strong style="color: #b91c1c;">{weakness['title']}</strong> {weakness['description']}
                    </span>
                </li>
            """

        html_content += """
                </ul>
            </div>
        </div>
        """

        components.html(html_content, height=320, scrolling=False)
    
    def _render_strategic_recommendations(self):
        """전략적 제안 렌더링"""
        html_content = """
        <div style="
            background: linear-gradient(145deg, #f0f9ff, #e0f2fe);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.1), 0 2px 4px -1px rgba(14, 165, 233, 0.06);
            padding: 1.5rem;
            margin-top: 0rem;
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
        """

        for i, recommendation in enumerate(self.company_info.get('conclusion', {}).get('strategic_recommendations', []), 1):
            html_content += f"""
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
                        ">{i}</span>
                        {recommendation['title']}
                    </h4>
                    <ul style="
                        padding-left: 1.5rem;
                        margin-bottom: 0;
                    ">
            """
            
            for item in recommendation['items']:
                html_content += f"""
                        <li style="margin-bottom: 0.5rem;">{item}</li>
                """
            
            html_content += """
                    </ul>
                </div>
            """

        html_content += """
            </div>
        </div>
        """

        components.html(html_content, height=500, scrolling=False)
