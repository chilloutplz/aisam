from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_DIR = BASE_DIR / "prompts"


def load_prompt(path: str) -> str:
    file = PROMPT_DIR / path

    with open(file, encoding="utf-8") as f:
        return f.read().strip()


def build_system_prompt(
    unit_content, 
    unit_title,):

    core_skills = unit_content.get("coreSkills", [])

    skills_text = " / ".join(
        f"{s['name']} - {s['explain']}"
        for s in core_skills
    )

    template = load_prompt("template.txt")

    return template.format(

        philosophy=load_prompt("common/philosophy.txt"),

        conversation=load_prompt("common/conversation.txt"),

        safety=load_prompt("common/safety.txt"),

        output_style=load_prompt("common/output_style.txt"),
        
        unit_title=unit_title,

        term=unit_content.get("term", ""),

        term_meaning=unit_content.get("termMeaning", ""),

        name_origin=unit_content.get("nameOrigin", ""),

        big_picture=" ".join(
            unit_content.get("bigPicture", [])
        ),

        skills=skills_text,
        
    )