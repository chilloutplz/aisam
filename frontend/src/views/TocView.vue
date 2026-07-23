<template>
  <div class="page-wide">
    <div class="header-row">
      <button class="back" @click="goHome">◂ 과목 다시 고르기</button>
    </div>

    <div class="breadcrumb">{{ subjectLabel }} <span class="sep">▸</span> 전체 학년</div>
    <h1 class="chalk-title" style="font-size: 28px; margin: 0 0 12px;">{{ subjectLabel }} 목차</h1>

    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <p class="hint">◂ ▸ 옆으로 넘기면 다른 학년이 보여요</p>

      <div class="board" ref="boardRef">
        <section v-for="g in grades" :key="g" class="column" :ref="(el) => setColumnRef(el, g)">
          <div class="column-header">
            <span class="chalk-title column-title">{{ g }}</span>
          </div>

          <div class="column-body">
            <div v-for="d in domainsForGrade(g)" :key="d.domain" class="domain-group">
              <div class="domain-label" :style="{ color: d.chalk }">
                {{ d.domain }}
                <span class="semester-badge">{{ d.semester }}</span>
              </div>

              <button
                v-for="u in d.units"
                :key="u.id"
                class="unit-card"
                :class="{ done: u.status === 'done', current: u.id === lastUnitId }"
                :style="u.status === 'done' ? { borderColor: d.chalk + '77' } : {}"
                :disabled="u.status !== 'done'"
                @click="u.status === 'done' && openUnit(u.id)"
              >
                <span class="dot" :style="{ color: u.status === 'done' ? d.chalk : 'rgba(241,237,228,0.25)' }">
                  {{ u.status === 'done' ? '●' : '○' }}
                </span>
                <span class="unit-title">{{ u.title }}</span>
                <span v-if="u.status !== 'done'" class="badge">준비중</span>
              </button>
            </div>
          </div>
        </section>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { fetchCurriculum } from "../api.js";
import { saveState, clearState, loadState } from "../storage.js";

const router = useRouter();

const GRADE_ORDER = ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"];

const savedState = loadState() || {};
const currentSubject = savedState.subject || "수학";
const subjectLabel = currentSubject;
const lastUnitId = savedState.lastUnitId || null;

const domains = ref([]);
const loading = ref(true);
const error = ref(null);
const boardRef = ref(null);
const columnRefs = {};

function setColumnRef(el, grade) {
  if (el) columnRefs[grade] = el;
}

const grades = computed(() => {
  const present = [...new Set(domains.value.map((d) => d.grade))];
  return present.sort((a, b) => GRADE_ORDER.indexOf(a) - GRADE_ORDER.indexOf(b));
});

function domainsForGrade(g) {
  return domains.value.filter((d) => d.grade === g);
}

function openUnit(unitId) {
  saveState({ lastUnitId: unitId });
  router.push({ name: "unit", params: { id: unitId } });
}

function goHome() {
  clearState();
  router.push({ name: "home" });
}

onMounted(async () => {
  try {
    const data = await fetchCurriculum(currentSubject);
    domains.value = data.domains;
    loading.value = false;

    // loading이 false가 되어 칸(column)들이 실제로 화면에 그려진 뒤에야
    // columnRefs가 채워지므로, 반드시 그 다음에 스크롤 위치를 계산해야 한다.
    await nextTick();
    const lastUnitDomain = lastUnitId
      ? domains.value.find((d) => d.units.some((u) => u.id === lastUnitId))
      : null;
    const targetGrade = lastUnitDomain ? lastUnitDomain.grade : grades.value[0];
    const targetEl = columnRefs[targetGrade];
    if (targetEl && boardRef.value) {
      boardRef.value.scrollLeft = targetEl.offsetLeft - 12;
    }
  } catch (e) {
    error.value = e.message;
    loading.value = false;
  }
});
</script>

<style scoped>
.page-wide {
  width: 100%;
  padding: 32px 0 24px 16px;
}
.header-row { padding-right: 16px; }
.back {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 16px;
  font-size: 13px;
  color: rgba(241, 237, 228, 0.5);
}
.breadcrumb { font-size: 12px; color: rgba(241, 237, 228, 0.45); margin-bottom: 8px; padding-right: 16px; }
.sep { color: rgba(241, 237, 228, 0.25); }
.loading, .error { font-size: 14px; color: rgba(241,237,228,0.5); padding-right: 16px; }

.hint { font-size: 11px; color: rgba(241,237,228,0.35); margin: 0 0 12px; }

.board {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 12px;
  scroll-snap-type: x proximity;
  -webkit-overflow-scrolling: touch;
}
.column {
  flex: 0 0 auto;
  width: 240px;
  scroll-snap-align: start;
  background: rgba(241, 237, 228, 0.03);
  border: 1px solid rgba(241, 237, 228, 0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 260px);
}
.column-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(241, 237, 228, 0.1);
  position: sticky;
  top: 0;
  background: #16211c;
  border-radius: 12px 12px 0 0;
}
.column-title { font-size: 18px; color: #f1ede4; }

.column-body {
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.domain-group { margin-bottom: 10px; }
.domain-label {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 2px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.semester-badge {
  font-size: 9px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(241, 237, 228, 0.08);
  color: rgba(241, 237, 228, 0.4);
}

.unit-card {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 10px;
  margin-bottom: 6px;
  border-radius: 8px;
  text-align: left;
  border: 1px solid rgba(241, 237, 228, 0.08);
  background: rgba(241, 237, 228, 0.02);
}
.unit-card.done { background: rgba(241, 237, 228, 0.05); }
.unit-card.current { box-shadow: 0 0 0 2px #56a3d9 inset; }
.unit-title {
  flex: 1;
  font-size: 13px;
  line-height: 1.35;
  color: rgba(241, 237, 228, 0.4);
}
.unit-card.done .unit-title { color: #f1ede4; }
.badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(241, 237, 228, 0.06);
  color: rgba(241, 237, 228, 0.3);
}
</style>
