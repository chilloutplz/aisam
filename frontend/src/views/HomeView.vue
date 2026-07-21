<template>
  <div class="page">
    <h1 class="chalk-title" style="font-size: 32px; margin: 0 0 4px;">AI Sam</h1>
    <!-- 파랑 분필 + 분홍 분필 조합 멘트 -->
    <p class="subtitle">
      <svg class="chalk-speech-icon" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- 손으로 그린 말풍선 외곽선 -->
        <path 
          d="M12 20 C12 10, 88 10, 88 20 C88 52, 78 55, 58 55 C42 55, 25 74, 20 80 C23 67, 12 63, 12 20 Z" 
          stroke="#f2aec1" 
          stroke-width="5.5" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        />
        <!-- 삐뚤빼뚤 2차 겹침선 -->
        <path 
          d="M15 23 C15 13, 85 13, 85 23 C85 50, 75 53, 55 53 C40 53, 27 69, 23 75 C25 65, 15 61, 15 23 Z" 
          stroke="#f2aec1" 
          stroke-width="2.5" 
          stroke-linecap="round" 
          stroke-linejoin="round" 
          opacity="0.6"
          stroke-dasharray="5 3"
        />
        
        <!-- 안쪽 점 3개 -->
        <circle class="chalk-dot dot-1" cx="35" cy="38" r="4.2" fill="#f2aec1" />
        <circle class="chalk-dot dot-2" cx="50" cy="38" r="4.2" fill="#f2aec1" />
        <circle class="chalk-dot dot-3" cx="65" cy="38" r="4.2" fill="#f2aec1" />
      </svg>

      <span class="speech-text">
        <span class="blue-chalk">“가벼운 마음으로 시작하세요.</span><br />
        <span class="pink-chalk">언제든 도와드릴게요!”</span>
      </span>
    </p>

    <div class="block">
      <h2 class="label">과목</h2>
      <div class="choices">
        <button
          v-for="s in SUBJECTS"
          :key="s.name"
          class="choice"
          :class="{ active: subject === s.name, disabled: !s.ready }"
          @click="selectSubject(s)"
        >{{ s.name }}<span v-if="!s.ready" class="soon">준비중</span></button>
      </div>
    </div>

    <p v-if="notReadyYet" class="notice">
      {{ subject }}은(는) 아직 준비 중이에요. 지금은 수학만 만들어져 있어요.
    </p>

    <footer class="philosophy-card">
      <div class="card-tag">
        <!-- 손으로 겹쳐 그린 듯한 파란 분필 별 SVG -->
        <svg class="chalk-star-icon" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- 메인 러프 라인 -->
          <path 
            d="M48 5 L65 40 L97 36 L68 59 L82 92 L50 71 L18 90 L30 58 L3 37 L38 41 Z" 
            stroke="#8fc4e8" 
            stroke-width="5" 
            stroke-linecap="round" 
            stroke-linejoin="round"
          />
          <!-- 추가 스케치 라인 -->
          <path 
            d="M50 8 L63 38 L94 38 L65 57 L75 88 L48 66 L23 88 L33 55 L8 38 L36 39" 
            stroke="#8fc4e8" 
            stroke-width="2.5" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            opacity="0.6"
            stroke-dasharray="4 2"
          />
        </svg>
        PHILOSOPHY
      </div>

      <p class="philosophy-title">숲을 보고, 나만의 속도로 깊어지는 시간</p>
      <p class="philosophy-desc">
        단순한 문제 풀이를 넘어 배움의 이유와 본질을 이해하고,<br />
        AI Sam과 함께 나만의 깊이를 만들어갑니다.
      </p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { saveState } from "../storage.js";

const router = useRouter();

const SUBJECTS = [
  { name: "수학", ready: true },
  { name: "과학", ready: false },
];

const subject = ref(null);
const notReadyYet = ref(false);

function selectSubject(s) {
  subject.value = s.name;
  if (!s.ready) {
    notReadyYet.value = true;
    return;
  }
  notReadyYet.value = false;
  saveState({ subject: s.name, lastUnitId: null });
  router.push({ name: "toc" });
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Nanum+Pen+Script&display=swap');

/* 서브타이틀 및 대화 텍스트 */
.subtitle {
  font-size: 13.5px;
  margin: 0 0 32px;
  line-height: 1.6;
  letter-spacing: -0.01em;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.speech-text {
  display: inline-block;
  font-family: 'Nanum Pen Script', 'Gowun Dodum', cursive, sans-serif;
  font-size: 19px;
  line-height: 1.4;
  letter-spacing: 0.01em;
}

/* 분필 텍스트 색상 및 글로우 효과 */
.blue-chalk {
  color: #8fc4e8;
  font-weight: 500;
  text-shadow: 
    0 0 3px rgba(143, 196, 232, 0.6),
    0 0 10px rgba(143, 196, 232, 0.4),
    0 0 18px rgba(143, 196, 232, 0.2);
}

.pink-chalk {
  color: #f2aec1;
  font-weight: 500;
  text-shadow: 
    0 0 3px rgba(242, 174, 193, 0.6),
    0 0 10px rgba(242, 174, 193, 0.4),
    0 0 18px rgba(242, 174, 193, 0.2);
}

/* 선택 블록 */
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
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.choice.active {
  background: rgba(86, 163, 217, 0.2);
  border-color: #56a3d9;
  color: #8fc4e8;
}
.choice.disabled {
  opacity: 0.5;
}
.soon {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(241, 237, 228, 0.1);
  color: rgba(241, 237, 228, 0.4);
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

/* 하단 철학 영역 */
.philosophy-card {
  margin-top: 48px;
  padding: 16px 18px;
  border-radius: 12px;
  background: rgba(241, 237, 228, 0.03);
  border: 1px solid rgba(241, 237, 228, 0.08);
  position: relative;
}

.card-tag {
  font-family: 'Comic Sans MS', 'Gowun Dodum', 'Nanum Pen Script', 'Cafe24 Ssurround air', sans-serif;
  font-size: 11px;
  letter-spacing: 0.05em;
  font-weight: 700;
  color: #8fc4e8;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  text-shadow: 0 0 4px rgba(143, 196, 232, 0.4);
}

.chalk-star-icon {
  width: 16px;
  height: 16px;
  filter: drop-shadow(0 0 3px rgba(143, 196, 232, 0.7)) 
          drop-shadow(0 0 8px rgba(143, 196, 232, 0.4));
  transform: rotate(-5deg);
}

.philosophy-title {
  font-family: 'Gowun Dodum', 'Cafe24 Ssurround air', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: rgba(241, 237, 228, 0.9);
  margin: 0 0 8px;
  letter-spacing: -0.02em;
  text-shadow: 0 0 5px rgba(241, 237, 228, 0.2);
}

.philosophy-desc {
  font-size: 12.5px;
  line-height: 1.65;
  color: rgba(241, 237, 228, 0.45);
  margin: 0;
  letter-spacing: -0.01em;
}

/* 말풍선 SVG 아이콘 */
.chalk-speech-icon {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  margin-top: 0px;
  transform: rotate(-4deg);
  filter: drop-shadow(0 0 3px rgba(242, 174, 193, 0.8)) 
          drop-shadow(0 0 10px rgba(242, 174, 193, 0.4));
}

/* 말풍선 안쪽 점 스톱모션 애니메이션 */
.chalk-dot {
  opacity: 0.15;
  transform-origin: center;
  transform: scale(0.7);
  animation: chalkDotStep 3.2s infinite steps(1);
}

.dot-1 {
  animation-delay: 0s;
}
.dot-2 {
  animation-delay: 0.8s;
}
.dot-3 {
  animation-delay: 1.6s;
}

@keyframes chalkDotStep {
  0% {
    opacity: 0.15;
    transform: scale(0.7);
  }
  25%, 75% {
    opacity: 1;
    transform: scale(1.3);
  }
  85%, 100% {
    opacity: 0.15;
    transform: scale(0.7);
  }
}
</style>