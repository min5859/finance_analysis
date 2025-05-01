import pandas as pd
import os
import json

class DataLoader:
    """재무 데이터 로더 클래스"""
    
    def __init__(self, data_source):
        """
        DataLoader 클래스 초기화
        
        Args:
            data_source: JSON 파일 경로 또는 JSON 데이터 객체
        """
        if isinstance(data_source, str):
            # 파일 경로인 경우
            data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_file = os.path.join(data_dir, "data/companies", data_source)
            self.json_filename = data_source
            
            with open(json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            # JSON 데이터 객체인 경우
            self.data = data_source
            self.json_filename = None
        
        # 데이터 프레임으로 변환
        self._convert_to_dataframes()
    
    def _convert_to_dataframes(self):
        """JSON 데이터를 pandas DataFrame으로 변환"""
        # 빈 배열 처리 함수
        def process_empty_arrays(data_dict):
            if not isinstance(data_dict, dict):
                return data_dict
            
            processed = {}
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    processed[key] = process_empty_arrays(value)
                elif isinstance(value, list):
                    if not value:  # 빈 배열인 경우
                        processed[key] = [0] * len(data_dict.get('year', []))
                    else:
                        processed[key] = value
                else:
                    processed[key] = value
            return processed
        
        # 데이터 전처리
        processed_data = process_empty_arrays(self.data)
        
        # 데이터 프레임으로 변환
        self.performance_data = pd.DataFrame(processed_data.get('performance_data', {}))
        self.balance_sheet_data = pd.DataFrame(processed_data.get('balance_sheet_data', {}))
        self.stability_data = pd.DataFrame(processed_data.get('stability_data', {}))
        self.cash_flow_data = pd.DataFrame(processed_data.get('cash_flow_data', {}))
        self.working_capital_data = pd.DataFrame(processed_data.get('working_capital_data', {}))
        self.profitability_data = pd.DataFrame(processed_data.get('profitability_data', {}))
        self.growth_rates = pd.DataFrame(processed_data.get('growth_rates', {}))
        self.dupont_data = pd.DataFrame(processed_data.get('dupont_data', {}))
        self.radar_data = pd.DataFrame(processed_data.get('radar_data', {}))
        self.insights = processed_data.get('insights', {})
    
    def get_company_name(self):
        """회사명 가져오기"""
        return self.data.get('company_name', '알 수 없음')
    
    def get_sector(self):
        """업종 가져오기"""
        return self.data.get('sector', '알 수 없음')
    
    def get_financial_data(self, data_type):
        """
        재무 데이터 가져오기
        
        Args:
            data_type (str): 데이터 유형 (예: 'income_statement', 'balance_sheet', 'cash_flow')
            
        Returns:
            dict: 해당 유형의 재무 데이터
        """
        return self.data.get(data_type, {})
    
    def get_all_data(self):
        """모든 재무 데이터 가져오기"""
        return self.data
    
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
    
    def export_to_json(self, output_file=None):
        """
        현재 데이터를 JSON 파일로 내보내기
        
        Args:
            output_file (str, optional): 출력 파일 경로. 없으면 현재 json_filename 기반으로 생성
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
            data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            company_dir = os.path.join(data_dir, "data/companies")
            
            # companies 디렉토리가 없으면 생성
            if not os.path.exists(company_dir):
                os.makedirs(company_dir)
            
            filename = self.json_filename or 'default.json'
            if not filename.endswith('.json'):
                filename += '.json'
            
            output_file = os.path.join(company_dir, filename)
        
        # JSON 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)
            
        return output_file
