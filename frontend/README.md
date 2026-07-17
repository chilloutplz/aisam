# AI Sam - Vue3 프론트엔드

## 실행 방법

```bash
npm install
cp .env.example .env.local   # 필요하면 API 주소 수정
npm run dev
```

기본적으로 `http://localhost:8000/api`(Django 백엔드)를 바라봅니다.
Django 백엔드를 먼저 실행해두고, 이 프론트엔드를 `npm run dev`로 켜면
`http://localhost:5173`에서 확인할 수 있습니다.

## 배포용 빌드

```bash
npm run build
```
`dist/` 폴더가 생성됩니다. 이 폴더를 아무 정적 파일 호스팅(Netlify, Vercel,
또는 Django의 STATIC 폴더)에 올리면 됩니다.

## 구조

- `src/api.js` — Django API 호출 (목차/단원상세/채팅)
- `src/views/HomeView.vue` — 학교급·학년·과목 선택
- `src/views/TocView.vue` — 학기 → 영역 → 단원 아코디언 목차
- `src/views/UnitView.vue` — 단원 서사/이름유래/스킬/문제 + AI 채팅
- `src/components/QuizSection.vue` — 문제 카루셀(직접 입력 후 확인, 다른 문제 풀기)
- `src/components/Diagram.vue` — 칠판 스타일 SVG 다이어그램 11종

디자인은 원래 React 프로토타입(칠판/분필 컨셉, 다크 그린 배경)을 그대로
옮긴 것입니다.
