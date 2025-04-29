import streamlit as st
import json
import base64

class IframeChartComponent:
    """iframe을 사용한 Chart.js 통합 컴포넌트"""
    
    @staticmethod
    def render_chart_in_card(chart_type, data, options=None, height=500, title=None, card_style=None):
        """
        Chart.js 차트를 카드 내부에 iframe으로 렌더링
        
        Args:
            chart_type (str): 차트 타입 (bar, line, radar 등)
            data (dict): 차트 데이터
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
        """
        # 기본 카드 스타일
        default_card_style = {
            "background-color": "white",
            "border-radius": "10px",
            "padding": "20px",
            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08)",
            "margin-bottom": "20px"
        }
        
        # 사용자 정의 스타일 적용
        if card_style:
            default_card_style.update(card_style)
        
        # 카드 스타일 문자열 생성
        card_style_str = "; ".join([f"{k}: {v}" for k, v in default_card_style.items()])
        
        # HTML 템플릿 생성 (전체 웹 페이지)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                }}
                .chart-container {{
                    position: relative;
                    width: 100%;
                    height: {height}px;
                    padding: 10px;
                    box-sizing: border-box;
                }}
                .card-title {{
                    font-size: 18px;
                    font-weight: bold;
                    text-align: center;
                    margin-bottom: 20px;
                    color: #333;
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                {f'<div class="card-title">{title}</div>' if title else ''}
                <canvas id="myChart"></canvas>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const ctx = document.getElementById('myChart').getContext('2d');
                    const chartData = {json.dumps(data)};
                    const chartOptions = {json.dumps(options) if options else '{}'};
                    
                    new Chart(ctx, {{
                        type: '{chart_type}',
                        data: chartData,
                        options: chartOptions
                    }});
                }});
            </script>
        </body>
        </html>
        """
        
        # HTML을 base64로 인코딩
        html_bytes = html_content.encode('utf-8')
        encoded = base64.b64encode(html_bytes).decode()
        
        # iframe 생성을 위한 HTML
        iframe_html = f"""
        <div style="{card_style_str}">
            <iframe src="data:text/html;base64,{encoded}" width="100%" height="{height + 40}px" frameborder="0" scrolling="no"></iframe>
        </div>
        """
        
        # iframe HTML 렌더링
        st.markdown(iframe_html, unsafe_allow_html=True)
    
    @staticmethod
    def create_bar_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None):
        """
        막대 차트를 카드 내부에 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
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
                    "position": "top",
                    "labels": {
                        "font": {
                            "size": 12
                        }
                    }
                },
                "title": {
                    "display": True,
                    "text": "차트 제목",
                    "font": {
                        "size": 16
                    }
                },
                "tooltip": {
                    "enabled": True
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "ticks": {
                        "font": {
                            "size": 12
                        }
                    }
                },
                "x": {
                    "ticks": {
                        "font": {
                            "size": 12
                        }
                    }
                }
            }
        }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card("bar", data, default_options, height, title, card_style)
    
    @staticmethod
    def create_line_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None):
        """
        선형 차트를 카드 내부에 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
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
                    "position": "top",
                    "labels": {
                        "font": {
                            "size": 12
                        }
                    }
                },
                "title": {
                    "display": True,
                    "text": "차트 제목",
                    "font": {
                        "size": 16
                    }
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "ticks": {
                        "font": {
                            "size": 12
                        }
                    }
                },
                "x": {
                    "ticks": {
                        "font": {
                            "size": 12
                        }
                    }
                }
            }
        }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card("line", data, default_options, height, title, card_style)
    
    @staticmethod
    def create_radar_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None):
        """
        레이더 차트를 카드 내부에 생성
        
        Args:
            labels (list): 각도 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
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
                    "position": "top",
                    "labels": {
                        "font": {
                            "size": 12
                        }
                    }
                },
                "title": {
                    "display": True,
                    "text": "차트 제목",
                    "font": {
                        "size": 16
                    }
                }
            },
            "scales": {
                "r": {
                    "beginAtZero": True,
                    "ticks": {
                        "font": {
                            "size": 12
                        }
                    },
                    "pointLabels": {
                        "font": {
                            "size": 12
                        }
                    }
                }
            }
        }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card("radar", data, default_options, height, title, card_style)