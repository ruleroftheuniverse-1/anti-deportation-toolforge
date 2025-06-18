import requests
import csv
from datetime import datetime

# GitHub Search Query
query = "immigration+OR+deportation+OR+asylum+OR+sanctuary+in:name,description,readme"
url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=50"
headers = {'Accept': 'application/vnd.github.v3+json'}

# Make the request
response = requests.get(url, headers=headers)
data = response.json()

# Parse and store the results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"immigration_tools_github_scan_{timestamp}.csv"

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Source", "Category", "Description", "Link"])
    writer.writeheader()
    for item in data.get("items", []):
        writer.writerow({
            "Name": item["name"],
            "Source": "GitHub",
            "Category": "Repo",
            "Description": item["description"],
            "Link": item["html_url"]
        })

print(f"Saved {len(data.get('items', []))} projects to {filename}")
