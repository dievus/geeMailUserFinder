# geeMailUserFinder

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

<p align="center">
  <img src="https://github.com/dievus/GeeMailUserFinder/blob/main/images/geeMailUserFinder.jpg" />
</p>

geeMailUserFinder is used for identifying valid Gmail accounts without the risk of account lockouts. The tool parses responses to identify if a cookie is issued for valid accounts, and responds appropriately if the user is valid. 

Note that on occasion you may find that an email account that returns valid is not actual valid. This is likely due to the username not being permitted in the Gmail system, and I believe they issue a cookie for those as a way to prevent them.


## Usage
##### Installing geeMailUserFinder
```git clone https://github.com/dievus/geeMailUserFinder.git```

##### Change directories to geeMailUserFinder and run:
```pip3 install -r requirements.txt```

This will run the install script to add necessary dependencies to your system.

```python3 geeMailUserFinder.py -h```

##### This will output the help menu, which contains the following flags:

### ---Validate a single email---
python3 geeMailUserFinder.py -e test@test.com

### ---Validate a list of emails and write to file---
```python3 geeMailUserFinder.py -r testemails.txt -w valid.txt```

### ---Validate a list of emails, write to file and timeout between requests---
```python3 geeMailUserFinder.py -r emails.txt -w validemails.txt -t 30```

### ---Validate a list of emails and timeout between requests---
```python3 geeMailUserFinder.py -r emails.txt -t 30```

### ---Validate a list of emails using verbose mode---
```python3 geeMailUserFinder.py -r emails.txt -v```



### Notes
Keep in mind that Google may or may not appreciate account testing like this on their services. 
