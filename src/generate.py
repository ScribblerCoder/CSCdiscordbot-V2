import uuid
import csv


# EDIT THESE VARIABLES
############################################
NAME_FIELD      = "Full Name:"
EMAIL_FIELD     = "University Email Address (Ex: Niz20190210@std.psut.edu.jo)"
NUMBER_FIELD    = "Phone Number:"
ID_FIELD        = "Student ID:"
MAJOR_FIELD     = "What is your Major?"
CLASS_FIELD     = "What level of training would you like to receive?"
############################################



reader = csv.DictReader(open('members_sheet.csv', 'r', encoding="utf8"))
# readerb = csv.DictReader(open('beginners_sheet.csv', 'r', encoding="utf8"))
# readeri = csv.DictReader(open('intermediate_sheet.csv', 'r', encoding="utf8"))

members_dict_list = []
# beg_dict_list = []
# int_dict_list = []

for line in reader:
    members_dict_list.append(line)

# for line in readerb:
#     beg_dict_list.append(line)

# for line in readeri:
#     int_dict_list.append(line)


# what.....
# new_list = []
# abid = []
# aiid = []
# bid = []
# iid = []

# for i in beg_dict_list:
#     abid.append(i['What is Your Student ID?'])

# for i in int_dict_list:
#     aiid.append(i['What is your Student ID?'])




new_list = []

for member in members_dict_list:
    temp_dict = {}

    # renaming field names
    temp_dict['name']   =   member[NAME_FIELD]
    temp_dict['email']  =   member[EMAIL_FIELD]
    temp_dict['number'] =   member[NUMBER_FIELD]
    temp_dict['ID']     =   member[ID_FIELD]
    temp_dict['major']  =   member[MAJOR_FIELD]
    temp_dict['class']  =   member[CLASS_FIELD]

    
    temp_dict['token'] = str(uuid.uuid4())        # unique token for each member for discord verification
    temp_dict['registered'] = ''
    new_list.append(temp_dict)





# this code is reeeeeaaaallly ????????????????
# for d in members_dict_list:
#     new_dict = dict()
#     new_dict['name'] = d[NAME_FIELD]
#     new_dict['email'] = d[EMAIL_FIELD]
#     new_dict['number'] = d[NUMBER_FIELD]
#     new_dict['ID'] = d[ID_FIELD]
#     new_dict['major'] = d[MAJOR_FIELD]
#     new_dict['class'] = ''
#     if d['What level of training would you like to receive?'].split()[0] == 'Beginner':
#         for b in beg_dict_list:
#             if new_dict['ID'] == b['What is Your Student ID?']:
#                 new_dict['class'] = f'Beginner/{b["Which Session would you like to join?"].split()[0]}'
#                 bid.append(new_dict['ID'])
#                 del b
#                 break

#     elif d['What level of training would you like to receive?'].split()[0] == 'Intermediate':
#         for i in int_dict_list:
#             if new_dict['ID'] == i['What is your Student ID?']:
#                 new_dict['class'] = 'Intermediate/Thursday'
#                 iid.append(new_dict['ID'])
#                 del i
#                 break
#     else:
#         new_dict['class'] = 'None'
    
#     if new_dict['class'] == '':
#         new_dict['class'] = 'None'
#     new_dict['token'] = str(uuid.uuid4())
#     new_dict['registered'] = ''
#     new_list.append(new_dict)


keys = new_list[0].keys()

with open('final.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(new_list)

# print(list(set(abid) - set(bid)))
# print(list(set(aiid) - set(iid)))