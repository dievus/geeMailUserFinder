#!/usr/bin/python3
import re
import requests as request_handler
import argparse
import textwrap
import sys
import time
from colorama import Fore, Style, init

def definitions():
    global info, close, success, fail
    info, fail, close, success = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + Style.BRIGHT

def banner():
    print(Fore.YELLOW + Style.BRIGHT + "")
    print('                    __  ___      _ __   __  __                  _______           __            ')    
    print('   ____ ____  ___  /  |/  /___ _(_) /  / / / /_______  _____   / ____(_)___  ____/ /__  _____')
    print('  / __ `/ _ \/ _ \/ /|_/ / __ `/ / /  / / / / ___/ _ \/ ___/  / /_  / / __ \/ __  / _ \/ ___/')
    print(' / /_/ /  __/  __/ /  / / /_/ / / /  / /_/ (__  )  __/ /     / __/ / / / / / /_/ /  __/ /    ')
    print(' \__, /\___/\___/_/  /_/\__,_/_/_/   \____/____/\___/_/     /_/   /_/_/ /_/\__,_/\___/_/     ')
    print('/____/                                                                                       ')
    print("                                   Version 1.0.0                                         ")
    print("                               A project by The Mayor                                    ")
    print("                       geeMailUserFinder.py -h to get started                            \n" + Style.RESET_ALL)
    print("-" * 90)


def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''
---Validate a single email---
python3 geeMailUserFinder.py -e test@test.com\n
---Validate a list of emails and write to file---
python3 geeMailUserFinder.py -r testemails.txt -w valid.txt\n
---Validate a list of emails, write to file and timeout between requests---
python3 geeMailUserFinder.py -r emails.txt -w validemails.txt -t 30\n
---Validate a list of emails and write to CSV---
python3 geeMailUserFinder.py -r emails.txt -c validemails.csv -t 30\n
---Validate a list of emails and timeout between requests---
python3 geeMailUserFinder.py -r emails.txt -t 30\n
---Validate a list of emails using verbose mode---
python3 geeMailUserFinder.py -r emails.txt -v\n
'''))
    opt_parser.add_argument(
        '-e', '--email', help='Runs geeMailUserFinder against a single email')
    opt_parser.add_argument(
        '-r', '--read', help='Reads email addresses from file')
    opt_parser.add_argument(
        '-w', '--write', help='Writes valid emails to text file')
    opt_parser.add_argument(
        '-t', '--timeout', help='Set timeout between checks.')
    opt_parser.add_argument(
        '-v', '--verbose', help='Verbose mode', action='store_true')
    opt_parser.add_argument('-u', '--userlist', help='Reads usernames from file')
    opt_parser.add_argument('-d', '--domain', help='Uses manually entered domain.')
    opt_parser.add_argument('-c', '--checkdomain', help='Checks if domain is valid. Requires -d <domain>', action='store_false')
    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()

def handler():
    if args.read and args.userlist and args.email is not None or args.read and args.userlist is not None:
        print(fail + '\n[-] Please select only one option and try again.')    
        sys.exit()
    if args.email is not None:
        single_test()
    if args.read is not None:
        gmail_test()
    if args.userlist is not None:
        gmail_users()
    if args.checkdomain is not None and args.domain is None:
        print(fail + '\n[-] Please enter a domain to check. -c -d <domain>')
        sys.exit()
    if args.checkdomain is not None and args.domain is not None and args.email is None:    
        domain_test()
    



def single_test():
    if args.email is not None:
        email = args.email
        url = "https://mail.google.com/mail/gxlu?email=" + email + "&zx=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        request = request_handler.head(url)
        response = request.text
        cook_check = str(request.cookies.get_dict())
        valid_response = re.search("'COMPASS':", cook_check)
        if args.verbose is not None:
            print(request.status_code, response)
        if valid_response:
            print(success + f'\n[!] {email} - Valid Gmail account!')
        else:
            print(fail + f'\n[-] {email} - Invalid Gmail account.')
    else:
        pass

def gmail_test():
    # counter = 0
    if args.read is not None:  
        with open(args.read, 'r') as line_count:
            lines = len(line_count.readlines())
            print(info + f'\n[!] Loading {lines} emails to test.\n')
        with open(args.read, 'r') as f:
            counter = 0
            for line in f:
                email = line.split()
                email = ' '.join(email)
                url = "https://mail.google.com/mail/gxlu?email=" + email + "&zx=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                request = request_handler.get(url)
                cook_check = str(request.cookies.get_dict())
                valid_response = re.search("'COMPASS':", cook_check)
                if args.verbose:
                    print('\n',email, url, request, request.status_code)
                if valid_response:
                    b = " Result -   Valid Email Found! [+]"
                    print(success + f'[+] {email:53} {b}' + Style.RESET_ALL)
                    counter = counter + 1
                    if args.write is not None:
                        with open(args.write, 'a') as valid_emails:
                            valid_emails.write(f"{email}\n")
                else:
                    b = " Result - Invalid Email Found! [-]"
                    print(fail + f'[-] {email:53} {b}' + Style.RESET_ALL)
                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print(
                    fail + '\n[-] There were no valid logins found. [-]' + close)
            if counter == 1:
                print(
                    info + '\n[info] geeMail User Finder discovered one valid login account.' + close)
            if counter > 1:
                print(
                    info + f'\n[info] geeMail User Finder discovered {counter} valid login accounts.' + close)

    else:
            pass

def gmail_users():
    # counter = 0
    print(info + f'\n [!] Checking if target domain uses GSuite.')
    domain_test()
    if args.userlist is not None:  
        with open(args.userlist, 'r') as line_count:
            lines = len(line_count.readlines())
            print(info + f'\n[!] Loading {lines} usernames to test.\n')
        with open(args.userlist, 'r') as f:
            counter = 0
            for line in f:
                username = line.split()
                username = ' '.join(username)
                email = username + '@' + args.domain
                url = "https://mail.google.com/mail/gxlu?email=" + email + "&zx=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                request = request_handler.get(url)
                cook_check = str(request.cookies.get_dict())
                valid_response = re.search("'COMPASS':", cook_check)
                if args.verbose:
                    print('\n',email, url, request, request.status_code)
                if valid_response:
                    b = " Result -   Valid Email Found! [+]"
                    print(success + f'[+] {email:53} {b}')
                    counter = counter + 1
                    if args.write is not None:
                        with open(args.write, 'a') as valid_emails:
                            valid_emails.write(f"{email}\n")
                else:
                    b = " Result - Invalid Email Found! [-]"
                    print(fail + f'[-] {email:53} {b}')
                if args.timeout is not None:
                    time.sleep(int(args.timeout))
            if counter == 0:
                print(
                    fail + '\n[-] There were no valid logins found. [-]' + close)
            if counter == 1:
                print(
                    info + '\n[info] geeMail User Finder discovered one valid login account.' + close)
            if counter > 1:
                print(
                    info + f'\n[info] geeMail User Finder discovered {counter} valid login accounts.' + close)

    else:
            pass

def domain_test():
    domain = args.domain
    url = f'https://www.google.com/a/{domain}/ServiceLogin?https://docs.google.com/a/{domain}'
    request = request_handler.get(url)
    re.search("Server error", request.text)
    if args.verbose:
        print(request.text)    
    if re.search("Server error", request.text):
        print(fail + f'\n[-] {domain} - Invalid GSuite domain!')
    else:
        print(success + f'\n[+] {domain} - Valid GSuite domain!')

if __name__ == '__main__':
    try:
        init()
        definitions()
        banner()
        options()
        print(Fore.YELLOW + Style.BRIGHT +
            f'\n[info] Starting geeMail User Finder at {time.ctime()}' + Style.RESET_ALL)    
        handler()
        # single_test()
        # gmail_test()
        # gmail_users()
        print(
            info + f'\n[info] Scan completed at {time.ctime()}\n' + close)
    except KeyboardInterrupt:
        print(fail + '\n[-] User Interrupt. [-]' + close)
        print(
            info + f'\n[info] Scan completed at {time.ctime()}\n' + close)
        sys.exit()
    except FileNotFoundError:
        print(fail + '\n[-] File not found. Check filename and try again [-]' + close)
