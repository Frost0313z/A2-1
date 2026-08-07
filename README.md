# 코디세이 과제

코디세이 **AI 네이티브 과정**(최대 5개월) 학습 기록 및 과제 저장소.
과정 소개: https://codyssey.kr/daejeon/apply/course

## 과정 개요

| 단계 | 기간 | 내용 |
|---|---|---|
| 01. AI 도구 학습 | 1개월 | 생성형 AI, 자동화 도구 활용 |
| 02. AI 활용 학습 | 1개월 | 개발환경, 언어, AI 코딩도구 |
| 03. AI 응용 학습 | 3개월 + Final-Project | 협업 중심 실전 서비스 개발, 팀 단위 AI Agent Final-Project |

## 폴더 구조

각 단계 폴더 아래에 차시별 폴더를 만들고, 그 안은 아래 3분류로 통일합니다.

```
01. AI 도구 학습/
  <차시 번호>. <차시명>/
    materials/   전달받은 강의자료·참고자료 (원본)
    output/      직접 만든 결과물
    assets/      결과물 제작에 쓰인 이미지 등 리소스
02. AI 활용 학습/
03. AI 응용 학습/
기타/            과정 외 부가 자료 (특강 등)
```

새 차시가 시작되면 `<차시 번호>. <차시명>/materials`, `output`, `assets` 3개 폴더를 만들고 시작하면 됩니다.

Python 프로젝트가 결과물인 미션은 `scripts/new_mission.py`로 반복 작업을 자동화합니다.

**`new` — 세션 폴더 + 표준 파이썬 프로젝트 스캐폴딩**

```bash
python scripts/new_mission.py new 02 "02. Python 심화" todo-cli \
  --description "터미널 할 일 관리 프로그램" --github
```

`<stage> <session_name> <project_name>` 순서로 받아 `output/<project_name>/`에 표준 파이썬 프로젝트(`main.py` + 패키지 + `.gitignore` + `LICENSE` + 목차·기능·설계 노트 구간이 있는 `README.md`)를 만들고 git init·첫 커밋까지 수행합니다. `--github`를 주면 GitHub 저장소 생성과 push까지 이어서 합니다. 이 프로젝트 경로는 자체 GitHub 저장소로 별도 관리되므로 루트 `.gitignore`에 자동으로 추가됩니다.

**`env-doc` — 개발 환경 증빙을 README에 자동 반영**

```bash
python scripts/new_mission.py env-doc "02. AI 활용 학습/01. Python 및 Git 기초/output/prompt-manager" --write
```

`python -V`, `git --version`, `git config user.name/email`, `git log --oneline --graph --all` 실행 결과를 모아 README의 `<!-- ENV_EVIDENCE_START -->` ~ `<!-- ENV_EVIDENCE_END -->` 구간에 채워 넣습니다(마커가 없으면 "개발 환경 확인" 섹션을 새로 추가). `--write` 없이 실행하면 마크다운을 화면에 출력만 합니다. 커밋을 더 쌓은 뒤 다시 실행해도 마커 구간만 교체되어 중복되지 않습니다.

## 진행 현황

- [x] 01 - 02. 멀티모달 콘텐츠 제작
- [x] 01 - 04. AI기반 UIUX 디자인 시안 제작
- [x] 02 - 01. Python 및 Git 기초 — [prompt-manager](https://github.com/Frost0313z/prompt-manager)
- [x] 02 - 02. Python 응용 API 활용 국내 여행지 추천 프로그램 개발 — [travel-planner](https://github.com/Frost0313z/travel-planner)
- [x] 02 - 03. AI 웹 개발 — [fridge-chef](https://github.com/Frost0313z/fridge-chef) *(Vercel 배포 예정)*
- [ ] 03. AI 응용 학습 (예정)

새 차시를 추가할 때마다 이 목록을 갱신합니다.
