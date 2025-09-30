import textwrap
from typing import List, Optional

import pandas as pd
import streamlit as st
from tabulate import tabulate

import fitz

class BaseSlide:
    """모든 슬라이드의 기본 클래스"""
    
    def __init__(self, data_loader, title="슬라이드"):
        self.data_loader = data_loader
        self.title = title
        self.pdf_sections: List[dict] = []
    
    def get_title(self):
        """슬라이드 제목 반환"""
        return self.title
    
    def render_header(self):
        """슬라이드 헤더 렌더링"""
        st.markdown(f'<h2 class="slide-header">{self.title}</h2>', unsafe_allow_html=True)

    def reset_pdf_sections(self):
        """PDF 섹션 초기화"""
        self.pdf_sections = []

    def add_pdf_section(self, title: str, content: str, kind: str = "text"):
        """PDF로 내보낼 섹션 추가"""
        if not content:
            return
        self.pdf_sections.append({
            "title": title,
            "content": content,
            "kind": kind
        })

    def add_table_section(self, title: str, data, headers: Optional[List[str]] = None):
        """표 형태의 데이터를 PDF 섹션으로 추가"""
        if data is None:
            return

        table_str = ""
        if isinstance(data, pd.DataFrame):
            if not data.empty:
                table_str = tabulate(data, headers="keys", tablefmt="grid", showindex=False)
        else:
            if headers is None:
                table_str = tabulate(data, headers="keys", tablefmt="grid", showindex=False)
            else:
                table_str = tabulate(data, headers=headers, tablefmt="grid", showindex=False)

        if table_str:
            self.add_pdf_section(title, table_str, kind="table")
    
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

    def render_pdf_export_button(self, filename: Optional[str] = None):
        """PDF 다운로드 버튼 렌더링"""
        if not self.pdf_sections:
            return

        pdf_bytes = self._create_pdf_document(self.pdf_sections)
        default_filename = f"{self.title.replace(' ', '_')}.pdf"
        st.download_button(
            "📄 PDF로 내보내기",
            data=pdf_bytes,
            file_name=filename or default_filename,
            mime="application/pdf",
            key=f"download_{self.title.replace(' ', '_')}"
        )

    def _create_pdf_document(self, sections: List[dict]) -> bytes:
        """섹션 정보를 기반으로 PDF 생성"""
        doc = fitz.open()
        page = doc.new_page()
        margin = 36
        y_position = margin

        for section in sections:
            page, y_position = self._insert_wrapped_text(doc, page, y_position, section["title"], fontsize=14, bold=True)
            y_position += 4

            if section["kind"] == "table":
                page, y_position = self._insert_table_text(doc, page, y_position, section["content"])
            else:
                page, y_position = self._insert_wrapped_text(doc, page, y_position, section["content"], fontsize=11)

            y_position += 8

        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes

    def _insert_wrapped_text(self, doc, page, y_position, text, fontsize=11, bold=False):
        """페이지에 줄바꿈 적용된 텍스트 삽입"""
        if not text:
            return page, y_position

        margin = 36
        max_width = page.rect.width - 2 * margin
        wrap_width = max(int(max_width / (fontsize * 0.55)), 20)
        fontname = "helv" if not bold else "helv"

        paragraphs = text.split("\n")
        for paragraph in paragraphs:
            lines = textwrap.wrap(paragraph, width=wrap_width) or [""]
            for line in lines:
                if y_position > page.rect.height - margin:
                    page = doc.new_page()
                    y_position = margin
                page.insert_text((margin, y_position), line, fontsize=fontsize, fontname=fontname)
                y_position += fontsize + 2
            y_position += 4

        return page, y_position

    def _insert_table_text(self, doc, page, y_position, table_text):
        """표 형태의 문자열을 PDF에 삽입"""
        if not table_text:
            return page, y_position

        margin = 36
        fontsize = 9
        for line in table_text.split("\n"):
            if y_position > page.rect.height - margin:
                page = doc.new_page()
                y_position = margin
            page.insert_text((margin, y_position), line, fontsize=fontsize, fontname="cour")
            y_position += fontsize + 2

        return page, y_position
