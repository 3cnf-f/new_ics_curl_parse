import requests
with open('ics.url') as f:
    url_raw = f.read()

url_in=url_raw.strip('\n')
try:
    response = requests.get(url_in)
    if response.status_code == 200:

        with open('ics.ics','w') as f:
            f.write(response.text)
        print(response.text)
    else:
        print(f"error code from requests {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f'the following error ocurred {e}')
