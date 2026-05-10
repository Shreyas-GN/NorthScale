import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json,text/plain,*/*",
    "Referer": "https://www.nseindia.com/",
}

session = requests.Session()

# Bootstrap session
print("Bootstrapping session...")
session.get("https://www.nseindia.com", headers=headers)

url = "https://www.nseindia.com/api/quote-equity?symbol=TCS"

print(f"Fetching data from: {url}")
response = session.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response (First 500 chars):\n{response.text[:500]}")
