# CSCdiscordbot

Cyber Security Club's discord bot. A remake of **[CSCbot](https://github.com/Hiexy/CSCBot)**





## How to run (docker)

1- copy the members csv file and call it `members_sheet.csv`

2- Add the following roles to the discord server

```
- Member
- Beginner Class <class_number> <academic_year> <first_sem/second_sem> 
- Intermediate Class 1 <academic_year> <first_sem/second_sem> 
```

2- fix [generate.py](generate.py) field names with your field names from the registeration form 

3- generate members' csv file  

```console
foo@bar:~$ python generate.py
```

4- build and run the docker container 
```console
foo@bar:~$ sudo bash build.sh    # use sudo if not in docker group
```