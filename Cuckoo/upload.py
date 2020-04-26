import requests


url = 'http://127.0.0.1:81'

#Getting the CSRF token for authentication
response = requests.get(url)
cookies_list = response.headers['Set-Cookie'].split(';')
print(cookies_list)
csrf_token = cookies_list[0].split('=')[1]
print(csrf_token)



# mal_file = {'file' : open('test.docx' , 'rb')}

# print(response.status_code)
# print(response.text)

