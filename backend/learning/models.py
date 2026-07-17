from django.db import models


class Domain(models.Model):
    """수와 연산 / 문자와 식 / 함수 / 기하 / 확률과 통계 같은 영역"""
    name = models.CharField(max_length=50, unique=True)
    chalk_color = models.CharField(max_length=20, default="#F2C94C")
    semester = models.CharField(max_length=10, choices=[("1학기", "1학기"), ("2학기", "2학기")])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.semester} · {self.name}"


class Unit(models.Model):
    """단원 하나. 콘텐츠(서사/이름유래/스킬/문제)는 content JSON에 통째로 저장."""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="units")
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
    #   "prev": "...", "next": "..."
    # }
    content = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["domain__order", "order"]

    def __str__(self):
        return self.title
