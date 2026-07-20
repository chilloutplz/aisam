<template>
  <div class="page">
    <h1 class="chalk-title" style="font-size: 32px; margin: 0 0 4px;">AI Sam</h1>
    <p style="font-size: 13px; color: rgba(241,237,228,0.45); margin: 0 0 32px;">
      학교급과 과목을 골라서 시작해봐
    </p>

    <div class="block">
      <h2 class="label">학교급</h2>
      <div class="choices">
        <button
          v-for="l in LEVELS"
          :key="l.key"
          class="choice"
          :class="{ active: level === l.key }"
          @click="selectLevel(l.key)"
        >{{ l.label }}</button>
      </div>
    </div>

    <div class="block" v-if="levelData">
      <h2 class="label">학년</h2>
      <div class="choices">
        <button
          v-for="g in levelData.grades"
          :key="g"
          class="choice"
          :class="{ active: grade === g }"
          @click="selectGrade(g)"
        >{{ g }}</button>
      </div>
    </div>

    <div class="block" v-if="grade">
      <h2 class="label">과목</h2>
      <div class="choices">
        <button
          v-for="s in SUBJECTS"
          :key="s"
          class="choice"
          :class="{ active: subject === s }"
          @click="selectSubject(s)"
        >{{ s }}</button>
      </div>
    </div>

    <p v-if="notReadyYet" class="notice">
      {{ levelData.label }} {{ grade }} {{ subject }}은(는) 아직 준비 중이에요. 지금은 중학교 2학년 수학만 만들어져 있어요.
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import { saveState } from "../storage.js";

const router = useRouter();

const LEVELS = [
  { key: "elementary", label: "초등학교", grades: ["1학년", "2학년", "3학년", "4학년", "5학년", "6학년"] },
  { key: "middle", label: "중학교", grades: ["1학년", "2학년", "3학년"] },
  { key: "high", label: "고등학교", grades: ["1학년", "2학년", "3학년"] },
];
const SUBJECTS = ["수학", "영어", "국어", "과학", "사회"];

function isReady(level, grade, subject) {
  if (subject !== "수학") return false;
  if (level === "middle") return ["2학년", "3학년"].includes(grade);
  if (level === "high") return ["1학년", "2학년", "3학년"].includes(grade);
  return false;
}

const level = ref(null);
const grade = ref(null);
const subject = ref(null);

const levelData = computed(() => LEVELS.find((l) => l.key === level.value));
const ready = computed(() => level.value && grade.value && subject.value && isReady(level.value, grade.value, subject.value));
const notReadyYet = computed(() => level.value && grade.value && subject.value && !ready.value);

function selectLevel(key) {
  level.value = key;
  grade.value = null;
  subject.value = null;
}
function selectGrade(g) {
  grade.value = g;
  subject.value = null;
}
function selectSubject(s) {
  subject.value = s;
}

watch(ready, (val) => {
  if (val) {
    saveState({ level: level.value, grade: grade.value, subject: subject.value, lastUnitId: null });
    router.push({ name: "toc" });
  }
});
</script>

<style scoped>
.block {
  margin-bottom: 24px;
}
.label {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.02em;
  color: rgba(241, 237, 228, 0.5);
  margin: 0 0 8px;
}
.choices {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.choice {
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 14px;
  background: rgba(241, 237, 228, 0.06);
  border: 1px solid rgba(241, 237, 228, 0.18);
  color: rgba(241, 237, 228, 0.75);
  transition: all 0.15s;
}
.choice.active {
  background: rgba(86, 163, 217, 0.2);
  border-color: #56a3d9;
  color: #8fc4e8;
}
.notice {
  margin-top: 16px;
  font-size: 13px;
  line-height: 1.6;
  padding: 12px;
  border-radius: 8px;
  background: rgba(241, 237, 228, 0.05);
  color: rgba(241, 237, 228, 0.5);
}
</style>
