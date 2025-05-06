import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from typing import Dict, Any

class ValuationDisplay:
    def __init__(self, valuation_data: Dict[str, Any]):
        """기업가치 평가 결과 표시 클래스 초기화
        
        Args:
            valuation_data (dict): 기업가치 평가 결과
        """
        self.valuation_data = valuation_data
        self.company_name = valuation_data.get("company", "기업명 없음")
        self.ebitda_valuation = valuation_data.get("ebitda_valuation", {})
        self.dcf_valuation = valuation_data.get("dcf_valuation", {})
        self.assumptions = valuation_data.get("assumptions", {})
        self.calculations = valuation_data.get("calculations", {})
        self.summary = valuation_data.get("summary", "")
        self.scenarios = ["보수적", "기본", "낙관적"]
        
    def display(self):
        """기업가치 평가 결과를 표시"""
        if not self.valuation_data:
            st.error("기업가치 평가 데이터가 없습니다.")
            return
            
        self._add_custom_styles()
        self._display_header()
        self._display_valuation_results()
        self._display_assumptions()
        self._display_calculations()
        
    def _display_header(self):
        """헤더와 요약 정보 표시"""
        st.markdown(f"""
        <div class="valuation-header">
            <div class="valuation-header-title">{self.company_name} 기업가치 평가</div>
            <div class="valuation-header-summary">{self.summary}</div>
        </div>
        """, unsafe_allow_html=True)
        
    def _display_valuation_results(self):
        """평가 결과 섹션 표시"""
        st.markdown('<div class="section-title"><span>1</span>평가 결과</div>', unsafe_allow_html=True)
        
        # 데이터 준비
        ebitda_values = [
            self.ebitda_valuation.get("conservative", 0),
            self.ebitda_valuation.get("base", 0),
            self.ebitda_valuation.get("optimistic", 0)
        ]
        dcf_values = [
            self.dcf_valuation.get("conservative", 0),
            self.dcf_valuation.get("base", 0),
            self.dcf_valuation.get("optimistic", 0)
        ]
        
        self._display_metric_cards(ebitda_values, dcf_values)
        self._display_comparison_chart(ebitda_values, dcf_values)
        self._display_result_cards(ebitda_values, dcf_values)
        self._display_radar_chart(ebitda_values, dcf_values)
        
    def _display_metric_cards(self, ebitda_values, dcf_values):
        """메트릭 카드 표시"""
        st.markdown('<div class="subsection-title">기업가치 평가 요약</div>', unsafe_allow_html=True)
        
        avg_base = (self.ebitda_valuation.get("base", 0) + self.dcf_valuation.get("base", 0)) / 2
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            delta_value = (self.ebitda_valuation.get('base', 0) - avg_base)
            delta_color = "positive" if delta_value >= 0 else "negative"
            
            avg_ebitda = sum(ebitda_values) / 3
            if avg_ebitda >= 10000:
                avg_ebitda_display = f"{avg_ebitda/10000:.2f} 조원"
            else:
                avg_ebitda_display = f"{avg_ebitda:.2f} 억원"
                
            if abs(delta_value) >= 10000:
                delta_display = f"{delta_value/10000:+.2f} 조원"
            else:
                delta_display = f"{delta_value:+.2f} 억원"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">EBITDA 평균 기업가치</div>
                <div class="metric-value">{avg_ebitda_display}</div>
                <div class="metric-delta {delta_color}">{delta_display}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            delta_value = (self.dcf_valuation.get('base', 0) - avg_base)
            delta_color = "positive" if delta_value >= 0 else "negative"
            
            avg_dcf = sum(dcf_values) / 3
            if avg_dcf >= 10000:
                avg_dcf_display = f"{avg_dcf/10000:.2f} 조원"
            else:
                avg_dcf_display = f"{avg_dcf:.2f} 억원"
                
            if abs(delta_value) >= 10000:
                delta_display = f"{delta_value/10000:+.2f} 조원"
            else:
                delta_display = f"{delta_value:+.2f} 억원"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">DCF 평균 기업가치</div>
                <div class="metric-value">{avg_dcf_display}</div>
                <div class="metric-delta {delta_color}">{delta_display}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_avg = (sum(ebitda_values) + sum(dcf_values)) / 6
            if total_avg >= 10000:
                total_avg_display = f"{total_avg/10000:.2f} 조원"
            else:
                total_avg_display = f"{total_avg:.2f} 억원"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">종합 평균 기업가치</div>
                <div class="metric-value">{total_avg_display}</div>
                <div class="metric-subtitle">EBITDA 및 DCF 통합 평균</div>
            </div>
            """, unsafe_allow_html=True)
            
    def _display_comparison_chart(self, ebitda_values, dcf_values):
        """비교 차트 표시"""
        st.markdown('<div class="subsection-title">기업가치 평가 비교</div>', unsafe_allow_html=True)
        
        df = pd.DataFrame({
            "시나리오": self.scenarios * 2,
            "평가방식": ["EBITDA"] * 3 + ["DCF"] * 3,
            "기업가치(조원)": ebitda_values + dcf_values
        })
        
        fig = px.bar(
            df, 
            x="시나리오", 
            y="기업가치(조원)", 
            color="평가방식", 
            barmode="group",
            text_auto='.2f',
            color_discrete_map={"EBITDA": "#3b82f6", "DCF": "#8b5cf6"},
            title=f"{self.company_name} 기업가치 평가 (단위: 조원)"
        )
        
        self._update_chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    def _display_result_cards(self, ebitda_values, dcf_values):
        """결과 카드 표시"""
        col1, col2 = st.columns(2)

        with col1:
            # EBITDA 카드를 생성하여 HTML 컴포넌트로 렌더링
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px;">
                <div style="font-size: 18px; font-weight: 600; color: #333; margin-bottom: 15px;">EBITDA 방식 평가결과</div>
            """

            for i, scenario in enumerate(self.scenarios):
                value = self.ebitda_valuation.get(['conservative', 'base', 'optimistic'][i], 0)
                if value >= 10000:
                    value_formatted = f"{value/10000:.2f} 조원"
                else:
                    value_formatted = f"{value:.2f} 억원"

                bg_color = "#dbeafe" if i == 1 else "white"
                border_color = "#3b82f6" if i == 1 else "#e5e7eb"

                html_content += f"""
                <div style="display: flex; justify-content: space-between; background-color: {bg_color}; border-left: 3px solid {border_color}; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="font-weight: 500; color: #333;">{scenario}</div>
                    <div style="font-weight: 600; color: #111;">{value_formatted}</div>
                </div>
                """

            html_content += "</div>"

            # HTML 컴포넌트 사용 - 높이 자동 계산
            height = 60 + len(self.scenarios) * 60  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)

        with col2:
            # DCF 카드를 생성하여 HTML 컴포넌트로 렌더링
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px;">
                <div style="font-size: 18px; font-weight: 600; color: #333; margin-bottom: 15px;">DCF 방식 평가결과</div>
            """

            for i, scenario in enumerate(self.scenarios):
                value = self.dcf_valuation.get(['conservative', 'base', 'optimistic'][i], 0)
                if value >= 10000:
                    value_formatted = f"{value/10000:.2f} 조원"
                else:
                    value_formatted = f"{value:.2f} 억원"

                bg_color = "#f3e8ff" if i == 1 else "white"
                border_color = "#8b5cf6" if i == 1 else "#e5e7eb"

                html_content += f"""
                <div style="display: flex; justify-content: space-between; background-color: {bg_color}; border-left: 3px solid {border_color}; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                    <div style="font-weight: 500; color: #333;">{scenario}</div>
                    <div style="font-weight: 600; color: #111;">{value_formatted}</div>
                </div>
                """

            html_content += "</div>"

            # HTML 컴포넌트 사용 - 높이 자동 계산
            height = 60 + len(self.scenarios) * 60  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)

    def _display_radar_chart(self, ebitda_values, dcf_values):
        """방사형 차트 표시"""
        st.markdown('<div class="subsection-title">시나리오별 평가 비교</div>', unsafe_allow_html=True)
        
        max_value = max(max(ebitda_values + [0.01]), max(dcf_values + [0.01]))
        ebitda_norm = [val / max_value for val in ebitda_values]
        dcf_norm = [val / max_value for val in dcf_values]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=ebitda_norm + [ebitda_norm[0]],
            theta=self.scenarios + [self.scenarios[0]],
            fill='toself',
            name='EBITDA 방식',
            line_color='#3b82f6',
            fillcolor='rgba(59, 130, 246, 0.2)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=dcf_norm + [dcf_norm[0]],
            theta=self.scenarios + [self.scenarios[0]],
            fill='toself',
            name='DCF 방식',
            line_color='#8b5cf6',
            fillcolor='rgba(139, 92, 246, 0.2)'
        ))
        
        self._update_radar_chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    def _display_assumptions(self):
        """가정 섹션 표시"""
        st.markdown('<div class="section-title"><span>2</span>가치 평가 계산 가정</div>', unsafe_allow_html=True)
        
        if not self.assumptions:
            st.info("가치 평가 가정 정보가 없습니다.")
            return
            
        self._display_assumption_cards()
        self._display_assumption_radar_chart()
        
    def _display_assumption_cards(self):
        """가정 카드 표시"""
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_ebitda_multipliers()
            self._display_growth_rates()
            
        with col2:
            self._display_discount_rates()
            self._display_terminal_growth_rates()
            
    def _display_ebitda_multipliers(self):
        """EBITDA 승수 카드 표시"""
        st.markdown('<div class="subsection-title">EBITDA 승수</div>', unsafe_allow_html=True)
        ebitda_multipliers = self.assumptions.get("ebitda_multipliers", {})
        
        if ebitda_multipliers:
            # HTML 문자열 생성
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        margin-bottom: 15px; border-top: 4px solid #3b82f6;">
            """
            
            for i, scenario in enumerate(self.scenarios):
                value = ebitda_multipliers.get(['conservative', 'base', 'optimistic'][i], "-")
                
                html_content += f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; 
                            border-bottom: 1px solid #f1f5f9;">
                    <div style="font-weight: 500; color: #475569;">{scenario}</div>
                    <div style="font-weight: 600; color: #1e293b;">{value}×</div>
                </div>
                """
            
            html_content += "</div>"
            
            # HTML 컴포넌트 사용
            height = 30 + len(self.scenarios) * 50  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)
        else:
            st.info("EBITDA 승수 정보가 없습니다.")
            
    def _display_discount_rates(self):
        """할인율 카드 표시"""
        st.markdown('<div class="subsection-title">DCF 할인율 (WACC)</div>', unsafe_allow_html=True)
        discount_rates = self.assumptions.get("discount_rates", {})
        
        if discount_rates:
            # HTML 문자열 생성
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        margin-bottom: 15px; border-top: 4px solid #8b5cf6;">
            """
            
            for i, scenario in enumerate(self.scenarios):
                value = discount_rates.get(['conservative', 'base', 'optimistic'][i], 0)
                
                html_content += f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; 
                            border-bottom: 1px solid #f1f5f9;">
                    <div style="font-weight: 500; color: #475569;">{scenario}</div>
                    <div style="font-weight: 600; color: #1e293b;">{value:.1f}%</div>
                </div>
                """
            
            html_content += "</div>"
            
            # HTML 컴포넌트 사용
            height = 30 + len(self.scenarios) * 50  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)
        else:
            st.info("할인율 정보가 없습니다.")
            
    def _display_growth_rates(self):
        """성장률 카드 표시"""
        st.markdown('<div class="subsection-title">매출 성장률</div>', unsafe_allow_html=True)
        growth_rates = self.assumptions.get("growth_rates", {})
        
        if growth_rates:
            # HTML 문자열 생성
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        margin-bottom: 15px; border-top: 4px solid #10b981;">
            """
            
            for i, scenario in enumerate(self.scenarios):
                value = growth_rates.get(['conservative', 'base', 'optimistic'][i], 0)
                
                html_content += f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; 
                            border-bottom: 1px solid #f1f5f9;">
                    <div style="font-weight: 500; color: #475569;">{scenario}</div>
                    <div style="font-weight: 600; color: #1e293b;">{value:.1f}%</div>
                </div>
                """
            
            html_content += "</div>"
            
            # HTML 컴포넌트 사용
            height = 30 + len(self.scenarios) * 50  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)
        else:
            st.info("성장률 정보가 없습니다.")
            
    def _display_terminal_growth_rates(self):
        """영구 성장률 카드 표시"""
        st.markdown('<div class="subsection-title">영구 성장률</div>', unsafe_allow_html=True)
        terminal_growth_rates = self.assumptions.get("terminal_growth_rates", {})
        
        if terminal_growth_rates:
            # HTML 문자열 생성
            html_content = """
            <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                        margin-bottom: 15px; border-top: 4px solid #f59e0b;">
            """
            
            for i, scenario in enumerate(self.scenarios):
                value = terminal_growth_rates.get(['conservative', 'base', 'optimistic'][i], 0)
                
                html_content += f"""
                <div style="display: flex; justify-content: space-between; padding: 10px; 
                            border-bottom: 1px solid #f1f5f9;">
                    <div style="font-weight: 500; color: #475569;">{scenario}</div>
                    <div style="font-weight: 600; color: #1e293b;">{value:.1f}%</div>
                </div>
                """
            
            # 마지막 항목은 밑줄 제거
            html_content = html_content.replace('border-bottom: 1px solid #f1f5f9;', '', 1)
            html_content += "</div>"
            
            # HTML 컴포넌트 사용
            height = 30 + len(self.scenarios) * 50  # 기본 높이 + 시나리오당 높이
            st.components.v1.html(html_content, height=height)
        else:
            st.info("영구 성장률 정보가 없습니다.")
            
    def _display_assumption_radar_chart(self):
        """가정 방사형 차트 표시"""
        st.markdown('<div class="subsection-title">시나리오별 평가 가정 비교</div>', unsafe_allow_html=True)
        
        ebitda_multipliers = self.assumptions.get("ebitda_multipliers", {})
        discount_rates = self.assumptions.get("discount_rates", {})
        growth_rates = self.assumptions.get("growth_rates", {})
        terminal_growth_rates = self.assumptions.get("terminal_growth_rates", {})
        
        if all([ebitda_multipliers, discount_rates, growth_rates, terminal_growth_rates]):
            radar_data = self._prepare_radar_data(
                ebitda_multipliers, discount_rates, growth_rates, terminal_growth_rates
            )
            self._create_assumption_radar_chart(radar_data)
        else:
            st.info("모든 가정 정보가 없어 방사형 차트를 생성할 수 없습니다.")
            
    def _prepare_radar_data(self, ebitda_multipliers, discount_rates, growth_rates, terminal_growth_rates):
        """방사형 차트 데이터 준비"""
        max_ebitda_mult = max([
            ebitda_multipliers.get("conservative", 0),
            ebitda_multipliers.get("base", 0),
            ebitda_multipliers.get("optimistic", 0)
        ])
        
        max_discount = max([
            discount_rates.get("conservative", 0),
            discount_rates.get("base", 0),
            discount_rates.get("optimistic", 0)
        ])
        
        max_growth = max([
            growth_rates.get("conservative", 0),
            growth_rates.get("base", 0),
            growth_rates.get("optimistic", 0)
        ])
        
        max_terminal = max([
            terminal_growth_rates.get("conservative", 0),
            terminal_growth_rates.get("base", 0),
            terminal_growth_rates.get("optimistic", 0)
        ])
        
        return {
            "보수적": [
                ebitda_multipliers.get("conservative", 0) / max_ebitda_mult if max_ebitda_mult else 0,
                discount_rates.get("conservative", 0) / max_discount if max_discount else 0,
                growth_rates.get("conservative", 0) / max_growth if max_growth else 0,
                terminal_growth_rates.get("conservative", 0) / max_terminal if max_terminal else 0
            ],
            "기본": [
                ebitda_multipliers.get("base", 0) / max_ebitda_mult if max_ebitda_mult else 0,
                discount_rates.get("base", 0) / max_discount if max_discount else 0,
                growth_rates.get("base", 0) / max_growth if max_growth else 0,
                terminal_growth_rates.get("base", 0) / max_terminal if max_terminal else 0
            ],
            "낙관적": [
                ebitda_multipliers.get("optimistic", 0) / max_ebitda_mult if max_ebitda_mult else 0,
                discount_rates.get("optimistic", 0) / max_discount if max_discount else 0,
                growth_rates.get("optimistic", 0) / max_growth if max_growth else 0,
                terminal_growth_rates.get("optimistic", 0) / max_terminal if max_terminal else 0
            ]
        }
        
    def _create_assumption_radar_chart(self, radar_data):
        """가정 방사형 차트 생성"""
        categories = ["EBITDA 승수", "할인율", "성장률", "영구성장률"]
        colors = ["#3b82f6", "#10b981", "#f97316"]
        
        fig = go.Figure()
        
        for i, (scenario, values) in enumerate(radar_data.items()):
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=scenario,
                line_color=colors[i],
                fillcolor=f"rgba({','.join(str(int(c)) for c in px.colors.hex_to_rgb(colors[i]))}, 0.2)"
            ))
        
        self._update_radar_chart_layout(fig)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
    def _display_calculations(self):
        """계산 섹션 표시"""
        st.markdown('<div class="section-title"><span>3</span>가치 평가 상세 설명</div>', unsafe_allow_html=True)
        
        if not self.calculations:
            st.info("가치 평가 계산 설명 정보가 없습니다.")
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_ebitda_calculation()
            
        with col2:
            self._display_dcf_calculation()
            
        self._display_additional_calculations()
        
    def _display_ebitda_calculation(self):
        """EBITDA 계산 설명 표시"""
        st.markdown('<div class="subsection-title">EBITDA 방식 설명</div>', unsafe_allow_html=True)

        avg_ebitda = self.calculations.get("average_ebitda", 0)
        ebitda_description = self.calculations.get("ebitda_description", "")

        # HTML 문자열 생성
        html_content = """
        <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    margin-bottom: 15px; border-left: 5px solid #3b82f6;">
        """

        if avg_ebitda:
            html_content += f"""
            <div style="background: #f8fafc; border-radius: 8px; padding: 12px; margin-bottom: 12px; 
                        display: flex; justify-content: space-between;">
                <div style="font-weight: 600; color: #475569;">평균 EBITDA</div>
                <div style="font-weight: 700; color: #1e293b;">{avg_ebitda:,.0f} 백만원</div>
            </div>
            """

        if ebitda_description:
            html_content += f"""
            <div style="font-size: 14px; line-height: 1.7; color: #334155;">
                {ebitda_description}
            </div>
            """
        else:
            html_content += """
            <div style="font-size: 14px; color: #94a3b8; font-style: italic; text-align: center; padding: 20px 0;">
                EBITDA 계산 방식에 대한 설명이 없습니다.
            </div>
            """

        html_content += "</div>"

        # HTML 컴포넌트 사용
        # 설명 텍스트의 길이에 따라 높이 조정 (문자 길이 기준으로 대략적인 높이 추정)
        description_height = len(ebitda_description) // 3 if ebitda_description else 60
        height = 100 + description_height  # 기본 높이 + 설명 텍스트 높이
        st.components.v1.html(html_content, height=height)

    def _display_dcf_calculation(self):
        """DCF 계산 설명 표시"""
        st.markdown('<div class="subsection-title">DCF 방식 설명</div>', unsafe_allow_html=True)

        dcf_description = self.calculations.get("dcf_description", "")

        # HTML 문자열 생성
        html_content = """
        <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                    margin-bottom: 15px; border-left: 5px solid #8b5cf6;">
        """

        if dcf_description:
            html_content += f"""
            <div style="font-size: 14px; line-height: 1.7; color: #334155;">
                {dcf_description}
            </div>
            """
        else:
            html_content += """
            <div style="font-size: 14px; color: #94a3b8; font-style: italic; text-align: center; padding: 20px 0;">
                DCF 계산 방식에 대한 설명이 없습니다.
            </div>
            """

        html_content += "</div>"

        # HTML 컴포넌트 사용
        # 설명 텍스트의 길이에 따라 높이 조정 (문자 길이 기준으로 대략적인 높이 추정)
        description_height = len(dcf_description) // 3 if dcf_description else 60
        height = 100 + description_height  # 기본 높이 + 설명 텍스트 높이
        st.components.v1.html(html_content, height=height)

    def _display_additional_calculations(self):
        """추가 계산 설명 표시"""
        for key, value in self.calculations.items():
            if key not in ["average_ebitda", "ebitda_description", "dcf_description"] and isinstance(value, str):
                # 섹션 제목 표시
                st.markdown(f'<div class="subsection-title">{key}</div>', unsafe_allow_html=True)
                
                # HTML 문자열 생성
                html_content = f"""
                <div style="background: white; border-radius: 10px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                            margin-bottom: 15px; border-left: 5px solid #10b981;">
                    <div style="font-size: 14px; line-height: 1.7; color: #334155;">
                        {value}
                    </div>
                </div>
                """
                
                # HTML 컴포넌트 사용
                # 설명 텍스트의 길이에 따라 높이 조정 (문자 길이 기준으로 대략적인 높이 추정)
                description_height = len(value) // 3 if value else 60
                height = 80 + description_height  # 기본 높이 + 설명 텍스트 높이
                st.components.v1.html(html_content, height=height)
               
    def _update_chart_layout(self, fig):
        """차트 레이아웃 업데이트"""
        fig.update_layout(
            font=dict(family="Pretendard, sans-serif", size=14),
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1
            ),
            plot_bgcolor="rgba(255,255,255,0.95)",
            paper_bgcolor="rgba(255,255,255,0)",
            height=450,
            margin=dict(l=20, r=20, t=60, b=80),
            title=dict(
                font=dict(size=18, family="Pretendard, sans-serif", color="#1e293b")
            ),
            xaxis=dict(
                title=dict(font=dict(size=14, family="Pretendard, sans-serif", color="#475569")),
                gridcolor="rgba(0,0,0,0.05)",
                tickfont=dict(family="Pretendard, sans-serif", color="#475569")
            ),
            yaxis=dict(
                title=dict(font=dict(size=14, family="Pretendard, sans-serif", color="#475569")),
                gridcolor="rgba(0,0,0,0.05)",
                tickfont=dict(family="Pretendard, sans-serif", color="#475569")
            )
        )
        
        fig.update_traces(
            marker_line_width=1,
            marker_line_color="rgba(0,0,0,0.1)",
            opacity=0.9,
            hoverinfo="y+name",
            hovertemplate="<b>%{y:.2f} 조원</b><extra></extra>",
            textposition="outside",
            textfont=dict(family="Pretendard, sans-serif", size=12)
        )
        
    def _update_radar_chart_layout(self, fig):
        """방사형 차트 레이아웃 업데이트"""
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10, color="#64748b"),
                    gridcolor="rgba(0,0,0,0.05)"
                ),
                angularaxis=dict(
                    tickfont=dict(size=14, family="Pretendard, sans-serif", color="#334155"),
                    gridcolor="rgba(0,0,0,0.05)"
                ),
                bgcolor="rgba(255,255,255,0.95)"
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(family="Pretendard, sans-serif", size=12, color="#475569"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=20, b=60),
            height=500
        )
        
    def _add_custom_styles(self):
        """고급 커스텀 CSS 스타일 추가"""
        st.markdown("""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        
        /* 기본 스타일 */
        * {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
        }
        
        /* 헤더 스타일 */
        .valuation-header {
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            border-radius: 12px;
            padding: 24px 30px;
            color: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2), 0 5px 10px rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .valuation-header-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
        }
        
        .valuation-header-summary {
            font-size: 16px;
            line-height: 1.6;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 400;
        }
        
        /* 섹션 타이틀 스타일 */
        .section-title {
            display: flex;
            align-items: center;
            font-size: 22px;
            font-weight: 700;
            color: #1e293b;
            margin: 40px 0 20px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .section-title span {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            margin-right: 12px;
            font-weight: 600;
        }
        
        .subsection-title {
            font-size: 18px;
            font-weight: 600;
            color: #334155;
            margin: 25px 0 12px 0;
            display: flex;
            align-items: center;
        }
        
        .subsection-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 16px;
            background: #3b82f6;
            margin-right: 8px;
            border-radius: 4px;
        }
        
        /* 메트릭 카드 스타일 */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }
        
        .metric-title {
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 4px;
        }
        
        .metric-delta {
            font-size: 14px;
            font-weight: 600;
        }
        
        .metric-delta.positive {
            color: #10b981;
        }
        
        .metric-delta.negative {
            color: #ef4444;
        }
        
        .metric-subtitle {
            font-size: 12px;
            color: #94a3b8;
            font-weight: 500;
        }
        
        /* 결과 카드 스타일 */
        .card-container {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .result-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            border-left: 3px solid;
        }
        
        .scenario {
            font-weight: 500;
            color: #475569;
        }
        
        .value {
            font-weight: 600;
            color: #1e293b;
        }
        
        /* 가정 카드 스타일 */
        .assumption-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
            border-top: 4px solid;
        }
        
        .assumption-card.blue {
            border-top-color: #3b82f6;
        }
        
        .assumption-card.purple {
            border-top-color: #8b5cf6;
        }
        
        .assumption-card.green {
            border-top-color: #10b981;
        }
        
        .assumption-card.amber {
            border-top-color: #f59e0b;
        }
        
        .assumption-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .assumption-row:last-child {
            border-bottom: none;
        }
        
        .assumption-label {
            font-weight: 500;
            color: #475569;
        }
        
        .assumption-value {
            font-weight: 600;
            color: #1e293b;
        }
        
        /* 설명 카드 스타일 */
        .explanation-card {
            background: white;
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
            border-left: 4px solid;
        }
        
        .explanation-card.blue {
            border-left-color: #3b82f6;
        }
        
        .explanation-card.purple {
            border-left-color: #8b5cf6;
        }
        
        .explanation-card.green {
            border-left-color: #10b981;
        }
        
        .explanation-highlight {
            background: #f8fafc;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
        }
        
        .highlight-label {
            font-weight: 600;
            color: #475569;
        }
        
        .highlight-value {
            font-weight: 700;
            color: #1e293b;
        }
        
        .explanation-content {
            font-size: 14px;
            line-height: 1.7;
            color: #334155;
        }
        
        .explanation-empty {
            font-size: 14px;
            color: #94a3b8;
            font-style: italic;
            text-align: center;
            padding: 20px 0;
        }
        
        /* Streamlit 기본 요소 스타일 조정 */
        .stPlotlyChart {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            border: 1px solid #e5e7eb;
        }
        
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }
        
        .stInfo {
            font-family: 'Pretendard', sans-serif;
            border-radius: 8px;
        }
        
        .element-container .stAlert {
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

def display_valuation_results(valuation_data: Dict[str, Any]):
    """Streamlit에서 기업가치 평가 결과 시각화 - 고급 UI 버전
    
    Args:
        valuation_data (dict): 기업가치 평가 결과
    """
    display = ValuationDisplay(valuation_data)
    display.display()