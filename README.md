# CSCdiscordbot

Cyber Security Club's discord bot. A remake of **[CSCbot](https://github.com/Hiexy/CSCBot)**





## How to run (docker)

1- copy the members csv file and call it `members_sheet.csv`

2- fix [generate.py](generate.py) field names with your field names from the registeration form 


3- generate members' csv file  

```console
foo@bar:~$ python generate.py
```

4- build and run the docker container 
```console
foo@bar:~$ sudo bash build.sh    # use sudo if not in docker group
```