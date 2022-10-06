# CSCdiscordbot

Cyber Security Club's discord bot. A remake of **[CSCbot](https://github.com/Hiexy/CSCBot)**





## How to run (docker)

- fix [generate.py](generate.py)'s field names with your field names from the registeration form 


- generate members' csv file  

```console
foo@bar:~$ python generate.py
```

- build and run the docker container 
```console
foo@bar:~$ sudo bash build.sh    # use sudo if not in docker group
```