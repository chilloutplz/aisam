# AI Sam

중2 수학 학습 앱. Django 백엔드 + Vue3 프론트엔드.

## 구조

```
aisam/
├── backend/     Django API (목차/단원상세/AI채팅 프록시)
│   ├── config/       프로젝트 설정 (settings, urls)
│   └── learning/     Domain·Unit 모델, API 뷰, 커리큘럼 데이터
└── frontend/     Vue3 앱 (홈 → 목차 → 단원 화면)
```

각 폴더의 README.md에 실행 방법이 따로 있습니다.

## 빠른 시작

```bash
# 터미널 1 - 백엔드
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py load_curriculum
export OPENROUTER_API_KEY="키"
python manage.py runserver

# 터미널 2 - 프론트엔드
cd frontend
npm install
npm run dev
```

브라우저에서 http://localhost:5173 열면 됩니다.
