"""브랜드 브리프를 바탕으로 브랜드 스토리를 생성한다."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parent
BRIEF_PATH = BASE_DIR / "brief.json"
OUTPUT_DIR = BASE_DIR / "output"


def create_client() -> OpenAI:
    """.env에서 API 키를 읽어 OpenAI 클라이언트를 만든다."""
    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("GPT_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(".env에 GPT_API_KEY 또는 OPENAI_API_KEY를 설정하세요.")
    return OpenAI(api_key=api_key)


def generate_story(brief: dict) -> str:
    """브리프를 바탕으로 200~300자 분량의 브랜드 스토리를 생성한다."""
    brand_name = brief.get("brand_name", "이름을 정하는 중인 브랜드")
    category = brief.get("category", brief.get("industry", ""))
    target = brief.get("target_audience", brief.get("target", ""))
    core_values = brief.get("core_values", brief.get("keywords", []))
    values = ", ".join(core_values)
    tone = brief.get("tone", "다정하고 편안한 톤")
    description = brief.get("description", "")

    print("[브랜드 스토리 생성 시작]")
    print(f"브랜드명: {brand_name}")
    print(f"카테고리: {category}")
    print("-" * 40)

    prompt = f"""
당신은 푸드테크 브랜드 전문 카피라이터입니다.
아래 브랜드 정보를 바탕으로 감성적인 브랜드 스토리를 작성해주세요.

브랜드명: {brand_name}
카테고리: {category}
타겟 고객: {target}
핵심 가치: {values}
톤앤매너: {tone}
서비스 설명: {description}

조건:
- 200~300자 분량
- 브랜드의 탄생 배경과 철학을 담을 것
- 타겟 고객의 공감을 이끌어낼 것
- {tone} 톤으로 작성할 것
"""

    response = create_client().chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "당신은 브랜드 스토리 전문 작가입니다."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )
    story = (response.choices[0].message.content or "").strip()

    print("[생성된 브랜드 스토리]")
    print(story)
    print("-" * 40)
    return story


def save_story(brand_name: str, story: str) -> Path:
    """생성된 브랜드 스토리를 JSON 파일로 저장한다."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "brand_story.json"
    output = {"brand_name": brand_name, "brand_story": story}
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"저장 완료: {output_path}")
    return output_path


def main() -> None:
    """content.py를 단독으로 실행할 때 사용할 진입점."""
    brief = json.loads(BRIEF_PATH.read_text(encoding="utf-8"))
    story = generate_story(brief)
    save_story(brief.get("brand_name", "이름을 정하는 중인 브랜드"), story)


if __name__ == "__main__":
    main()
