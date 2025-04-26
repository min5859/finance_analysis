import streamlit as st

class BaseSlide:
    """모든 슬라이드의 기본 클래스"""
    
    def __init__(self, data_loader, title="슬라이드"):
        self.data_loader = data_loader
        self.title = title
    
    def get_title(self):
        """슬라이드 제목 반환"""
        return self.title
    
    def render_header(self):
        """슬라이드 헤더 렌더링"""
        st.markdown(f'<h2 class="slide-header">{self.title}</h2>', unsafe_allow_html=True)
    
    def render_insight_card(self, title, content):
        """인사이트 카드 렌더링"""
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="font-weight: bold;">{title}</h4>', unsafe_allow_html=True)
        st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_info_card(self, title, color, metrics_data, footer_text=None):
        """정보 카드 렌더링"""
        st.markdown(f'<div class="info-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="text-align: center; color: {color};">{title}</h3>', unsafe_allow_html=True)
        
        for idx, row in metrics_data.iterrows():
            year = row.get('year', '')
            value = row.get('value', '')
            value_class = "negative" if value < 0 else "highlight" if isinstance(value, (int, float)) else "highlight"
            
            st.markdown(
                f'<div class="metric-container">'
                f'<span>{year}년</span><span class="{value_class}">{value}</span>'
                f'</div>', 
                unsafe_allow_html=True
            )
        
        if footer_text:
            st.markdown(
                f'<div style="text-align: right; font-size: 0.8rem; margin-top: 0.5rem;">{footer_text}</div>', 
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render(self):
        """슬라이드 렌더링 - 자식 클래스에서 구현해야 함"""
        self.render_header()
        st.warning("이 슬라이드는 아직 구현되지 않았습니다.")
