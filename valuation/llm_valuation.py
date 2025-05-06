import os
import json
import logging
import re
import requests
from anthropic import Anthropic

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("financial_analyzer.valuation")

class ValuationAnalyzer:
    """LLM을 이용한 기업 가치 평가를 위한 클래스"""
    
    def __init__(self):
        """분석기 클래스 초기화"""
        self.client = None
    
    def analyze_company_value(self, company_info, financial_data, industry_info, api_key):
        """LLM을 이용한 기업 가치 분석
        
        Args:
            company_info (dict): 기업 기본 정보
            financial_data (dict): 재무 데이터
            industry_info (dict): 산업 정보
            api_key (str): Anthropic API 키
            
        Returns:
            dict: LLM 분석 결과
        """
        if not api_key:
            return {
                "status": "error",
                "message": "API 키가 설정되지 않았습니다."
            }
        
        try:
            # Anthropic 클라이언트 초기화
            self.client = Anthropic(api_key=api_key)
            
            # 재무 데이터 준비
            finances, ratios = self._prepare_financial_data(financial_data)
            sector_info = self._prepare_industry_info(industry_info)
            
            # 프롬프트 생성
            prompt = self._create_valuation_prompt(company_info, finances, ratios, sector_info)
            
            # Anthropic API 호출
            response = self.client.messages.create(
                model="claude-3-7-sonnet-20250219",  # Claude 모델 사용
                # model="claude-3-5-sonnet-20240620",
                system="당신은 기업 가치 평가와 M&A 분석을 전문으로 하는 금융 애널리스트입니다. 주어진 기업의 재무 데이터를 바탕으로 정확한 기업 가치 평가를 수행하고, 결과를 JSON 형식으로 반환합니다.",
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.2,
                max_tokens=4000
            )
            
            # 응답 파싱
            return self._parse_llm_response(response.content[0].text)
            
        except Exception as e:
            logger.error(f"LLM 분석 오류: {str(e)}")
            return {
                "status": "error",
                "message": f"분석 중 오류가 발생했습니다: {str(e)}"
            }
    
    def _prepare_financial_data(self, financial_data):
        """재무 데이터 준비"""
        years = financial_data.get("years", [])
        assets = financial_data.get("assets", [])
        liabilities = financial_data.get("liabilities", [])
        equity = financial_data.get("equity", [])
        revenue = financial_data.get("revenue", [])
        operating_profit = financial_data.get("operating_profit", [])
        net_income = financial_data.get("net_income", [])
        fcf = financial_data.get("fcf", [])
        
        # 재무 정보 테이블 형태로 변환
        finances = []
        for i in range(len(years)):
            if i < len(assets) and i < len(liabilities) and i < len(equity) and i < len(revenue) and i < len(operating_profit) and i < len(net_income):
                finances.append({
                    "연도": years[i],
                    "자산": assets[i],
                    "부채": liabilities[i],
                    "자본": equity[i],
                    "매출액": revenue[i],
                    "영업이익": operating_profit[i],
                    "당기순이익": net_income[i],
                    "FCF": fcf[i] if i < len(fcf) else None
                })
        
        # 비율 계산
        ratios = []
        for i in range(len(years)):
            if i < len(assets) and i < len(liabilities) and i < len(equity) and i < len(revenue) and i < len(operating_profit) and i < len(net_income):
                ratio = {}
                ratio["연도"] = years[i]
                
                # 부채비율
                if equity[i] > 0:
                    ratio["부채비율"] = round((liabilities[i] / equity[i]) * 100, 2)
                else:
                    ratio["부채비율"] = None
                
                # 영업이익률
                if revenue[i] > 0:
                    ratio["영업이익률"] = round((operating_profit[i] / revenue[i]) * 100, 2)
                else:
                    ratio["영업이익률"] = None
                
                # 순이익률
                if revenue[i] > 0:
                    ratio["순이익률"] = round((net_income[i] / revenue[i]) * 100, 2)
                else:
                    ratio["순이익률"] = None
                
                # ROE
                if equity[i] > 0:
                    ratio["ROE"] = round((net_income[i] / equity[i]) * 100, 2)
                else:
                    ratio["ROE"] = None
                
                # ROA
                if assets[i] > 0:
                    ratio["ROA"] = round((net_income[i] / assets[i]) * 100, 2)
                else:
                    ratio["ROA"] = None
                
                ratios.append(ratio)
        
        return finances, ratios
    
    def _prepare_industry_info(self, industry_info):
        """산업 정보 준비"""
        sector_info = ""
        if industry_info:
            sector_info = f"""
            산업 관련 정보:
            산업군: {industry_info.get('sector', '알 수 없음')}
            경쟁사 평균 PER: {industry_info.get('avg_per', '알 수 없음')}
            경쟁사 평균 PBR: {industry_info.get('avg_pbr', '알 수 없음')}
            """
        return sector_info
    
    def _create_valuation_prompt(self, company_info, finances, ratios, sector_info):
        """LLM 프롬프트 생성"""
        company_name = company_info.get('corp_name', '알 수 없음')
        company_sector = company_info.get('sector', '알 수 없음')
        
        prompt = f"""
        # 기업 정보
        기업명: {company_name}
        업종: {company_sector}
        
        # 재무 정보 (단위: 백만원)
        {json.dumps(finances, ensure_ascii=False, indent=2)}
        
        # 재무 비율
        {json.dumps(ratios, ensure_ascii=False, indent=2)}
        
        {sector_info}
        
        다음 형식으로 분석해주세요:
        
        1. EBITDA와 DCF 두가지 방식으로 보수적, 기본, 낙관적 3가지로 기업가치를 평가
        2. 결과는 다음 JSON 구조로 출력하되, 계산 과정과 가정에 대한 설명도 포함할 것:
        
        {{
          "company": "{company_name}",
          "ebitda_valuation": {{
            "conservative": 숫자값,
            "base": 숫자값,
            "optimistic": 숫자값
          }},
          "dcf_valuation": {{
            "conservative": 숫자값,
            "base": 숫자값,
            "optimistic": 숫자값
          }},
          "assumptions": {{
            "ebitda_multipliers": {{
              "conservative": 숫자값,
              "base": 숫자값,
              "optimistic": 숫자값
            }},
            "discount_rates": {{
              "conservative": 숫자값,
              "base": 숫자값,
              "optimistic": 숫자값
            }},
            "growth_rates": {{
              "conservative": 숫자값,
              "base": 숫자값,
              "optimistic": 숫자값
            }},
            "terminal_growth_rates": {{
              "conservative": 숫자값,
              "base": 숫자값,
              "optimistic": 숫자값
            }}
          }},
          "calculations": {{
            "ebitda_description": "EBITDA 계산 방식에 대한 설명",
            "dcf_description": "DCF 계산 방식에 대한 간략한 설명"
          }},
          "summary": "기업 가치 평가에 대한 종합적인 분석 및 설명"
        }}
        
        중요:
        1. 금액 단위는 억원으로 통일하세요. 원 단위로 표기된 금액은 억원 단위로 변환하세요 (1억원 = 100,000,000원).
        2. 각 시나리오별 계산에 사용된 가정(EBITDA 승수, 할인율, 성장률 등)을 명확히 포함할 것
        3. EBITDA와 DCF 계산 방식에 대한 간략한 설명 포함
        4. JSON 구조는 유지하되, 각 항목에 대한 설명을 포함하여 결과의 신뢰성 제공
        5. 모든 숫자값은 단위를 제외한 숫자만 출력하고, 콤마(,)나 소수점 외 다른 기호 사용 금지
        """
        return prompt
    
    def _parse_llm_response(self, response):
        """LLM 응답 파싱"""
        try:
            # 텍스트에서 JSON 부분만 추출
            json_pattern = r'({[\s\S]*})'
            match = re.search(json_pattern, response)
            
            if match:
                json_str = match.group(1)
                valuation_data = json.loads(json_str)
            else:
                # 응답이 이미 JSON 형식이면 바로 로드
                valuation_data = json.loads(response)
            
            return {
                "status": "success",
                "valuation_data": valuation_data
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {str(e)}")
            return {
                "status": "error",
                "message": f"JSON 파싱 오류: {str(e)}",
                "raw_content": response
            }