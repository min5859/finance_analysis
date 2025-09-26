import streamlit as st
from components.utils import get_pdf_print_script

class BaseSlide:
    """모든 슬라이드의 기본 클래스"""
    
    def __init__(self, data_loader=None, title="슬라이드"):
        self.data_loader = data_loader
        self.title = title
    
    def get_title(self):
        """슬라이드 제목 반환"""
        return self.title
    
    def render_header(self):
        """슬라이드 헤더 렌더링"""
        st.markdown(f'<h2 class="slide-header">{self.title}</h2>', unsafe_allow_html=True)
    
    def render_pdf_button(self):
        """PDF 인쇄 버튼 렌더링"""
        # 각 버튼에 고유한 키를 부여하여 상태 충돌 방지
        button_key = f"pdf_button_{self.title.replace(' ', '_')}"

        if st.button("PDF로 인쇄", key=button_key, type="primary"):
            # JavaScript를 직접 호출하는 대신 세션 상태를 사용하여 트리거
            st.session_state['run_pdf_print'] = True
            st.session_state['pdf_print_title'] = self.title

        if st.session_state.get('run_pdf_print', False) and st.session_state.get('pdf_print_title') == self.title:
            st.markdown(get_pdf_print_script(self.title), unsafe_allow_html=True)
            st.markdown('<script>printAsPDF();</script>', unsafe_allow_html=True)
            st.session_state['run_pdf_print'] = False
            st.session_state['pdf_print_title'] = None

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
    
    def render_content(self):
        """슬라이드 콘텐츠 렌더링 - 자식 클래스에서 구현해야 함"""
        st.warning("이 슬라이드는 아직 구현되지 않았습니다.")

    def render(self):
        """전체 슬라이드 렌더링 파이프라인"""
        self.render_header()

        st.markdown('<div id="pdf-content">', unsafe_allow_html=True)
        self.render_content()
        st.markdown('</div>', unsafe_allow_html=True)

        # "재무제표 분석 시작" 슬라이드에서는 PDF 버튼을 렌더링하지 않음
        if self.title != "재무제표 분석 시작":
            self.render_pdf_button()
