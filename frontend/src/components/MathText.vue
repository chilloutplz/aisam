<template>
  <span v-html="rendered"></span>
</template>

<script setup>
import { computed } from "vue";
import katex from "katex";

const props = defineProps({
  text: { type: String, default: "" },
});

// "일반 텍스트 $x^2+1$ 더 텍스트" 처럼 $...$ 로 감싸진 부분만 수식으로 렌더링하고
// 나머지는 그대로 둔다. $ 기호가 하나만 있거나 짝이 안 맞으면 원래 텍스트를 그대로 보여준다.
function renderMixedText(text) {
  if (!text) return "";
  const parts = text.split(/(\$[^$]+\$)/g);
  return parts
    .map((part) => {
      if (part.startsWith("$") && part.endsWith("$") && part.length > 2) {
        const formula = part.slice(1, -1);
        try {
          return katex.renderToString(formula, { throwOnError: false, displayMode: false });
        } catch {
          return escapeHtml(part);
        }
      }
      return escapeHtml(part);
    })
    .join("");
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
