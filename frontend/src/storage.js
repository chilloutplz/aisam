const KEY = "aisam_last_state";

export function saveState(partial) {
  const current = loadState() || {};
  localStorage.setItem(KEY, JSON.stringify({ ...current, ...partial }));
}

export function loadState() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function clearState() {
  localStorage.removeItem(KEY);
}
