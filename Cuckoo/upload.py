import requests

url = 'http://127.0.0.1:81/submit/'

file = {'file' : open('test.docx' , 'rb')}

response = requests.post(url, files = file )
print(response.status_code)
print(response.text)

