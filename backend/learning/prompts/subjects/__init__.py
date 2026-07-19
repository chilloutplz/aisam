"""과목별 프롬프트 모음.

새 과목을 추가하려면:
  1. 이 폴더에 새 파일 만들기 (예: english.py, PROMPT 상수 하나 정의)
  2. 아래에서 import하고 SUBJECT_PROMPTS에 한 줄 추가

그게 전부다. philosophy.py나 다른 과목 파일은 건드릴 필요 없다.
"""

from .math import MATH_PROMPT

SUBJECT_PROMPTS = {
    "수학": MATH_PROMPT,
    # "영어": ENGLISH_PROMPT,   # 나중에 이런 식으로 추가
}
