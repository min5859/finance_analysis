import streamlit as st
from components.slides.base_slide import BaseSlide
from components.charts.iframe_chart_component import IframeChartComponent
from config.app_config import COLOR_PALETTE
import os
import json
import datetime

class IndustryComparisonSlide(BaseSlide):
    """업계비교 현황 슬라이드"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader, "Comparative Financial Profile")
        self._load_company_info()
    
    def _load_company_info(self):
        """회사 정보 로드"""
        # 현재 연도를 가져옴
        current_year = str(datetime.datetime.now().year)
        
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
                    # report_year가 없으면 현재 연도를 기본값으로 추가
                    if 'report_year' not in self.company_info:
                        self.company_info['report_year'] = current_year
            except Exception:
                self.company_info = {
                    "company_name": "회사명 정보 없음",
                    "sector": "업종 정보 없음",
                    "report_year": current_year  # 현재 연도를 기본값으로 설정
                }
        else:
            self.company_info = {
                "company_name": "회사명 정보 없음",
                "sector": "업종 정보 없음",
                "report_year": current_year  # 현재 연도를 기본값으로 설정
            }
    
    def render(self):
        """슬라이드 렌더링"""
        self.render_header()
        self._render_radar_chart()
    
    def _render_radar_chart(self):
        """레이더 차트 렌더링"""
        radar_data = self.data_loader.get_radar_data()
        
        # 회사명 가져오기
        company_name = self.company_info.get('company_name', '회사')
        
        # 보고서 연도 가져오기 (JSON에서 가져오거나 현재 연도 사용)
        current_year = str(datetime.datetime.now().year)
        report_year = self.company_info.get('report_year', current_year)
        
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
            "layout": {
                "padding": {
                    "left": 10,
                    "right": 10,
                    "top": 0,
                    "bottom": 30  # 하단에 더 많은 패딩 추가
                }
            },
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
                    "display": False,
                    "text": f"재무지표 종합 비교 ({report_year}년)",  # JSON에서 가져온 연도 사용
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
                },
                "datalabels": {
                    "display": True,
                    "color": "black",
                    "font": {
                        "weight": "bold",
                        "size": 11
                    },
                    "formatter": "function(value) { return value.toLocaleString(); }",
                    "align": "end",
                    "offset": 10,
                    "borderRadius": 4,
                    "padding": 4
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
        
        # IframeChartComponent를 사용하여 레이더 차트 렌더링
        IframeChartComponent.create_radar_chart_in_card(
            labels=labels,
            datasets=datasets,
            options=options,
            height=450,
            title=f"재무지표 종합 비교 ({report_year}년)",  # JSON에서 가져온 연도 사용
            card_style={
                "background-color": "white",
                "border-radius": "10px",
                "padding": "0px",
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
                "margin-bottom": "0px"
            },
            use_datalabels=True  # datalabels 플러그인 사용 설정
        )
        
        # 차트 하단에 분석 요약 추가
        st.markdown(f"""
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