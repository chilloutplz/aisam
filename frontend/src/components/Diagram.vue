<template>
  <!-- 직사각형 넓이 -->
  <svg v-if="type === 'rect_2x_3x'" viewBox="0 0 200 110" class="diagram">
    <rect x="30" y="15" width="140" height="80" fill="none" :stroke="stroke" stroke-width="1.5" />
    <text x="100" y="10" text-anchor="middle" font-size="13" :fill="chalk">2x</text>
    <text x="16" y="59" text-anchor="middle" font-size="13" :fill="chalk">3x</text>
  </svg>

  <!-- 정육면체 부피 -->
  <svg v-else-if="type === 'cube_x'" viewBox="0 0 200 130" class="diagram">
    <rect x="40" y="45" width="70" height="70" fill="none" :stroke="stroke" stroke-width="1.5" />
    <rect x="65" y="20" width="70" height="70" fill="none" :stroke="stroke" stroke-width="1.2" opacity="0.6" />
    <line x1="40" y1="45" x2="65" y2="20" :stroke="stroke" stroke-width="1.2" opacity="0.6" />
    <line x1="110" y1="45" x2="135" y2="20" :stroke="stroke" stroke-width="1.2" opacity="0.6" />
    <line x1="40" y1="115" x2="65" y2="90" :stroke="stroke" stroke-width="1.2" opacity="0.6" />
    <line x1="110" y1="115" x2="135" y2="90" :stroke="stroke" stroke-width="1.2" opacity="0.6" />
    <text x="75" y="128" text-anchor="middle" font-size="13" :fill="chalk">x</text>
  </svg>

  <!-- 정사각형 두 개 비교 -->
  <svg v-else-if="type === 'two_squares_ab'" viewBox="0 0 220 110" class="diagram">
    <rect x="20" y="15" width="80" height="80" fill="none" :stroke="stroke" stroke-width="1.5" />
    <text x="60" y="112" text-anchor="middle" font-size="13" :fill="chalk">a</text>
    <rect x="130" y="45" width="50" height="50" fill="none" :stroke="stroke" stroke-width="1.5" />
    <text x="155" y="112" text-anchor="middle" font-size="13" :fill="chalk">b</text>
  </svg>

  <!-- 수직선 위 x>4 -->
  <svg v-else-if="type === 'numberline_x_gt_4'" viewBox="0 0 220 60" class="diagram diagram--wide">
    <line x1="15" y1="30" x2="205" y2="30" :stroke="stroke" stroke-width="1.5" />
    <polygon points="205,25 215,30 205,35" :fill="stroke" />
    <line v-for="n in 7" :key="n" :x1="30 + (n - 1) * 28" y1="25" :x2="30 + (n - 1) * 28" y2="35" :stroke="stroke" stroke-width="1" />
    <circle :cx="30 + 4 * 28" cy="30" r="5" fill="#16211c" :stroke="chalk" stroke-width="2" />
    <text :x="30 + 4 * 28" y="48" text-anchor="middle" font-size="11" :fill="chalk">4</text>
    <line :x1="30 + 4 * 28" y1="30" x2="205" y2="30" :stroke="chalk" stroke-width="2.5" />
    <text :x="30 + 6 * 28 + 8" y="18" text-anchor="middle" font-size="11" fill="rgba(241,237,228,0.5)">x&gt;4</text>
  </svg>

  <!-- 두 직선의 교점 -->
  <svg v-else-if="type === 'twolines_intersect'" viewBox="0 0 200 130" class="diagram">
    <line x1="20" y1="20" x2="180" y2="110" :stroke="stroke" stroke-width="1.5" />
    <line x1="20" y1="110" x2="180" y2="20" :stroke="stroke" stroke-width="1.5" />
    <circle cx="100" cy="65" r="4.5" :fill="chalk" />
    <text x="112" y="60" font-size="11" :fill="chalk">해 (x, y)</text>
  </svg>

  <!-- 평행선 -->
  <svg v-else-if="type === 'parallel_lines'" viewBox="0 0 200 100" class="diagram">
    <line x1="20" y1="80" x2="180" y2="20" :stroke="stroke" stroke-width="1.5" />
    <line x1="20" y1="95" x2="180" y2="35" :stroke="stroke" stroke-width="1.5" />
    <text x="140" y="55" font-size="10" :fill="chalk">절대 안 만남</text>
  </svg>

  <!-- 기울기/y절편 직선 -->
  <svg v-else-if="type === 'slope_intercept_line'" viewBox="0 0 200 160" class="diagram">
    <line x1="20" y1="140" x2="190" y2="140" :stroke="stroke" stroke-width="1.2" />
    <line x1="20" y1="140" x2="20" y2="10" :stroke="stroke" stroke-width="1.2" />
    <text x="192" y="145" font-size="10" fill="rgba(241,237,228,0.4)">x</text>
    <text x="12" y="12" font-size="10" fill="rgba(241,237,228,0.4)">y</text>
    <line x1="20" y1="110" x2="150" y2="40" :stroke="chalk" stroke-width="2" />
    <circle cx="20" cy="110" r="4" fill="#16211c" :stroke="chalk" stroke-width="2" />
    <text x="28" y="118" font-size="10" :fill="chalk">y절편 (0,b)</text>
    <line x1="60" y1="90" x2="100" y2="90" stroke="rgba(241,237,228,0.5)" stroke-width="1" stroke-dasharray="3,2" />
    <line x1="100" y1="90" x2="100" y2="60" stroke="rgba(241,237,228,0.5)" stroke-width="1" stroke-dasharray="3,2" />
    <text x="72" y="103" font-size="9" fill="rgba(241,237,228,0.5)">1</text>
    <text x="104" y="78" font-size="9" fill="rgba(241,237,228,0.5)">기울기 a</text>
  </svg>

  <!-- 이등변삼각형 -->
  <svg v-else-if="type === 'isosceles_triangle'" viewBox="0 0 180 140" class="diagram">
    <polygon points="90,15 20,120 160,120" fill="none" :stroke="stroke" stroke-width="1.5" />
    <line x1="90" y1="15" x2="90" y2="120" :stroke="chalk" stroke-width="1.2" stroke-dasharray="3,2" />
    <text x="60" y="70" font-size="10" :fill="chalk">AB</text>
    <text x="118" y="70" font-size="10" :fill="chalk">AC</text>
    <text x="30" y="135" font-size="10" fill="rgba(241,237,228,0.5)">밑각</text>
    <text x="140" y="135" font-size="10" fill="rgba(241,237,228,0.5)">밑각</text>
  </svg>

  <!-- 닮은 삼각형 -->
  <svg v-else-if="type === 'similar_triangles'" viewBox="0 0 220 130" class="diagram">
    <polygon points="30,110 90,110 55,30" fill="none" :stroke="stroke" stroke-width="1.5" />
    <polygon points="120,120 210,120 155,20" fill="none" :stroke="stroke" stroke-width="1.5" />
    <text x="55" y="128" text-anchor="middle" font-size="10" :fill="chalk">작은 삼각형</text>
    <text x="165" y="18" text-anchor="middle" font-size="10" :fill="chalk">큰 삼각형</text>
  </svg>

  <!-- 직각삼각형 a,b,c -->
  <svg v-else-if="type === 'right_triangle_abc'" viewBox="0 0 180 140" class="diagram">
    <polygon points="20,120 20,20 150,120" fill="none" :stroke="stroke" stroke-width="1.5" />
    <rect x="20" y="105" width="15" height="15" fill="none" :stroke="stroke" stroke-width="1" />
    <text x="10" y="75" font-size="11" :fill="chalk">a</text>
    <text x="85" y="132" font-size="11" :fill="chalk">b</text>
    <text x="90" y="65" font-size="11" fill="#f2c94c">c(빗변)</text>
  </svg>

  <!-- 부호 있는 수의 덧셈 -->
  <svg v-else-if="type === 'signed_addition_example'" viewBox="0 0 260 70" class="diagram diagram--wide">
    <line x1="10" y1="45" x2="250" y2="45" :stroke="stroke" stroke-width="1.5" />
    <polygon points="250,41 258,45 250,49" :fill="stroke" />
    <line v-for="n in 13" :key="n" :x1="30 + (n - 1) * 16" y1="41" :x2="30 + (n - 1) * 16" y2="49" :stroke="stroke" stroke-width="1" />
    <text :x="30 + 8 * 16" y="60" text-anchor="middle" font-size="10" fill="rgba(241,237,228,0.4)">0</text>
    <circle :cx="30 + 1 * 16" cy="45" r="4" fill="#e06c75" />
    <text :x="30 + 1 * 16" y="20" text-anchor="middle" font-size="10" fill="#e06c75">-7</text>
    <line :x1="30 + 1 * 16" y1="30" :x2="30 + 4 * 16" y2="30" :stroke="chalk" stroke-width="1.5" />
    <text :x="(30 + 1 * 16 + 30 + 4 * 16) / 2" y="24" text-anchor="middle" font-size="10" :fill="chalk">+3</text>
    <circle :cx="30 + 4 * 16" cy="45" r="4.5" fill="#16211c" stroke="#f2c94c" stroke-width="2" />
    <text :x="30 + 4 * 16" y="60" text-anchor="middle" font-size="10" fill="#f2c94c">-4</text>
  </svg>
</template>

<script setup>
defineProps({
  type: { type: String, required: true },
  chalk: { type: String, default: "#8fc4e8" },
});
const stroke = "rgba(241,237,228,0.75)";
</script>

<style scoped>
.diagram {
  width: 100%;
  max-width: 220px;
  display: block;
  margin: 0 auto 4px;
}
.diagram--wide {
  max-width: 280px;
}
</style>
