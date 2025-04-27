import pandas as pd
import os
import json

class DataLoader:
    """재무 데이터 로드 및 관리 클래스"""
    
    def __init__(self, json_filename=None):
        """
        데이터 로더 초기화
        
        Args:
            json_filename (str, optional): 분석할 JSON 파일명. 기본값은 None (default.json 사용)
        """
        self.json_filename = json_filename
        self._load_data()
    
    def _load_data(self):
        """JSON 파일에서 재무 데이터 로드"""
        # 파일 경로 설정
        data_dir = os.path.dirname(os.path.abspath(__file__))
        
        if self.json_filename:
            json_file = os.path.join(data_dir, f"companies/{self.json_filename}")
        else:
            # 기본 회사 데이터 사용
            json_file = os.path.join(data_dir, "companies/default.json")
        
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"데이터 파일이 존재하지 않습니다: {json_file}")
        
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
            self.growth_rates = pd.DataFrame(financial_data.get('growth_rates', {}))
            self.dupont_data = pd.DataFrame(financial_data.get('dupont_data', {}))
            self.radar_data = pd.DataFrame(financial_data.get('radar_data', {}))
            self.insights = financial_data.get('insights', {})
        except Exception as e:
            raise Exception(f"JSON 파일 로드 중 오류 발생: {str(e)}")
    
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
            data_dir = os.path.dirname(os.path.abspath(__file__))
            company_dir = os.path.join(data_dir, "companies")
            
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
