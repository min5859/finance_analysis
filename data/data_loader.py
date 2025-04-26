import pandas as pd

class DataLoader:
    """재무 데이터 로드 및 관리 클래스"""
    
    def __init__(self):
        self._load_data()
        self._calculate_growth_rates()
        self._prepare_dupont_analysis()
        self._prepare_radar_data()
    
    def _load_data(self):
        """기본 재무 데이터 로드"""
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
    
    def _calculate_growth_rates(self):
        """성장률 계산"""
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
        self.dupont_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            '순이익률': [3.84, 4.18, 6.36],
            '자산회전율': [2.56, 2.33, 1.78],
            '재무레버리지': [1.72, 1.64, 1.42],
            'ROE': [16.8, 15.7, 15.7]
        })
    
    def _prepare_radar_data(self):
        """레이더 차트 데이터 준비"""
        self.radar_data = pd.DataFrame({
            'metric': ['ROE', 'ROA', '영업이익률', '순이익률', '재무안정성', '유동성'],
            '풍전비철': [14.4, 11.2, 5.4, 6.4, 3.4, 2.09],
            '업계평균': [8.5, 5.0, 3.5, 2.0, 0.9, 1.5]
        })
    
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
