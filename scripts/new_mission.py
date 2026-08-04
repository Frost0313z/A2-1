#!/usr/bin/env python3
"""새 코디세이 미션 세션을 표준 구조로 스캐폴딩한다.

사용 예:
    python scripts/new_mission.py 02 "02. Python 심화" todo-cli \\
        --description "터미널 할 일 관리 프로그램" --github

만들어지는 것:
  <stage>/<session_name>/{materials,output,assets}
  <stage>/<session_name>/output/<project_name>/  (main.py + <package>/ 표준 파이썬 구조)
  프로젝트 폴더는 git init 후 첫 커밋까지 완료된 상태로 반환된다.
  --github를 주면 GitHub 저장소를 생성하고 첫 push까지 수행한다.
"""

import argparse
import subprocess
from pathlib import Path

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


def create_session(root, stage, session_name):
    session_dir = root / STAGE_DIRS[stage] / session_name
    for sub in ("materials", "assets"):
        (session_dir / sub).mkdir(parents=True, exist_ok=True)
        (session_dir / sub / ".gitkeep").touch()
    (session_dir / "output").mkdir(parents=True, exist_ok=True)
    return session_dir


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
    (project_dir / "README.md").write_text(
        f"# {project_name}\n\n{description}\n\n"
        "## 실행 방법\n\n```bash\npython main.py\n```\n",
        encoding="utf-8",
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


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=STAGE_DIRS, help="01/02/03 중 하나")
    parser.add_argument("session_name", help='예: "02. Python 심화"')
    parser.add_argument("project_name", help="output/ 아래에 만들 프로젝트 폴더명 (= GitHub 저장소명)")
    parser.add_argument("--package", default=None, help="파이썬 패키지명 (기본값: project_name의 -를 _로 변환)")
    parser.add_argument("--description", default="", help="프로젝트 설명")
    parser.add_argument("--github", action="store_true", help="GitHub 저장소도 생성하고 push한다")
    parser.add_argument("--root", default=None, help="코디세이 과제 루트 경로 (기본값: 이 스크립트의 상위 폴더)")
    args = parser.parse_args()

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


if __name__ == "__main__":
    main()
