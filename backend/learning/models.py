from django.db import models


class Domain(models.Model):
    """수와 연산 / 문자와 식 / 함수 / 기하 / 확률과 통계 같은 영역"""
    subject = models.CharField(max_length=30, default="수학")   # 수학, 영어, 국어...
    grade = models.CharField(max_length=20, default="중2")       # 중1, 중2, 고1...
    name = models.CharField(max_length=50)
    chalk_color = models.CharField(max_length=20, default="#F2C94C")
    semester = models.CharField(max_length=10, choices=[("1학기", "1학기"), ("2학기", "2학기")])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["subject", "grade", "order"]
        unique_together = [("subject", "grade", "name")]

    def __str__(self):
        return f"{self.subject} {self.grade} · {self.semester} · {self.name}"


class Unit(models.Model):
    """단원 하나. 콘텐츠(서사/이름유래/스킬/문제)는 content JSON에 통째로 저장."""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="units")

    # 재배포해도 안 바뀌는 고유 식별자 (예: "rational-repeating-decimal").
    # 이 값 기준으로 갱신(upsert)하기 때문에, 나중에 진도 기록 등을 이 slug나
    # PK에 연결해도 재배포 때문에 깨지지 않는다.
    slug = models.SlugField(max_length=100, unique=True)

    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_ready = models.BooleanField(default=False)  # 콘텐츠가 채워져서 학생이 볼 수 있는 상태인지

    # content 구조 예시:
    # {
    #   "term": "유리수",
    #   "termMeaning": "...",
    #   "bigPicture": ["...", "..."],
    #   "nameOrigin": "...",
    #   "coreSkills": [{"name": "...", "explain": "...", "visual": "..."}],
    #   "problems": {"concept": [...], "skill": [...], "application": [...], "challenge": [...]},
    # }
    content = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["domain__order", "order"]

    def __str__(self):
        return self.title
