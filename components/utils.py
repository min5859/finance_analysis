import streamlit as st
import base64

def get_pdf_print_script(title: str) -> str:
    """
    슬라이드 콘텐츠를 PDF로 인쇄하는 JavaScript 코드를 반환합니다.

    Args:
        title (str): PDF 파일의 제목입니다.

    Returns:
        str: 실행할 JavaScript 코드입니다.
    """
    # 참고: 이 접근 방식은 html2pdf.js를 사용하여 클라이언트 측에서 PDF를 생성합니다.
    # Streamlit의 동적이고 복잡한 CSS-in-JS 스타일링으로 인해,
    # 생성된 PDF의 스타일이 원본 페이지와 완벽하게 일치하지 않을 수 있습니다.
    # 특히 동적으로 로드되는 차트나 복잡한 컴포넌트에서 스타일 깨짐이 발생할 수 있습니다.
    pdf_print_js = f"""
    <script>
    function printAsPDF() {{
        const element = document.getElementById('pdf-content');
        if (element) {{
            // 모든 'st-emotion-cache' 클래스를 가진 요소의 스타일을 직접 주입합니다.
            const styledElements = element.querySelectorAll('[class*="st-emotion-cache"]');
            styledElements.forEach(el => {{
                const styles = window.getComputedStyle(el);
                let styleString = '';
                for (let i = 0; i < styles.length; i++) {{
                    const key = styles[i];
                    const value = styles.getPropertyValue(key);
                    // 특정 스타일은 제외합니다.
                    if (key.indexOf('font') !== -1 || key.indexOf('color') !== -1 || key.indexOf('background') !== -1 || key.indexOf('padding') !== -1 || key.indexOf('margin') !== -1 || key.indexOf('border') !== -1 || key.indexOf('display') !== -1 || key.indexOf('justify-content') !== -1 || key.indexOf('align-items') !==-1 || key.indexOf('width') !== -1) {{
                        styleString += `${{key}}: ${{value}}; `;
                    }}
                }}
                el.setAttribute('style', styleString);
            }});

            const opt = {{
                margin:       [0.5, 0.5, 0.5, 0.5],
                filename:     '{title}.pdf',
                image:        {{ type: 'jpeg', quality: 0.98 }},
                html2canvas:  {{ scale: 2, useCORS: true, letterRendering: true }},
                jsPDF:        {{ unit: 'in', format: 'letter', orientation: 'portrait' }},
                pagebreak:    {{ mode: ['avoid-all', 'css', 'legacy'] }}
            }};

            // html2pdf 라이브러리를 사용하여 PDF를 생성합니다.
            html2pdf().from(element).set(opt).save();
        }}
    }}

    // html2pdf.js 스크립트를 동적으로 로드합니다.
    if (!window.html2pdf) {{
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js';
        document.head.appendChild(script);
    }}
    </script>
    """
    return pdf_print_js