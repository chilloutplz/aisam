<template>
  <div class="page">
    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else-if="unit">
      <button class="back" @click="$router.push({ name: 'toc' })">◂ 목차로</button>

      <div class="trail">
        <div class="trail-row">
          <button
            v-if="unit.prevUnit"
            class="trail-side trail-link"
            @click="goToUnit(unit.prevUnit.id)"
          >◂ {{ unit.prevUnit.title }}</button>
          <span v-else class="trail-side trail-empty">처음 단원이야</span>

          <button
            v-if="unit.nextUnit"
            class="trail-side right trail-link"
            @click="goToUnit(unit.nextUnit.id)"
          >{{ unit.nextUnit.title }} ▸</button>
          <span v-else class="trail-side right trail-empty">마지막 단원이야</span>
        </div>
        <div class="trail-line"></div>
        <div class="trail-center">
          <span class="trail-badge">지금 배우는 단원</span>
          <h1 class="chalk-title unit-title">{{ unit.title }}</h1>
        </div>
      </div>

      <section class="section">
        <h2 class="chalk-heading section-heading" style="color:#f2c94c;">{{ unit.term }}란?</h2>
        <p class="paragraph"><MathText :text="unit.termMeaning" /></p>
        <h2 class="chalk-heading section-heading" style="color:#f2c94c; margin-top: 20px;">왜 {{ unit.term }}가 필요했을까</h2>
        <p v-for="(p, i) in unit.bigPicture" :key="i" class="paragraph"><MathText :text="p" /></p>
      </section>

      <section class="name-origin">
        <h2 class="chalk-heading section-heading" style="color:#c58fe8;">이름은 왜 '{{ unit.term }}'일까</h2>
        <p class="paragraph small"><MathText :text="unit.nameOrigin" /></p>
      </section>

      <section class="skills">
        <h2 class="chalk-heading section-heading" style="color:#6fcf97;">핵심 스킬</h2>
        <div class="skill-card" v-for="(skill, i) in unit.coreSkills" :key="i">
          <h3 class="skill-name">{{ skill.name }}</h3>
          <p class="skill-explain"><MathText :text="skill.explain" /></p>
          <Diagram v-if="skill.visual" :type="skill.visual" chalk="#f2c94c" />
        </div>
      </section>

      <section class="problem-tabs">
        <div v-for="s in SECTIONS" :key="s.key" class="tab-block">
          <button
            class="tab-header"
            :style="{ borderColor: openSection === s.key ? s.chalk : 'rgba(241,237,228,0.15)' }"
            @click="toggleSection(s.key)"
          >
            <span class="tab-icon">{{ s.icon }}</span>
            <span class="chalk-heading tab-label">{{ s.label }}</span>
            <span class="tab-count">{{ unit.problems[s.key].length }}문제</span>
            <span class="chevron">{{ openSection === s.key ? '▲' : '▼' }}</span>
          </button>
          <div v-if="openSection === s.key" class="tab-body">
            <p v-if="s.optional" class="optional-note">필수 아님 — 여기까지 편하게 풀렸으면, 더 해보고 싶을 때만.</p>
            <QuizSection :bank="unit.problems[s.key]" :chalk="s.chalk" />
          </div>
        </div>
      </section>

      <section class="chat">
        <div class="chat-title-row">
          <span>✦</span>
          <h2 class="chalk-heading chat-title">궁금한 거 물어보기</h2>
        </div>
        <div ref="scrollBox" class="chat-box">
          <div v-for="(m, i) in messages" :key="i" class="msg-row" :class="m.role">
            <div class="msg-bubble" :class="m.role">{{ m.content }}</div>
          </div>
          <div v-if="chatLoading" class="msg-row assistant">
            <div class="msg-bubble assistant loading-bubble">생각 중...</div>
          </div>
        </div>
        <div class="chat-input-row">
          <input
            v-model="input"
            placeholder="이 단원에 대해 물어보기"
            class="chat-input"
            @keydown.enter="sendMessage"
          />
          <button class="send-btn" :disabled="chatLoading" @click="sendMessage">➤</button>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from "vue";
import { useRouter } from "vue-router";
import { fetchUnit, sendChatMessage } from "../api.js";
import Diagram from "../components/Diagram.vue";
import QuizSection from "../components/QuizSection.vue";
import MathText from "../components/MathText.vue";
import { saveState } from "../storage.js";

const router = useRouter();

const props = defineProps({ id: { type: [String, Number], required: true } });

function goToUnit(unitId) {
  saveState({ lastUnitId: unitId });
  router.push({ name: "unit", params: { id: unitId } });
}

const SECTIONS = [
  { key: "concept", label: "개념 이해", icon: "📖", chalk: "#f2c94c" },
  { key: "skill", label: "기술 적용", icon: "🔧", chalk: "#6fcf97" },
  { key: "application", label: "응용", icon: "🧩", chalk: "#eb8a6d" },
  { key: "challenge", label: "도전", icon: "🔥", chalk: "#e06c75", optional: true },
];

const unit = ref(null);
const loading = ref(true);
const error = ref(null);
const openSection = ref("concept");

const messages = ref([
  { role: "assistant", content: "안녕! 나는 이 단원 안에서 같이 이야기 나눌 도우미야. 뭐든 편하게 물어봐." },
]);
const input = ref("");
const chatLoading = ref(false);
const scrollBox = ref(null);

function toggleSection(key) {
  openSection.value = openSection.value === key ? null : key;
}

async function loadUnit() {
  loading.value = true;
  error.value = null;
  try {
    unit.value = await fetchUnit(props.id);
    // 목차나 이전/다음 버튼을 거치지 않고 URL로 직접 들어온 경우에도
    // "마지막으로 보던 단원"이 정확히 기록되도록 여기서도 저장한다.
    saveState({ lastUnitId: Number(props.id) });
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(loadUnit);
watch(() => props.id, loadUnit);

async function scrollToBottom() {
  await nextTick();
  if (scrollBox.value) scrollBox.value.scrollTop = scrollBox.value.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text || chatLoading.value) return;
  messages.value.push({ role: "user", content: text });
  input.value = "";
  chatLoading.value = true;
  scrollToBottom();
  try {
    const reply = await sendChatMessage(props.id, messages.value.map((m) => ({ role: m.role, content: m.content })));
    messages.value.push({ role: "assistant", content: reply });
  } catch (e) {
    messages.value.push({ role: "assistant", content: `연결에 문제가 생겼어: ${e.message}` });
  } finally {
    chatLoading.value = false;
    scrollToBottom();
  }
}
</script>

<style scoped>
.loading, .error { font-size: 14px; color: rgba(241, 237, 228, 0.5); }
.back {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 24px;
  font-size: 13px;
  color: rgba(241, 237, 228, 0.5);
}

.trail { margin-bottom: 32px; }
.trail-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: rgba(241, 237, 228, 0.45);
}
.trail-side { max-width: 40%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.trail-side.right { text-align: right; }
.trail-link {
  color: #8fc4e8;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
  background: none;
  padding: 0;
}
.trail-empty { color: rgba(241, 237, 228, 0.3); }
.trail-line {
  margin-top: 8px;
  height: 0;
  border-top: 1px dashed rgba(241, 237, 228, 0.25);
}
.trail-center { margin-top: 12px; text-align: center; }
.trail-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.02em;
  padding: 2px 8px;
  border-radius: 999px;
  margin-bottom: 8px;
  background: rgba(86, 163, 217, 0.15);
  color: #8fc4e8;
}
.unit-title { font-size: 30px; margin: 0; color: #f1ede4; }

.section { margin-bottom: 24px; }
.section-heading { font-size: 18px; margin: 0 0 8px; }
.paragraph { font-size: 15px; line-height: 1.7; margin: 0 0 10px; color: #f1ede4; }
.paragraph.small { font-size: 14px; color: rgba(241, 237, 228, 0.85); }

.name-origin {
  margin-bottom: 32px;
  border-radius: 12px;
  padding: 16px;
  background: rgba(197, 143, 232, 0.08);
  border: 1px solid rgba(197, 143, 232, 0.25);
}

.skills { margin-bottom: 32px; }
.skill-card {
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(111, 207, 151, 0.08);
  border: 1px solid rgba(111, 207, 151, 0.22);
}
.skill-name { font-size: 14px; font-weight: 500; margin: 0 0 4px; color: #6fcf97; }
.skill-explain { font-size: 14px; line-height: 1.6; margin: 0; color: rgba(241, 237, 228, 0.85); }

.problem-tabs { margin-bottom: 32px; }
.tab-block { margin-bottom: 12px; }
.tab-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 4px;
  border-bottom: 2px solid;
}
.tab-icon { font-size: 14px; }
.tab-label { font-size: 16px; color: #f1ede4; }
.tab-count { font-size: 12px; color: rgba(241, 237, 228, 0.4); margin-left: auto; }
.chevron { color: rgba(241, 237, 228, 0.5); }
.tab-body { padding-top: 12px; }
.optional-note { font-size: 12px; margin-bottom: 8px; color: rgba(224, 108, 117, 0.75); }

.chat-title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.chat-title { font-size: 18px; color: #f1ede4; }
.chat-box {
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 8px;
  overflow-y: auto;
  max-height: 320px;
  min-height: 120px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(241, 237, 228, 0.12);
}
.msg-row { display: flex; margin-bottom: 8px; }
.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }
.msg-bubble {
  max-width: 85%;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  color: #f1ede4;
}
.msg-bubble.user { background: rgba(143, 196, 232, 0.18); }
.msg-bubble.assistant { background: rgba(241, 237, 228, 0.06); }
.loading-bubble { color: rgba(241, 237, 228, 0.5); }
.chat-input-row { display: flex; gap: 8px; }
.chat-input {
  flex: 1;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 14px;
  background: rgba(241, 237, 228, 0.06);
  border: 1px solid rgba(241, 237, 228, 0.2);
  color: #f1ede4;
  outline: none;
}
.send-btn {
  border-radius: 8px;
  padding: 0 14px;
  background: #56a3d9;
  color: #16211c;
  font-size: 16px;
}
.send-btn:disabled { opacity: 0.4; }
</style>
