import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from typing import Dict, Any

def display_valuation_results(valuation_data: Dict[str, Any]):
    """Streamlit에서 기업가치 평가 결과 시각화 - 단일 페이지 버전
    
    Args:
        valuation_data (dict): 기업가치 평가 결과
    """
    if not valuation_data:
        st.error("기업가치 평가 데이터가 없습니다.")
        return
    
    company_name = valuation_data.get("company", "기업명 없음")
    ebitda_valuation = valuation_data.get("ebitda_valuation", {})
    dcf_valuation = valuation_data.get("dcf_valuation", {})
    assumptions = valuation_data.get("assumptions", {})
    calculations = valuation_data.get("calculations", {})
    summary = valuation_data.get("summary", "")
    
    # 헤더와 요약 정보
    st.markdown(f"""
    <div style="
        background: linear-gradient(to right, #4b6cb7, #182848);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="color: white; margin-top: 0;">{company_name} 기업가치 평가</h2>
        <p style="margin-bottom: 0; font-size: 1.1rem;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 섹션 1: 평가 결과
    st.markdown("## 1. 평가 결과")
    
    # 데이터 준비
    scenarios = ["보수적", "기본", "낙관적"]
    ebitda_values = [
        ebitda_valuation.get("conservative", 0) / 1000000,
        ebitda_valuation.get("base", 0) / 1000000,
        ebitda_valuation.get("optimistic", 0) / 1000000
    ]
    dcf_values = [
        dcf_valuation.get("conservative", 0) / 1000000,
        dcf_valuation.get("base", 0) / 1000000,
        dcf_valuation.get("optimistic", 0) / 1000000
    ]
    
    # 요약 메트릭 (3개 열)
    st.subheader("기업가치 평가 요약")
    col1, col2, col3 = st.columns(3)
    
    # 기본 시나리오 평균값
    avg_base = (ebitda_valuation.get("base", 0) + dcf_valuation.get("base", 0)) / 2
    
    with col1:
        st.metric(
            label="EBITDA 평균 기업가치", 
            value=f"{sum(ebitda_values) / 3:.2f} 조원",
            delta=f"{(ebitda_valuation.get('base', 0) - avg_base) / 1000000:.2f} 조원"
        )
    
    with col2:
        st.metric(
            label="DCF 평균 기업가치", 
            value=f"{sum(dcf_values) / 3:.2f} 조원",
            delta=f"{(dcf_valuation.get('base', 0) - avg_base) / 1000000:.2f} 조원"
        )
    
    with col3:
        st.metric(
            label="종합 평균 기업가치", 
            value=f"{(sum(ebitda_values) + sum(dcf_values)) / 6:.2f} 조원"
        )
    
    # 데이터프레임 생성
    df = pd.DataFrame({
        "시나리오": scenarios * 2,
        "평가방식": ["EBITDA"] * 3 + ["DCF"] * 3,
        "기업가치(조원)": ebitda_values + dcf_values
    })
    
    # 1. 막대 그래프
    st.subheader("기업가치 평가 비교")
    
    fig = px.bar(
        df, 
        x="시나리오", 
        y="기업가치(조원)", 
        color="평가방식", 
        barmode="group",
        text_auto='.1f',
        color_discrete_map={"EBITDA": "#4472C4", "DCF": "#ED7D31"},
        title=f"{company_name} 기업가치 평가 (단위: 조원)"
    )
    
    fig.update_layout(
        font=dict(family="Arial", size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 평가 결과 테이블 (2열 구조)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### EBITDA 방식")
        st.dataframe({
            "시나리오": scenarios,
            "기업가치": [
                f"{ebitda_valuation.get('conservative', 0):,}",
                f"{ebitda_valuation.get('base', 0):,}",
                f"{ebitda_valuation.get('optimistic', 0):,}"
            ]
        }, hide_index=True)
    
    with col2:
        st.markdown("### DCF 방식")
        st.dataframe({
            "시나리오": scenarios,
            "기업가치": [
                f"{dcf_valuation.get('conservative', 0):,}",
                f"{dcf_valuation.get('base', 0):,}",
                f"{dcf_valuation.get('optimistic', 0):,}"
            ]
        }, hide_index=True)
    
    # 방사형 차트 - 시나리오별 평가 비교
    st.subheader("시나리오별 평가 비교")
    
    # 데이터 정규화 (최대값 기준)
    max_value = max(max(ebitda_values + [0.01]), max(dcf_values + [0.01]))
    ebitda_norm = [val / max_value for val in ebitda_values]
    dcf_norm = [val / max_value for val in dcf_values]
    
    # 방사형 차트 생성
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=ebitda_norm + [ebitda_norm[0]],
        theta=scenarios + [scenarios[0]],
        fill='toself',
        name='EBITDA 방식',
        line_color='#4472C4'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=dcf_norm + [dcf_norm[0]],
        theta=scenarios + [scenarios[0]],
        fill='toself',
        name='DCF 방식',
        line_color='#ED7D31'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 섹션 2: 계산 가정
    st.markdown("---")
    st.markdown("## 2. 가치 평가 계산 가정")
    
    # 가정 정보 표시
    if assumptions:
        # 가정 데이터 표시 - 2개 열로 나란히 배치
        col1, col2 = st.columns(2)
        
        # EBITDA 승수
        with col1:
            st.markdown("### EBITDA 승수")
            ebitda_multipliers = assumptions.get("ebitda_multipliers", {})
            
            if ebitda_multipliers:
                st.dataframe({
                    "시나리오": scenarios,
                    "승수": [
                        ebitda_multipliers.get("conservative", "-"),
                        ebitda_multipliers.get("base", "-"),
                        ebitda_multipliers.get("optimistic", "-")
                    ]
                }, hide_index=True)
            else:
                st.info("EBITDA 승수 정보가 없습니다.")
        
        # DCF 할인율
        with col2:
            st.markdown("### DCF 할인율 (WACC)")
            discount_rates = assumptions.get("discount_rates", {})
            
            if discount_rates:
                st.dataframe({
                    "시나리오": scenarios,
                    "할인율(%)": [
                        f"{discount_rates.get('conservative', 0):.1f}",
                        f"{discount_rates.get('base', 0):.1f}",
                        f"{discount_rates.get('optimistic', 0):.1f}"
                    ]
                }, hide_index=True)
            else:
                st.info("할인율 정보가 없습니다.")
        
        # 성장률
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 매출 성장률")
            growth_rates = assumptions.get("growth_rates", {})
            
            if growth_rates:
                st.dataframe({
                    "시나리오": scenarios,
                    "성장률(%)": [
                        f"{growth_rates.get('conservative', 0):.1f}",
                        f"{growth_rates.get('base', 0):.1f}",
                        f"{growth_rates.get('optimistic', 0):.1f}"
                    ]
                }, hide_index=True)
            else:
                st.info("성장률 정보가 없습니다.")
        
        with col2:
            st.markdown("### 영구 성장률")
            terminal_growth_rates = assumptions.get("terminal_growth_rates", {})
            
            if terminal_growth_rates:
                st.dataframe({
                    "시나리오": scenarios,
                    "영구성장률(%)": [
                        f"{terminal_growth_rates.get('conservative', 0):.1f}",
                        f"{terminal_growth_rates.get('base', 0):.1f}",
                        f"{terminal_growth_rates.get('optimistic', 0):.1f}"
                    ]
                }, hide_index=True)
            else:
                st.info("영구 성장률 정보가 없습니다.")
        
        # 방사형 차트로 가정 비교
        st.subheader("시나리오별 평가 가정 비교")
        
        # 가정 데이터 준비
        if all([ebitda_multipliers, discount_rates, growth_rates, terminal_growth_rates]):
            # 데이터 정규화를 위한 최대값
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
            
            # 정규화된 데이터
            radar_data = {
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
            
            # 방사형 차트 생성
            categories = ["EBITDA 승수", "할인율", "성장률", "영구성장률"]
            
            fig = go.Figure()
            
            for scenario, values in radar_data.items():
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    name=scenario
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("모든 가정 정보가 없어 방사형 차트를 생성할 수 없습니다.")
    
    else:
        st.info("가치 평가 가정 정보가 없습니다.")
    
    # 섹션 3: 상세 설명
    st.markdown("---")
    st.markdown("## 3. 가치 평가 상세 설명")
    
    if calculations:
        # EBITDA 계산 설명
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### EBITDA 방식 설명")
            
            avg_ebitda = calculations.get("average_ebitda", 0)
            ebitda_description = calculations.get("ebitda_description", "")
            
            if avg_ebitda:
                st.markdown(f"**평균 EBITDA**: {avg_ebitda:,.0f} 백만원")
            
            if ebitda_description:
                st.markdown(ebitda_description)
            else:
                st.info("EBITDA 계산 방식에 대한 설명이 없습니다.")
        
        with col2:
            # DCF 계산 설명
            st.markdown("### DCF 방식 설명")
            
            dcf_description = calculations.get("dcf_description", "")
            
            if dcf_description:
                st.markdown(dcf_description)
            else:
                st.info("DCF 계산 방식에 대한 설명이 없습니다.")
        
        # 추가 설명 있을 경우
        for key, value in calculations.items():
            if key not in ["average_ebitda", "ebitda_description", "dcf_description"] and isinstance(value, str):
                st.markdown(f"### {key}")
                st.markdown(value)
    
    else:
        st.info("가치 평가 계산 설명 정보가 없습니다.")