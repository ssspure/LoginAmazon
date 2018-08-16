import re

proxyIP = 'unknown, 159.65.162.141'

regexp = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

if regexp.findall(proxyIP):
    proxyIP = regexp.findall(proxyIP)[0]
else:
    proxyIP = "No"

print(proxyIP)