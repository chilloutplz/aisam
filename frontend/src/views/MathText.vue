<template>
  <span v-html="rendered"></span>
</template>

<script setup>
import { computed } from "vue";
import katex from "katex";

const props = defineProps({
  text: { type: String, default: "" },
});

// 처리 순서가 중요하다:
// 1) 먼저 $...$ 수식을 찾아 KaTeX로 렌더링해두고, 원문에서는 그 자리를 안전한 임시 토큰으로 바꿔둔다.
//    (이렇게 안 하면 "**$수식$**"처럼 별표가 수식을 통째로 감싼 경우, $ 기준으로 먼저 쪼개면서
//     별표 두 개가 서로 다른 조각으로 갈라져 짝을 못 맞추는 문제가 생긴다.)
// 2) 수식이 사라진 안전한 텍스트에서 markdownToSafeHtml로 **굵게**, --- 등을 처리한다.
// 3) 마지막으로 임시 토큰을 실제 렌더링된 수식 HTML로 되돌린다.
function renderMixedText(text) {
  if (!text) return "";

  const formulas = [];
  const withPlaceholders = text.replace(/\$[^$]+\$/g, (match) => {
    const formula = match.slice(1, -1);
    let html;
    try {
      html = katex.renderToString(formula, { throwOnError: false, displayMode: false });
    } catch {
      html = escapeHtml(match);
    }
    const token = `\u0000MATH${formulas.length}\u0000`;
    formulas.push(html);
    return token;
  });

  let safe = markdownToSafeHtml(withPlaceholders);

  formulas.forEach((html, i) => {
    safe = safe.replace(`\u0000MATH${i}\u0000`, html);
  });

  return safe;
}

function markdownToSafeHtml(str) {
  let safe = escapeHtml(str);
  // **굵게** -> <strong> (별표가 그대로 안 보이게 실제로 굵게 렌더링)
  safe = safe.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  // 줄 전체가 --- 뿐인 구분선은 그냥 제거 (군더더기라 대화체에 안 어울림)
  safe = safe.replace(/(^|<br\/>)\s*---+\s*(?=<br\/>|$)/g, "$1");
  // 수식 밖으로 새어나온 \dots 는 말줄임표로 보이게
  safe = safe.replace(/\\dots/g, "…");
  return safe;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br/>");
}

const rendered = computed(() => renderMixedText(props.text));
</script>
