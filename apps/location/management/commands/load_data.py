import json
from django.core.management.base import BaseCommand
from apps.location.models import Region, Area, Village


class Command(BaseCommand):
    help = 'Populate the database with regions, areas, and villages from JSON file'

    def handle(self, *args, **kwargs):
        with open('/home/mzmpro/PycharmProjects/mahallatanlovbot/mahalla_list_updated.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            region_name = item['region']
            city_district_name = item['city_district']
            village_name = item['mahalla_name']

            # Get or create Region
            region, created = Region.objects.get_or_create(name=region_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Region created: {region_name}'))

            # Get or create Area
            area, created = Area.objects.get_or_create(name=city_district_name, region=region)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Area created: {city_district_name} in region {region_name}'))

            # Get or create Village
            village, created = Village.objects.get_or_create(name=village_name, area=area)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Village created: {village_name} in area {city_district_name}'))

        self.stdout.write(self.style.SUCCESS('Database population complete'))
