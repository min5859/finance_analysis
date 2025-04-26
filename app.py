import streamlit as st
from config.app_config import setup_page_config, load_custom_css
from data.data_loader import DataLoader
from components.dashboard import Dashboard

def main():
    # 페이지 설정
    setup_page_config()
    
    # 커스텀 CSS 로드
    load_custom_css()
    
    # 데이터 로드
    data_loader = DataLoader()
    
    # 대시보드 생성 및 렌더링
    dashboard = Dashboard(data_loader)
    dashboard.render()

if __name__ == "__main__":
    main()
