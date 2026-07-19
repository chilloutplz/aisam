"""철학(philosophy) + 과목(subjects) + 단원별 내용을 조립해서
최종 시스템 프롬프트를 만든다. views.py는 이 build_system_prompt()만 가져다 쓴다."""

from .philosophy import PHILOSOPHY_PROMPT
from .subjects import SUBJECT_PROMPTS


def build_system_prompt(subject, unit_title, unit_content):
    core_skills = unit_content.get("coreSkills", [])
    skills_text = " / ".join(f"{s['name']} - {s['explain']}" for s in core_skills)

    subject_prompt = SUBJECT_PROMPTS.get(subject, "")

    unit_block = f"""지금 학생이 공부 중인 단원은 다음과 같아.

단원명: {unit_title}
용어: {unit_content.get('term', '')} — {unit_content.get('termMeaning', '')}
이름의 유래: {unit_content.get('nameOrigin', '')}
왜 이 단원이 필요했는지: {' '.join(unit_content.get('bigPicture', []))}
핵심 스킬: {skills_text}"""

    parts = [PHILOSOPHY_PROMPT]
    if subject_prompt:
        parts.append(subject_prompt)
    parts.append(unit_block)

    return "\n\n".join(parts)
