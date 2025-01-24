# %%
# Requires your BAC version's datapack's data folder
# Requires a completed advancement file named "advancements.json"
# Both of these should be stored in same directory as this script

# IMPORTANT: datapack file format was changed in 1.21
# advancements directory changed to advancement (yeah right)
# would need to change back if backporting to 1.20 and lower

# outputs files needed for tracker's data folder in this same directory

import json, os, csv, re
from collections import defaultdict

DATAPACK_DIR = "data/pack/data/" 
COMPLETED_PATH = "data/advancements.json"
OUTPUT_DIR = "output/"

# Load completed json
def get_adv_data():
    with open(COMPLETED_PATH, 'r') as f:
        adv_data = json.load(f)
    return adv_data

def get_adv_list(adv_data):
    filtered = defaultdict(lambda:[])
    adv_list = []
    for x in list(adv_data.keys()):
        if x == "DataVersion":
            continue
        if x[:17] != 'minecraft:recipes':
            # advlist for building adv_col.csv that later code needs
            adv_list.append([x])
            tab, adv = x.split('/')
            filtered[tab].append(adv)
    for tab in filtered:
        print(tab, len(filtered[tab]))
    return adv_list


def get_advancements():
    advancements = [
        ['display_name', 'true_name', 'icon']
    ]

    for root in ['minecraft', 'blazeandcave']:
        folder_path = f'{DATAPACK_DIR}{root}/advancement'
        for tab in os.listdir(folder_path):
            tab_path = os.path.join(folder_path, tab)
            root = folder_path.split('/')[1]
            prefix = f'{root}:{tab}'
            for adv in os.listdir(tab_path):
                true_name = f'{prefix}/{adv[:-5]}'
                adv_path = os.path.join(tab_path, adv)
                # Print next json to open
                print(adv_path)
                try:
                    with open(adv_path, 'r') as f:
                        # If this fails Cavinator left a json error (yay!)
                        # Just navigate to the most recent json file and fix
                        data = json.load(f)
                        display_name = data['display']['title']['translate']
                        icon = data['display']['icon']['id'][10:]
                except json.JSONDecodeError:
                    raise Exception(f"Invalid JSON in {adv_path}, cavinator missed it, you must fix it.")
                except KeyError:
                    display_name = "NOT AN ADVANCEMENT"
                advancements.append([display_name, true_name, icon])
    return advancements

# def write_adv_col(advlist):
#     with open('output/adv_col.csv', 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerows(advlist)

# def write_adv_to_path(advancements):
#     with open('output/advname_to_path.csv', 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file, delimiter='\t')
#         writer.writerows(advancements)

def print_missing_advs(advancements, adv_data):
    for row in advancements[1:]:
        if row[1] not in adv_data:
            print(row[1])

# For generating a list of all the items, and their mapping to adv

def get_item_to_adv(adv_data):
    stack_blocks = set(adv_data["blazeandcave:challenges/stack_all_the_blocks"]['criteria'].keys())
    stack_items = set(adv_data["blazeandcave:challenges/stack_all_the_items"]['criteria'].keys())

    blocks = set(adv_data["blazeandcave:challenges/all_the_blocks"]['criteria'].keys())
    items = set(adv_data["blazeandcave:challenges/all_the_items"]['criteria'].keys())

    print(len(stack_items), len(stack_blocks), len(stack_items.union(stack_blocks)))
    print(len(items), len(blocks), len(items.union(blocks)))
    print(items.union(blocks).difference(stack_items.union(stack_blocks)))
    all_items = items.union(blocks)
    stack_all_items = stack_items.union(stack_blocks)

    everything = all_items.union(stack_all_items)

    item_to_adv = []

    for item in list(everything):
        adv = None
        if item in stack_blocks:
            adv = "blazeandcave:challenges/stack_all_the_blocks"
        elif item in stack_items:
            adv = "blazeandcave:challenges/stack_all_the_items"
        elif item in blocks:
            adv = "blazeandcave:challenges/all_the_blocks"
        elif item in items:
            adv = "blazeandcave:challenges/all_the_items"
        item_to_adv.append([item, adv])

    item_to_adv = sorted(item_to_adv,  key=lambda x: x[0])
    return item_to_adv

# def write_item_to_adv(item_to_adv):
#     with open('output/item_to_adv.csv', 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file, delimiter='\t')
#         writer.writerows(item_to_adv)

def get_stack_size(item_to_adv):
    # Adding column for stack sizes
    with open(f"{DATAPACK_DIR}/blazeandcave/advancement/challenges/stack_all_the_blocks.json") as f:
        stack_blocks_json = json.load(f)['criteria']

    with open(f"{DATAPACK_DIR}/blazeandcave/advancement/challenges/stack_all_the_items.json") as f:
        stack_items_json = json.load(f)['criteria']

    item_adv_stack_size = []
    for item, adv in item_to_adv:
        stacksize = 1
        try:
            if item in stack_blocks_json:
                stacksize = stack_blocks_json[item]['conditions']['items'][0]['count']
            elif item in stack_items_json:
                stacksize = stack_items_json[item]['conditions']['items'][0]['count']
        except KeyError:
            pass
        name = ' '.join(word.capitalize() for word in item.split('_'))
        item_adv_stack_size.append([name, item, adv, stacksize])

    item_adv_stack_size = sorted(item_adv_stack_size, key=lambda x: x[0])
    return item_adv_stack_size

def write_stack_size(item_adv_stacksize):
    with open('output/item_adv_stacksize.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        writer.writerows(item_adv_stacksize)

# adv_col = []
# with open('output/adv_col.csv') as f:
#     reader = csv.reader(f, delimiter='\t')
#     for row in reader:
#         adv_col.append(row)

# adv_to_cell = []
# for i, adv in enumerate(adv_col):
#     adv_to_cell.append([adv, f'E{i}'])

# reference = '''IF(ISBLANK(A3), {"","",""}, {{A3, "Adv/Item", "Description"};IFERROR({FILTER({'All Items/Blocks'!$C$2:$D, 'All Items/Blocks'!$G$2:$G}, 'All Items/Blocks'!$B$2:$B=A3);{"","",""}}, {"", "", ""})})'''
# full_string = reference

# for i in range(20):
#     row = i + 4
#     full_string += ';' + reference.replace("A3", f'A{row}')

# print(full_string)

def parse_path(adv_path):
    adv_info = re.match('(\w+):(\w+)\/(\w+)', adv_path)
    return adv_info.groups()

def get_criteria():
    '''
        Reads all the advancement criterias and stores it
    '''

    every_adv = []
    with open(f"{OUTPUT_DIR}/adv_col.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            every_adv.append(row[0])
    with open(COMPLETED_PATH, 'r') as f:
        everything_data = json.load(f)

    adv_reqs = {}
    for adv_path in every_adv:
        folder, tab, adv = parse_path(adv_path)
        file_path = os.path.join(DATAPACK_DIR, folder, 'advancement', tab, adv) + '.json'
        with open(file_path, 'r') as f:
            adv_data = json.load(f)
            if 'requirements' in adv_data.keys():
                adv_reqs[adv_path] = list(adv_data['requirements'])
            else:
                adv_reqs[adv_path] = list(everything_data[adv_path]['criteria'].keys())
    return adv_reqs

def write_criteria(adv_reqs):
    with open(f"{OUTPUT_DIR}/adv_criteria_requirements.json", 'w', encoding='utf-8') as f:
        json.dump(adv_reqs, f)

def write_csv(filename, data):
    with open(f"{OUTPUT_DIR}/{filename}.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        writer.writerows(data)

def write_json(filename, data):
    with open(f"{OUTPUT_DIR}/{filename}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == "__main__":
    adv_data = get_adv_data()
    adv_list = get_adv_list(adv_data)
    advancements = get_advancements()
    print_missing_advs(advancements, adv_data)

    write_csv("advname_to_path", advancements)
    write_csv("adv_col", adv_list)

    item_to_adv = get_item_to_adv(adv_data)
    stack_size = get_stack_size(item_to_adv)
    print(stack_size)
    write_csv("item_to_adv", item_to_adv)
    write_csv("item_adv_stacksize", stack_size)

    criteria = get_criteria()   

    write_json("adv_criteria_requirements", criteria)


# %%
