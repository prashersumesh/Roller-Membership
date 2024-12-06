### Roller Automation 

This project aims to automate all the repetative tasks that are performed in the roller platform. 

1. Memebership Form Automation
    This project has following features: 
        - Login to roller 
        - Configure membership setting to get all the membership only
        - For each date: 
          - Check if that date contains membership
            - if contains: click on each membership and extract all details with signature. 
        - Convert colleced data into terms and condition pdf with signature attached. 



### Setting up the project: 
1. Install the enviroment 
   
```
pip install -r requirements.txt 
```

2. Run respective automation file. 

```
python membership_bot.py
```