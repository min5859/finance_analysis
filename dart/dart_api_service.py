import requests
import logging
import zipfile
import io
import xml.etree.ElementTree as ET
import os
import streamlit as st

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance_analysis")

class DartApiService:
    """DART OpenAPI와 상호작용하는 서비스 클래스"""
    
    def __init__(self, api_key=None):
        """DART API 서비스 클래스 초기화
        
        Args:
            api_key (str, optional): DART OpenAPI 키. 없으면 환경변수나 Streamlit secrets에서 로드
        """
        # API 키 설정
        self.api_key = api_key if api_key else self._get_api_key()
        self.base_url = "https://opendart.fss.or.kr/api"
        
        if not self.api_key:
            logger.warning("API 키가 설정되지 않았습니다.")
    
    def _get_api_key(self):
        """환경변수 또는 Streamlit secrets에서 API 키 가져오기"""
        api_key = ""
        # 환경변수에서 시도
        try:
            api_key = os.getenv("DART_API_KEY", "")
        except:
            pass
            
        # Streamlit secrets에서 시도
        if not api_key:
            try:
                api_key = st.secrets["DART_API_KEY"]
            except:
                pass
                
        return api_key
    
    def get_corp_codes(self):
        """기업 코드 목록 조회
        
        Returns:
            list: 기업 코드, 이름, 주식 코드 정보 목록
        """
        url = f"{self.base_url}/corpCode.xml"
        params = {
            "crtfc_key": self.api_key
        }
        
        if not self.api_key:
            logger.error("API 키가 없습니다.")
            return None
        
        try:
            logger.info("기업 코드 목록 조회 API 호출")
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"API 호출 에러: {response.status_code}")
                return None
            
            # zip 파일을 메모리에서 처리
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                xml_data = zip_file.read(zip_file.namelist()[0])
            
            # XML 파싱
            root = ET.fromstring(xml_data)
            corp_list = []
            
            for company in root.findall('list'):
                corp_code = company.findtext('corp_code')
                corp_name = company.findtext('corp_name')
                stock_code = company.findtext('stock_code')
                modify_date = company.findtext('modify_date')
                
                if stock_code and stock_code.strip():  # 상장 기업만 필터링
                    corp_list.append({
                        'corp_code': corp_code,
                        'corp_name': corp_name,
                        'stock_code': stock_code,
                        'modify_date': modify_date
                    })
            
            logger.info(f"총 {len(corp_list)}개의 기업 코드를 검색했습니다.")
            return corp_list
        except Exception as e:
            logger.error(f"기업 코드 조회 오류: {str(e)}")
            return None
    
    def get_company_info(self, corp_code):
        """기업 기본 정보 조회
        
        Args:
            corp_code (str): 기업 고유 코드
            
        Returns:
            dict: 기업 기본 정보
        """
        url = f"{self.base_url}/company.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code
        }
        
        try:
            logger.info(f"기업 정보 API 호출: {corp_code}")
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"기업 정보 조회 에러: {response.status_code}")
                return None
            
            data = response.json()
            if data.get('status') != '000':
                logger.error(f"기업 정보 API 오류: {data.get('message')}")
                return None
            
            return data
        except Exception as e:
            logger.error(f"기업 정보 조회 오류: {str(e)}")
            return None
    
    def get_audit_report(self, corp_code, bsns_year, reprt_code="11011"):
        """감사 보고서 정보 조회
        
        Args:
            corp_code (str): 기업 고유 코드
            bsns_year (str): 사업연도
            reprt_code (str, optional): 보고서 코드. 기본값은 "11011" (사업보고서)
            
        Returns:
            dict: 감사 보고서 정보
        """
        # 외부감사 실시 현황 조회
        audit_url = f"{self.base_url}/irdsSttus.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code
        }
        
        try:
            logger.info(f"감사 보고서 API 호출: {corp_code} {bsns_year}")
            response = requests.get(audit_url, params=params)
            
            if response.status_code != 200:
                logger.error(f"감사 보고서 조회 에러: {response.status_code}")
                return None
            
            data = response.json()
            if data.get('status') != '000':
                logger.error(f"감사 보고서 API 오류: {data.get('message')}")
                return None
            
            # 공시 서류 원문 정보 조회
            disc_url = f"{self.base_url}/list.json"
            disc_params = {
                "crtfc_key": self.api_key,
                "corp_code": corp_code,
                "bsns_year": bsns_year,
                "pblntf_ty": "A",
                "page_count": 100
            }
            
            disc_response = requests.get(disc_url, params=disc_params)
            if disc_response.status_code != 200:
                logger.error(f"공시 목록 조회 에러: {disc_response.status_code}")
                return data  # 외부감사 정보만이라도 반환
            
            disc_data = disc_response.json()
            if disc_data.get('status') != '000':
                logger.error(f"공시 목록 API 오류: {disc_data.get('message')}")
                return data  # 외부감사 정보만이라도 반환
            
            # 공시 목록에서 감사보고서 찾기
            audit_reports = []
            for item in disc_data.get('list', []):
                report_nm = item.get('report_nm', '')
                if '감사보고서' in report_nm:
                    # 해당 보고서의 상세 정보 가져오기
                    rcp_no = item.get('rcept_no')
                    doc_url = f"{self.base_url}/document.json"
                    doc_params = {
                        "crtfc_key": self.api_key,
                        "rcept_no": rcp_no
                    }
                    
                    doc_response = requests.get(doc_url, params=doc_params)
                    if doc_response.status_code == 200:
                        doc_data = doc_response.json()
                        if doc_data.get('status') == '000':
                            # 원본 공시 정보와 문서 정보 합치기
                            combined_data = {
                                'disclosure_info': item,
                                'document_info': doc_data
                            }
                            audit_reports.append(combined_data)
            
            # 외부감사 정보와 감사보고서 정보 합치기
            data['audit_reports'] = audit_reports
            return data
            
        except Exception as e:
            logger.error(f"감사 보고서 조회 오류: {str(e)}")
            return None
    
    def get_financial_statements(self, corp_code, bsns_year, reprt_code="11011"):
        """사업보고서 재무제표 정보 조회
        
        Args:
            corp_code (str): 기업 고유 코드
            bsns_year (str): 사업연도
            reprt_code (str, optional): 보고서 코드. 기본값은 "11011" (사업보고서)
            
        Returns:
            dict: 재무제표 정보
        """
        url = f"{self.base_url}/fnlttSinglAcntAll.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code,
            "fs_div": "CFS"  # 연결재무제표
        }
        
        try:
            logger.info(f"재무제표 API 호출: {corp_code} {bsns_year}")
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                logger.error(f"재무제표 조회 에러: {response.status_code}")
                return None
            
            data = response.json()
            if data.get('status') != '000':
                logger.error(f"재무제표 API 오류: {data.get('message')}")
                return None
            
            return data
        except Exception as e:
            logger.error(f"재무제표 조회 오류: {str(e)}")
            return None