import streamlit as st
import json

class ChartJSComponent:
    """Chart.js를 사용하기 위한 기본 컴포넌트"""
    
    @staticmethod
    def render_chart(chart_type, data, options=None, height=500):
        """
        Chart.js 차트를 렌더링하는 메서드
        
        Args:
            chart_type (str): 차트 타입 (bar, line, radar 등)
            data (dict): 차트 데이터
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
        """
        chart_id = f"chart_{hash(str(data))}"
        
        # Chart.js 스크립트와 HTML
        chart_js = f"""
        <div style="height: {height}px; width: 100%;">
            <canvas id="{chart_id}"></canvas>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            // DOMContentLoaded 이벤트를 사용하여 문서가 로드된 후 차트 생성
            document.addEventListener('DOMContentLoaded', function() {{
                const ctx = document.getElementById('{chart_id}');
                if (ctx) {{
                    const data = {json.dumps(data)};
                    const options = {json.dumps(options) if options else '{}'};
                    
                    new Chart(ctx, {{
                        type: '{chart_type}',
                        data: data,
                        options: options
                    }});
                }}
            }});
            
            // Streamlit의 리렌더링 이벤트를 감지하여 차트 다시 생성
            const observer = new MutationObserver(function(mutations) {{
                const canvas = document.getElementById('{chart_id}');
                if (canvas && !canvas.chart) {{
                    const data = {json.dumps(data)};
                    const options = {json.dumps(options) if options else '{}'};
                    
                    canvas.chart = new Chart(canvas, {{
                        type: '{chart_type}',
                        data: data,
                        options: options
                    }});
                }}
            }});
            
            observer.observe(document.body, {{ childList: true, subtree: true }});
        </script>
        """
        
        st.components.v1.html(chart_js, height=height + 50)
    
    @staticmethod
    def create_bar_chart(labels, datasets, options=None, height=500):
        """
        막대 차트 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        default_options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": "차트 제목"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
        
        if options:
            default_options.update(options)
        
        ChartJSComponent.render_chart("bar", data, default_options, height)
    
    @staticmethod
    def create_line_chart(labels, datasets, options=None, height=500):
        """
        선형 차트 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        default_options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": "차트 제목"
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True
                }
            }
        }
        
        if options:
            default_options.update(options)
        
        ChartJSComponent.render_chart("line", data, default_options, height)
    
    @staticmethod
    def create_radar_chart(labels, datasets, options=None, height=500):
        """
        레이더 차트 생성
        
        Args:
            labels (list): 각도 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        default_options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {
                    "position": "top"
                },
                "title": {
                    "display": True,
                    "text": "차트 제목"
                }
            },
            "scales": {
                "r": {
                    "beginAtZero": True
                }
            }
        }
        
        if options:
            default_options.update(options)
        
        ChartJSComponent.render_chart("radar", data, default_options, height)