const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api";

export async function fetchCurriculum() {
  const res = await fetch(`${API_BASE}/curriculum/`);
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
  if (!res.ok) throw new Error(data.error || "답을 가져오지 못했어요");
  return data.reply;
}
