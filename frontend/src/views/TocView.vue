<template>
  <div class="page">
    <button class="back" @click="goHome">◂ 과목 다시 고르기</button>

    <div class="breadcrumb">{{ subjectLabel }} <span class="sep">▸</span> 전체 학년</div>
    <h1 class="chalk-title" style="font-size: 32px; margin: 0 0 16px;">{{ subjectLabel }} 목차</h1>

    <div v-if="loading" class="loading">불러오는 중...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <template v-else>
      <div class="progress-card">
        <div class="progress-row">
          <span class="progress-label">완성된 단원</span>
          <span class="progress-value chalk-heading">{{ doneCount }} / {{ totalCount }}</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: (doneCount / totalCount) * 100 + '%' }"></div>
        </div>
      </div>

      <section v-for="g in grades" :key="g" class="grade-block">
        <button class="grade-header" :class="{ open: openGrade === g }" @click="toggleGrade(g)">
          <span class="chalk-title grade-title">{{ g }}</span>
          <span class="count">{{ gradeDone(g) }}/{{ gradeTotal(g) }}</span>
          <span class="chevron">{{ openGrade === g ? '▲' : '▼' }}</span>
        </button>

        <div v-if="openGrade === g" class="domains">
          <section v-for="d in domainsForGrade(g)" :key="d.domain" class="domain">
            <button
              class="domain-header"
              :style="{ borderColor: openDomain === d.domain ? d.chalk : 'rgba(241,237,228,0.15)' }"
              @click="toggleDomain(d.domain)"
            >
              <span class="chalk-heading domain-title" :style="{ color: d.chalk }">{{ d.domain }}</span>
              <span class="semester-badge">{{ d.semester }}</span>
              <span class="count">{{ doneInDomain(d) }}/{{ d.units.length }}</span>
              <span class="chevron">{{ openDomain === d.domain ? '▲' : '▼' }}</span>
            </button>

            <div v-if="openDomain === d.domain" class="units">
              <button
                v-for="u in d.units"
                :key="u.id"
                class="unit-row"
                :class="{ done: u.status === 'done' }"
                :style="u.status === 'done' ? { borderColor: d.chalk + '55' } : {}"
                :disabled="u.status !== 'done'"
                @click="u.status === 'done' && openUnit(u.id)"
              >
                <span class="dot" :style="{ color: u.status === 'done' ? d.chalk : 'rgba(241,237,228,0.25)' }">
                  {{ u.status === 'done' ? '●' : '○' }}
                </span>
                <span class="unit-title">{{ u.title }}</span>
                <span v-if="u.status !== 'done'" class="badge">준비중</span>
                <span v-else class="arrow">›</span>
              </button>
            </div>
          </section>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { fetchCurriculum } from "../api.js";
import { saveState, clearState, loadState } from "../storage.js";

const router = useRouter();

const GRADE_ORDER = ["초1", "초2", "초3", "초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"];

const savedState = loadState() || {};
const currentSubject = savedState.subject || "수학";
const subjectLabel = currentSubject;

const domains = ref([]);
const loading = ref(true);
const error = ref(null);
const openGrade = ref(null);
const openDomain = ref(null);

const doneCount = ref(0);
const totalCount = ref(0);

// 실제 데이터에 존재하는 학년만, 교육과정 순서(GRADE_ORDER) 기준으로 뽑아낸다.
const grades = computed(() => {
  const present = [...new Set(domains.value.map((d) => d.grade))];
  return present.sort((a, b) => GRADE_ORDER.indexOf(a) - GRADE_ORDER.indexOf(b));
});

function domainsForGrade(g) {
  return domains.value.filter((d) => d.grade === g);
}
function gradeDone(g) {
  return domainsForGrade(g).reduce((sum, d) => sum + doneInDomain(d), 0);
}
function gradeTotal(g) {
  return domainsForGrade(g).reduce((sum, d) => sum + d.units.length, 0);
}
function doneInDomain(d) {
  return d.units.filter((u) => u.status === "done").length;
}
function toggleGrade(g) {
  openGrade.value = openGrade.value === g ? null : g;
}
function toggleDomain(name) {
  openDomain.value = openDomain.value === name ? null : name;
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
    // grade를 안 넘기면 이 과목의 전체 학년을 다 받아온다 (학년을 넘나드는 하나의 지도)
    const data = await fetchCurriculum(currentSubject);
    domains.value = data.domains;
    totalCount.value = domains.value.reduce((sum, d) => sum + d.units.length, 0);
    doneCount.value = domains.value.reduce((sum, d) => sum + doneInDomain(d), 0);

    const state = loadState();
    const lastUnitDomain = state?.lastUnitId
      ? domains.value.find((d) => d.units.some((u) => u.id === state.lastUnitId))
      : null;

    if (lastUnitDomain) {
      openGrade.value = lastUnitDomain.grade;
      openDomain.value = lastUnitDomain.domain;
    } else if (grades.value.length) {
      openGrade.value = grades.value[0];
      const firstDomain = domainsForGrade(openGrade.value)[0];
      if (firstDomain) openDomain.value = firstDomain.domain;
    }
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.back {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 16px;
  font-size: 13px;
  color: rgba(241, 237, 228, 0.5);
}
.breadcrumb {
  font-size: 12px;
  color: rgba(241, 237, 228, 0.45);
  margin-bottom: 8px;
}
.sep { color: rgba(241, 237, 228, 0.25); }
.loading, .error { font-size: 14px; color: rgba(241,237,228,0.5); }

.progress-card {
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 32px;
  background: rgba(86, 163, 217, 0.1);
  border: 1px solid rgba(86, 163, 217, 0.25);
}
.progress-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 8px;
}
.progress-label { font-size: 13px; color: rgba(241,237,228,0.6); }
.progress-value { font-size: 18px; color: #8fc4e8; }
.progress-bar {
  height: 6px;
  width: 100%;
  border-radius: 3px;
  overflow: hidden;
  background: rgba(241, 237, 228, 0.1);
}
.progress-fill {
  height: 100%;
  border-radius: 3px;
  background: #56a3d9;
}

.grade-block { margin-bottom: 16px; }
.grade-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(241, 237, 228, 0.04);
  border: 1px solid rgba(241, 237, 228, 0.12);
}
.grade-header.open {
  background: rgba(86, 163, 217, 0.12);
  border-color: #56a3d9;
}
.grade-title { font-size: 20px; color: #f1ede4; }
.grade-header.open .grade-title { color: #8fc4e8; }
.count { font-size: 11px; color: rgba(241,237,228,0.4); margin-left: 4px; }
.chevron { margin-left: auto; color: rgba(241,237,228,0.6); }

.domains { padding: 12px 0 0 4px; }
.domain { margin-bottom: 12px; }
.domain-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 2px solid;
}
.domain-title { font-size: 18px; }
.semester-badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(241, 237, 228, 0.08);
  color: rgba(241, 237, 228, 0.45);
}

.units {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 12px;
}
.unit-row {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  text-align: left;
  border: 1px solid rgba(241, 237, 228, 0.08);
  background: transparent;
}
.unit-row.done {
  background: rgba(241, 237, 228, 0.05);
}
.unit-title {
  flex: 1;
  font-size: 15px;
  line-height: 1.4;
  color: rgba(241, 237, 228, 0.45);
}
.unit-row.done .unit-title {
  color: #f1ede4;
}
.badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(241, 237, 228, 0.06);
  color: rgba(241, 237, 228, 0.35);
}
.arrow {
  color: rgba(241, 237, 228, 0.4);
  font-size: 16px;
}
</style>
