# This script is used to fix to add the token and section of the members
import csv
import hashlib


def hash_password(msg):
    salt = 'CSC'.encode('utf-8')
    hash = hashlib.md5(salt + msg.encode('utf-8')).hexdigest()
    return hash


reader = csv.DictReader(open('sheet.csv', 'r'))

dict_list = []

for line in reader:
    dict_list.append(line)

new_list = []
for ls in dict_list:
    new_dict = dict()
    new_dict['name'] = ls['First and last name']
    new_dict['email'] = ls['Email']
    new_dict['ID'] = ls['University ID']
    if ls['I have read the three training courses\' descriptions above, and I acknowledge the prerequisites needed.'] == 'Yes':
        training = ls['After reading the outline, the course you choose to attend is:']
        if 'Intermediate' in training:
            new_dict['training'] = 'Intermediate'
        elif 'Penetration' in training:
            new_dict['training'] = 'pentest'
        else:
            if 'Thursday' in training:
                new_dict['training'] = 'beginner1'
            if 'Saturday' in training:
                new_dict['training'] = 'beginner2'
    else:
        new_dict['training'] = ''
    if new_dict['name'] == '':
        new_dict['name'] = ls['First and last Name']
    if new_dict['email'] == '':
        new_dict['email'] = ls['email']
    if new_dict['ID'] == '':
        new_dict['ID'] = ls['University\'s ID']
    token = hash_password(new_dict['name'])
    new_dict['token'] = token
    new_dict['registered'] = ''
    new_list.append(new_dict)


keys = new_list[0].keys()

with open('final.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(new_list)
#poggerzzz
