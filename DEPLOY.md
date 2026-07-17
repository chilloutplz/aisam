# 클라우드타입 배포 가이드

이 저장소는 하나의 GitHub 레포 안에 `backend`(Django)와 `frontend`(Vue3)가
같이 있습니다. 클라우드타입에서는 이 둘을 **서로 다른 두 개의 서비스**로
각각 배포합니다.

## 순서

**반드시 backend를 먼저 배포**해야 합니다. frontend가 backend의 주소를
알아야 하기 때문입니다.

---

## 1단계: Backend 배포

1. 클라우드타입 대시보드에서 새 서비스 생성 → GitHub 저장소(`aisam`) 선택
2. **서브 디렉토리**를 `backend`로 설정
3. 프리셋: `Python` (Django) 선택
4. 빌드/실행 설정에서 **설정변경** 클릭 후:
   - **시작 명령어**:
     ```
     gunicorn config.wsgi:application --bind 0.0.0.0:8000
     ```
   - **사전 실행(prestart) 명령어**:
     ```
     python manage.py migrate && python manage.py load_curriculum && python manage.py collectstatic --noinput
     ```
   - **포트**: `8000`
5. **환경변수** 설정:
   | 이름 | 값 |
   |---|---|
   | `OPENROUTER_API_KEY` | OpenRouter에서 발급받은 키 |
   | `DJANGO_SECRET_KEY` | 아무 긴 임의 문자열 (아래 명령으로 생성 가능) |
   | `DJANGO_DEBUG` | `False` |
   | `ALLOWED_HOSTS` | 처음엔 `*`로 두고, 배포 후 실제 도메인이 정해지면 그 도메인으로 교체 |

   `DJANGO_SECRET_KEY` 생성 명령 (로컬에서 실행):
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

6. 배포 완료 후, 클라우드타입이 자동으로 부여한 주소를 확인합니다.
   (예: `https://port-0-aisam-xxxxx.sel4.cloudtype.app`)
   → 이 주소를 다음 단계(frontend)에서 씁니다.

7. (선택) 이제 `ALLOWED_HOSTS` 환경변수를 `*` 대신 위에서 확인한 실제
   도메인으로 바꾸면 조금 더 안전합니다.

---

## 2단계: Frontend 배포

1. 새 서비스 생성 → 같은 GitHub 저장소 선택
2. **서브 디렉토리**를 `frontend`로 설정
3. 프리셋: `Vue3` 선택
4. 빌드 설정 확인:
   - `docbase`: `/dist`
   - `spa`: 켜기 (vue-router가 새로고침해도 깨지지 않도록)
5. **환경변수** 설정:
   | 이름 | 값 |
   |---|---|
   | `VITE_API_BASE` | 1단계에서 확인한 backend 주소 + `/api` (예: `https://port-0-aisam-xxxxx.sel4.cloudtype.app/api`) |

   ⚠️ Vite는 빌드 시점에 환경변수를 파일에 박아 넣기 때문에, 이 값은
   **빌드하기 전에** 반드시 설정돼 있어야 합니다. 나중에 값만 바꾸면
   재배포(재빌드)를 한 번 더 해줘야 반영됩니다.

6. 배포 완료 후 클라우드타입이 부여한 주소로 접속하면 됩니다.

7. (선택) backend의 `CORS_ALLOWED_ORIGINS` 환경변수에 이 frontend 주소를
   추가하면 조금 더 안전합니다 (지금은 기본값이 전체 허용에 가깝게
   되어 있어서 안 해도 당장은 작동합니다).

---

## 주의할 점

- **데이터는 매 배포마다 새로 채워짐**: `load_curriculum`이 prestart에서
  매번 실행되기 때문에, DB(SQLite)가 컨테이너 재시작으로 초기화돼도
  문제없습니다. 콘텐츠는 코드(`learning/curriculum.json`)에 있는 게
  기준이라, 오히려 매번 최신 상태로 맞춰지는 게 의도된 동작입니다.
- **OpenRouter 무료 한도**: 하루 50회 제한이 있습니다. 자세한 내용은
  `backend/README.md` 참고.
