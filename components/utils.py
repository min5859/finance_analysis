def get_print_button_html() -> str:
    """
    브라우저의 인쇄 기능을 호출하는 HTML 버튼을 반환합니다.

    Returns:
        str: `window.print()`를 호출하는 `onclick` 이벤트가 포함된 HTML 버튼 문자열.
    """
    button_html = """
    <div style="text-align: right; margin-top: 20px;">
        <button onclick="window.print()" style="
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
    """
    return button_html