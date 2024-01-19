import csv
from django.core.management.base import BaseCommand
from culturizateApp.models import Cuadro
import os

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(script_dir, 'obras_arte.csv')

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            csv_reader = csv.DictReader(file, fieldnames=['cuadro', 'autor', 'year', 'description', 'a', 'b', 'c', 'image'])

            for row_number,row in enumerate(csv_reader,start=1):
                try:
                    Cuadro.objects.update_or_create(
                        cuadro=row['cuadro'],
                        autor=row['autor'],
                        year=row['year'],
                        description=row['description'],
                        a=row['a'],
                        b=row['b'],
                        c=row['c'],
                        image=row['image'],
                    )
                except ValueError as e:
                    # Captura la excepción y muestra la línea problemática
                    self.stdout.write(self.style.WARNING(f"Error en la línea {row_number}: {e}"))
                    self.stdout.write(self.style.WARNING(f"Contenido de la línea: {row}"))
                except Exception as ex:
                    # Captura otras excepciones que puedan ocurrir
                    self.stdout.write(self.style.ERROR(f"Otra excepción en la línea {row_number}: {ex}"))
                    self.stdout.write(self.style.ERROR(f"Contenido de la línea: {row}"))


        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
