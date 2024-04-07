import json, os, csv
from collections import defaultdict

with open('advancements.json', 'r') as f:
    adv_data = json.load(f)

filtered = defaultdict(lambda:[])
for x in list(adv_data.keys()):
    if x == "DataVersion":
        continue
    if x[:17] != 'minecraft:recipes':
        print(x)
        tab, adv = x.split('/')
        filtered[tab].append(adv)

for tab in filtered:
    print(tab, len(filtered[tab]))

advancements = [
    ['display_name', 'true_name']
]

for root in ['minecraft', 'blazeandcave']:
    folder_path = f'data/{root}/advancements'
    for tab in os.listdir(folder_path):
        tab_path = os.path.join(folder_path, tab)
        root = folder_path.split('/')[1]
        prefix = f'{root}:{tab}'
        for adv in os.listdir(tab_path):
            true_name = f'{prefix}/{adv[:-5]}'
            adv_path = os.path.join(tab_path, adv)
            try:
                with open(adv_path, 'r') as f:
                    data = json.load(f)
                    display_name = data['display']['title']['translate']
            except KeyError:
                display_name = "NOT AN ADVANCEMENT"
            advancements.append([display_name, true_name])

with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter='\t')
    writer.writerows(advancements)

print("Printing Missing Achievements")
# print(adv_data.keys())
for row in advancements[1:]:
    if row[1] not in adv_data:
        print(row[1])