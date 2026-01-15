import csv
from django.core.management.base import BaseCommand
from elections.models import State, County, CountyResult

class Command(BaseCommand):
    help = "Load csv into DB"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **opts):
        csv_path = opts["csv_path"]

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                state, _ = State.objects.get_or_create(name=row["state"].strip())
                county, _ = County.objects.get_or_create(
                    state=state,
                    name=row["county"].strip(),
                )

                CountyResult.objects.create(
                    county=county,
                    current_votes=int(row["current_votes"]),
                    total_votes=int(row["total_votes"]),
                    percent=float(row["percent"]) if row["percent"] else None,
                )

        self.stdout.write(self.style.SUCCESS("CSV imported successfully"))
