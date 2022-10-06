import uuid
import csv

readerm = csv.DictReader(open('members_sheet.csv', 'r', encoding="utf8"))
readerb = csv.DictReader(open('beginners_sheet.csv', 'r', encoding="utf8"))
readeri = csv.DictReader(open('intermediate_sheet.csv', 'r', encoding="utf8"))

members_dict_list = []
beg_dict_list = []
int_dict_list = []

for line in readerm:
    members_dict_list.append(line)

for line in readerb:
    beg_dict_list.append(line)

for line in readeri:
    int_dict_list.append(line)

new_list = []
abid = []
aiid = []
bid = []
iid = []

for i in beg_dict_list:
    abid.append(i['What is Your Student ID?'])

for i in int_dict_list:
    aiid.append(i['What is your Student ID?'])


for d in members_dict_list:
    new_dict = dict()
    new_dict['name'] = d['What is your Name?']
    new_dict['email'] = d['Email address']
    new_dict['number'] = d['What is your Phone Number?']
    new_dict['ID'] = d['What is your Student ID?']
    new_dict['major'] = d['What is your Major?']
    new_dict['class'] = ''
    if d['What level of training would you like to receive?'].split()[0] == 'Beginner':
        for b in beg_dict_list:
            if new_dict['ID'] == b['What is Your Student ID?']:
                new_dict['class'] = f'Beginner/{b["Which Session would you like to join?"].split()[0]}'
                bid.append(new_dict['ID'])
                del b
                break

    elif d['What level of training would you like to receive?'].split()[0] == 'Intermediate':
        for i in int_dict_list:
            if new_dict['ID'] == i['What is your Student ID?']:
                new_dict['class'] = 'Intermediate/Thursday'
                iid.append(new_dict['ID'])
                del i
                break
    else:
        new_dict['class'] = 'None'
    
    if new_dict['class'] == '':
        new_dict['class'] = 'None'
    new_dict['token'] = str(uuid.uuid4())
    new_dict['registered'] = ''
    new_list.append(new_dict)


keys = new_list[0].keys()

with open('final.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(new_list)

print(list(set(abid) - set(bid)))
print(list(set(aiid) - set(iid)))