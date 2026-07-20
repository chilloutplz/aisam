<template>
  <div class="page">
    <button class="back" @click="goHome">◂ 학교급·과목 다시 고르기</button>

    <div class="breadcrumb">{{ subjectLabel }} <span class="sep">▸</span> {{ gradeLabel }}</div>
    <h1 class="chalk-title" style="font-size: 32px; margin: 0 0 16px;">{{ gradeShort }} {{ subjectLabel }} 목차</h1>

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

      <section v-for="sem in semesters" :key="sem.label" class="semester">
        <button class="semester-header" :class="{ open: openSemester === sem.label }" @click="toggleSemester(sem.label)">
          <span class="chalk-title semester-title">{{ sem.label }}</span>
          <span class="count">{{ semDone(sem) }}/{{ semTotal(sem) }}</span>
          <span class="chevron">{{ openSemester === sem.label ? '▲' : '▼' }}</span>
        </button>

        <div v-if="openSemester === sem.label" class="domains">
          <section v-for="d in domainsFor(sem)" :key="d.domain" class="domain">
            <button
              class="domain-header"
              :style="{ borderColor: openDomain === d.domain ? d.chalk : 'rgba(241,237,228,0.15)' }"
              @click="toggleDomain(d.domain)"
            >
              <span class="chalk-heading domain-title" :style="{ color: d.chalk }">{{ d.domain }}</span>
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

const LEVEL_PREFIX = { elementary: "초", middle: "중", high: "고" };

// "2학년" -> "2", "3학년" -> "3" 식으로 숫자만 추출해서 백엔드가 쓰는 "중2" 형태로 변환
function toBackendGrade(level, grade) {
  const num = (grade || "").replace("학년", "");
  return `${LEVEL_PREFIX[level] || ""}${num}`;
}

const savedState = loadState() || {};
const currentSubject = savedState.subject || "수학";
const currentGrade = toBackendGrade(savedState.level, savedState.grade) || "중2";

const subjectLabel = currentSubject;
const gradeShort = currentGrade;
const gradeLabel = savedState.level && savedState.grade
  ? `${{ elementary: "초등학교", middle: "중학교", high: "고등학교" }[savedState.level]} ${savedState.grade}`
  : "중학교 2학년";

function openUnit(unitId) {
  saveState({ lastUnitId: unitId });
  router.push({ name: "unit", params: { id: unitId } });
}

function goHome() {
  clearState();
  router.push({ name: "home" });
}

const domains = ref([]);
const loading = ref(true);
const error = ref(null);
const openSemester = ref(null);
const openDomain = ref(null);

const doneCount = ref(0);
const totalCount = ref(0);

// 학기 목록을 하드코딩하지 않고, 실제로 받아온 domains의 semester 필드에서 뽑아낸다.
// 이렇게 하면 학년마다 어떤 영역이 몇 학기인지 달라져도(예: 중2는 함수가 2학기, 중3은 1학기)
// 항상 실제 데이터 기준으로 맞게 그룹핑된다.
const semesters = computed(() => {
  const labels = [...new Set(domains.value.map((d) => d.semester))];
  return labels.sort().map((label) => ({ label }));
});

function domainsFor(sem) {
  return domains.value.filter((d) => d.semester === sem.label);
}
function semDone(sem) {
  return domainsFor(sem).reduce((sum, d) => sum + doneInDomain(d), 0);
}
function semTotal(sem) {
  return domainsFor(sem).reduce((sum, d) => sum + d.units.length, 0);
}
function doneInDomain(d) {
  return d.units.filter((u) => u.status === "done").length;
}
function toggleSemester(label) {
  openSemester.value = openSemester.value === label ? null : label;
}
function toggleDomain(name) {
  openDomain.value = openDomain.value === name ? null : name;
}

onMounted(async () => {
  try {
    const data = await fetchCurriculum(currentSubject, currentGrade);
    domains.value = data.domains;
    totalCount.value = domains.value.reduce((sum, d) => sum + d.units.length, 0);
    doneCount.value = domains.value.reduce((sum, d) => sum + doneInDomain(d), 0);

    // 마지막으로 보던 단원이 있으면, 그 단원이 속한 영역/학기를 찾아서 펼쳐준다.
    const state = loadState();
    const lastUnitDomain = state?.lastUnitId
      ? domains.value.find((d) => d.units.some((u) => u.id === state.lastUnitId))
      : null;

    if (lastUnitDomain) {
      openDomain.value = lastUnitDomain.domain;
      openSemester.value = lastUnitDomain.semester;
    } else if (domains.value.length) {
      openDomain.value = domains.value[0].domain;
      openSemester.value = domains.value[0].semester;
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

.semester { margin-bottom: 16px; }
.semester-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-radius: 8px;
  background: rgba(241, 237, 228, 0.04);
  border: 1px solid rgba(241, 237, 228, 0.12);
}
.semester-header.open {
  background: rgba(86, 163, 217, 0.12);
  border-color: #56a3d9;
}
.semester-title { font-size: 20px; color: #f1ede4; }
.semester-header.open .semester-title { color: #8fc4e8; }
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
