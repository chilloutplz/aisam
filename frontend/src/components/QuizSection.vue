<template>
  <div class="quiz">
    <div class="quiz-top">
      <span class="quiz-count">문제 {{ pos + 1 }} / {{ bank.length }}</span>
      <button class="shuffle-btn" :style="{ color: chalk }" @click="goToNext">⤭ 다른 문제 풀기</button>
    </div>

    <p class="question">{{ item.q }}</p>

    <Diagram v-if="item.visual" :type="item.visual" :chalk="chalk" />

    <input
      v-model="userAnswer"
      :disabled="revealed"
      placeholder="먼저 직접 풀어서 답을 적어봐"
      class="answer-input"
      :style="{ borderColor: nudge ? '#eb8a6d' : 'rgba(241,237,228,0.2)' }"
      @input="nudge = false"
    />

    <p v-if="nudge" class="nudge">답을 먼저 적어봐야 확인할 수 있어. 틀려도 괜찮으니 써보고 눌러줘.</p>

    <button v-if="!revealed" class="check-btn" :style="{ background: chalk + '22', color: chalk, borderColor: chalk + '55' }" @click="handleCheck">
      정답 확인하기
    </button>

    <div v-else class="reveal">
      <p class="your-answer">네가 쓴 답: <span>{{ userAnswer }}</span></p>
      <p class="correct-answer"><span :style="{ color: chalk }">정답 · </span>{{ item.a }}</p>
      <div class="reveal-actions">
        <button class="retry" @click="retrySame">같은 문제 다시 풀기</button>
        <button class="next" :style="{ color: chalk }" @click="goToNext">다른 문제 풀어보기 →</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import Diagram from "./Diagram.vue";

const props = defineProps({
  bank: { type: Array, required: true },
  chalk: { type: String, required: true },
});

function shuffledIndices(length) {
  const arr = Array.from({ length }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

const order = ref(shuffledIndices(props.bank.length));
const pos = ref(0);
const userAnswer = ref("");
const revealed = ref(false);
const nudge = ref(false);

const item = computed(() => props.bank[order.value[pos.value]]);

function handleCheck() {
  if (!userAnswer.value.trim()) {
    nudge.value = true;
    return;
  }
  nudge.value = false;
  revealed.value = true;
}

function goToNext() {
  const nextPos = (pos.value + 1) % order.value.length;
  if (nextPos === 0) order.value = shuffledIndices(props.bank.length);
  pos.value = nextPos;
  userAnswer.value = "";
  revealed.value = false;
  nudge.value = false;
}

function retrySame() {
  userAnswer.value = "";
  revealed.value = false;
  nudge.value = false;
}

// bank가 바뀌면(다른 단원으로 이동 등) 상태 초기화
watch(
  () => props.bank,
  (newBank) => {
    order.value = shuffledIndices(newBank.length);
    pos.value = 0;
    userAnswer.value = "";
    revealed.value = false;
    nudge.value = false;
  }
);
</script>

<style scoped>
.quiz {
  border-radius: 8px;
  padding: 16px;
  background: rgba(241, 237, 228, 0.05);
  border: 1px solid rgba(241, 237, 228, 0.14);
}
.quiz-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.quiz-count { font-size: 11px; color: rgba(241, 237, 228, 0.4); }
.shuffle-btn { font-size: 12px; font-weight: 500; }
.question { font-size: 15px; line-height: 1.6; margin: 0 0 12px; color: #f1ede4; }
.answer-input {
  width: 100%;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
  margin-bottom: 8px;
  background: rgba(241, 237, 228, 0.06);
  border: 1px solid;
  color: #f1ede4;
  outline: none;
}
.answer-input:disabled { opacity: 0.6; }
.nudge { font-size: 12px; margin-bottom: 8px; color: #eb8a6d; }
.check-btn {
  font-size: 14px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid;
}
.reveal {
  margin-top: 4px;
  padding-top: 12px;
  border-top: 1px dashed rgba(241, 237, 228, 0.2);
}
.your-answer { font-size: 14px; margin: 0 0 4px; color: rgba(241,237,228,0.5); }
.your-answer span { color: #f1ede4; }
.correct-answer { font-size: 14px; line-height: 1.6; margin: 0 0 12px; color: rgba(241,237,228,0.85); }
.correct-answer span { font-weight: 500; }
.reveal-actions { display: flex; gap: 12px; }
.retry { font-size: 12px; text-decoration: underline; color: rgba(241,237,228,0.4); }
.next { font-size: 12px; font-weight: 500; }
</style>
