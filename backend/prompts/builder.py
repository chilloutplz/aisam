# prompts/builder.py
import os
from pathlib import Path

# 파일의 절대 경로를 기준으로 prompts 폴더 위치 지정
PROMPTS_DIR = Path(__file__).resolve().parent

def load_prompt_file(file_path):
    """텍스트 파일을 안전하게 읽어오는 헬퍼 함수"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"[Warning] 프롬프트 파일을 찾을 수 없습니다: {file_path}")
        return ""

def build_system_prompt(unit_content, unit_title):
    """
    텍스트 파일 조각들을 읽어와 최종 시스템 프롬프트를 빌드합니다.
    views.py에서 이 함수만 불러서 사용합니다.
    """
    # 1. common 폴더 내의 가이드라인 조각들 로드
    philosophy = load_prompt_file(PROMPTS_DIR / "common" / "philosophy.txt")
    conversation = load_prompt_file(PROMPTS_DIR / "common" / "conversation.txt")
    output_style = load_prompt_file(PROMPTS_DIR / "common" / "output_style.txt")
    safety = load_prompt_file(PROMPTS_DIR / "common" / "safety.txt")
    
    # 2. 메인 베이스 템플릿 로드
    main_template = load_prompt_file(PROMPTS_DIR / "template.txt")
    
    # 3. 데이터 포맷팅 준비
    core_skills = unit_content.get("coreSkills", [])
    skills_text = " / ".join(f"{s['name']} - {s['explain']}" for s in core_skills)
    big_picture_text = ' '.join(unit_content.get('bigPicture', []))
    
    # 4. template.txt 안에 공통 파일 내용 삽입 (1차 조립)
    combined_template = (
        main_template
        .replace("{philosophy}", philosophy)
        .replace("{conversation}", conversation)
        .replace("{output_style}", output_style)
        .replace("{safety}", safety)
    )
    
    # 5. 최종 단원 컨텍스트 파라미터 치환 (2차 조립)
    return combined_template.format(
        unit_title=unit_title,
        term=unit_content.get('term', ''),
        term_meaning=unit_content.get('termMeaning', ''),
        name_origin=unit_content.get('nameOrigin', ''),
        big_picture=big_picture_text,
        skills_text=skills_text
    )