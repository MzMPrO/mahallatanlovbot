import json
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from apps.location.models import Region, Area, Village

# Load the JSON data
json_file_path = 'Cleaned_Mahallalar.json'
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Iterate through the data and add it to the database
for item in data:
    region_name = item['Region']
    district_name = item['District_City']
    village_name = item['Citizen_Assembly']

    # Get or create the Region
    region, created = Region.objects.get_or_create(name=region_name)

    # Get or create the Area
    area, created = Area.objects.get_or_create(name=district_name, region=region)

    # Get or create the Village
    village, created = Village.objects.get_or_create(name=village_name, area=area)

print("Data imported successfully.")
