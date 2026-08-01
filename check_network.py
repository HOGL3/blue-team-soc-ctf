import requests
import re
from urllib.parse import urljoin

base_url = "http://127.0.0.1:8001/"
session = requests.Session()

# Get CSRF token
login_url = urljoin(base_url, "/login/")
try:
    response = session.get(login_url)
    csrf_token = session.cookies.get('csrftoken')
except Exception as e:
    print(f"Failed to fetch login page: {e}")
    exit(1)

# Login
payload = {
    'username': 'mchen',
    'password': 'Password123!',
    'csrfmiddlewaretoken': csrf_token
}
headers = {'Referer': login_url}
session.post(login_url, data=payload, headers=headers)

# Fetch Dashboard
dashboard_url = urljoin(base_url, "/dashboard/")
response = session.get(dashboard_url)

static_urls = re.findall(r'(/static/[a-zA-Z0-9_\-\./]+)', response.text)
static_urls = list(set(static_urls))

print("Static Assets Required by Dashboard:")
failed_count = 0
for url in static_urls:
    full_url = urljoin(base_url, url)
    res = session.get(full_url)
    print(f"[{res.status_code}] {url}")
    if res.status_code != 200:
        failed_count += 1

print(f"\nTotal Failed Assets: {failed_count} out of {len(static_urls)}")
