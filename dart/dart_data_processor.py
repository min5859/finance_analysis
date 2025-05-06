import pandas as pd
import streamlit as st
class DartDataProcessor:
    """DART API 재무 데이터 가공 및 처리 클래스"""
    
    @staticmethod
    def extract_financial_data(financial_data):
        """DART API 재무제표 데이터에서 원하는 정보 추출 및 가공
        
        Args:
            financial_data (dict): DART API에서 가져온 재무제표 데이터
            
        Returns:
            dict: 가공된 재무 데이터
        """
        if not financial_data or 'list' not in financial_data:
            return None
        
        # 데이터 리스트
        financial_list = financial_data['list']
        
        # 재무상태표 항목 추출
        bs_items = [item for item in financial_list if item.get('sj_div') == 'BS']
        
        # 손익계산서 항목 추출
        is_items = [item for item in financial_list if item.get('sj_div') in ['IS', 'CIS']]
        
        # 현금흐름표 항목 추출
        cf_items = [item for item in financial_list if item.get('sj_div') == 'CF']

        # 항목별로 정리된 결과 반환
        return {
            'balance_sheet': bs_items,
            'income_statement': is_items,
            'cash_flow': cf_items
        }
    
    @staticmethod
    def create_financial_statement_df(financial_items):
        """재무제표 항목을 DataFrame으로 변환
        
        Args:
            financial_items (list): 재무제표 항목 리스트
            
        Returns:
            pandas.DataFrame: 재무제표 데이터프레임
        """
        # 데이터프레임 생성을 위한 데이터 준비
        data = []
        
        for item in financial_items:
            # 필요한 정보 추출
            account_id = item.get('account_id', '')
            account_nm = item.get('account_nm', '')
            
            # 당기, 전기, 전전기 금액 추출
            thstrm_amount = item.get('thstrm_amount', '0').replace(',', '')
            frmtrm_amount = item.get('frmtrm_amount', '0').replace(',', '')
            bfefrmtrm_amount = item.get('bfefrmtrm_amount', '0').replace(',', '')
            
            # 금액을 정수로 변환 (실패하면 0으로 설정)
            try:
                thstrm_amount = int(thstrm_amount) 
                frmtrm_amount = int(frmtrm_amount)
                bfefrmtrm_amount = int(bfefrmtrm_amount)
            except ValueError:
                thstrm_amount = 0
                frmtrm_amount = 0
                bfefrmtrm_amount = 0
            
            # 백만원 단위로 변환 (원 단위에서 백만원 단위로)
            thstrm_amount_mil = thstrm_amount // 1000000
            frmtrm_amount_mil = frmtrm_amount // 1000000
            bfefrmtrm_amount_mil = bfefrmtrm_amount // 1000000
            
            # 데이터 리스트에 추가
            data.append({
                '계정과목코드': account_id,
                '계정과목명': account_nm,
                '당기': thstrm_amount_mil,
                '전기': frmtrm_amount_mil,
                '전전기': bfefrmtrm_amount_mil
            })
        
        # 데이터프레임 생성
        return pd.DataFrame(data)