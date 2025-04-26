# 기업 재무 분석 대시보드

이 프로젝트는 기업의 재무 데이터를 시각화하여 분석하는 대시보드 애플리케이션입니다. 재무제표의 주요 항목과 재무비율을 Chart.js를 사용하여 시각적으로 표현하고, 분석 인사이트를 제공합니다.

## 주요 기능

- 여러 기업의 재무 데이터 분석 가능 (JSON 기반 데이터 로딩)
- 재무상태표, 손익계산서, 현금흐름표 시각화
- 수익성, 성장성, 안정성, 운전자본 효율성 분석
- Chart.js를 사용한 인터랙티브 차트 제공
- 종합 결론 및 전략적 제안 제시

## 설치 방법

1. Python 3.8 이상 설치
2. 필요한 패키지 설치: 
```
pip install -r requirements.txt
```

## 실행 방법

```
streamlit run app.py
```

## 새로운 기업 데이터 추가하기

새로운 기업의 재무 데이터를 추가하려면 다음 단계를 따르세요:

1. `data/companies` 디렉토리에 새로운 JSON 파일을 생성합니다.
2. JSON 파일 형식은 다음과 같은 구조를 가져야 합니다:

```json
{
    "company_name": "회사명",
    "company_code": "종목코드",
    "sector": "업종",
    "performance_data": {
        "year": ["2022", "2023", "2024"],
        "매출액": [9470, 8730, 6760],
        "영업이익": [430, 330, 360],
        "순이익": [360, 360, 430],
        "영업이익률": [4.5, 3.8, 5.4],
        "순이익률": [3.8, 4.2, 6.4]
    },
    "balance_sheet_data": {
        // 재무상태표 관련 데이터
    },
    "stability_data": {
        // 안정성 지표 데이터
    },
    "cash_flow_data": {
        // 현금흐름 데이터
    },
    "working_capital_data": {
        // 운전자본 데이터
    },
    "profitability_data": {
        // 수익성 지표 데이터
    },
    "growth_rates": {
        // 성장률 데이터
    },
    "dupont_data": {
        // 듀폰 분석 데이터
    },
    "radar_data": {
        // 레이더 차트 데이터
    }
}
```

3. 애플리케이션을 실행하고 드롭다운 메뉴에서 새로 추가된 기업을 선택합니다.

## 기존 기업 데이터 변환하기

```python
from data.data_loader import DataLoader

# 기존 데이터 로드
loader = DataLoader()

# JSON 파일로 내보내기
output_file = loader.export_to_json("data/companies/my_company.json")
print(f"데이터가 {output_file}에 저장되었습니다.")
```

## 프로젝트 구조

```
finance_analysis/
├── app.py                  # 애플리케이션 메인 파일
├── config/                 # 설정 파일
├── components/             # 컴포넌트 모듈
│   ├── charts/             # 차트 관련 컴포넌트
│   └── slides/             # 슬라이드 컴포넌트
├── data/                   # 데이터 관련 모듈
│   ├── data_loader.py      # 데이터 로더 클래스
│   └── companies/          # 회사별 JSON 데이터 파일
└── requirements.txt        # 의존성 패키지 목록
```

## 기여하기

이슈나 개선 사항이 있으면 GitHub 이슈를 통해 제보해주세요.