import urllib.request, ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"
response = urllib.request.urlopen(url)
print(response)
for line in urllib.request.urlopen(url):
    line = line.decode('utf-8')
    if '<title' in line:
        print(line.strip())