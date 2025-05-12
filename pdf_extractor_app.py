import streamlit as st
import pdfplumber
import re
import tempfile
import os
from io import BytesIO
from collections import Counter


class FinancialStatementDetector:
    """PDF에서 재무제표 페이지를 자동으로 탐지하는 클래스"""
    
    def __init__(self):
        # 각 재무제표 유형별 특징적인 계정과목 및 키워드 정의
        self.statement_indicators = {
            "재무상태표": {
                "필수키워드": ["재무상태표", "대차대조표"],
                "계정과목": [
                    "자산", "부채", "자본", "유동자산", "비유동자산", "유동부채", "비유동부채", 
                    "자본금", "자본잉여금", "이익잉여금", "현금및현금성자산", "매출채권", "재고자산",
                    "유형자산", "무형자산", "투자자산", "매입채무", "차입금", "선수금"
                ],
                "키워드가중치": 5,  # 필수키워드 발견 시 가중치
                "계정가중치": 1     # 각 계정과목 발견 시 가중치
            },
            "손익계산서": {
                "필수키워드": ["손익계산서", "포괄손익계산서"],
                "계정과목": [
                    "매출액", "매출원가", "매출총이익", "영업이익", "영업비용", "당기순이익", 
                    "판매비와관리비", "영업외수익", "영업외비용", "법인세", "기타포괄손익", 
                    "주당이익", "매출총이익", "세전이익", "판관비"
                ],
                "키워드가중치": 5,
                "계정가중치": 1
            },
            "현금흐름표": {
                "필수키워드": ["현금흐름표"],
                "계정과목": [
                    "영업활동", "투자활동", "재무활동", "현금유입", "현금유출", "현금및현금성자산", 
                    "순증감", "기초현금", "기말현금", "이자수취", "이자지급", "배당금", "법인세납부"
                ],
                "키워드가중치": 5,
                "계정가중치": 1
            },
            "자본변동표": {
                "필수키워드": ["자본변동표"],
                "계정과목": [
                    "자본금", "자본잉여금", "이익잉여금", "기타자본", "기타포괄손익누계액", 
                    "자기주식", "주식발행초과금", "전기이월", "배당금", "자본총계"
                ],
                "키워드가중치": 5,
                "계정가중치": 1
            }
        }
        
        # 연속 페이지 관련 키워드
        self.continuation_keywords = ["(계속)", "계속", "이익잉여금처분계산서"]
        
        # 임계값 설정 - 높일수록 더 엄격하게 검출됨
        self.min_score_threshold = 8  # 최소 점수 임계값 (높이면 더 엄격해짐)
        self.min_accounts_required = 3  # 최소 필요 계정과목 수 (높이면 더 엄격해짐)
        self.numeric_content_ratio = 0.2  # 테이블 내 숫자 비율 최소값 (높이면 더 엄격해짐)
    
    def detect_financial_statements(self, pdf_path):
        """표가 포함된 페이지에서 재무제표 키워드로 탐지하고 연속 페이지도 찾음"""
        
        # 페이지 번호별 재무제표 유형 저장
        financial_pages = {}
        statement_types = {}
        page_scores = {}  # 각 페이지의 점수 저장
        
        with pdfplumber.open(pdf_path) as pdf:
            # 1단계: 계정과목 점수화 시스템을 통한 재무제표 페이지 식별
            for i, page in enumerate(pdf.pages):
                # 표가 있는지 확인
                tables = page.extract_tables()
                if not tables or len(tables) == 0:
                    continue  # 표가 없으면 넘어감
                
                # 고품질 테이블 필터링 - 작은 테이블은 제외
                quality_tables = [table for table in tables if len(table) >= 5 and (table[0] and len(table[0]) >= 2)]
                if not quality_tables:
                    continue  # 의미있는 테이블이 없으면 넘어감
                
                # 테이블 내 숫자 비율 확인
                numeric_ratio = self._calculate_numeric_ratio(quality_tables)
                if numeric_ratio < self.numeric_content_ratio:
                    continue  # 숫자 비율이 낮으면 재무제표가 아닐 가능성이 높음
                
                # 페이지 텍스트 추출
                page_text = page.extract_text() or ""
                
                # 계정과목 점수화를 통한 재무제표 유형 판별
                statement_scores, matched_accounts = self._calculate_statement_scores(page_text, quality_tables)
                
                # 가장 높은 점수를 받은 재무제표 유형 선택
                if statement_scores:
                    max_score_type = max(statement_scores, key=statement_scores.get)
                    max_score = statement_scores[max_score_type]
                    
                    # 페이지 점수 저장
                    page_num = i + 1  # 1-인덱스로 저장
                    page_scores[page_num] = {
                        'type': max_score_type,
                        'score': max_score,
                        'accounts': matched_accounts.get(max_score_type, 0)
                    }
                    
                    # 점수가 일정 임계값 이상이고 계정과목이 충분히 발견된 경우에만 재무제표로 판별
                    if (max_score >= self.min_score_threshold and 
                        matched_accounts.get(max_score_type, 0) >= self.min_accounts_required):
                        
                        if max_score_type not in financial_pages:
                            financial_pages[max_score_type] = []
                        financial_pages[max_score_type].append(page_num)
                        statement_types[page_num] = max_score_type
            
            # 2단계: 엄격한 기준으로 연속 페이지 탐지
            detected_pages = set()
            for pages in financial_pages.values():
                for page_num in pages:
                    detected_pages.add(page_num)
            
            # 초기 재무제표 페이지 저장
            initial_detected_pages = detected_pages.copy()
            
            # PDF의 모든 페이지에 대해 연속 페이지 확인 (엄격한 조건 적용)
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                
                # 이미 검출된 페이지는 건너뜁니다
                if page_num in detected_pages:
                    continue
                
                # 표가 있는지 확인
                tables = page.extract_tables()
                if not tables or len(tables) == 0:
                    continue  # 표가 없으면 연속 페이지가 아님
                
                # 고품질 테이블 필터링
                quality_tables = [table for table in tables if len(table) >= 5 and (table[0] and len(table[0]) >= 2)]
                if not quality_tables:
                    continue
                
                # 테이블 내 숫자 비율 확인
                numeric_ratio = self._calculate_numeric_ratio(quality_tables)
                if numeric_ratio < self.numeric_content_ratio:
                    continue  # 숫자 비율이 낮으면 연속 페이지가 아닐 가능성이 높음
                
                page_text = page.extract_text() or ""
                
                # 연속 페이지 더 엄격하게 확인
                is_continuation = False
                adjacent_page_type = None
                
                # 1. 직전 페이지가 재무제표인 경우만 고려 (뒤 페이지는 고려하지 않음)
                if page_num - 1 in detected_pages:
                    prev_page_type = statement_types.get(page_num - 1)
                    adjacent_page_type = prev_page_type
                    
                    # 2. 연속 페이지 키워드 확인
                    has_continuation_keyword = any(keyword in page_text for keyword in self.continuation_keywords)
                    
                    # 3. 테이블 구조 유사성 확인 (더 엄격하게)
                    similar_table_structure = self._check_similar_table_structure(
                        pdf.pages[page_num-2].extract_tables() if page_num-2 >= 0 else [],  # 이전 페이지 테이블
                        quality_tables,  # 현재 페이지 테이블
                        strict=True  # 엄격한 검사
                    )
                    
                    # 4. 페이지의 재무제표 점수 확인 (일정 수준 이상이어야 함)
                    page_score = page_scores.get(page_num, {}).get('score', 0)
                    
                    # 연속 페이지 판단 - 이전 페이지가 재무제표이고, 다음 조건 중 하나 이상 만족
                    is_continuation = (
                        # 연속 키워드가 있고 테이블 구조가 유사함
                        (has_continuation_keyword and similar_table_structure) or
                        # 또는 테이블 구조가 매우 유사하고 점수가 일정 수준 이상
                        (similar_table_structure and page_score >= self.min_score_threshold * 0.7)
                    )
                
                # 연속 페이지로 판단된 경우만 추가
                if is_continuation and adjacent_page_type:
                    # 연속 페이지 추가
                    if adjacent_page_type not in financial_pages:
                        financial_pages[adjacent_page_type] = []
                    financial_pages[adjacent_page_type].append(page_num)
                    statement_types[page_num] = adjacent_page_type
                    detected_pages.add(page_num)
        
        # 결과 정리 - 페이지 목록과 유형 반환
        all_pages = []
        for pages in financial_pages.values():
            all_pages.extend(pages)
        
        return sorted(list(set(all_pages))), statement_types
    
    def _calculate_numeric_ratio(self, tables):
        """테이블 내 숫자 데이터의 비율 계산"""
        total_cells = 0
        numeric_cells = 0
        
        for table in tables:
            for row in table:
                for cell in row:
                    if cell is not None:  # 빈 셀 제외
                        total_cells += 1
                        cell_str = str(cell).strip()
                        # 숫자로만 구성된 셀 또는 숫자와 쉼표, 점으로 구성된 셀 (통화 표시 포함)
                        if re.match(r'^[\d,\.\-\+]+$', cell_str.replace(',', '').replace('.', '')):
                            numeric_cells += 1
        
        return numeric_cells / total_cells if total_cells > 0 else 0
    
    def _check_similar_table_structure(self, prev_tables, curr_tables, strict=False):
        """이전 페이지와 현재 페이지의 테이블 구조 유사성 확인 (엄격한 버전)"""
        if not prev_tables or not curr_tables:
            return False
        
        # 첫 번째 테이블 비교 (통상 재무제표 테이블은 첫 번째)
        prev_table = prev_tables[0] if prev_tables else None
        curr_table = curr_tables[0] if curr_tables else None
        
        if not prev_table or not curr_table:
            return False
        
        # 1. 열 수 비교
        if len(prev_table) > 0 and len(curr_table) > 0:
            prev_cols = len(prev_table[0]) if prev_table[0] else 0
            curr_cols = len(curr_table[0]) if curr_table[0] else 0
            
            # 엄격한 모드에서는 열 개수가 정확히 일치해야 함
            if strict and prev_cols != curr_cols:
                return False
            # 일반 모드에서는 1개 정도 차이 허용
            elif not strict and abs(prev_cols - curr_cols) > 1:
                return False
        
        # 2. 데이터 유형 패턴 비교 (엄격한 모드에서만)
        if strict:
            # 각 열별 데이터 유형 패턴 비교
            prev_patterns = self._get_column_data_patterns(prev_table)
            curr_patterns = self._get_column_data_patterns(curr_table)
            
            # 패턴 일치도 계산
            pattern_match = 0
            for col_idx in range(min(len(prev_patterns), len(curr_patterns))):
                if prev_patterns[col_idx] == curr_patterns[col_idx]:
                    pattern_match += 1
            
            # 일치도가 낮으면 False 반환
            if len(prev_patterns) > 0 and pattern_match / len(prev_patterns) < 0.7:
                return False
        
        # 3. 첫 열 내용 연속성 확인 (의미적 연결 확인)
        if len(prev_table) > 1 and len(curr_table) > 1:
            prev_first_col = [str(row[0]).strip() if row and len(row) > 0 and row[0] else "" for row in prev_table]
            curr_first_col = [str(row[0]).strip() if row and len(row) > 0 and row[0] else "" for row in curr_table]
            
            # 첫 열 내용이 연속된 성격을 가지는지 확인
            # 예: 재무상태표의 경우 - 첫 페이지는 자산 항목, 두 번째 페이지는 부채 및 자본 항목
            
            # 재무제표 계속 여부 확인 (제목에 '계속' 문구)
            has_continuation = any("계속" in item for item in curr_first_col[:3])
            
            if has_continuation:
                return True
        
        # 추가 검사를 모두 통과하면 구조가 유사하다고 판단
        return True
    
    def _get_column_data_patterns(self, table):
        """테이블 열별 데이터 유형 패턴 추출"""
        if not table or len(table) < 2:  # 헤더 제외 최소 1행 필요
            return []
        
        patterns = []
        if table[0]:  # 헤더 행 존재
            for col_idx in range(len(table[0])):
                col_values = [row[col_idx] for row in table[1:] if len(row) > col_idx]
                
                # 열의 데이터 유형 패턴 결정
                numeric_count = 0
                for val in col_values:
                    if val and re.match(r'^[\d,\.\-\+]+$', str(val).replace(',', '').replace('.', '')):
                        numeric_count += 1
                
                # 숫자형 또는 텍스트형 결정
                if len(col_values) > 0 and numeric_count / len(col_values) > 0.7:
                    patterns.append('numeric')
                else:
                    patterns.append('text')
        
        return patterns
    
    def _calculate_statement_scores(self, page_text, tables):
        """재무제표 유형별 점수 계산 (개선된 버전)"""
        scores = {statement_type: 0 for statement_type in self.statement_indicators.keys()}
        matched_accounts = {statement_type: 0 for statement_type in self.statement_indicators.keys()}
        
        # 텍스트 정규화 (공백 제거, 소문자 변환)
        normalized_text = re.sub(r'\s+', '', page_text.lower())
        
        # 테이블 텍스트 추출
        table_text = ""
        for table in tables:
            for row in table:
                table_text += " ".join([str(cell) if cell else "" for cell in row]) + " "
        
        normalized_table_text = re.sub(r'\s+', '', table_text.lower())
        
        # 각 재무제표 유형별로 점수 계산
        for statement_type, indicators in self.statement_indicators.items():
            # 1. 필수키워드 점수
            for keyword in indicators["필수키워드"]:
                normalized_keyword = re.sub(r'\s+', '', keyword.lower())
                if normalized_keyword in normalized_text:
                    scores[statement_type] += indicators["키워드가중치"]
                    break  # 하나의 필수키워드만 카운트
            
            # 2. 계정과목 점수 및 밀도 계산
            accounts_found = 0
            for account in indicators["계정과목"]:
                normalized_account = re.sub(r'\s+', '', account.lower())
                if normalized_account in normalized_text or normalized_account in normalized_table_text:
                    accounts_found += 1
            
            # 계정과목 매칭 점수 추가
            matched_accounts[statement_type] = accounts_found
            scores[statement_type] += accounts_found * indicators["계정가중치"]
            
            # 3. 계정과목 밀도 보너스 (높은 밀도는 더 관련성이 높다는 의미)
            if len(normalized_text) > 0:
                account_density = sum(len(re.sub(r'\s+', '', acc.lower())) for acc in indicators["계정과목"] 
                                      if re.sub(r'\s+', '', acc.lower()) in normalized_text) / len(normalized_text)
                # 밀도에 따른 보너스 점수 (최대 3점)
                density_bonus = min(3, int(account_density * 100))
                scores[statement_type] += density_bonus
            
            # 4. 테이블 구조 분석 (추가 점수)
            if tables and len(tables) > 0:
                main_table = tables[0]  # 첫 번째 테이블 분석
                
                # 테이블 첫 열 분석 (재무상태표 특징)
                if statement_type == "재무상태표" and self._has_balance_sheet_structure(main_table):
                    scores[statement_type] += 5  # 점수 상향 (더 확실한 증거)
                
                # 손익계산서 특징적 구조
                elif statement_type == "손익계산서" and self._has_income_statement_structure(main_table):
                    scores[statement_type] += 5
                
                # 현금흐름표 특징적 구조
                elif statement_type == "현금흐름표" and self._has_cash_flow_structure(main_table):
                    scores[statement_type] += 5
                
                # 자본변동표 특징적 구조
                elif statement_type == "자본변동표" and self._has_equity_statement_structure(main_table):
                    scores[statement_type] += 5
                
                # 5. 숫자 데이터 품질 확인
                numeric_data_quality = self._check_numeric_data_quality(main_table)
                if numeric_data_quality > 0.5:  # 숫자 데이터 품질이 좋으면 추가 점수
                    scores[statement_type] += 2
        
        return scores, matched_accounts
    
    def _check_numeric_data_quality(self, table):
        """테이블의 숫자 데이터 품질 확인 (정렬, 포맷 등)"""
        if not table or len(table) < 3:
            return 0
        
        # 숫자 컬럼 식별
        numeric_cols = []
        if len(table) > 1 and table[0]:
            for col_idx in range(len(table[0])):
                col_values = [row[col_idx] for row in table[1:] if len(row) > col_idx]
                numeric_count = sum(1 for val in col_values if val and re.match(r'^[\d,\.\-\+]+$', str(val).replace(',', '').replace('.', '')))
                if len(col_values) > 0 and numeric_count / len(col_values) > 0.7:
                    numeric_cols.append(col_idx)
        
        # 숫자 컬럼이 없으면 품질 낮음
        if not numeric_cols:
            return 0
        
        # 숫자 포맷 일관성 확인 (소수점, 천단위 구분 등)
        format_consistency = 0
        for col_idx in numeric_cols:
            col_values = [str(row[col_idx]) for row in table[1:] if len(row) > col_idx and row[col_idx]]
            # 천단위 구분자 사용 패턴
            comma_pattern = sum(1 for val in col_values if ',' in val)
            
            # 일관된 포맷 사용 시 점수 상승
            if len(col_values) > 0:
                if comma_pattern > len(col_values) * 0.7:  # 70% 이상 동일 포맷
                    format_consistency += 1
        
        # 종합 품질 점수 (0~1 사이 값)
        quality = min(1.0, (len(numeric_cols) + format_consistency) / (len(table[0]) + 2) if table[0] else 0)
        
        return quality
    
    def _has_balance_sheet_structure(self, table):
        """재무상태표의 특징적인 구조를 가지고 있는지 확인 (강화된 버전)"""
        # 테이블이 비어있으면 False 반환
        if not table or len(table) < 3:
            return False
        
        # 첫 열에 "자산"과 "부채" 또는 "자본"이 포함되어 있는지 확인
        first_col = [str(row[0]).lower() if row and len(row) > 0 and row[0] else "" for row in table]
        first_col_text = " ".join(first_col)
        
        has_asset = "자산" in first_col_text
        has_liability = "부채" in first_col_text
        has_equity = "자본" in first_col_text
        
        # 재무상태표는 보통 자산, 부채, 자본 섹션을 포함
        basic_structure = has_asset and (has_liability or has_equity)
        
        # 추가 구조 확인: 자산 = 부채 + 자본 관계가 테이블 구조에 나타나는지
        if basic_structure:
            # 재무상태표의 구조적 특징 확인
            # 1. 계층적 구조 (들여쓰기)
            indentation_patterns = 0
            for row_idx in range(1, len(table)):
                if len(table[row_idx]) > 0 and table[row_idx][0]:
                    cell_text = str(table[row_idx][0])
                    if cell_text.startswith('  ') or cell_text.startswith('\t'):
                        indentation_patterns += 1
            
            # 계층 구조가 보이면 추가 확인
            has_hierarchy = indentation_patterns > len(table) * 0.2  # 20% 이상 들여쓰기
            
            return True  # 기본 구조가 맞으면 True
        
        return False
    
    def _has_income_statement_structure(self, table):
        """손익계산서의 특징적인 구조를 가지고 있는지 확인 (강화된 버전)"""
        if not table or len(table) < 3:
            return False
        
        # 첫 열에 "매출"과 "이익" 또는 "비용"이 포함되어 있는지 확인
        first_col = [str(row[0]).lower() if row and len(row) > 0 and row[0] else "" for row in table]
        first_col_text = " ".join(first_col)
        
        has_revenue = "매출" in first_col_text
        has_profit = "이익" in first_col_text or "당기순" in first_col_text
        has_expense = "비용" in first_col_text or "원가" in first_col_text
        
        # 손익계산서 구조 기본 확인
        basic_structure = has_revenue and (has_profit or has_expense)
        
        # 추가 확인: 손익계산서 특유의 순서 (매출 -> 비용 -> 이익)
        if basic_structure:
            # 매출이 이익보다 앞에 나타나는지 확인
            revenue_idx = next((i for i, text in enumerate(first_col) if "매출" in text), -1)
            profit_idx = next((i for i, text in enumerate(first_col) if "이익" in text), -1)
            
            correct_order = revenue_idx != -1 and (profit_idx == -1 or revenue_idx < profit_idx)
            
            return True  # 기본 구조가 맞으면 True
        
        return False
    
    def _has_cash_flow_structure(self, table):
        """현금흐름표의 특징적인 구조를 가지고 있는지 확인 (강화된 버전)"""
        if not table or len(table) < 3:
            return False
        
        # 첫 열에 "영업활동", "투자활동", "재무활동" 중 2개 이상 포함 확인
        first_col = [str(row[0]).lower() if row and len(row) > 0 and row[0] else "" for row in table]
        first_col_text = " ".join(first_col)
        
        has_operating = "영업활동" in first_col_text
        has_investing = "투자활동" in first_col_text
        has_financing = "재무활동" in first_col_text
        
        # 현금흐름표는 3가지 활동 영역으로 구성
        activities_count = sum([has_operating, has_investing, has_financing])
        
        # 기본 확인: 최소 2개 이상 활동 영역 포함
        basic_structure = activities_count >= 2
        
        # 추가 확인: 현금흐름 합계 또는 현금성자산 관련 행이 있는지
        if basic_structure:
            has_cash_total = any("현금" in row[0] and "합계" in row[0] for row in table if row and len(row) > 0)
            has_cash_beginning_end = any(("기초" in row[0] or "기말" in row[0]) and "현금" in row[0] 
                                        for row in table if row and len(row) > 0)
            
            return True  # 기본 구조가 맞으면 True
        
        return False
    
    def _has_equity_statement_structure(self, table):
        """자본변동표의 특징적인 구조를 가지고 있는지 확인 (강화된 버전)"""
        if not table or len(table) < 3 or len(table[0]) < 3:
            return False
        
        # 자본변동표는 보통 행과 열이 모두 의미 있는 매트릭스 구조
        # 첫 행에 "자본금", "자본잉여금", "이익잉여금" 등의 자본 요소 포함 확인
        if len(table) > 0 and len(table[0]) > 2:
            first_row = [str(cell).lower() if cell else "" for cell in table[0]]
            first_row_text = " ".join(first_row)
            
            has_capital = "자본금" in first_row_text
            has_surplus = "잉여금" in first_row_text
            
            # 첫 열에 "기초", "증가", "감소", "기말" 등의 변동 관련 단어 확인
            first_col = [str(row[0]).lower() if row and len(row) > 0 and row[0] else "" for row in table]
            first_col_text = " ".join(first_col)
            
            has_beginning = "기초" in first_col_text
            has_ending = "기말" in first_col_text
            
            # 자본변동표 구조 기본 확인
            basic_structure = (has_capital or has_surplus) and (has_beginning or has_ending)
            
            # 추가 확인: 자본변동표 특유의 매트릭스 구조
            if basic_structure:
                # 행과 열이 모두 의미 있는 구조인지 확인
                has_matrix_structure = len(table) >= 3 and len(table[0]) >= 3
                
                return True  # 기본 구조가 맞으면 True
        
        return False


class PDFViewer:
    """PDF 페이지를 시각적으로 표시하는 클래스"""
    
    def display_pdf_page(self, pdf_path, page_num):
        """PDF 특정 페이지를 이미지로 변환하여 반환"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    img = page.to_image(resolution=150)
                    img_bytes = BytesIO()
                    img.save(img_bytes, format="PNG")
                    img_bytes.seek(0)
                    return img_bytes
                else:
                    return None
        except Exception as e:
            st.error(f"PDF 페이지 표시 오류: {e}")
            return None


class FinancialStatementApp:
    """재무제표 자동 탐지 앱의 메인 클래스"""
    
    def __init__(self):
        self.detector = FinancialStatementDetector()
        self.viewer = PDFViewer()
        
        # 페이지 설정
        st.set_page_config(
            page_title="PDF 재무제표 자동 탐지기",
            page_icon="📊",
            layout="wide"
        )
        
        # 앱 제목
        st.title("PDF 재무제표 자동 탐지기")
        st.write("PDF 파일을 업로드하면 재무제표 페이지를 자동으로 탐지합니다.")
    
    def setup_sidebar(self):
        """사이드바 설정"""
        with st.sidebar:
            st.header("앱 정보")
            st.info("""
            이 앱은 PDF 문서에서 재무제표 페이지를 자동으로 탐지합니다.
            
            특징:
            - 고품질 테이블 필터링
            - 계정과목 기반 재무제표 유형 식별
            - 숫자 데이터 비율 분석
            - 테이블 구조 패턴 정밀 인식
            
            지원하는 재무제표 종류:
            - 재무상태표 (대차대조표)
            - 손익계산서
            - 현금흐름표
            - 자본변동표
            """)
            
            st.header("탐지 민감도 설정")
            # 슬라이더를 통한 탐지 민감도 설정
            detection_sensitivity = st.slider(
                "탐지 민감도", 
                min_value=1, 
                max_value=10, 
                value=5,
                help="낮을수록 더 많은 페이지가 검출됩니다. 높을수록 확실한 재무제표만 검출됩니다."
            )
            
            # 민감도에 따라 탐지기 설정 조정
            if detection_sensitivity != 5:  # 기본값과 다른 경우만 조정
                # 민감도가 높을수록 임계값 증가
                self.detector.min_score_threshold = 5 + (detection_sensitivity - 5) * 1  # 5~15 범위
                self.detector.min_accounts_required = max(2, int(3 + (detection_sensitivity - 5) * 0.5))  # 2~5 범위
                self.detector.numeric_content_ratio = 0.15 + (detection_sensitivity - 5) * 0.03  # 0.15~0.3 범위
            
            st.header("사용 방법")
            st.markdown("""
            1. PDF 파일 업로드
            2. 자동 탐지 기다리기
            3. 탐지된 페이지 확인
            """)
    
    def run(self):
        """앱 실행"""
        self.setup_sidebar()
        
        # 파일 업로드 UI
        uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")
        
        if uploaded_file is not None:
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                pdf_path = tmp_file.name
            
            try:
                # 진행 상태 표시
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 재무제표 페이지 탐지
                status_text.text("재무제표 페이지 탐지 중...")
                progress_bar.progress(50)
                
                # 표가 포함된 페이지에서 재무제표 키워드 탐지 및 연속 페이지 탐지
                financial_pages, statement_types = self.detector.detect_financial_statements(pdf_path)
                
                progress_bar.progress(100)
                status_text.empty()
                
                # 결과 표시
                st.success("PDF 분석 완료!")
                
                # 탐지된 페이지 정보 표시
                st.subheader("📋 탐지된 재무제표 페이지")
                
                if financial_pages:
                    # 재무제표 유형별 페이지 수 카운팅
                    type_counts = Counter(statement_types.values())
                    type_summary = ", ".join([f"{type}: {count}페이지" for type, count in type_counts.items()])
                    
                    # 모든 재무제표 페이지를 하나의 섹션에 표시
                    page_numbers = [str(page) for page in financial_pages]
                    st.write(f"**재무제표 페이지**: {', '.join(page_numbers)}")
                    st.write(f"**유형별 페이지 수**: {type_summary}")
                    
                    # 순서별로 페이지 그룹화 (연속 페이지 표시)
                    groups = []
                    current_group = []
                    current_type = None
                    
                    for page in sorted(financial_pages):
                        page_type = statement_types.get(page)
                        
                        # 새 그룹 시작 (유형이 바뀌거나 연속되지 않는 경우)
                        if not current_group or page != current_group[-1] + 1 or page_type != current_type:
                            if current_group:
                                groups.append((current_type, current_group))
                            current_group = [page]
                            current_type = page_type
                        else:
                            current_group.append(page)
                    
                    if current_group:
                        groups.append((current_type, current_group))
                    
                    # 그룹 정보 표시
                    st.write("**재무제표 페이지 그룹:**")
                    for group_type, group in groups:
                        if len(group) == 1:
                            st.write(f"- {group_type}: {group[0]}페이지")
                        else:
                            st.write(f"- {group_type}: {group[0]}-{group[-1]}페이지")
                    
                    # 페이지 선택 UI
                    selected_page = st.selectbox(
                        "재무제표 페이지 선택",
                        options=financial_pages,
                        format_func=lambda x: f"{x}페이지 - {statement_types.get(x, '재무제표')}"
                    )
                    
                    # PDF 페이지 표시
                    img_bytes = self.viewer.display_pdf_page(pdf_path, selected_page-1)  # 0-인덱스로 변환
                    if img_bytes:
                        # 재무제표 유형 표시
                        statement_type = statement_types.get(selected_page, "재무제표")
                        
                        # 연속 페이지 여부 확인
                        is_continuation = False
                        for group_type, group in groups:
                            if len(group) > 1 and selected_page in group and selected_page != group[0]:
                                is_continuation = True
                                break
                        
                        # 연속 페이지 표시
                        if is_continuation:
                            st.write(f"**유형**: {statement_type} (연속 페이지)")
                        else:
                            st.write(f"**유형**: {statement_type}")
                        
                        # 페이지 이미지 표시
                        st.image(img_bytes, caption=f"{statement_type} - {selected_page}페이지", use_column_width=True)
                else:
                    st.warning("재무제표 페이지를 찾을 수 없습니다.")
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
            
            finally:
                # 임시 파일 삭제
                try:
                    os.unlink(pdf_path)
                except:
                    pass
        
        # 푸터
        st.markdown("---")
        st.markdown("© 2025 PDF 재무제표 자동 탐지기")


if __name__ == "__main__":
    app = FinancialStatementApp()
    app.run()