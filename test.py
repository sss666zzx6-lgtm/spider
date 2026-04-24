import requests

# url = "https://www.cloudflare.com/cdn-cgi/trace"
url = "https://tls.browserleaks.com/json"
response = requests.get(url)
print(response.text)