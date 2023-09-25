import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredients, Tags


class Command(BaseCommand):
    help = "Загрезка Ингредиентов"
    CSV_DIR = "/app/data/"
    CSV_FILES = {"ingredients": Ingredients,
                 "tags": Tags}

    def handle(self, *args, **options):
        self.run()

    def run(self):
        self.load_data()

    def load_data(self):
        for file, models in self.CSV_FILES.items():
            count = 1
            model = models
            with open(
                self.CSV_DIR + file + ".csv", encoding="utf8", newline=""
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row["id"] = count
                    obj = model(**row)
                    obj.save()
                    count += 1
