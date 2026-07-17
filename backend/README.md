# AI Sam - Django 백엔드

## 실행 방법

```bash
python3 -m venv venv
source venv/bin/activate        # Windows는: venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py load_curriculum   # 13개 단원 데이터 적재

cp .env.example .env
# .env 파일을 열어서 OPENROUTER_API_KEY= 뒤에 발급받은 키를 붙여넣기

python manage.py runserver
```

다음에 다시 실행할 때는 가상환경 생성(`python3 -m venv venv`)과 `.env` 설정은
건너뛰고, `source venv/bin/activate`부터 시작하면 됩니다.

OpenRouter API 키는 https://openrouter.ai (Sign In → Keys → Create Key)에서
신용카드 없이 무료로 발급받을 수 있습니다.

기본 모델은 `qwen/qwen3-next-80b-a3b-instruct:free` (무료)입니다. 다른 모델로
바꾸고 싶으면:
```bash
export OPENROUTER_MODEL="다른모델슬러그:free"
```
무료 모델 목록은 https://openrouter.ai/models?max_price=0 에서 확인할 수
있습니다. (무료 모델 라인업은 수시로 바뀌니 실행 전에 한 번씩 확인하는 게
좋습니다.)

## API 엔드포인트

- `GET /api/curriculum/` — 학기·영역별 단원 목록(제목, 완료여부)
- `GET /api/units/<id>/` — 단원 하나의 전체 콘텐츠(서사, 이름유래, 핵심스킬, 문제)
- `POST /api/chat/<id>/` — 학생 질문을 서버가 대신 AI에게 물어봐서 답을 돌려줌
  - body: `{"messages": [{"role": "user", "content": "질문"}]}`
  - 응답: `{"reply": "..."}`

## 왜 이 구조인가

- 채팅 요청을 **서버(Django)가 대신** AI API에 보내기 때문에, 학생(아들) 쪽에서는
  어떤 계정으로도 로그인할 필요가 없습니다. Claude나 Gemini 소비자 계정은 보통
  18세 이상만 만들 수 있다는 제약이 있는데, 이 구조로는 그 제약 자체가 적용되지
  않습니다.
- AI 호출은 OpenRouter를 통해 Qwen 무료 모델을 사용합니다. OpenRouter는 OpenAI
  호환 형식이라, 나중에 다른 모델로 바꾸고 싶으면 `OPENROUTER_MODEL` 환경변수만
  바꾸면 됩니다.
- 콘텐츠(단원 설명, 문제)는 `learning/curriculum.json`에서 가져왔고, 이건 원래
  React 프로토타입에 있던 13개 단원 데이터를 그대로 추출한 것입니다.

## 다음 할 일 (프론트엔드)

이 저장소에는 백엔드(API)만 있습니다. Vue3로 프론트엔드를 만들 때, React
프로토타입에서 썼던 칠판(다크 그린 배경 + 분필색) 디자인을 그대로 옮기면 됩니다.
화면 흐름은 홈(학교급/학년/과목 선택) → 목차(학기→영역→단원 아코디언) → 단원
상세(+채팅)로 동일합니다.