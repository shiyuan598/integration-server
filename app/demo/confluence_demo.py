import requests
import json # loads / dumps

headers = {
    'Content-Type': 'application/json',
}
response = requests.get(
    'https://confluence.zhito.com:8090/rest/api/space/ITD',
    headers=headers,
    auth=("wangshiyuan", "zhito26@#"))
print(response, response.text)

response = requests.get(
    'https://confluence.zhito.com:8090/rest/api/content/56102841',
    headers=headers,
    auth=("wangshiyuan", "zhito26@#"))
print("\n\n", response, response.text) # _links.webui
