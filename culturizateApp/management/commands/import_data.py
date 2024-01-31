import csv
from django.core.management.base import BaseCommand
from culturizateApp.models import BaseQuestion
import os

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, 'questions.csv')

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row_number,row in enumerate(csv_reader,start=1):
                try:
                    BaseQuestion.objects.get_or_create(
                        question_text=row['question_text'],
                        correct_option=row['correct_option'],
                        nivel_dificultad=row['nivel_dificultad'],
                        category=row['category'],
                        points=row['points'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                    )
                except ValueError as e:
                    # Captura la excepción y muestra la línea problemática
                    self.stdout.write(self.style.WARNING(f"Error en la línea {row_number}: {e}"))
                    self.stdout.write(self.style.WARNING(f"Contenido de la línea: {row}"))
                except Exception as ex:
                    # Captura otras excepciones que puedan ocurrir
                    self.stdout.write(self.style.ERROR(f"Otra excepción en la línea {row_number}: {ex}"))


        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
