import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.chart_js_component import ChartJSComponent
from config.app_config import COLOR_PALETTE
import os
import json

class IndustryComparisonSlide(BaseSlide):
    """업계비교 현황 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "업계비교 현황")
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
        self._render_radar_chart()
    
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
            ">{company_name} 업계비교 현황</h1>
            <p style="
                color: rgba(255, 255, 255, 0.9); 
                font-size: 1.1rem; 
                margin-top: 0.5rem;
                margin-bottom: 0;
                font-weight: 500;
            ">2024년 업계 대비 재무지표 비교</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_radar_chart(self):
        """레이더 차트 렌더링"""
        # 차트 상단에 매력적인 헤더 추가
        st.markdown("""
        <div style="
            text-align: center;
            margin-bottom: 1rem;
        ">
            <h3 style="
                color: #1e40af;
                font-weight: 700;
                display: inline-block;
                padding: 0.5rem 1.5rem;
                background: linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.1));
                border-radius: 9999px;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
                margin: 0;
            ">
                업계 비교 현황
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
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
                "backgroundColor": f"{COLOR_PALETTE['primary']}60",  # 더 진한 투명도
                "borderColor": COLOR_PALETTE["primary"],
                "borderWidth": 2,
                "pointBackgroundColor": COLOR_PALETTE["primary"],
                "pointHoverBackgroundColor": "#ffffff",
                "pointHoverBorderColor": COLOR_PALETTE["primary"],
                "pointHoverBorderWidth": 3,
                "pointHoverRadius": 7
            },
            {
                "label": "업계평균",
                "data": radar_data['업계평균'].tolist(),
                "backgroundColor": f"{COLOR_PALETTE['success']}40",
                "borderColor": COLOR_PALETTE["success"],
                "borderWidth": 2,
                "pointBackgroundColor": COLOR_PALETTE["success"],
                "pointHoverBackgroundColor": "#ffffff",
                "pointHoverBorderColor": COLOR_PALETTE["success"],
                "pointHoverBorderWidth": 3,
                "pointHoverRadius": 7
            }
        ]
        
        # Chart.js 옵션 설정 - 향상된 디자인
        options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {
                    "position": "top",
                    "labels": {
                        "font": {
                            "size": 14,
                            "weight": "bold"
                        },
                        "padding": 20,
                        "usePointStyle": True,
                        "pointStyleWidth": 10
                    }
                },
                "title": {
                    "display": True,
                    "text": f"재무지표 종합 비교 (2024년)",
                    "font": {
                        "size": 18,
                        "weight": "bold"
                    },
                    "padding": {
                        "top": 10,
                        "bottom": 30
                    }
                },
                "tooltip": {
                    "backgroundColor": "rgba(255, 255, 255, 0.9)",
                    "titleColor": "#1e40af",
                    "bodyColor": "#1f2937",
                    "titleFont": {
                        "weight": "bold"
                    },
                    "bodyFont": {
                        "size": 14
                    },
                    "borderColor": "#e5e7eb",
                    "borderWidth": 1,
                    "cornerRadius": 8,
                    "padding": 12,
                    "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                }
            },
            "scales": {
                "r": {
                    "beginAtZero": True,
                    "max": max(radar_data[company_column].max(), radar_data['업계평균'].max()) * 1.2,
                    "angleLines": {
                        "color": "rgba(210, 210, 210, 0.4)",
                        "lineWidth": 1
                    },
                    "grid": {
                        "color": "rgba(210, 210, 210, 0.4)",
                        "circular": True
                    },
                    "pointLabels": {
                        "font": {
                            "size": 12,
                            "weight": "bold"
                        },
                        "color": "#4b5563"
                    },
                    "ticks": {
                        "showLabelBackdrop": False,
                        "color": "#6b7280",
                        "backdropColor": "rgba(255, 255, 255, 0.75)"
                    }
                }
            },
            "elements": {
                "line": {
                    "tension": 0.1  # 더 부드러운 선
                }
            },
            "animation": {
                "duration": 2000,  # 애니메이션 지속 시간
                "easing": "easeOutQuart"  # 애니메이션 이징 함수
            }
        }
        
        # 차트 컨테이너에 스타일 적용
        st.markdown("""
        <div style="
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            padding: 1rem;
            margin-top: 1rem;
        ">
        """, unsafe_allow_html=True)
        
        # 차트 높이 증가
        with st.container():
            st.write("")  # 약간의 여백 추가
            # Chart.js로 차트 렌더링
            ChartJSComponent.create_radar_chart(labels, datasets, options, height=450)
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
        
        # 차트 하단에 분석 요약 추가
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, #f5f3ff, #ede9fe);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
            border-left: 4px solid #8b5cf6;
        ">
            <p style="
                margin: 0;
                color: #5b21b6;
                font-weight: 500;
                line-height: 1.6;
            ">
                <span style="font-weight: 700;">종합 평가:</span> 
                해당 기업은 업계 평균 대비 모든 주요 재무지표에서 우수한 성과를 보이고 있으며, 
                특히 <span style="font-weight: 700;">재무안정성</span>과 <span style="font-weight: 700;">수익성 지표</span>에서 
                탁월한 경쟁력을 갖추고 있습니다.
            </p>
        </div>
        """, unsafe_allow_html=True) 