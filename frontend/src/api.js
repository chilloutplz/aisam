const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

export async function fetchCurriculum(subject = "수학", grade = "중2") {
  const res = await fetch(`${API_BASE}/curriculum/?subject=${encodeURIComponent(subject)}&grade=${encodeURIComponent(grade)}`);
  if (!res.ok) throw new Error("목차를 불러오지 못했어요");
  return res.json();
}

export async function fetchUnit(unitId) {
  const res = await fetch(`${API_BASE}/units/${unitId}/`);
  if (!res.ok) throw new Error("단원 내용을 불러오지 못했어요");
  return res.json();
}

export async function sendChatMessage(unitId, messages) {
  const res = await fetch(`${API_BASE}/chat/${unitId}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
  const data = await res.json();
  // 상태코드가 아니라 응답 body의 error 필드로 판단 (일부 배포 플랫폼 게이트웨이가
  // 4xx/5xx 응답을 자체 에러 페이지로 가로채는 것을 피하기 위해 항상 200으로 옴)
  if (data.error) throw new Error(data.error);
  return data.reply;
}
