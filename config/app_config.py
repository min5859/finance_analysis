import streamlit as st

def setup_page_config():
    """페이지 기본 설정"""
    st.set_page_config(
        layout="wide", 
        page_title="풍전비철 재무 분석",
        page_icon="📊"
    )

def load_custom_css():
    """커스텀 CSS 로드"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem !important;
            font-weight: 700 !important;
            color: white !important;
            background: linear-gradient(to right, #4f46e5, #3b82f6);
            padding: 1.5rem;
            border-radius: 0.75rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .slide-header {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #1f2937 !important;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: #4b5563 !important;
            margin-bottom: 1rem;
        }
        .info-card {
            background-color: #f9fafb;
            border-radius: 0.5rem;
            padding: 1rem;
            border: 1px solid #e5e7eb;
            margin-bottom: 1rem;
        }
        .insight-card {
            background: linear-gradient(to right, #f3f4f6, #f9fafb);
            border-radius: 0.5rem;
            padding: 1rem;
            border: 1px solid #e5e7eb;
            margin-top: 1rem;
        }
        .metric-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .highlight {
            color: #4f46e5;
            font-weight: 600;
        }
        .negative {
            color: #ef4444;
            font-weight: 600;
        }
        .positive {
            color: #10b981;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

# 색상 팔레트 정의
COLOR_PALETTE = {
    "primary": "#4f46e5",    # 인디고
    "secondary": "#3b82f6",  # 블루
    "success": "#10b981",    # 에메랄드
    "warning": "#f59e0b",    # 앰버
    "danger": "#ef4444",     # 레드
    "info": "#8b5cf6",       # 퍼플
    "light": "#f3f4f6",      # 라이트 그레이
    "dark": "#1f2937"        # 다크 그레이
}
