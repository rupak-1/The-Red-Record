import pandas as pd
from dateutil import parser


charges = {}
state_abbreviations = {"NY": "New York","Tex": "Texas", "Ala": "Alabama", "Miss": "Mississippi", "Ark": "Arkansas", "Ga": "Georgia", "La": "Louisiana", "Fla": "Florida", "Mo": "Missouri", "Ky": "Kentucky", "SC": "South Carolina", "Va": "Virginia", "Texas": "Texas", "Ill": "Illinois", "Tenn": "Tennessee", "Ohio":"Ohio", "Pa":"Pennsylvania", "Kan":"Kansas", "W Va":"West Virginia", "Md":"Maryland"}

with open("Resources\\records.txt", "r") as file:
    data = file.read()

data = data.split("\n")

current_charge = None
current_charge_id = 0
current_year = 1892
rows  = []

for line in data:
    if line.isnumeric():
        current_year += 1
    elif line.isupper():
        current_charge = line.capitalize()
        if current_charge not in charges:
            charges[current_charge] = current_charge_id
            current_charge_id += 1
    else:
        records = line.split(";")

        for row in records:
            copy_row = row
            row = row.split(',')
            date = name = city = state = "Unknown"
            first_name = last_name = None
            if len(row) == 4:
                date, name, city, state = row
            else:
                continue
            date = parser.parse(f"{date.strip()} {str(current_year)}").strftime("%B %d, %Y")
            name = name.strip()
            city = city.strip()

            if "unknown" not in name and len(name.split()) == 2:
                first_name, last_name = name.split()
            try:
                state = state_abbreviations[state.strip().replace('.', '')]
            except:
                continue
            rows.append([charges[current_charge], current_charge, date, date.split()[0], name, first_name, last_name, city, state])

# print(rows)
df = pd.DataFrame(rows, columns=["Charge_Id", "Charge", "Date", "month", "Full Name", "First Name", "Last Name", "City", "State"])
df.to_excel("charges_1.xlsx")
