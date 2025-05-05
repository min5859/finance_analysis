import streamlit as st
import json
import base64

class IframeChartComponent:
    """iframe을 사용한 Chart.js 통합 컴포넌트"""
    
    @staticmethod
    def get_common_chart_options():
        """
        모든 차트 타입에 공통으로 적용되는 기본 옵션을 반환합니다.
        
        Returns:
            dict: 차트 공통 기본 옵션
        """
        return {
            "responsive": True,
            "maintainAspectRatio": False,
            "layout": {
                "padding": {
                    "left": 10,
                    "right": 10,
                    "top": -10,
                    "bottom": 30  # 하단에 더 많은 패딩 추가
                }
            },
            "interaction": {
                "mode": "index",
                "intersect": False
            },
            "plugins": {
                "legend": {
                    "position": "top",
                    "labels": {
                        "usePointStyle": True,
                        "font": {
                            "family": "'Noto Sans KR', sans-serif",
                            "size": 12
                        },
                        "padding": 20
                    }
                },
                "title": {
                    "display": False,
                    "text": "차트 제목",
                    "font": {
                        "family": "'Noto Sans KR', sans-serif",
                        "size": 18,
                        "weight": "600"
                    },
                    "padding": {
                        "top": 10,
                        "bottom": 20
                    }
                },
                "tooltip": {
                    "enabled": True,
                    "backgroundColor": "rgba(20, 20, 30, 0.95)",
                    "titleFont": {
                        "family": "'Noto Sans KR', sans-serif",
                        "size": 14
                    },
                    "bodyFont": {
                        "family": "'Noto Sans KR', sans-serif",
                        "size": 13
                    },
                    "padding": 12,
                    "cornerRadius": 8,
                    "caretSize": 6,
                    "boxPadding": 6
                }
            },
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "grid": {
                        "drawBorder": False,
                        "color": "rgba(200, 200, 200, 0.15)"
                    },
                    "ticks": {
                        "font": {
                            "family": "'Noto Sans KR', sans-serif",
                            "size": 12
                        },
                        "color": "#666",
                        "padding": 10
                    }
                },
                "x": {
                    "grid": {
                        "display": False
                    },
                    "ticks": {
                        "font": {
                            "family": "'Noto Sans KR', sans-serif",
                            "size": 12
                        },
                        "color": "#666",
                        "padding": 10
                    }
                }
            },
            "animation": {
                "duration": 1000,
                "easing": "easeOutQuart"
            }
        }
    
    @staticmethod
    def render_chart_in_card(chart_type, data, options=None, height=500, title=None, card_style=None, additional_scripts=None, use_datalabels=False):
        """
        Chart.js 차트를 카드 내부에 iframe으로 렌더링
        
        Args:
            chart_type (str): 차트 타입 (bar, line, radar 등)
            data (dict): 차트 데이터
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
            additional_scripts (str, optional): HTML <head>에 추가할 스크립트 태그
            use_datalabels (bool, optional): datalabels 플러그인 사용 여부
        """
        # 기본 카드 스타일
        default_card_style = {
            "background-color": "white",
            "border-radius": "16px",
            "padding": "20px",
            "box-shadow": "0 10px 25px rgba(0, 0, 0, 0.1), 0 5px 10px rgba(0, 0, 0, 0.05)",
            "margin-bottom": "20px",
            "border": "1px solid rgba(0, 0, 0, 0.05)",
            "transition": "all 0.3s ease"
        }
        
        # 사용자 정의 스타일 적용
        if card_style:
            default_card_style.update(card_style)
        
        # 카드 스타일 문자열 생성
        card_style_str = "; ".join([f"{k}: {v}" for k, v in default_card_style.items()])
        
        # datalabels 플러그인 스크립트
        datalabels_script = """
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
        <script>
            // 차트 생성 전에 datalabels 플러그인 등록
            if (typeof Chart !== 'undefined') {
                Chart.register(ChartDataLabels);
            }
        </script>
        """
        
        # 추가 라이브러리 및 폰트 추가
        additional_libs = """
        <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
        """
        
        # 추가 스크립트 준비
        scripts_to_include = additional_libs
        if use_datalabels:
            scripts_to_include += datalabels_script
        if additional_scripts:
            scripts_to_include += additional_scripts
        
        # HTML 템플릿 생성 (전체 웹 페이지)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            {scripts_to_include}
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                    font-family: 'Noto Sans KR', sans-serif;
                }}
                
                .chart-container {{
                    position: relative;
                    width: 100%;
                    height: {height}px;
                    padding: 10px;
                    box-sizing: border-box;
                    background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(250,250,255,0.6) 100%);
                    border-radius: 12px;
                }}
                
                .card-title {{
                    font-size: 20px;
                    font-weight: 600;
                    text-align: center;
                    margin-bottom: 24px;
                    color: #333;
                    letter-spacing: -0.02em;
                    position: relative;
                    padding-bottom: 10px;
                }}
                
                .card-title:after {{
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 40px;
                    height: 3px;
                    background: linear-gradient(90deg, #6366f1, #8b5cf6);
                    border-radius: 3px;
                }}
                
                .chart-backdrop {{
                    border-radius: 12px;
                    box-shadow: inset 0 0 10px rgba(0,0,0,0.03);
                    background-color: rgba(245,247,250,0.4);
                    width: 100%;
                    height: calc(100% - 60px);
                    position: absolute;
                    top: 60px;
                    left: 0;
                    z-index: 0;
                }}
                
                canvas {{
                    position: relative;
                    z-index: 1;
                }}
            </style>
        </head>
        <body>
            <div class="chart-container">
                {f'<div class="card-title">{title}</div>' if title else ''}
                <div class="chart-backdrop"></div>
                <canvas id="myChart"></canvas>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    // 차트 렌더링을 위한 컨텍스트 및 설정
                    const ctx = document.getElementById('myChart').getContext('2d');
                    const chartData = {json.dumps(data)};
                    const chartOptions = {json.dumps(options) if options else '{}'};
                    
                    // 그라디언트 생성 함수
                    function createGradient(ctx, color, start=0, end=1) {{
                        const gradient = ctx.createLinearGradient(0, 0, 0, ctx.canvas.height);
                        gradient.addColorStop(start, color + 'DD');
                        gradient.addColorStop(end, color + '22');
                        return gradient;
                    }}
                    
                    // 데이터셋에 그라디언트 적용
                    if (chartData.datasets && '{chart_type}' === 'bar') {{
                        chartData.datasets.forEach(dataset => {{
                            if (dataset.backgroundColor && typeof dataset.backgroundColor === 'string' && !dataset.backgroundColor.includes('gradient')) {{
                                dataset.backgroundColor = createGradient(ctx, dataset.backgroundColor);
                            }}
                        }});
                    }}
                    
                    // 차트 생성
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
            <iframe src="data:text/html;base64,{encoded}" width="100%" height="{height + 30}px" frameborder="0" scrolling="no"></iframe>
        </div>
        """
        
        # iframe HTML 렌더링
        st.markdown(iframe_html, unsafe_allow_html=True)
    
    @staticmethod
    def create_bar_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None, additional_scripts=None, use_datalabels=False):
        """
        막대 차트를 카드 내부에 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
            additional_scripts (str, optional): 추가적인 HTML 스크립트
            use_datalabels (bool, optional): datalabels 플러그인 사용 여부
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        # 공통 옵션 가져오기
        default_options = IframeChartComponent.get_common_chart_options()
        
        # bar 차트 특화 옵션 - 이미 공통 옵션에 포함되어 있으므로 추가 설정 불필요
        
        # datalabels 플러그인 사용 시 기본 옵션 추가
        if use_datalabels and "plugins" in default_options:
            default_options["plugins"]["datalabels"] = {
                "display": True,
                "color": "black",
                "font": {
                    "family": "'Noto Sans KR', sans-serif",
                    "weight": "bold",
                    "size": 11
                },
                "formatter": "function(value) { return value.toLocaleString(); }",
                "anchor": "end",
                "align": "top",
                "offset": 6,
                "backgroundColor": "rgba(255, 255, 255, 0.7)",
                "borderRadius": 4,
                "padding": 4
            }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card(
            "bar", data, default_options, height, title, card_style, 
            additional_scripts, use_datalabels
        )
    
    @staticmethod
    def create_line_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None, additional_scripts=None, use_datalabels=False):
        """
        선형 차트를 카드 내부에 생성
        
        Args:
            labels (list): x축 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
            additional_scripts (str, optional): 추가적인 HTML 스크립트
            use_datalabels (bool, optional): datalabels 플러그인 사용 여부
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        # 공통 옵션 가져오기
        default_options = IframeChartComponent.get_common_chart_options()
        
        # line 차트 특화 옵션
        default_options["elements"] = {
            "line": {
                "tension": 0.4
            },
            "point": {
                "radius": 4,
                "hoverRadius": 6,
                "borderWidth": 2
            }
        }
        
        # datalabels 플러그인 사용 시 기본 옵션 추가
        if use_datalabels and "plugins" in default_options:
            default_options["plugins"]["datalabels"] = {
                "display": True,
                "color": "black",
                "font": {
                    "family": "'Noto Sans KR', sans-serif",
                    "weight": "bold",
                    "size": 11
                },
                "formatter": "function(value) { return value.toLocaleString(); }",
                "anchor": "end",
                "align": "top",
                "offset": 6,
                "backgroundColor": "rgba(255, 255, 255, 0.7)",
                "borderRadius": 4,
                "padding": 4
            }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card(
            "line", data, default_options, height, title, card_style, 
            additional_scripts, use_datalabels
        )
    
    @staticmethod
    def create_radar_chart_in_card(labels, datasets, options=None, height=500, title=None, card_style=None, additional_scripts=None, use_datalabels=False):
        """
        레이더 차트를 카드 내부에 생성
        
        Args:
            labels (list): 각도 라벨
            datasets (list): 데이터셋 리스트
            options (dict, optional): 차트 옵션
            height (int, optional): 차트 높이
            title (str, optional): 카드 제목
            card_style (dict, optional): 카드 스타일
            additional_scripts (str, optional): 추가적인 HTML 스크립트
            use_datalabels (bool, optional): datalabels 플러그인 사용 여부
        """
        data = {
            "labels": labels,
            "datasets": datasets
        }
        
        # 공통 옵션 가져오기
        default_options = IframeChartComponent.get_common_chart_options()
        
        # radar 차트 특화 옵션
        default_options["scales"] = {
            "r": {
                "beginAtZero": True,
                "ticks": {
                    "display": True,
                    "backdropColor": "rgba(255, 255, 255, 0.75)",
                    "font": {
                        "family": "'Noto Sans KR', sans-serif",
                        "size": 10
                    },
                    "color": "#666"
                },
                "pointLabels": {
                    "font": {
                        "family": "'Noto Sans KR', sans-serif",
                        "size": 12,
                        "weight": "500"
                    },
                    "color": "#333"
                },
                "grid": {
                    "color": "rgba(200, 200, 200, 0.2)"
                },
                "angleLines": {
                    "color": "rgba(200, 200, 200, 0.4)"
                }
            }
        }
        
        default_options["elements"] = {
            "line": {
                "borderWidth": 2
            },
            "point": {
                "radius": 4,
                "hoverRadius": 6,
                "borderWidth": 2
            }
        }
        
        # datalabels 플러그인 사용 시 기본 옵션 추가
        if use_datalabels and "plugins" in default_options:
            default_options["plugins"]["datalabels"] = {
                "display": True,
                "color": "white",
                "backgroundColor": "function(context) { return context.dataset.borderColor; }",
                "borderRadius": 4,
                "font": {
                    "family": "'Noto Sans KR', sans-serif",
                    "weight": "bold",
                    "size": 10
                },
                "formatter": "function(value) { return value.toLocaleString(); }",
                "padding": 4,
                "textShadowBlur": 3,
                "textShadowColor": "rgba(0, 0, 0, 0.3)"
            }
        
        if options:
            # 중첩 사전 업데이트
            for k, v in options.items():
                if isinstance(v, dict) and k in default_options and isinstance(default_options[k], dict):
                    default_options[k].update(v)
                else:
                    default_options[k] = v
        
        IframeChartComponent.render_chart_in_card(
            "radar", data, default_options, height, title, card_style, 
            additional_scripts, use_datalabels
        )