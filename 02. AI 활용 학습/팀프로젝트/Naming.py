"""브랜드 네이밍과 슬로건 생성 기능."""

from main import ask_llm, parse_json_response


def generate_naming(brief: dict) -> list:
    """브랜드명 후보 3~5개와 의미를 생성한다."""
    prompt = f"""
다음 브랜드 브리프를 참고해 브랜드명 후보 3~5개를 제안해줘.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief.get('tone', '자유롭게')}

아래 JSON 배열 형식으로만 답해. 다른 설명이나 코드 블록은 추가하지 마.
[{{"name": "브랜드명", "meaning": "의미 또는 유래"}}]
"""
    return parse_json_response(ask_llm(prompt))


def generate_slogan(brief: dict) -> list:
    """브랜드 슬로건 3개를 생성한다."""
    prompt = f"""
다음 브랜드 브리프를 참고해 슬로건 3개를 제안해줘.

업종: {brief['industry']}
타겟: {brief['target']}
키워드: {', '.join(brief['keywords'])}
톤앤매너: {brief.get('tone', '자유롭게')}

아래 JSON 배열 형식으로만 답해. 다른 설명이나 코드 블록은 추가하지 마.
["슬로건 1", "슬로건 2", "슬로건 3"]
"""
    return parse_json_response(ask_llm(prompt))
