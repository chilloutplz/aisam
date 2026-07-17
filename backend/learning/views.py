import json
import os

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Domain, Unit


@require_GET
def curriculum_list(request):
    """학기 -> 영역 -> 단원(제목/완료여부)만 가볍게 내려주는 목차 API"""
    domains = Domain.objects.prefetch_related("units").all()
    data = []
    for d in domains:
        data.append({
            "domain": d.name,
            "chalk": d.chalk_color,
            "semester": d.semester,
            "units": [
                {"id": u.id, "title": u.title, "status": "done" if u.is_ready else "todo"}
                for u in d.units.all()
            ],
        })
    return JsonResponse({"domains": data})


@require_GET
def unit_detail(request, unit_id):
    """단원 하나의 전체 콘텐츠(서사/이름유래/스킬/문제)를 내려주는 API"""
    try:
        unit = Unit.objects.get(id=unit_id, is_ready=True)
    except Unit.DoesNotExist:
        return JsonResponse({"error": "unit not found or not ready"}, status=404)
    return JsonResponse({"id": unit.id, "title": unit.title, **unit.content})


def build_system_prompt(unit_content, unit_title):
    core_skills = unit_content.get("coreSkills", [])
    skills_text = " / ".join(f"{s['name']} - {s['explain']}" for s in core_skills)
    return f"""너는 중학교 2학년 수학 단원 학습 도우미야. 지금 학생이 공부 중인 단원은 다음과 같아.

단원명: {unit_title}
용어: {unit_content.get('term', '')} — {unit_content.get('termMeaning', '')}
이름의 유래: {unit_content.get('nameOrigin', '')}
왜 이 단원이 필요했는지: {' '.join(unit_content.get('bigPicture', []))}
핵심 스킬: {skills_text}

규칙:
- 학생이 이 단원과 관련해 궁금해하는 것(용어의 유래, 역사적 배경, 왜 이렇게 정의됐는지, 직관과 충돌하는 부분 등)은 적극적으로, 충분히 풀어준다. "그건 나중에 알아도 돼", "일단 문제부터 풀어보자" 같은 말로 호기심을 끊지 않는다.
- 이 단원과 아예 무관한 주제로 완전히 벗어나면, 짧게 답해주되 자연스럽게 이 단원으로 돌아온다.
- 중2 학생 눈높이로, 짧고 구체적인 예시나 이야기를 들어 설명한다.
- 대화를 서둘러 정리하려는 말투를 쓰지 않는다.
- 한국어로 답한다."""


def call_openrouter(system_prompt, messages):
    """OpenRouter 무료 API 호출 (기본 모델: Qwen). OPENROUTER_API_KEY 환경변수 필요."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None, "OPENROUTER_API_KEY 환경변수가 설정되어 있지 않습니다."

    model = os.environ.get("OPENROUTER_MODEL", "qwen/qwen3-next-80b-a3b-instruct:free")
    url = "https://openrouter.ai/api/v1/chat/completions"

    chat_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        role = "user" if m["role"] == "user" else "assistant"
        chat_messages.append({"role": role, "content": m["content"]})

    body = {"model": model, "messages": chat_messages}
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 429:
            return None, (
                "오늘 무료 사용 횟수를 다 썼어요 (OpenRouter 무료 모델은 하루 50회 제한). "
                "내일 다시 쓰거나, OpenRouter 계정에 $10을 충전하면 하루 1000회로 늘어나요."
            )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return text, None
    except Exception as e:
        return None, str(e)


@csrf_exempt
@require_POST
def chat_proxy(request, unit_id):
    """학생 채팅 메시지를 받아서, 서버가 대신 LLM을 호출해 답을 돌려주는 프록시.
    이 방식이면 학생(아들) 쪽에서는 별도 로그인/계정이 전혀 필요 없다."""
    print(f"[chat_proxy] 요청 도착: unit_id={unit_id}", flush=True)

    try:
        unit = Unit.objects.get(id=unit_id, is_ready=True)
    except Unit.DoesNotExist:
        print(f"[chat_proxy] unit {unit_id} 없음", flush=True)
        return JsonResponse({"error": "unit not found"}, status=404)

    try:
        payload = json.loads(request.body)
        messages = payload["messages"]  # [{role: "user"|"assistant", content: "..."}]
    except (KeyError, json.JSONDecodeError):
        print("[chat_proxy] 잘못된 payload", flush=True)
        return JsonResponse({"error": "invalid payload, expected {messages: [...]}"}, status=400)

    system_prompt = build_system_prompt(unit.content, unit.title)
    print("[chat_proxy] OpenRouter 호출 시작...", flush=True)
    reply, error = call_openrouter(system_prompt, messages)

    if error:
        print(f"[chat_proxy] OpenRouter 에러: {error}", flush=True)
        return JsonResponse({"error": error}, status=502)

    print("[chat_proxy] OpenRouter 응답 성공", flush=True)
    return JsonResponse({"reply": reply})
