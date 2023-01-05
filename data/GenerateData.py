from faker import Factory
import random
import json

marital = ["Single", "Married"]

fakerFR = Factory.create('fr_FR')

employees = dict()

# https://faker.readthedocs.io/en/latest/locales/fr_FR.html

for i in range (0, 10):
    date_de_naissance = str(fakerFR.date_of_birth(tzinfo=None, minimum_age=20, maximum_age=100))
    name = fakerFR.last_name().upper()
    employee = {"lastname": name,
                "firstname": fakerFR.first_name(),
                "id": str(int(random.random()*1000+8000)),
                "gender": str(int(random.random()*2+1)),
                "nation": "64",
                "DOB": date_de_naissance,
                "marital": marital[int(random.random()*2)]}
    employees[name] = employee

with open(r'S:\github\pyselenium\data\employees.json', 'w', encoding='utf-8') as f:
    json.dump(employees, f, ensure_ascii=False, indent=4)
