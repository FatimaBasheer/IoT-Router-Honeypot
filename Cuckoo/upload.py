import requests


url = 'http://127.0.0.1:81'

# #Getting the CSRF token for authen
# response = requests.get(url)
# cookies_list = response.headers['Set-Cookie'].split(';')
# print(cookies_list)
# csrf_token = cookies_list[0]
# print(csrf_token)

# #Forming the header for uploading the file
# cuckoo_headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
# }
# cuckoo_headers['Cookie'] = csrf_token
# print(cuckoo_headers)
# mal_file = {'file' : open('test.docx' , 'rb')}

# #sending the file
# response = requests.post(url, headers= cuckoo_headers, files= mal_file)
# print(response.status_code)
# print(response.text)
client = requests.session() #sets cookie
for x in client.cookies:
    print(x)
