import json
import os
from django.core.management.base import BaseCommand
from learning.models import Domain, Unit

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "curriculum.json")


class Command(BaseCommand):
    help = "curriculum.json(React 프로토타입에서 추출된 데이터)을 DB에 적재합니다."

    def handle(self, *args, **options):
        with open(DATA_PATH, encoding="utf-8") as f:
            data = json.load(f)

        units_by_key = data["units"]          # { "RATIONAL_UNIT": {...}, ... }
        curriculum = data["curriculum"]        # [ {domain, chalk, units:[{title,status,data:"RATIONAL_UNIT"}]}, ... ]
        semesters = data["semesters"]          # [ {label, domains:[...]}, ... ]

        # 영역(domain) 이름 -> 학기 라벨 매핑
        domain_to_semester = {}
        for sem in semesters:
            for dname in sem["domains"]:
                domain_to_semester[dname] = sem["label"]

        Unit.objects.all().delete()
        Domain.objects.all().delete()

        domain_order = 0
        for group in curriculum:
            domain_order += 1
            domain = Domain.objects.create(
                name=group["domain"],
                chalk_color=group["chalk"],
                semester=domain_to_semester.get(group["domain"], "1학기"),
                order=domain_order,
            )

            unit_order = 0
            for u in group["units"]:
                unit_order += 1
                is_ready = u["status"] == "done"
                content = {}
                if is_ready and "data" in u:
                    content = units_by_key.get(u["data"], {})

                Unit.objects.create(
                    domain=domain,
                    title=u["title"],
                    order=unit_order,
                    is_ready=is_ready,
                    content=content,
                )

        self.stdout.write(self.style.SUCCESS(
            f"적재 완료: 영역 {Domain.objects.count()}개, 단원 {Unit.objects.count()}개"
        ))
