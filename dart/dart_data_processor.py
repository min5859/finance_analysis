import pandas as pd
import streamlit as st
import datetime

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
    
    @staticmethod
    def extract_optimized_financial_data(financial_data):
        """LLM 분석용으로 최적화된 핵심 재무 데이터 추출
        
        Args:
            financial_data (dict): DART API에서 가져온 재무제표 데이터
            
        Returns:
            dict: 최적화된 재무 데이터
        """
        if not financial_data or 'list' not in financial_data:
            return None
        
        # 기본 데이터 추출
        financial_list = financial_data['list']
        
        # 핵심 계정과목 정의
        key_bs_accounts = [
            '자산총계', '부채총계', '자본총계', '유동자산', '비유동자산', 
            '유동부채', '비유동부채', '자본금', '이익잉여금', '현금및현금성자산',
            '매출채권', '재고자산', '매입채무'
        ]
        
        key_is_accounts = [
            '매출액', '매출원가', '매출총이익', '판매비와관리비', '영업이익', 
            '당기순이익', '법인세비용차감전순이익'
        ]
        
        key_cf_accounts = [
            '영업활동현금흐름', '투자활동현금흐름', '재무활동현금흐름', 
            '기초현금및현금성자산', '기말현금및현금성자산'
        ]
        
        # 각 재무제표 핵심 항목 필터링 및 간소화
        bs_items = DartDataProcessor._filter_and_simplify_items(
            financial_list, 'BS', key_bs_accounts
        )
        
        is_items = DartDataProcessor._filter_and_simplify_items(
            financial_list, ['IS', 'CIS'], key_is_accounts
        )
        
        cf_items = DartDataProcessor._filter_and_simplify_items(
            financial_list, 'CF', key_cf_accounts
        )
        
        # 핵심 재무비율 계산 - 3년치 데이터 포함
        ratios = DartDataProcessor._calculate_key_financial_ratios(bs_items, is_items, cf_items)
        
        # 최적화된 데이터 반환
        return {
            'balance_sheet': bs_items,
            'income_statement': is_items,
            'cash_flow': cf_items,
            'financial_ratios': ratios
        }
    
    @staticmethod
    def _filter_and_simplify_items(financial_list, sj_div, key_accounts):
        """재무제표 항목 필터링 및 단순화 - 억원 단위로 변환
        
        Args:
            financial_list (list): 재무제표 항목 리스트
            sj_div (str or list): 재무제표 구분 코드
            key_accounts (list): 핵심 계정과목 리스트
            
        Returns:
            list: 필터링 및 단순화된 항목 리스트
        """
        filtered_items = []
        
        # sj_div가 리스트인 경우 처리
        if isinstance(sj_div, list):
            sj_div_list = sj_div
        else:
            sj_div_list = [sj_div]
        
        for item in financial_list:
            if item.get('sj_div') in sj_div_list:
                account_nm = item.get('account_nm', '')
                
                # 핵심 계정과목만 선택
                if any(key_account in account_nm for key_account in key_accounts):
                    # 필요한 필드만 포함하여 항목 단순화
                    # 각 금액을 억원 단위로 변환
                    simplified_item = {
                        'account_nm': account_nm,
                        'thstrm_amount': DartDataProcessor._convert_to_billion(item.get('thstrm_amount', '0')),
                        'frmtrm_amount': DartDataProcessor._convert_to_billion(item.get('frmtrm_amount', '0')),
                        'bfefrmtrm_amount': DartDataProcessor._convert_to_billion(item.get('bfefrmtrm_amount', '0'))
                    }
                    filtered_items.append(simplified_item)
        
        return filtered_items
    
    @staticmethod
    def _convert_to_billion(amount_str):
        """원 단위 금액을 억원 단위로 변환
        
        Args:
            amount_str (str): 원 단위 금액 문자열
            
        Returns:
            float: 억원 단위 금액
        """
        try:
            # 문자열이 아닌 경우 처리
            if not isinstance(amount_str, str):
                if isinstance(amount_str, (int, float)):
                    return round(float(amount_str) / 100000000, 2)
                return 0.0
                
            # 음수 값 처리
            is_negative = amount_str.startswith('-')
            amount_str = amount_str.replace('-', '')
            
            # 콤마 제거 후 정수로 변환
            amount = int(amount_str.replace(',', ''))
            
            # 억원 단위로 변환 (1억원 = 100,000,000원)
            result = round(amount / 100000000, 2)
            
            # 음수인 경우 다시 음수로 변환
            if is_negative:
                result = -result
                
            return result
        except (ValueError, AttributeError, TypeError):
            return 0.0
    
    @staticmethod
    def _calculate_key_financial_ratios(bs_items, is_items, cf_items):
        """3년치 핵심 재무비율 계산
        
        Args:
            bs_items (list): 재무상태표 항목
            is_items (list): 손익계산서 항목
            cf_items (list): 현금흐름표 항목
            
        Returns:
            dict: 3년치 재무비율 데이터
        """
        # 기간별 데이터 컬럼명
        periods = ['thstrm_amount', 'frmtrm_amount', 'bfefrmtrm_amount']
        years = []
        
        # 연도 정보 추출 (최신 항목에서 가져옴)
        if bs_items and len(bs_items) > 0:
            # 최신 항목의 report_year에서 연도 추출 (있다고 가정)
            # 실제로는 report_year에서 적절히 계산 필요
            current_year = datetime.datetime.now().year
            years = [str(current_year-2+i) for i in range(3)]
        else:
            # 기본값으로 최근 3년
            current_year = datetime.datetime.now().year
            years = [str(current_year-3+i) for i in range(3)]
        
        # 재무비율 초기화
        ratios = {
            'year': years,
            'ROA': [0.0, 0.0, 0.0],
            'ROE': [0.0, 0.0, 0.0],
            '부채비율': [0.0, 0.0, 0.0],
            '영업이익률': [0.0, 0.0, 0.0],
            '순이익률': [0.0, 0.0, 0.0],
            '유동비율': [0.0, 0.0, 0.0]
        }
        
        try:
            # 각 기간별로 재무비율 계산
            for i, period in enumerate(periods):
                # 재무상태표 값 추출
                assets = DartDataProcessor._find_value_by_account(bs_items, '자산총계', period)
                liabilities = DartDataProcessor._find_value_by_account(bs_items, '부채총계', period)
                equity = DartDataProcessor._find_value_by_account(bs_items, '자본총계', period)
                current_assets = DartDataProcessor._find_value_by_account(bs_items, '유동자산', period)
                current_liabilities = DartDataProcessor._find_value_by_account(bs_items, '유동부채', period)
                
                # 손익계산서 값 추출
                revenue = DartDataProcessor._find_value_by_account(is_items, '매출액', period)
                operating_profit = DartDataProcessor._find_value_by_account(is_items, '영업이익', period)
                net_income = DartDataProcessor._find_value_by_account(is_items, '당기순이익', period)
                
                # 현금흐름표 값 추출 (필요 시)
                op_cash_flow = DartDataProcessor._find_value_by_account(cf_items, '영업활동현금흐름', period)
                
                # 재무비율 계산
                if assets > 0:
                    ratios['ROA'][i] = round((net_income / assets) * 100, 2)
                
                if equity > 0:
                    ratios['ROE'][i] = round((net_income / equity) * 100, 2)
                    ratios['부채비율'][i] = round((liabilities / equity) * 100, 2)
                    
                if revenue > 0:
                    ratios['영업이익률'][i] = round((operating_profit / revenue) * 100, 2)
                    ratios['순이익률'][i] = round((net_income / revenue) * 100, 2)
                    
                if current_liabilities > 0:
                    ratios['유동비율'][i] = round((current_assets / current_liabilities) * 100, 2)
                
                # 추가 재무비율 계산 가능
                # 예: 현금흐름비율, 부채상환능력, 영업현금흐름비율 등
        
        except Exception as e:
            # 오류 발생 시 로깅
            print(f"재무비율 계산 중 오류 발생: {str(e)}")
        
        return ratios
    
    @staticmethod
    def _find_value_by_account(items, account_name, period='thstrm_amount'):
        """항목 리스트에서 특정 계정과목의 특정 기간 값 찾기
        
        Args:
            items (list): 항목 리스트
            account_name (str): 계정과목명
            period (str): 기간 ('thstrm_amount', 'frmtrm_amount', 'bfefrmtrm_amount')
            
        Returns:
            float: 찾은 값 (없으면 0.0)
        """
        for item in items:
            if account_name in item.get('account_nm', ''):
                # 문자열에서 수치로 변환 (필요시 콤마 제거 등 처리)
                value_str = item.get(period, '0')
                if isinstance(value_str, str):
                    value_str = value_str.replace(',', '')
                try:
                    return float(value_str)
                except (ValueError, TypeError):
                    return 0.0
        return 0.0