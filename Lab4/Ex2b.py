url = input("Enter a URL: ")

domain = url.split("//")[1].split("/")[0]
tld = domain.split(".")[-1]

print("Domain:", domain)
print("TLD:", tld)