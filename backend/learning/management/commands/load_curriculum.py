import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from learning.models import Domain, Unit

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "curriculum_data"


class Command(BaseCommand):
    help = (
        "learning/curriculum_data/ 안의 과목별 JSON 파일들을 DB에 적재(upsert)합니다. "
        "기존 데이터를 지우지 않고, slug 기준으로 있으면 갱신·없으면 새로 만듭니다."
    )

    def handle(self, *args, **options):
        if not DATA_DIR.exists():
            self.stderr.write(f"데이터 폴더가 없습니다: {DATA_DIR}")
            return

        json_files = sorted(DATA_DIR.glob("*.json"))
        if not json_files:
            self.stderr.write(f"{DATA_DIR} 안에 JSON 파일이 없습니다.")
            return

        total_domains = 0
        total_units = 0

        for path in json_files:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            subject = data.get("subject", "수학")
            grade = data.get("grade", "중2")

            domain_order = 0
            for group in data["domains"]:
                domain_order += 1
                domain, _ = Domain.objects.update_or_create(
                    subject=subject,
                    grade=grade,
                    name=group["domain"],
                    defaults={
                        "chalk_color": group.get("chalk", "#F2C94C"),
                        "semester": group.get("semester", "1학기"),
                        "order": domain_order,
                    },
                )
                total_domains += 1

                unit_order = 0
                for u in group["units"]:
                    unit_order += 1
                    is_ready = u["status"] == "done"

                    if is_ready and "slug" in u:
                        Unit.objects.update_or_create(
                            slug=u["slug"],
                            defaults={
                                "domain": domain,
                                "title": u["title"],
                                "order": unit_order,
                                "is_ready": True,
                                "content": u.get("content", {}),
                            },
                        )
                        total_units += 1
                    else:
                        # 아직 콘텐츠 없는(todo) 단원은 slug가 없을 수 있어서
                        # 제목 기준 임시 slug로 자리만 만들어둔다 (준비중 표시용)
                        placeholder_slug = f"todo-{subject}-{grade}-{group['domain']}-{u['title']}"
                        placeholder_slug = placeholder_slug.replace(" ", "-")
                        Unit.objects.update_or_create(
                            slug=placeholder_slug,
                            defaults={
                                "domain": domain,
                                "title": u["title"],
                                "order": unit_order,
                                "is_ready": False,
                                "content": {},
                            },
                        )

            self.stdout.write(f"  {path.name} 적재 완료 ({subject} {grade})")

        self.stdout.write(self.style.SUCCESS(
            f"전체 적재 완료: 파일 {len(json_files)}개, 영역 {total_domains}개, 완성 단원 {total_units}개"
        ))
