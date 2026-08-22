# A2-1 브랜드 아이덴티티 생성기

> 냉장고 속 재료로 오늘의 한 끼를 제안하는 푸드테크 서비스를 위한 AI 브랜드 제작 프로젝트

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
![Project](https://img.shields.io/badge/Codyssey-Term%20Project-F97316)

브랜드 브리프 하나를 입력하면 AI가 브랜드명, 슬로건, 스토리, 컬러 팔레트와 로고 시안을 순서대로 생성합니다. 팀원이 나누어 만든 기능을 `main.py` 하나에 통합해 전체 과정을 한 번에 실행할 수 있습니다.

## 결과 미리보기

| 로고 시안 1 | 로고 시안 2 |
|---|---|
| ![로고 시안 1](https://raw.githubusercontent.com/Frost0313z/A2-1/master/02.%20AI%20%ED%99%9C%EC%9A%A9%20%ED%95%99%EC%8A%B5/%ED%8C%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/output/logo_01.png) | ![로고 시안 2](https://raw.githubusercontent.com/Frost0313z/A2-1/master/02.%20AI%20%ED%99%9C%EC%9A%A9%20%ED%95%99%EC%8A%B5/%ED%8C%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/output/logo_02.png) |

![한글 폰트가 적용된 브랜드 컬러 팔레트](https://raw.githubusercontent.com/Frost0313z/A2-1/master/02.%20AI%20%ED%99%9C%EC%9A%A9%20%ED%95%99%EC%8A%B5/%ED%8C%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8/output/color_palette.png?v=3)

## 주요 기능

- 브랜드명 후보 3~5개와 의미 생성
- 브랜드 톤에 맞는 슬로건 3개 생성
- 탄생 배경과 철학을 담은 브랜드 스토리 생성
- 메인 컬러 1개와 서브 컬러 2~3개 추천
- 컬러 팔레트 PNG 자동 제작
- 서로 다른 방향의 로고 시안 2개 생성
- 모든 결과를 `brand_result.json`으로 통합 저장

## 동작 흐름

```text
brief.json
    ↓
브랜드 네이밍과 슬로건
    ↓
브랜드 스토리
    ↓
컬러 팔레트
    ↓
로고 시안 2개
    ↓
output/brand_result.json + PNG 결과물
```

## 프로젝트 위치

```text
02. AI 활용 학습/팀프로젝트/
├── main.py                 # 모든 기능을 합친 최종 실행 파일
├── Naming.py               # 네이밍·슬로건 담당 원본
├── content.py              # 브랜드 스토리 담당 원본
├── visual.py               # 컬러·로고 담당 원본
├── brief.json              # 브랜드 입력 정보
├── .env.example            # 환경변수 작성 예시
├── requirements.txt        # 필요한 파이썬 패키지
└── output/
    ├── brand_result.json
    ├── color_palette.png
    ├── logo_01.png
    └── logo_02.png
```

## 시작하기

### 1. 저장소 복제

```bash
git clone https://github.com/Frost0313z/A2-1.git
cd A2-1/"02. AI 활용 학습/팀프로젝트"
```

### 2. 가상환경 생성 및 활성화

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS 또는 Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. API 키 설정

`.env.example`을 복사해 `.env` 파일을 만들고 본인의 API 키를 입력합니다.

```env
OPENAI_API_KEY=여기에_본인의_API_키_입력

OPENAI_MODEL=gpt-4o-mini
OPENAI_TEXT_MODEL=gpt-4.1-mini
OPENAI_IMAGE_MODEL=gpt-image-2
```

> `.env`에는 비밀 API 키가 들어갑니다. GitHub, 메신저, 이메일 등에 공유하지 마세요.

### 5. 브랜드 정보 작성

`brief.json`에서 다음 정보를 원하는 브랜드에 맞게 수정합니다.

```json
{
  "industry": "브랜드 업종",
  "target": "주요 고객",
  "keywords": ["핵심", "키워드"],
  "tone": "브랜드가 말하는 분위기",
  "description": "서비스 설명"
}
```

### 6. 실행

```bash
python main.py
```

실행이 끝나면 `output` 폴더에서 JSON 결과와 PNG 이미지를 확인할 수 있습니다. 이미지 생성 API를 사용하므로 실행 시 API 사용량이 발생할 수 있습니다.

## 팀 역할

| 영역 | 담당 기능 | 파일 |
|---|---|---|
| 통합 | 브리프 입력, 전체 실행, 결과 저장 | `main.py` |
| 네이밍 | 브랜드명과 슬로건 생성 | `Naming.py` |
| 콘텐츠 | 브랜드 스토리 생성 | `content.py` |
| 비주얼 | 컬러 팔레트와 로고 생성 | `visual.py` |

## 현재 테스트 결과

- 전체 파이프라인 정상 종료
- 브랜드명 후보 5개 및 슬로건 3개 생성 확인
- 브랜드 스토리와 컬러 데이터 생성 확인
- 컬러 팔레트 및 로고 PNG 2개 생성 확인
- 최종 `brand_result.json` 저장 확인

## 보안 안내

- 실제 `.env` 파일은 `.gitignore`로 제외되어 있습니다.
- 팀원은 각자 발급받은 API 키를 사용해야 합니다.
- 공개된 키가 있다면 즉시 폐기하고 새 키를 발급하세요.

---

코디세이 AI Native Advanced · Term Project A
