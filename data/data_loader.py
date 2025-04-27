import pandas as pd
import os
import json

class DataLoader:
    """재무 데이터 로드 및 관리 클래스"""
    
    def __init__(self, company_code=None):
        """
        데이터 로더 초기화
        
        Args:
            company_code (str, optional): 분석할 회사 코드. 기본값은 None (기본 회사 사용)
        """
        self.company_code = company_code
        self._load_data()
        self._calculate_growth_rates()
        self._prepare_dupont_analysis()
        self._prepare_radar_data()
    
    def _load_data(self):
        """JSON 파일에서 재무 데이터 로드"""
        # 파일 경로 설정
        data_dir = os.path.dirname(os.path.abspath(__file__))
        
        if self.company_code:
            json_file = os.path.join(data_dir, f"companies/{self.company_code}.json")
        else:
            # 기본 회사 데이터 사용
            json_file = os.path.join(data_dir, "companies/default.json")
        
        # 파일이 없는 경우 기본 데이터 사용
        if not os.path.exists(json_file):
            self._load_default_data()
            return
        
        try:
            # JSON 파일 로드
            with open(json_file, 'r', encoding='utf-8') as f:
                financial_data = json.load(f)
            
            # 데이터 프레임으로 변환
            self.performance_data = pd.DataFrame(financial_data.get('performance_data', {}))
            self.balance_sheet_data = pd.DataFrame(financial_data.get('balance_sheet_data', {}))
            self.stability_data = pd.DataFrame(financial_data.get('stability_data', {}))
            self.cash_flow_data = pd.DataFrame(financial_data.get('cash_flow_data', {}))
            self.working_capital_data = pd.DataFrame(financial_data.get('working_capital_data', {}))
            self.profitability_data = pd.DataFrame(financial_data.get('profitability_data', {}))
            self.radar_data = pd.DataFrame(financial_data.get('radar_data', {}))
            self.insights = financial_data.get('insights', {})
        except Exception as e:
            print(f"JSON 파일 로드 중 오류 발생: {str(e)}")
            self._load_default_data()
    
    def _load_default_data(self):
        """기본 재무 데이터 로드 (하드코딩된 풍전비철 데이터)"""
        # 매출 및 수익성 데이터
        self.performance_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            '매출액': [9470, 8730, 6760],
            '영업이익': [430, 330, 360],
            '순이익': [360, 360, 430],
            '영업이익률': [4.5, 3.8, 5.4],
            '순이익률': [3.8, 4.2, 6.4]
        })

        # 재무상태표 항목 데이터
        self.balance_sheet_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            '총자산': [3683, 3827, 3859],
            '총부채': [683, 683, 871],
            '자본총계': [2158, 2498, 2988]
        })

        # 안정성 지표
        self.stability_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            '부채비율': [71, 53, 29],
            '유동비율': [189, 208, 209],
            '이자보상배율': [7.8, 4.4, 7.4]
        })

        # 현금흐름 데이터
        self.cash_flow_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            '영업활동': [155, 665, -146],
            '투자활동': [-31, -260, -4],
            '재무활동': [0, 0, 0],
            'FCF': [124, 405, -150]
        })

        # 운전자본 데이터 (CCC)
        self.working_capital_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            'DSO': [36.7, 32.2, 34.1],
            'DIO': [50.8, 43.2, 41.7],
            'DPO': [3.3, 3.3, 8.9],
            'CCC': [84.2, 72.1, 66.9]
        })

        # ROE 및 수익성 지표
        self.profitability_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            'ROE': [16.8, 14.6, 14.4],
            'ROA': [9.8, 9.5, 11.2],
            '영업이익률': [4.5, 3.8, 5.4],
            '순이익률': [3.8, 4.2, 6.4]
        })

        # 인사이트 데이터
        self.insights = {
            "balance_sheet": {
                "title": "재무상태표 분석",
                "content": "**재무상태표 분석:**\n- 총자산: 3년간 4.8% 완만한 증가 (3,683억원 → 3,859억원)\n- 자본총계: 3년간 38.5% 가파른 증가 (2,158억원 → 2,988억원)\n- 총부채: 2024년 27.5% 증가했으나 여전히 낮은 수준\n- 부채비율: 18% → 23%로 변화, 여전히 낮은 레버리지 유지\n- 전반적으로 건전한 재무 체력 구축으로 성장투자나 배당 확대가 가능한 상태"
            }
        }
    
    def _calculate_growth_rates(self):
        """성장률 계산"""
        if not hasattr(self, 'growth_rates'):
            # 성장률 계산 데이터
            self.growth_rates = pd.DataFrame({
                'year': ['2023', '2024'],
                '총자산성장률': [
                    ((self.balance_sheet_data['총자산'][1] / self.balance_sheet_data['총자산'][0]) - 1) * 100,
                    ((self.balance_sheet_data['총자산'][2] / self.balance_sheet_data['총자산'][1]) - 1) * 100
                ],
                '매출액성장률': [
                    ((self.performance_data['매출액'][1] / self.performance_data['매출액'][0]) - 1) * 100,
                    ((self.performance_data['매출액'][2] / self.performance_data['매출액'][1]) - 1) * 100
                ],
                '순이익성장률': [
                    ((self.performance_data['순이익'][1] / self.performance_data['순이익'][0]) - 1) * 100,
                    ((self.performance_data['순이익'][2] / self.performance_data['순이익'][1]) - 1) * 100
                ]
            })
    
    def _prepare_dupont_analysis(self):
        """듀폰 분석 데이터 준비"""
        if not hasattr(self, 'dupont_data'):
            self.dupont_data = pd.DataFrame({
                'year': ['2022', '2023', '2024'],
                '순이익률': [3.84, 4.18, 6.36],
                '자산회전율': [2.56, 2.33, 1.78],
                '재무레버리지': [1.72, 1.64, 1.42],
                'ROE': [16.8, 15.7, 15.7]
            })
    
    def _prepare_radar_data(self):
        """레이더 차트 데이터 준비"""
        if not hasattr(self, 'radar_data'):
            self.radar_data = pd.DataFrame({
                'metric': ['ROE', 'ROA', '영업이익률', '순이익률', '재무안정성', '유동성'],
                '풍전비철': [14.4, 11.2, 5.4, 6.4, 3.4, 2.09],
                '업계평균': [8.5, 5.0, 3.5, 2.0, 0.9, 1.5]
            })
    
    def export_to_json(self, output_file=None):
        """
        현재 데이터를 JSON 파일로 내보내기
        
        Args:
            output_file (str, optional): 출력 파일 경로. 없으면 회사 코드 기반으로 생성
        """
        # 데이터 수집
        data_dict = {
            'performance_data': self.performance_data.to_dict('list'),
            'balance_sheet_data': self.balance_sheet_data.to_dict('list'),
            'stability_data': self.stability_data.to_dict('list'),
            'cash_flow_data': self.cash_flow_data.to_dict('list'),
            'working_capital_data': self.working_capital_data.to_dict('list'),
            'profitability_data': self.profitability_data.to_dict('list'),
            'growth_rates': self.growth_rates.to_dict('list'),
            'dupont_data': self.dupont_data.to_dict('list'),
            'radar_data': self.radar_data.to_dict('list'),
            'insights': self.insights
        }
        
        # 출력 파일 경로 설정
        if not output_file:
            data_dir = os.path.dirname(os.path.abspath(__file__))
            company_dir = os.path.join(data_dir, "companies")
            
            # companies 디렉토리가 없으면 생성
            if not os.path.exists(company_dir):
                os.makedirs(company_dir)
            
            output_file = os.path.join(company_dir, f"{self.company_code or 'default'}.json")
        
        # JSON 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)
            
        return output_file
    
    def get_performance_data(self):
        return self.performance_data
    
    def get_balance_sheet_data(self):
        return self.balance_sheet_data
    
    def get_stability_data(self):
        return self.stability_data
    
    def get_cash_flow_data(self):
        return self.cash_flow_data
    
    def get_working_capital_data(self):
        return self.working_capital_data
    
    def get_profitability_data(self):
        return self.profitability_data
    
    def get_growth_rates(self):
        return self.growth_rates
    
    def get_dupont_data(self):
        return self.dupont_data
    
    def get_radar_data(self):
        return self.radar_data
    
    def get_insights(self):
        """인사이트 데이터 반환"""
        return self.insights
