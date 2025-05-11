import tempfile
import base64
from PIL import Image
import io
import os
import fitz  # PyMuPDF for PDF processing
from anthropic import Anthropic
import json

class FinancialStatementProcessor:
    """재무제표 처리 클래스: PDF 병합 및 분석을 처리합니다."""
    
    def __init__(self, api_key=None, prompt_path="prompt.txt", json_template_path="finance_format.json"):
        """
        FinancialStatementProcessor 클래스 초기화
        
        Args:
            api_key (str, optional): Anthropic API 키
            prompt_path (str, optional): 프롬프트 파일 경로
            json_template_path (str, optional): JSON 템플릿 파일 경로
        """
        self.api_key = api_key
        self.prompt_path = os.path.join(os.path.dirname(__file__), prompt_path)
        self.json_template_path = os.path.join(os.path.dirname(__file__), json_template_path)
        self.client = None
        
        if api_key:
            self.client = Anthropic(api_key=api_key)
            
        self.prompt = self.load_prompt()
        self.json_template = self.load_json_template()
    
    def load_prompt(self):
        """프롬프트 파일 로드"""
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return """재무제표 또는 감사보고서를 분석하여 다음 JSON 형식으로 정보를 추출하세요. 
            금액 단위는 억원이며, 비율은 %로 표기합니다. 모든 빈 필드를 채워주세요. 숫자는 소수점 둘째 자리까지만 표기하세요."""
    
    def load_json_template(self):
        """JSON 템플릿 파일 로드"""
        try:
            with open(self.json_template_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "{}"
    
    def set_api_key(self, api_key):
        """API 키 설정"""
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
    
    def merge_pdfs(self, pdf_files):
        """
        여러 PDF 파일을 하나로 병합
        
        Args:
            pdf_files (list): PDF 파일 객체 리스트
            
        Returns:
            bytes: 병합된 PDF 파일 바이트
        """
        merged_pdf = fitz.open()
        
        for pdf_file in pdf_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_file.getvalue())
                temp_path = temp_file.name
            
            pdf_document = fitz.open(temp_path)
            merged_pdf.insert_pdf(pdf_document)
            
            # 임시 파일 삭제
            pdf_document.close()
            os.unlink(temp_path)
        
        # 병합된 PDF를 메모리에 저장
        merged_bytes = io.BytesIO()
        merged_pdf.save(merged_bytes)
        merged_pdf.close()
        
        return merged_bytes.getvalue()
    
    def extract_text_from_pdf(self, pdf_bytes):
        """
        PDF 파일에서 텍스트 추출
        
        Args:
            pdf_bytes (bytes): PDF 파일 바이트
            
        Returns:
            dict: 추출된 텍스트와 페이지 수
        """
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_bytes)
            temp_path = temp_file.name
        
        doc = fitz.open(temp_path)
        text = ""
        page_count = len(doc)
        
        # 텍스트 추출
        for i in range(page_count):
            page = doc[i]
            text += page.get_text()
        
        # 임시 파일 삭제
        doc.close()
        os.unlink(temp_path)
        
        return {
            "text": text,
            "pages": page_count
        }
    
    def process_image(self, image_file):
        """
        이미지 파일 처리
        
        Args:
            image_file: 이미지 파일 객체
            
        Returns:
            dict: 이미지 바이트와 크기 정보
        """
        image = Image.open(image_file)
        
        # 이미지를 메모리에 저장
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        return {
            "image": image_bytes,
            "width": image.width,
            "height": image.height
        }
    
    def encode_image_to_base64(self, image_bytes):
        """이미지를 Base64로 인코딩"""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def _call_claude_api(self, system_message, user_message, temperature=0.1, max_tokens=8000):
        """
        Claude API 호출을 위한 공통 메서드
        
        Args:
            system_message (str): 시스템 메시지
            user_message (str or list): 사용자 메시지
            temperature (float): 모델 온도
            max_tokens (int): 최대 토큰 수
            
        Returns:
            str: API 응답
        """
        if not self.client:
            raise ValueError("API 키가 설정되지 않았습니다.")
            
        response = self.client.messages.create(
            model="claude-3-7-sonnet-20250219",
            system=system_message,
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.content[0].text

    def process_with_claude(self, file_data, temperature=0.1, custom_prompt=None):
        """
        Claude API를 사용하여 파일 처리
        
        Args:
            file_data (dict): 처리할 파일 데이터 (PDF 텍스트, 이미지 또는 JSON 데이터)
            temperature (float, optional): 모델 온도
            custom_prompt (str, optional): 사용자 지정 프롬프트
            
        Returns:
            str: API 응답
        """
        prompt = custom_prompt if custom_prompt else self.prompt
        system_message = f"{prompt}\n\nJSON 템플릿:\n{self.json_template}"
        
        # JSON 데이터 처리
        if isinstance(file_data, dict) and not any(key in file_data for key in ['text', 'image', 'sections']):
            user_message = f"다음 재무제표 데이터를 분석하여 지정된 JSON 형식으로 변환해주세요. 데이터: {json.dumps(file_data, ensure_ascii=False)}"
            return self._call_claude_api(system_message, user_message, temperature)
        
        # PDF 텍스트 처리
        elif 'text' in file_data:
            user_message = f"다음 재무제표 또는 감사보고서 내용을 분석하여 지정된 JSON 형식으로 변환해주세요. 문서 내용: {file_data['text'][:20000]}"
            return self._call_claude_api(system_message, user_message, temperature)
        # 이미지 처리
        elif 'image' in file_data:
            base64_image = self.encode_image_to_base64(file_data['image'])
            user_message = [
                {
                    "type": "text", 
                    "text": "이 재무제표나 감사보고서 이미지를 분석하여 지정된 JSON 형식으로 정보를 추출해주세요."
                },
                {
                    "type": "image", 
                    "source": {
                        "type": "base64", 
                        "media_type": "image/png",
                        "data": base64_image
                    }
                }
            ]
            return self._call_claude_api(system_message, user_message, temperature)
    
    def parse_json_response(self, json_result):
        """
        JSON 응답 파싱
        
        Args:
            json_result (str): JSON 문자열
            
        Returns:
            dict: 파싱된 JSON 객체
        """
        json_str = json_result
        
        # JSON 코드 블록에서 추출 시도
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # JSON 객체로 변환
        return json.loads(json_str)