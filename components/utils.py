def get_print_button_html() -> str:
    """
    브라우저의 인쇄 기능을 호출하는 HTML 컴포넌트를 반환합니다.

    Returns:
        str: `window.print()`를 호출하는 스크립트와 버튼이 포함된 완전한 HTML 문자열.
    """
    button_html = """
    <div style="text-align: right; margin-top: 20px;">
        <button id="print-button" style="
            background-color: #4F46E5;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            font-weight: bold;
        ">
            PDF로 인쇄
        </button>
    </div>
    <script>
        document.getElementById('print-button').addEventListener('click', function() {
            window.print();
        });
    </script>
    """
    return button_html