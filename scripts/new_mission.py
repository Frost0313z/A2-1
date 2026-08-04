#!/usr/bin/env python3
"""코디세이 미션 작업을 표준 구조로 준비하고, 반복되는 증빙/문서 작업을 자동화한다.

명령어:
  new       새 미션 세션 + 표준 파이썬 프로젝트를 스캐폴딩한다.
  env-doc   현재 개발 환경(Python/Git 버전, 커밋 로그)을 README용 마크다운으로 뽑아낸다.

사용 예:
    python scripts/new_mission.py new 02 "02. Python 심화" todo-cli \\
        --description "터미널 할 일 관리 프로그램" --github

    python scripts/new_mission.py env-doc \\
        "02. AI 활용 학습/01. Python 및 Git 기초/output/prompt-manager" --write
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STAGE_DIRS = {
    "01": "01. AI 도구 학습",
    "02": "02. AI 활용 학습",
    "03": "03. AI 응용 학습",
}

PYTHON_GITIGNORE = """__pycache__/
*.pyc
.venv/
venv/
.vscode/
*.egg-info/
"""

EVIDENCE_START = "<!-- ENV_EVIDENCE_START -->"
EVIDENCE_END = "<!-- ENV_EVIDENCE_END -->"


# ---------- new: 세션 + 표준 파이썬 프로젝트 스캐폴딩 ----------

def create_session(root, stage, session_name):
    session_dir = root / STAGE_DIRS[stage] / session_name
    for sub in ("materials", "assets"):
        (session_dir / sub).mkdir(parents=True, exist_ok=True)
        (session_dir / sub / ".gitkeep").touch()
    (session_dir / "output").mkdir(parents=True, exist_ok=True)
    return session_dir


def _git_author():
    result = subprocess.run(
        ["git", "config", "user.name"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    name = result.stdout.strip()
    return name or "Your Name"


def _mit_license(author):
    year = datetime.now().year
    return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def _readme_template(project_name, description, package_name):
    return f"""# {project_name}

{description}

## 목차

- [빠른 시작](#빠른-시작)
- [기능](#기능)
- [프로젝트 구조](#프로젝트-구조)
- [개발 환경 확인](#개발-환경-확인)
- [설계 노트](#설계-노트)
- [라이선스](#라이선스)

## 빠른 시작

```bash
python main.py
```

## 기능

(기능표를 채우세요: 번호 | 기능 | 설명)

## 프로젝트 구조

```
{project_name}/
├── main.py
└── {package_name}/
    ├── __init__.py
    ├── data.py
    └── core.py
```

## 개발 환경 확인

`python scripts/new_mission.py env-doc <이 프로젝트 경로> --write` 로 아래 구간을 채우세요.

{EVIDENCE_START}
{EVIDENCE_END}

## 설계 노트

- 데이터 구조를 이렇게 선택한 이유:
- 반복문·종료 조건을 이렇게 설계한 이유:
- 브랜치를 나눈(혹은 나누지 않은) 기준:
- 데이터 영속화 방안 제안:
- 동명 항목·값 충돌 처리 정책:

## 라이선스

[MIT](./LICENSE)
"""


def scaffold_python_project(output_dir, project_name, package_name, description):
    project_dir = output_dir / project_name
    package_dir = project_dir / package_name
    package_dir.mkdir(parents=True, exist_ok=True)

    (project_dir / ".gitignore").write_text(PYTHON_GITIGNORE, encoding="utf-8")
    (package_dir / "__init__.py").touch()
    (package_dir / "data.py").write_text(
        "# 기본 데이터를 여기에 정의한다.\n", encoding="utf-8"
    )
    (package_dir / "core.py").write_text(
        "def run():\n"
        '    print("여기에 메뉴/기능 함수를 기능별로 나눠 구현한다.")\n',
        encoding="utf-8",
    )
    (project_dir / "main.py").write_text(
        "import sys\n\n"
        f"from {package_name}.core import run\n\n"
        'if __name__ == "__main__":\n'
        '    if hasattr(sys.stdout, "reconfigure"):\n'
        '        sys.stdout.reconfigure(encoding="utf-8")\n'
        '        sys.stdin.reconfigure(encoding="utf-8")\n'
        "    run()\n",
        encoding="utf-8",
    )
    (project_dir / "LICENSE").write_text(_mit_license(_git_author()), encoding="utf-8")
    (project_dir / "README.md").write_text(
        _readme_template(project_name, description, package_name), encoding="utf-8"
    )
    return project_dir


def add_to_outer_gitignore(root, project_dir):
    gitignore = root / ".gitignore"
    rel_path = project_dir.relative_to(root).as_posix() + "/"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    if rel_path not in text:
        with gitignore.open("a", encoding="utf-8") as f:
            f.write(f"\n# {project_dir.name} 미션 (자체 GitHub 저장소로 별도 관리)\n{rel_path}\n")


def init_git(project_dir):
    subprocess.run(["git", "init", "-b", "main"], cwd=project_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
    subprocess.run(
        ["git", "commit", "-m", "chore: 프로젝트 구조 초기화"],
        cwd=project_dir,
        check=True,
    )


def create_github_repo(project_dir, repo_name, description):
    subprocess.run(
        [
            "gh", "repo", "create", repo_name,
            "--public", "--source=.", "--remote=origin",
            "--description", description,
        ],
        cwd=project_dir,
        check=True,
    )
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_dir, check=True)


def cmd_new(args):
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    package_name = args.package or args.project_name.replace("-", "_")

    session_dir = create_session(root, args.stage, args.session_name)
    project_dir = scaffold_python_project(
        session_dir / "output", args.project_name, package_name, args.description
    )
    add_to_outer_gitignore(root, project_dir)
    init_git(project_dir)

    if args.github:
        create_github_repo(project_dir, args.project_name, args.description)

    print(f"완료: {project_dir}")


# ---------- env-doc: 개발 환경 증빙을 README용 마크다운으로 생성 ----------

def _run(cmd, cwd):
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def capture_env_evidence(project_dir):
    entries = []

    py = _run(["python", "-V"], project_dir)
    entries.append(("python -V", (py.stdout + py.stderr).strip()))

    gv = _run(["git", "--version"], project_dir)
    entries.append(("git --version", gv.stdout.strip()))

    name = _run(["git", "config", "user.name"], project_dir).stdout.strip()
    email = _run(["git", "config", "user.email"], project_dir).stdout.strip()
    entries.append(("git config user.name / user.email", f"{name}\n{email}"))

    log = _run(["git", "log", "--oneline", "--graph", "--all"], project_dir)
    entries.append(("git log --oneline --graph --all", log.stdout.rstrip()))

    return entries


def render_evidence_markdown(entries):
    blocks = []
    for title, output in entries:
        blocks.append(f"`{title}`\n\n```\n{output}\n```")
    return "\n\n".join(blocks)


def write_evidence_to_readme(project_dir, markdown):
    readme = project_dir / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    block = f"{EVIDENCE_START}\n\n{markdown}\n\n{EVIDENCE_END}"

    if EVIDENCE_START in text and EVIDENCE_END in text:
        before, rest = text.split(EVIDENCE_START, 1)
        _, after = rest.split(EVIDENCE_END, 1)
        text = before + block + after
    else:
        text = text.rstrip() + "\n\n## 개발 환경 확인\n\n" + block + "\n"

    readme.write_text(text, encoding="utf-8")


def cmd_env_doc(args):
    project_dir = Path(args.project_dir).resolve()
    entries = capture_env_evidence(project_dir)
    markdown = render_evidence_markdown(entries)

    if args.write:
        write_evidence_to_readme(project_dir, markdown)
        print(f"README.md에 반영 완료: {project_dir / 'README.md'}")
    else:
        print(markdown)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="새 미션 세션 + 표준 파이썬 프로젝트 스캐폴딩")
    p_new.add_argument("stage", choices=STAGE_DIRS, help="01/02/03 중 하나")
    p_new.add_argument("session_name", help='예: "02. Python 심화"')
    p_new.add_argument("project_name", help="output/ 아래에 만들 프로젝트 폴더명 (= GitHub 저장소명)")
    p_new.add_argument("--package", default=None, help="파이썬 패키지명 (기본값: project_name의 -를 _로 변환)")
    p_new.add_argument("--description", default="", help="프로젝트 설명")
    p_new.add_argument("--github", action="store_true", help="GitHub 저장소도 생성하고 push한다")
    p_new.add_argument("--root", default=None, help="코디세이 과제 루트 경로 (기본값: 이 스크립트의 상위 폴더)")
    p_new.set_defaults(func=cmd_new)

    p_env = sub.add_parser(
        "env-doc", help="python/git 버전과 커밋 로그를 README용 마크다운으로 생성"
    )
    p_env.add_argument("project_dir", help="프로젝트 폴더 경로")
    p_env.add_argument(
        "--write", action="store_true",
        help="README.md의 '개발 환경 확인' 구간에 바로 반영 (마커가 없으면 새로 추가)"
    )
    p_env.set_defaults(func=cmd_env_doc)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
